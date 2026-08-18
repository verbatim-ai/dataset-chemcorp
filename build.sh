#!/usr/bin/env bash
# Build the ChemCorp corpus and the static site that publishes it.
# Documents land in website/docs/; the site pages are written to website/.
set -euo pipefail
cd "$(dirname "$0")"

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt

for f in gen_*.py; do
  [ "$f" = "gen_website.py" ] && continue
  python3 "$f"
done
python3 gen_website.py
