---
title: vibium mouse
---

Mouse control (click, move, down, up).

## Synopsis

```
vibium mouse [flags]
vibium mouse [command]
```

## Subcommands

### vibium mouse click

Click at coordinates or current position.

```
vibium mouse click [x] [y] [flags]
```

#### Flags

```
    --button int   Mouse button (0=left, 1=middle, 2=right)
```

```sh
vibium mouse click 100 200
# Left click at (100, 200)

vibium mouse click 100 200 --button 2
# Right click at (100, 200)

vibium mouse click
# Left click at current position
```

### vibium mouse down

Press a mouse button down.

```
vibium mouse down [flags]
```

#### Flags

```
    --button int   Mouse button (0=left, 1=middle, 2=right)
```

```sh
vibium mouse down
# Press left mouse button

vibium mouse down --button 2
# Press right mouse button
```

### vibium mouse move

Move the mouse to coordinates.

```
vibium mouse move [x] [y] [flags]
```

```sh
vibium mouse move 100 200
# Move mouse to position (100, 200)
```

### vibium mouse up

Release a mouse button.

```
vibium mouse up [flags]
```

#### Flags

```
    --button int   Mouse button (0=left, 1=middle, 2=right)
```

```sh
vibium mouse up
# Release left mouse button

vibium mouse up --button 2
# Release right mouse button
```
