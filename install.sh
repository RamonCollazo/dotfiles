#!/bin/bash
set -e

sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin init --apply RamonCollazo
cd ~ && mise install
