---
title: vibium webbotauth
sidebar:
  badge: Nightly
---

Create and inspect the Ed25519 key used for Web Bot Auth request signing.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium webbotauth [command]
```

## Subcommands

### vibium webbotauth directory

Print the JWKS directory to publish at /.well-known/http-message-signatures-directory.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium webbotauth directory [flags]
```

#### Flags

```
    --key string   Path to the Ed25519 key (PKCS#8 PEM)
```

```sh
vibium webbotauth directory --key web-bot-auth.pem
# {"keys":[{"kty":"OKP","crv":"Ed25519","x":"...","kid":"...","nbf":...}]}
```

### vibium webbotauth keygen

Generate an Ed25519 signing key (PKCS#8 PEM).

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium webbotauth keygen [flags]
```

#### Flags

```
-o, --output string   Write the key to this file (default: stdout)
```

```sh
vibium webbotauth keygen -o web-bot-auth.pem
# Wrote web-bot-auth.pem (keyid: poqkLGiymh_W0uP6PZFw-dvez3QJT5SolqXBCW38r0U)
```
