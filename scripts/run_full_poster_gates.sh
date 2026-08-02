#!/usr/bin/env sh
set -eu

test -s logbook/poster_embed.html
grep -q '<!doctype html>' logbook/poster_embed.html
grep -q 'Score boundary' logbook/poster_embed.html
grep -q 'Claim 3' logbook/poster_embed.html
grep -q 'No GPU was used' logbook/poster_embed.html
printf '%s\n' 'PASS: text-only poster structure, scope, and score boundary'
