#!/bin/bash
set -e

export HOME="${HOME:-/home/vscode}"
mkdir -p "$HOME/.local/bin"

curl -fsLS get.chezmoi.io -o /tmp/chezmoi-install.sh
sh /tmp/chezmoi-install.sh -b "$HOME/.local/bin" init --apply RamonCollazo
