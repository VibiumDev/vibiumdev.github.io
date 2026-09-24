---
title: vibium check
---

Verify a claim with an AI model.

## Synopsis

```
vibium check "<claim>" [-i <recording.zip>] [-o <evidence.zip>]
```

## Description

Asks a fresh AI verifier to investigate a claim and return **PASS**,
**FAIL**, or **INCONCLUSIVE**, with evidence. Live checks use the existing
browser session; `-i` checks a saved recording instead. Requires a
configured model provider — see [Run and Check](../run-and-check.md).

> Looking for the old checkbox command? Toggling checkboxes is now
> `vibium set` and `vibium unset`.

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
