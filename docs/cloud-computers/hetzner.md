---
title: "Browser server on Hetzner"
description: "Budget cloud instances via the hcloud CLI; Hetzner also offers dedicated bare-metal servers where the same installer works over SSH."
editUrl: https://github.com/VibiumDev/vibium/edit/main/docs/how-to-guides/cloud-computers/hetzner.md
---

<!-- Imported from docs/how-to-guides/cloud-computers/hetzner.md in VibiumDev/vibium by scripts/import_upstream_docs.py. Edit it there. -->

> This guide was added after the 26.8.21 release, so parts of it MAY need a nightly build. See [What's in Nightly](../nightly.md).

Budget cloud instances via the `hcloud` CLI; Hetzner also offers
dedicated bare-metal servers where the same installer works over SSH.

## Prereqs (human)

1. Hetzner Cloud account (console.hetzner.cloud; payment method required)
2. `brew install hcloud && hcloud context create vibium` (API token from
   the console)
3. An SSH key uploaded: `hcloud ssh-key list`

## Create

```bash
hcloud server create --name vibium-browser \
  --type cx32 --image ubuntu-24.04 --location fsn1 \
  --ssh-key <name> \
  --user-data-from-file deploy/cloud-computers/cloud-init.yml
hcloud server ip vibium-browser
```

First boot takes ~3–5 min while cloud-init installs Chrome. Snapshot
afterward and future boxes start in ~1 min. Locations: Falkenstein,
Nuremberg, Helsinki (EU), Ashburn, Hillsboro (US), Singapore.

## Connect

```bash
ssh -N -L 9515:127.0.0.1:9515 root@<server-ip> &
vibium start http://127.0.0.1:9515
vibium go https://example.com
vibium stop
```

chromedriver listens on loopback only; the tunnel is the only way in.

## Teardown

```bash
hcloud server delete vibium-browser
```

Hourly billing, capped at the monthly price.

## Bare metal

Hetzner's dedicated servers (Robot console, including the server
auction) are real hardware; `install-chrome.sh --service` works there
over SSH the same way. Provisioning is a manual order rather than an
API call, so treat dedicated boxes as a standing fleet, not burst
capacity.
