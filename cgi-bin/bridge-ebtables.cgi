#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

# ----------------------------------------------------------------------
# Action Handling
# ----------------------------------------------------------------------
if [ -n "$QUERY_STRING" ]; then
    # Parse Query String
    saveIFS=$IFS
    IFS='&'
    for pair in $QUERY_STRING; do
        IFS='=' read -r key value <<< "$pair"
        declare "$key"="$value"
    done
    IFS=$saveIFS
    
    if [ "$action" == "toggle_interface" ]; then
        # param: iface, state (0/1)
        "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar ebtables-guardar "$iface" "$state" > /dev/null
        echo "Location: /cgi-bin/bridge-ebtables.cgi"
        echo ""
        exit 0
    elif [ "$action" == "toggle_vlan" ]; then
        # param: vlan, state (0/1)
        "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar ebtables-guardar-vlan "$vlan" "$state" > /dev/null
        echo "Location: /cgi-bin/bridge-ebtables.cgi"
        echo ""
        exit 0
    fi
fi

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------

get_vlan_state() {
    local vid=$1
    local file="$DIR/$PROJECTE/$DIR_CONF/bridge_ebtables_vlan.conf"
    local state="0"
    if [ -f "$file" ]; then
        local line=$(grep "^$vid;" "$file")
        if [ -n "$line" ]; then
            state=$(echo "$line" | cut -d';' -f2)
        fi
    fi
    echo "$state"
}

get_iface_state() {
    local iface=$1
    local file="$DIR/$PROJECTE/$DIR_CONF/bridge_ebtables.conf"
    local state="0"
    if [ -f "$file" ]; then
        local line=$(grep "^$iface;" "$file")
        if [ -n "$line" ]; then
            state=$(echo "$line" | cut -d';' -f2)
        fi
    fi
    echo "$state"
}

# ----------------------------------------------------------------------
# Data Preparation
# ----------------------------------------------------------------------

# Read Bridge Membership to memory
# Structure: map[vlan_id] -> { untagged=[], tagged=[] }
# To emulate this in bash, we'll use strings with delimiters.

declare -A VLAN_MEMBERS_UNTAG
declare -A VLAN_MEMBERS_TAG
declare -A ALL_VLANS
declare -a IFACE_LIST

BRIDGE_IF_FILE="$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_IF"

