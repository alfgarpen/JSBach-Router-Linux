#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

# Expande VLANs: 1,2,5-7 → 1,2,5,6,7 (solo válidas)
expand_vlans() {
    local input="$1"
    local result=()

    IFS=',' read -ra parts <<< "$input"
    for part in "${parts[@]}"; do
        if [[ "$part" =~ ^[0-9]+-[0-9]+$ ]]; then
            start=${part%-*}
            end=${part#*-}
            for ((i=start; i<=end; i++)); do
                if (( i >= 0 && i <= 4094 )); then
                    result+=("$i")
                fi
            done
        elif [[ "$part" =~ ^[0-9]+$ ]]; then
            if (( part >= 0 && part <= 4094 )); then
                result+=("$part")
            fi
        fi
    done

    printf "%s\n" "${result[@]}" | sort -n -u | paste -sd ',' -
}

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Guardar Tag/Untag</title>
  <style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}
h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  font-weight: 700;
  color: #7dd3fc;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
}
pre {
  background: rgba(15, 23, 42, 0.9);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 0 18px rgba(0,0,0,0.5);
  color: #38bdf8;
  font-family: monospace;
  white-space: pre-wrap;
}
button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 10px 20px;
  border-radius: 999px;
  font-weight: 700;
}
</style>
</head>
<body>
<h2>Resultat configuració Tag / Untag</h2>
EOM

# Parámetros
int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
tag=$(echo "$QUERY_STRING" | sed -n 's/^.*tag=\([^&]*\).*$/\1/p')
untag=$(echo "$QUERY_STRING" | sed -n 's/^.*untag=\([^&]*\).*$/\1/p')

tag=$(urldecode "$tag")
untag=$(urldecode "$untag")

# Normalizar VLANs
TAG_FINAL=$(expand_vlans "$tag")
UNTAG_FINAL=$(expand_vlans "$untag")

echo "<pre>"
if [[ -z "$TAG_FINAL" && -z "$UNTAG_FINAL" ]]; then
    echo "ERROR: No s'ha especificat cap VLAN vàlida."
else
    echo "$($RUTA bridge configurar guardar bridge "$int" "$UNTAG_FINAL" "$TAG_FINAL")"
fi
echo "</pre>"

echo "<button onclick=\"location.href='/cgi-bin/bridge-configurar-taguntag.cgi'\">Tornar</button>"

echo "</body></html>"
