---
title: vibium webbotauth
---

Create and inspect the Ed25519 key used for Web Bot Auth request signing.

## Synopsis

```
vibium webbotauth [command]
```

## Subcommands

### vibium webbotauth directory

Print the JWKS directory to publish at /.well-known/http-message-signatures-directory.

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
