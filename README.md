# MAAS contributions

A single repository containing the Canonical MAAS ecosystem sources as
[git subtrees](https://git-scm.com/book/en/v2/Git-Tools-Subtree-Merging),
with full upstream history. It is used for staging patches before upstream
submission.

`main` tracks the upstreams unmodified. Patches live on branches of this repo
and are exported to the matching GitHub fork with `scripts/subtree.sh` to open
a pull request or Launchpad merge proposal.

## Subtrees

| Directory | Upstream | Branch | Fork (PR staging) | Purpose |
|---|---|---|---|---|
| `maas/` | [canonical/maas](https://github.com/canonical/maas) | master | [grewelltech/maas](https://github.com/grewelltech/maas) | Region/rack controller, API, GRUB templates |
| `curtin/` | [canonical/curtin](https://github.com/canonical/curtin) | main | [grewelltech/curtin](https://github.com/grewelltech/curtin) | Installer that runs in the ephemeral environment |
| `cloud-init/` | [canonical/cloud-init](https://github.com/canonical/cloud-init) | main | [grewelltech/cloud-init](https://github.com/grewelltech/cloud-init) | Cloud instance initialization |
| `cloud-initramfs-tools/` | [lp:cloud-initramfs-tools](https://git.launchpad.net/cloud-initramfs-tools) | master | [grewelltech/cloud-initramfs-tools](https://github.com/grewelltech/cloud-initramfs-tools) | Initramfs networking (BOOTIF, dyn-netconf, growroot) |
| `packer-maas/` | [canonical/packer-maas](https://github.com/canonical/packer-maas) | main | [grewelltech/packer-maas](https://github.com/grewelltech/packer-maas) | Packer templates for custom MAAS images |
| `maas-ui/` | [canonical/maas-ui](https://github.com/canonical/maas-ui) | main | [grewelltech/maas-ui](https://github.com/grewelltech/maas-ui) | Web UI |
| `maas-commissioning-scripts/` | [canonical/maas-commissioning-scripts](https://github.com/canonical/maas-commissioning-scripts) | master | [grewelltech/maas-commissioning-scripts](https://github.com/grewelltech/maas-commissioning-scripts) | Example commissioning scripts |

The list of upstreams and forks is in `scripts/upstreams.conf`.

## Workflow

Update one or all subtrees from upstream (on `main`):

```sh
scripts/subtree.sh pull curtin
scripts/subtree.sh pull --all
```

Work on a patch:

```sh
git checkout -b curtin/fix-foo main
# edit files under curtin/, commit as usual
```

Export the patch to the fork and open a PR from there:

```sh
scripts/subtree.sh push curtin fix-foo
# -> pushes branch fix-foo to grewelltech/curtin, rewritten to upstream layout
```

`split` without `push` creates the local branch only. Commits exported this
way have the same content and messages as in this repo, so keep each patch
branch limited to a single subtree directory.

## Active branches

### cloud-initramfs-tools

| Branch | Status | Description |
|---|---|---|
| `cloud-initramfs-tools/fix-bootif-udev-settle-timeout` | Testing | Tolerate udev settle timeout in BOOTIF resolution. On machines with slow non-network hardware (nfit/NVME persistent memory), `udevadm settle --timeout=10` returns non-zero under `set -e`, killing the init-premount script before BOOTIF is resolved to a real device name. Exported to `grewelltech/cloud-initramfs-tools:fix/bootif-udev-settle-timeout`. |

## Upstream contribution paths

| Package | Process |
|---|---|
| cloud-initramfs-tools | Merge proposal against `lp:cloud-initramfs-tools` master branch (push the split branch to Launchpad or point the proposal at the GitHub fork) |
| maas | PR against `canonical/maas` |
| curtin | PR against `canonical/curtin` |
| cloud-init | PR against `canonical/cloud-init` |
| packer-maas | PR against `canonical/packer-maas` |
| maas-ui | PR against `canonical/maas-ui` |
| maas-commissioning-scripts | PR against `canonical/maas-commissioning-scripts` |
