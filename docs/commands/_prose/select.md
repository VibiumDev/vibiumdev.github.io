## Description

Picks the option whose visible label matches `<option>` from the dropdown
referenced by `@e<num>`.

## Examples

```sh
vibium select @e5 "United States"
```

Find first, then select:

```sh
$ vibium find label "Country"
@e5  select  label="Country"

$ vibium select @e5 "Canada"
```

## See also

- [`vibium fill`](fill.md), [`vibium check`](check.md), [`vibium click`](click.md).
