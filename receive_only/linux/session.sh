#!/bin/sh
set -eu
base=/opt/moribot-openqq
run=/run/moribot-openqq
app="$base/vendor/openqq/openqq-v0.5.0-linux-x64"
fluxbox >/dev/null 2>&1 &
systemd-socket-activate --accept --inetd --listen="$run/rfb.sock" -E DISPLAY -E XAUTHORITY -E HOME /usr/bin/x11vnc -inetd -quiet -nopw -noxdamage >/dev/null 2>&1 &
"$base/novnc-venv/bin/websockify" --web=/usr/share/novnc --unix-listen="$run/novnc.sock" --unix-listen-mode=0600 --unix-target="$run/rfb.sock" >/dev/null 2>"$run/novnc-errors.log" &
exec "$base/vendor/node/bin/node" "$app/src/main.mjs" start --config "$base/config/openqq.json" --web-host 127.0.0.1
