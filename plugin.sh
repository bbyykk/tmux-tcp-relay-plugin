#!/usr/bin/env bash
case "$1" in
  toggle) "$TMUX_PLUGIN_MANAGER_PATH/tmux-tcp-relay-plugin/bin/toggle_server" ;;
  *) tmux display-message "usage: run toggle" ;;
esac
