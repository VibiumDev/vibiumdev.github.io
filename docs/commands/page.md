---
title: vibium page
---

Manage browser pages (new, close, switch).

## Synopsis

```
vibium page [flags]
vibium page [command]
```

## Subcommands

### vibium page close

Close a browser page by index or id (default: current page).

```
vibium page close [index or page id] [flags]
```

```sh
vibium page close
# Close current page (index 0)

vibium page close 1
# Close page at index 1

vibium page close A1B2C3D4
# Close the page with that id (from "vibium page new")
```

### vibium page new

Open a new browser page.

```
vibium page new [url] [flags]
```

#### Flags

```
    --isolated   Open the page in its own isolated context (separate cookies and storage)
```

New in nightly (not yet in the npm release): `--isolated`

```sh
vibium page new
# Open a blank new page

vibium page new https://example.com
# Open a new page and navigate to URL

vibium page new --isolated https://example.com
# Open the page in its own isolated context (separate cookies/storage):
#   New isolated page opened and navigated to https://example.com (page: A1B2...)
```

### vibium page switch

Switch to a browser page by index or URL substring.

```
vibium page switch [index or url] [flags]
```

```sh
vibium page switch 1
# Switch to page at index 1

vibium page switch google.com
# Switch to page containing "google.com" in URL
```