if [ -f "$BRIDGE_IF_FILE" ]; then
    while IFS=';' read -r iface untag tag _; do
        [[ "$iface" =~ ^#.*$ ]] && continue
        [ -z "$iface" ] && continue
        
        IFACE_LIST+=("$iface")
        
        # Untag
        if [ -n "$untag" ] && [ "$untag" != "0" ]; then
             VLAN_MEMBERS_UNTAG["$untag"]+="$iface "
             ALL_VLANS["$untag"]="1"
        fi
        
        # Tag
        if [ -n "$tag" ] && [ "$tag" != "0" ]; then
            for t in ${tag//,/ }; do
                VLAN_MEMBERS_TAG["$t"]+="$iface "
                ALL_VLANS["$t"]="1"
            done
        fi
    done < "$BRIDGE_IF_FILE"
fi

# ----------------------------------------------------------------------
# HTML Output
# ----------------------------------------------------------------------

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Bridge Ebtables Control</title>
<style>
/* Reuse styles from others */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
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
  margin-top: 30px;
}

.container {
    max-width: 900px;
    margin: auto;
}

table {
  border-collapse: collapse;
  margin-bottom: 20px;
  width: 100%;
  background: rgba(15, 23, 42, 0.85);
  border-radius: 8px;
  overflow: hidden;
}

td, th {
  border: 1px solid #475569;
  padding: 10px 14px;
  text-align: left;
  color: #e5e7eb;
}

th {
  background: rgba(34, 211, 238, 0.15);
  font-weight: 700;
  color: #7dd3fc;
}

.status-active {
    color: #4ade80;
    font-weight: bold;
}
.status-inactive {
    color: #94a3b8;
}

.btn {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
  border: none;
  transition: transform 0.1s;
}
.btn:hover { transform: translateY(-1px); }

.btn-enable {
  background: #0f766e;
  color: #fff;
  box-shadow: 0 2px 8px rgba(20, 184, 166, 0.4);
}
.btn-disable {
  background: #991b1b;
  color: #fff;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
}
.btn-back {
    background: #334155;
    color: white;
    margin-top: 20px;
}

.section-desc {
    margin-bottom: 12px;
    color: #94a3b8;
    font-size: 0.9em;
}

.badge {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85em;
    margin-right: 4px;
    display: inline-block;
}
.badge-tag { border-color: #a855f7; color: #e9d5ff; }
.badge-untag { border-color: #0ea5e9; color: #bae6fd; }

</style>
</head>
<body>
<div class="container">

  <h1>Aïllament de xarxa (Ebtables)</h1>
  
  <p class="section-desc">
    Gestiona l'aïllament de tràfic de capa 2 al bridge. Quan s'activa l'aïllament, el tràfic entre els dispositius afectats es bloqueja, però es manté l'accés a Internet (Gateway).
  </p>
  
  <!-- VLAN ISOLATION TABLE -->
  <h2>Aïllament per VLAN</h2>
  <p class="section-desc">
    Bloqueja la comunicació entre dispositius dins de la mateixa VLAN. Detecta automàticament ports Trunk i Access.
  </p>
  
  <table>
    <tr>
        <th style="width: 80px;">VLAN ID</th>
        <th>Interfícies (Untag/Access)</th>
        <th>Interfícies (Tag/Trunk)</th>
        <th style="width: 100px;">Estat</th>
        <th style="width: 120px;">Acció</th>
    </tr>
EOM

# Loop through Sorted VLAN keys
IFS=$'\n' sorted_vlans=($(sort -n <<<"${!ALL_VLANS[*]}"))
unset IFS

for vid in "${sorted_vlans[@]}"; do
    [ -z "$vid" ] && continue
    
    untagged_ifs="${VLAN_MEMBERS_UNTAG[$vid]}"
    tagged_ifs="${VLAN_MEMBERS_TAG[$vid]}"
    
    # Format Interface Lists with Badges
    formatted_untag=""
    for if in $untagged_ifs; do
        formatted_untag="$formatted_untag <span class='badge badge-untag'>$if</span>"
    done
    
    formatted_tag=""
    for if in $tagged_ifs; do
        formatted_tag="$formatted_tag <span class='badge badge-tag'>$if</span>"
    done
    
    # Get State
    state=$(get_vlan_state "$vid")
    
    # HTML Row
    echo "<tr>"
    echo "<td><strong>$vid</strong></td>"
    echo "<td>${formatted_untag:-<span style='color:#555'>-</span>}</td>"
    echo "<td>${formatted_tag:-<span style='color:#555'>-</span>}</td>"
    
    if [ "$state" == "1" ]; then
        echo "<td><span class='status-active'>Activat</span></td>"
        echo "<td><a href='?action=toggle_vlan&vlan=$vid&state=0' class='btn btn-disable'>Desactivar</a></td>"
    else
        echo "<td><span class='status-inactive'>Inactiu</span></td>"
        echo "<td><a href='?action=toggle_vlan&vlan=$vid&state=1' class='btn btn-enable'>Activar</a></td>"
    fi
    echo "</tr>"
done

if [ ${#sorted_vlans[@]} -eq 0 ]; then
    echo "<tr><td colspan='5' style='text-align:center'>No s'han detectat VLANs configurades.</td></tr>"
fi

cat << EOM
  </table>

  <!-- INTERFACE ISOLATION TABLE -->
  <h2>Aïllament per Interfície</h2>
  <p class="section-desc">
    Aïlla completament una interfície física de la resta de interfícies aïllades. (Mode clàssic)
  </p>
  
  <table>
    <tr>
        <th>Interfície</th>
        <th>Estat</th>
        <th>Acció</th>
    </tr>
EOM

for iface in "${IFACE_LIST[@]}"; do
    state=$(get_iface_state "$iface")
    
    echo "<tr>"
    echo "<td><strong>$iface</strong></td>"
    
    if [ "$state" == "1" ]; then
        echo "<td><span class='status-active'>Activat</span></td>"
        echo "<td><a href='?action=toggle_interface&iface=$iface&state=0' class='btn btn-disable'>Desactivar</a></td>"
    else
        echo "<td><span class='status-inactive'>Inactiu</span></td>"
        echo "<td><a href='?action=toggle_interface&iface=$iface&state=1' class='btn btn-enable'>Activar</a></td>"
    fi
    echo "</tr>"
done

cat << EOM
  </table>

  <br>
  <a href="/cgi-bin/bridge-menu.cgi" class="btn btn-back">Tornar al Menú</a>

</div>
</body>
</html>
EOM
