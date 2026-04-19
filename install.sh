#!/bin/bash
set -e

sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply RamonCollazo
mise install
