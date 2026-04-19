#!/bin/bash
set -e

mkdir -p ~/.local/bin
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin init --apply RamonCollazo
cd ~ && mise install
