## Description

`record start` begins a recording. From that point on, Vibium captures a
screenshot at every step. `record stop` ends the recording and writes the
captured screenshots to `record-<timestamp>.zip` in the current directory.
Pass `-o` to `record start` to choose the file.

The resulting archive is useful for:

- Sharing a reproducible bug report.
- Auditing what an agent did during an autonomous run.
- Spot-checking the visual state of a session after the fact.

## Examples

```sh
vibium record start -o session.zip
vibium go https://example.com
vibium click @e1
vibium record stop
ls session.zip
```

## See also

- [`vibium screenshot`](screenshot.md) — one-off capture instead of a session.
