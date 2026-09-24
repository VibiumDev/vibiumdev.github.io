## Description

Asks a fresh AI verifier to investigate a claim and return **PASS**,
**FAIL**, or **INCONCLUSIVE**, with evidence. Live checks use the existing
browser session; `-i` checks a saved recording instead. Requires a
configured model provider — see [Run and Check](../run-and-check.md).

> In `vibium@26.8.21` (the current npm release), `vibium check` still
> toggles a checkbox (`uncheck` unchecks). The AI check above — and the
> `set`/`unset` checkbox commands that replace the old names — are in the
> nightly builds and the next release.

## Examples

```sh
vibium check "the saved timezone is America/Chicago after refresh"
```

Check saved evidence instead of the live browser:

```sh
vibium check "the order confirmation was shown" -i record.zip
```

## See also

- [Run and Check](../run-and-check.md)
- [Model Providers](../ai-providers.md)
