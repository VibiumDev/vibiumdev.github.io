---
title: "Browser server on Google Cloud"
description: "A Compute Engine VM behind an SSH tunnel — with the nicest tunnel story of the platforms here, since gcloud compute ssh manages keys itself."
editUrl: https://github.com/VibiumDev/vibium/edit/main/docs/how-to-guides/cloud-computers/gcp.md
---

<!-- Imported from docs/how-to-guides/cloud-computers/gcp.md in VibiumDev/vibium by scripts/import_upstream_docs.py. Edit it there. -->

> This guide was added after the 26.8.21 release, so parts of it MAY need a nightly build. See [What's in Nightly](../nightly.md).

A Compute Engine VM behind an SSH tunnel — with the nicest tunnel
story of the platforms here, since `gcloud compute ssh` manages keys itself.

## Prereqs (human)

1. GCP project with billing enabled
2. `gcloud init` (the CLI drives everything, including the tunnel)

## Create

```bash
gcloud compute instances create vibium-browser \
  --machine-type=e2-medium --zone=us-central1-a \
  --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --metadata-from-file user-data=deploy/cloud-computers/cloud-init.yml
```

First boot takes ~3–5 min while cloud-init installs Chrome. Bake an
image afterward for ~1 min starts. Spot VMs (`--provisioning-model=SPOT`)
are fine for disposable boxes.

## Connect

```bash
gcloud compute ssh vibium-browser --zone=us-central1-a -- -N -L 9515:127.0.0.1:9515 &
vibium start http://127.0.0.1:9515
vibium go https://example.com
vibium stop
```

`gcloud compute ssh` manages keys for you; chromedriver stays on
loopback and the tunnel is the only way in.

## Teardown

```bash
gcloud compute instances delete vibium-browser --zone=us-central1-a
```

Per-second billing.
