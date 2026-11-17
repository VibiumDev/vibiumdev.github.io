## Description

Asks a fresh AI verifier to investigate a claim and return **PASS**,
**FAIL**, or **REVIEW**, with evidence. Live checks use the existing
browser session; `-i` checks a saved recording instead. Requires a
configured model provider — see [Run and Check](../run-and-check.md).

> Before 26.11.16, `vibium check` toggled a checkbox (and `uncheck`
> unchecked it). Checkboxes now use `set` and `unset`.

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
