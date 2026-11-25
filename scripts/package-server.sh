#!/bin/sh
# Paquet pour le serveur SATT : application compilée + synchronisation PHP + guide.
# Usage : npm run build && sh scripts/package-server.sh <sortie.zip>
set -e
OUT=$(realpath -m "$1"); T=$(mktemp -d)
mkdir -p "$T/parcours"
cp -r dist/. "$T/parcours/"
cp -r server/api "$T/parcours/api"
rm -f "$T/parcours/api/data/"*.sqlite*
echo '{"syncUrl": "api/sync.php"}' > "$T/parcours/config.json"
cp server/GUIDE_INSTALLATION.md "$T/"
(cd "$T" && rm -f "$OUT" && zip -qr "$OUT" .)
rm -rf "$T"
echo "$OUT"
