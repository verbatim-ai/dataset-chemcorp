python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
for f in gen_*.py; do python3 "$f"; done
