---
title: "Browser server on DigitalOcean"
description: "A droplet running Chrome + chromedriver behind an SSH tunnel."
editUrl: https://github.com/VibiumDev/vibium/edit/main/docs/how-to-guides/cloud-computers/digitalocean.md
---

<!-- Imported from docs/how-to-guides/cloud-computers/digitalocean.md in VibiumDev/vibium by scripts/import_upstream_docs.py. Edit it there. -->

> This guide was added after the 26.8.21 release, so parts of it MAY need a nightly build. See [What's in Nightly](../nightly.md).

A droplet running Chrome + chromedriver behind an SSH tunnel.
Per-second billing since 2026 — but **destroy, don't stop**: powered-off
droplets still bill.

## Prereqs (human)

1. DigitalOcean account with a payment method (nothing runs without one;
   promo links usually carry a $200/60-day credit)
2. `brew install doctl && doctl auth init` (API token from the dashboard)
3. An SSH key uploaded: `doctl compute ssh-key list`

## Create

```bash
doctl compute droplet create vibium-browser \
  --size s-2vcpu-4gb --image ubuntu-24-04-x64 --region nyc3 \
  --ssh-keys <fingerprint> \
  --user-data-file deploy/cloud-computers/cloud-init.yml --wait
doctl compute droplet get vibium-browser --format PublicIPv4
```

First boot takes ~3–5 min while cloud-init installs Chrome. Snapshot the
droplet afterward and future boxes start in ~1 min.

## Connect

```bash
ssh -N -L 9515:127.0.0.1:9515 root@<droplet-ip> &   # the tunnel
vibium start http://127.0.0.1:9515                  # classic endpoint → BiDi
vibium go https://example.com
vibium stop
```

chromedriver listens on loopback only; the tunnel is the only way in.

## Teardown (stops billing)

```bash
doctl compute droplet delete vibium-browser
```
