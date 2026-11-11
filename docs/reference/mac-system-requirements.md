---
title: "System Requirements"
description: "Hardware requirements for running two macOS guest VMs simultaneously with Xcode, iOS Simulator, and browser testing — plus Android Studio on the host."
editUrl: https://github.com/VibiumDev/vibium/edit/main/docs/reference/mac-system-requirements.md
---

<!-- Imported from docs/reference/mac-system-requirements.md in VibiumDev/vibium by scripts/import_upstream_docs.py. Edit it there. -->

Hardware requirements for running two macOS guest VMs simultaneously with Xcode, iOS Simulator, and browser testing — plus Android Studio on the host.

> **Note:** The Android emulator requires hardware virtualization and does not run inside macOS guest VMs (Apple Virtualization.framework does not support nested virtualization). Android Studio and the emulator must run directly on the host.

## Host Machine (Apple Silicon Mac)

|               | Minimum | Recommended |
| ------------- | ------- | ----------- |
| **RAM**       | 32 GB   | 64 GB       |
| **SSD**       | 512 GB  | 1 TB        |

## Each macOS Guest VM

|                    | Minimum | Recommended |
| ------------------ | ------- | ----------- |
| **RAM**            | 10 GB   | 16 GB       |
| **Virtual Disk**   | 192 GB  | 256 GB      |

## Assumed Guest Workload

- macOS (base install)
- Xcode + iOS Simulator runtimes
- Chrome and Firefox
- Development workspace and build caches

## Assumed Host Workload

- Two macOS guest VMs running simultaneously
- Android Studio + SDK + emulator
- Xcode and iOS Simulator on the host

## Notes

- Below 32 GB host RAM, the two-VM workflow is not supported. Drop to one VM or run without VM isolation.
- The Android emulator does not work inside macOS guest VMs — always run it on the host.
- 24 GB host RAM can run a single VM (10 GB) with Xcode, iOS Simulator, and Android Studio on the host, but this is tight.
- Guest virtual disks are sparse — a 256 GB virtual disk only consumes actual space as it fills, so oversizing has minimal cost on hosts with sufficient storage.
- After provisioning, monitor Activity Monitor's Memory Pressure graph (green = fine, yellow = tight, red = undersized) and Swap Used to verify the configuration is adequate.
