#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Bridge ebtables</title>"
echo "<meta charset='utf-8'>"
echo "<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
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
  letter-spacing: 0.6px;
  color: #7dd3fc;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 20px;
}

table {
  border-collapse: collapse;
  margin-bottom: 20px;
  width: 100%;
  max-width: 800px;
  background: rgba(15, 23, 42, 0.85);
  border-radius: 8px;
  overflow: hidden;
}

td, th {
  border: 1px solid #334155;
  padding: 12px 16px;
  text-align: left;
  color: #e5e7eb;
}

th {
  background: rgba(34, 211, 238, 0.1);
  color: #7dd3fc;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
}

tr:hover td {
  background: rgba(34, 211, 238, 0.05);
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  text-align: center;
  min-width: 80px;
}

.status-isolated {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.status-active {
  background: rgba(34, 197, 94, 0.2);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.4);
}

button {
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn-isolate {
  background: linear-gradient(135deg, #ef4444, #f87171);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-isolate:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.5);
}

.btn-unisolate {
  background: linear-gradient(135deg, #22c55e, #4ade80);
  color: #022c22;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.btn-unisolate:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(34, 197, 94, 0.5);
}

.interface-name {
  font-family: 'Monaco', 'Consolas', monospace;
  color: #fbbf24;
}

.back-link {
  display: inline-block;
  margin-top: 20px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
}

.back-link:hover {
  color: #e5e7eb;
  text-decoration: underline;
}
</style>
</head><body>"

echo "<h2>Gestió d'Aïllament (ebtables)</h2>"

# Processar accions si n'hi ha
QUERY_STRING="$QUERY_STRING"
saveIFS=$IFS
IFS='&'
for pair in $QUERY_STRING
do
  IFS='='
  read key value <<< "$pair"
  if [ "$key" == "cmd" ]; then COMMAND="$value"; fi
  if [ "$key" == "iface" ]; then IFACE="$value"; fi
  if [ "$key" == "vlanid" ]; then VLANID="$value"; fi
  if [ "$key" == "state" ]; then STATE="$value"; fi
  IFS='&'
done
IFS=$saveIFS

if [ "$COMMAND" == "update" ] && [ -n "$IFACE" ] && [ -n "$STATE" ]; then
    # Cridar al backend per actualitzar
    $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge configurar ebtables-guardar "$IFACE" "$STATE"
    # Petita pausa per assegurar que s'aplica abans de recarregar visualment
    sleep 0.5
fi

if [ "$COMMAND" == "vlan_update" ] && [ -n "$VLANID" ] && [ -n "$STATE" ]; then
    # Cridar al backend per actualitzar VLAN
    $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge configurar ebtables-guardar-vlan "$VLANID" "$STATE"
    sleep 0.5
fi

# Llegir configuració actual
CONF_FILE="$DIR/$PROJECTE/$DIR_CONF/bridge_ebtables.conf"
declare -A ISOLATION_MAP

if [ -f "$CONF_FILE" ]; then
    while IFS=';' read -r iface state _; do
        [[ "$iface" =~ ^#.*$ ]] && continue
        [ -z "$iface" ] && continue
        ISOLATION_MAP["$iface"]="$state"
    done < "$CONF_FILE"
fi

# Obtenir llista d'interfícies del bridge
# Es pot fer llegint bridge_if.conf o llistant interfícies reals
# Llegim bridge_if.conf per tenir les interfícies definides al sistema
BRIDGE_IF_FILE="$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_IF"

# Llegir configuració VLAN existent
CONF_VLAN_FILE="$DIR/$PROJECTE/$DIR_CONF/bridge_ebtables_vlan.conf"
declare -A VLAN_ISOLATION_MAP

if [ -f "$CONF_VLAN_FILE" ]; then
    while IFS=';' read -r vlanid state _; do
        [[ "$vlanid" =~ ^#.*$ ]] && continue
        [ -z "$vlanid" ] && continue
        VLAN_ISOLATION_MAP["$vlanid"]="$state"
    done < "$CONF_VLAN_FILE"
fi

# Parse bridge_if.conf to map interfaces to VLANs and separate active VLANs
declare -A IFACE_VLAN_MAP
declare -A VLAN_INTERFACES
# We use an array to preserve order or just sort later, but bash associative arrays are unordered.
# We will collect unique VLAN IDs.
declare -A ACTIVE_VLANS

if [ -f "$BRIDGE_IF_FILE" ]; then
    while IFS=';' read -r iface untag tag _; do
        [[ "$iface" =~ ^#.*$ ]] && continue
        [ -z "$iface" ] && continue
        
        # Guardar mapping Interfície -> VLAN UNTAG
        if [ -n "$untag" ] && [ "$untag" != "0" ]; then
            IFACE_VLAN_MAP["$iface"]="$untag"
            VLAN_INTERFACES["$untag"]+="$iface "
            ACTIVE_VLANS["$untag"]=1
        else
             IFACE_VLAN_MAP["$iface"]="-"
        fi
    done < "$BRIDGE_IF_FILE"
fi

echo "<h3>Aïllament per Interfície</h3>"
echo "<table>"
echo "<tr><th>Interfície</th><th>VLAN (Untag)</th><th>Estat Aïllament</th><th>Acció</th></tr>"

if [ -f "$BRIDGE_IF_FILE" ]; then
    while IFS=';' read -r iface _ _ _; do
        [[ "$iface" =~ ^#.*$ ]] && continue
        [ -z "$iface" ] && continue
        
        CURRENT_STATE="${ISOLATION_MAP[$iface]}"
        VLAN_ID="${IFACE_VLAN_MAP[$iface]}"
        
        if [ "$CURRENT_STATE" == "1" ]; then
            STATUS_HTML="<span class='status-badge status-isolated'>AÏLLAT</span>"
            ACTION_BTN="<button class='btn-unisolate' onclick=\"location.href='?cmd=update&iface=$iface&state=0'\">Desactivar</button>"
        else
            STATUS_HTML="<span class='status-badge status-active'>PERMÈS</span>"
            ACTION_BTN="<button class='btn-isolate' onclick=\"location.href='?cmd=update&iface=$iface&state=1'\">Activar</button>"
        fi
        
        echo "<tr>"
        echo "<td><span class='interface-name'>$iface</span></td>"
        echo "<td><span class='interface-name'>$VLAN_ID</span></td>"
        echo "<td>$STATUS_HTML</td>"
        echo "<td>$ACTION_BTN</td>"
        echo "</tr>"
        
    done < "$BRIDGE_IF_FILE"
fi

echo "</table>"

echo "<h3>Aïllament per VLAN</h3>"
echo "<table>"
echo "<tr><th>VLAN ID</th><th>Interfícies Membres</th><th>Estat Aïllament</th><th>Acció</th></tr>"

# Iterate over found VLANs
# Sort VLAN IDs numerically
SORTED_VLANS=$(echo "${!ACTIVE_VLANS[@]}" | tr ' ' '\n' | sort -n)

for vlanid in $SORTED_VLANS; do
    MEMBERS="${VLAN_INTERFACES[$vlanid]}"
    # Comprovar si aquesta VLAN està aïllada
    VLAN_STATE="${VLAN_ISOLATION_MAP[$vlanid]}"
    
    if [ "$VLAN_STATE" == "1" ]; then
         V_STATUS_HTML="<span class='status-badge status-isolated'>AÏLLAT</span>"
         V_ACTION_BTN="<button class='btn-unisolate' onclick=\"location.href='?cmd=vlan_update&vlanid=$vlanid&state=0'\">Desbloquejar VLAN</button>"
    else
         V_STATUS_HTML="<span class='status-badge status-active'>PERMÈS</span>"
         V_ACTION_BTN="<button class='btn-isolate' onclick=\"location.href='?cmd=vlan_update&vlanid=$vlanid&state=1'\">Aïllar VLAN</button>"
    fi
     
    echo "<tr>"
    echo "<td><strong>VLAN $vlanid</strong></td>"
    echo "<td><span class='interface-name'>$MEMBERS</span></td>"
    echo "<td>$V_STATUS_HTML</td>"
    echo "<td>$V_ACTION_BTN</td>"
    echo "</tr>"
done < <(echo "$SORTED_VLANS")

echo "</table>"

echo "<div style='margin-top: 20px; padding: 15px; background: rgba(30, 41, 59, 0.5); border-radius: 8px; font-size: 0.9em; color: #94a3b8;'>"
echo "<strong>Nota:</strong> Els ports aïllats no es poden comunicar entre ells, però mantenen accés a la sortida (Internet/Gateway)."
echo "</div>"
echo "</body></html>"
