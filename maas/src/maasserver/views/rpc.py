# Copyright 2014-2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Views relating to the region<-->cluster RPC mechanism.

Each region controller process starts its own RPC endpoint, and this
provides the means for clusters to discover what they are.
"""

import json

from django.http import HttpResponse

from maasserver.models.node import RegionController
from maasserver.models.staticipaddress import StaticIPAddress
from maasserver.routablepairs import find_addresses_between_nodes
from maasserver.utils import get_remote_ip


def get_endpoints():
    """Returns a list of ``(name, addr, port)`` tuples.

    Each tuple corresponds to somewhere an event-loop is listening
    within the whole region. The `name` is the event-loop name.
    """

    # Each regiond might be running a local bridge that duplicates the
    # same IP address across region controllers. Each region controller
    # must output a set of unique of IP addresses, to prevent the rack
    # controller from connecting to a different region controller then
    # the rack controller was expecting to be connecting to.
    def _unique_to_region(address, region, regions):
        for region_obj in regions:
            if region_obj != region:
                for process in region_obj.processes.all():
                    for endpoint in process.endpoints.all():
                        if endpoint.address == address:
                            return False
        return True

    regions = RegionController.objects.all()
    regions = regions.prefetch_related("processes", "processes__endpoints")
    all_endpoints = []
    for region_obj in regions:
        for process in region_obj.processes.all():
            for endpoint in process.endpoints.all():
                if _unique_to_region(endpoint.address, region_obj, regions):
                    all_endpoints.append(
                        (
                            "%s:pid=%d" % (region_obj.hostname, process.pid),
                            endpoint.address,
                            endpoint.port,
                        )
                    )
    return all_endpoints


def _find_requesting_node(request):
    """Return the node that made `request`, or None if it is not known.

    A rack controller that has not registered yet owns no addresses in the
    database, so this returns None while it is enlisting and the caller then
    leaves the endpoint list in its original order.
    """
    ip = get_remote_ip(request)
    if ip is None:
        return None
    sip = StaticIPAddress.objects.filter(ip=ip).first()
    return None if sip is None else sip.get_node()


def _rank_addresses_by_locality(node):
    """Return a key function ordering region addresses as seen from `node`.

    `find_addresses_between_nodes` yields pairs lowest metric first -- same
    node, then same subnet, then same VLAN, then same space -- so an address's
    position in that sequence is its order of preference. Addresses it does
    not report are ranked after every address it does, which keeps them
    available to a rack that shares nothing with the region while still
    preferring anything closer.
    """
    regions = RegionController.objects.all()
    ranks = {}
    for _, _, _, right_ip in find_addresses_between_nodes({node}, regions):
        ranks.setdefault(str(right_ip), len(ranks))
    unranked = len(ranks)
    return lambda endpoint: ranks.get(endpoint[0], unranked)


def info(request):
    """View returning a JSON document with information about RPC endpoints.

    Currently the only information returned is a list of `(host, port)` tuples
    on which the region has listening RPC endpoints.

    When the `rpc-advertise` service is not running this returns `None`
    instead of the list of event-loop endpoints. This denotes something along
    the lines of "I don't know". The cluster should not act on this, and
    instead ask again later.

    """
    endpoints = {}
    for name, addr, port in get_endpoints():
        if name in endpoints:
            endpoints[name].append((addr, port))
        else:
            endpoints[name] = [(addr, port)]

    # Offer each event-loop's addresses closest-first. A rack connects to the
    # first address that answers, so without an order it reaches the region
    # over an arbitrary one of the region's addresses, which on a multi-homed
    # region can be a path that works for the handshake and not afterwards.
    node = _find_requesting_node(request)
    if node is not None:
        rank = _rank_addresses_by_locality(node)
        endpoints = {
            name: sorted(addresses, key=rank)
            for name, addresses in endpoints.items()
        }

    # Each endpoint is an entry point into this event-loop.
    info = {"eventloops": endpoints}

    return HttpResponse(json.dumps(info), content_type="application/json")
