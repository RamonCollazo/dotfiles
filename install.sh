#!/bin/bash
set -e

sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply RamonCollazo
cd ~ && mise install
