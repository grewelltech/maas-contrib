#!/bin/bash

# due to the dependency below, this Dracut module needs to be ordered before the network Dracut module

# called by dracut
depends() {
    echo systemd-networkd
}
