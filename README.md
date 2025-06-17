# tmux-tcp-relay-plugin

This plugin allows multiple `tmux` sessions across different hosts within a **LAN** to **share the copy buffer** seamlessly.

---

## 📦 Installation (with [TPM](https://github.com/tmux-plugins/tpm))

1. Add the following line to your `.tmux.conf`:

   ```tmux
   set -g @plugin 'bbyykk/tmux-tcp-relay-plugin.git'
   ```

2. Install via TPM:

   - Press `Prefix + I` to fetch and install the plugin  
   - Or restart tmux and TPM will auto-install it

---

## 🚀 Usage

### Run as a TCP relay **server**

```tmux
set -g @tcp-relay-args 'server'
```

### Run as a TCP relay **client**

```tmux
set -g @tcp-relay-args 'tcp.relay.server.ip'
```

> Replace `tcp.relay.server.ip` with your actual server IP on the LAN.

### Alternative way as a TCP relay **client**
You can use the 'nc' command directly in any pane or window
```
nc tcp.relay.server.ip 5555
```
---

## 🔁 Toggle Relay

Press the following key binding to **toggle** the relay server or client:

```
Prefix + t
```
And it would create a new window that would share between every clients and server
