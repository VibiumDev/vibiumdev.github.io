---
title: What's in Nightly
---

Vibium publishes automated nightly builds from `main` as GitHub prereleases, ahead of the next npm release. This page is regenerated automatically by diffing the two binaries: everything listed here is in the current nightly but **not** in `vibium@26.8.21`, the latest npm release.

Get a nightly from the [releases page](https://github.com/VibiumDev/vibium/releases) — the `nightly-*` prereleases carry standalone binaries plus npm and Python packages. Nightlies are automated and unsupported.

## New commands

| Command | Description |
| ------- | ----------- |
| [`vibium config`](commands/config.md) | Manage Vibium settings files |
| [`vibium config init`](commands/config.md) | Write a commented settings file to the Vibium config directory. |
| [`vibium is set`](commands/is.md) | Check if a checkbox or radio is checked |
| [`vibium ready`](commands/ready.md) | Check the selected local browser executable files, then test AI when configured. No browser or driver is launched. |
| [`vibium ready ai`](commands/ready.md) | Require valid AI configuration and test authentication, model access, tool calling, and a structured response. |
| [`vibium ready browser`](commands/ready.md) | List discovered Vibium browser installations and check the selected Chrome or Firefox executable files. |
| [`vibium run`](commands/run.md) | Accomplish a live browser goal using VIBIUM_AI_* configuration. |
| [`vibium set`](commands/set.md) | Check a checkbox or radio button |
| [`vibium setup`](commands/setup.md) | Interactive setup for AI settings, agent skills, and the local browser. |
| [`vibium unset`](commands/unset.md) | Uncheck a checkbox |

## New flags on existing commands

| Command | New flags |
| ------- | --------- |
| [`vibium add-skill`](commands/add-skill.md) | `--agent` |
| [`vibium check`](commands/check.md) | `--ai-base-url`, `--base-url`, `--input`, `--keep-open`, `--model`, `--output`, `--provider`, `--reasoning-effort`, `--report` |
| [`vibium daemon start`](commands/daemon.md) | `--connect-caps` |
| [`vibium page new`](commands/page.md) | `--isolated` |
| [`vibium pdf`](commands/pdf.md) | `--background`, `--landscape`, `--margin`, `--page-height`, `--page-ranges`, `--page-width`, `--scale` |
| [`vibium pipe`](commands/pipe.md) | `--connect-caps`, `--no-browser` |
