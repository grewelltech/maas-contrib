# MAAS contributions

Forks and mirrors of Canonical MAAS ecosystem repositories, used for staging
patches before upstream submission.

## Repositories

| Repo | Upstream | Purpose |
|---|---|---|
| [maas](https://github.com/grewelltech/maas) | [canonical/maas](https://github.com/canonical/maas) | Region/rack controller, API, GRUB templates |
| [curtin](https://github.com/grewelltech/curtin) | [canonical/curtin](https://github.com/canonical/curtin) | Installer that runs in the ephemeral environment |
| [cloud-init](https://github.com/grewelltech/cloud-init) | [canonical/cloud-init](https://github.com/canonical/cloud-init) | Cloud instance initialization |
| [cloud-initramfs-tools](https://github.com/grewelltech/cloud-initramfs-tools) | [git.launchpad.net/cloud-initramfs-tools](https://git.launchpad.net/cloud-initramfs-tools) | Initramfs networking (BOOTIF, dyn-netconf, growroot) |
| [packer-maas](https://github.com/grewelltech/packer-maas) | [canonical/packer-maas](https://github.com/canonical/packer-maas) | Packer templates for custom MAAS images |
| [maas-ui](https://github.com/grewelltech/maas-ui) | [canonical/maas-ui](https://github.com/canonical/maas-ui) | Web UI |
| [maas-commissioning-scripts](https://github.com/grewelltech/maas-commissioning-scripts) | [canonical/maas-commissioning-scripts](https://github.com/canonical/maas-commissioning-scripts) | Example commissioning scripts |

## Active branches

### cloud-initramfs-tools

| Branch | Status | Description |
|---|---|---|
| `fix/bootif-udev-settle-timeout` | Testing | Tolerate udev settle timeout in BOOTIF resolution. On machines with slow non-network hardware (nfit/NVME persistent memory), `udevadm settle --timeout=10` returns non-zero under `set -e`, killing the init-premount script before BOOTIF is resolved to a real device name. |

## Upstream contribution paths

| Package | Repo | Process |
|---|---|---|
| cloud-initramfs-tools | Launchpad | Merge proposal against `lp:cloud-initramfs-tools` master branch |
| maas | GitHub | PR against `canonical/maas` |
| curtin | GitHub | PR against `canonical/curtin` |
| cloud-init | GitHub | PR against `canonical/cloud-init` |
