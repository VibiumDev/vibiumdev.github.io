---
title: vibium geolocation
---

Override the browser geolocation.

## Synopsis

```
vibium geolocation [latitude] [longitude] [flags]
```

## Flags

```
    --accuracy float   Accuracy in meters (default: 1)
```

## Examples

```sh
vibium geolocation 40.7128 -74.006
# Set location to New York City

vibium geolocation 51.5074 -0.1278 --accuracy 10
# Set location to London with 10m accuracy
```
