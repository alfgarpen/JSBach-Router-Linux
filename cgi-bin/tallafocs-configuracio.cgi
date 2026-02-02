#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Gestió Tallafocs per VLAN</title>

<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

.vlan-card {
  background: rgba(15, 23, 42, 0.85);
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 16px;
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.25);
}

.vlan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.vlan-title {
  font-size: 18px;
  font-weight: 700;
  color: #7dd3fc;
  border-left: 5px solid #22d3ee;
  padding-left: 12px;
}

.vlan-ip {
  font-size: 13px;
  color: #94a3b8;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 6px 16px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(34, 211, 238, 0.8);
}

button.warn {
  background: linear-gradient(135deg, #dc2626, #f87171);
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.5);
}

.status-ok {
  color: #4ade80;
  font-weight: 700;
}

.status-down {
  color: #f87171;
  font-weight: 700;
}
</style>
</head>
<body>
EOM

for linia in $(grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"); do
    nom=$(echo "$linia" | cut -d';' -f1)
    id=$(echo "$linia" | cut -d';' -f2)
    ip=$(echo "$linia" | cut -d';' -f3)

    estat_vlan=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat $id)

    if [ "$estat_vlan" == "CONNECTADA" ]; then
        estat_html="<span class='status-ok'>CONNECTADA</span>"
    else
        estat_html="<span class='status-down'>DESCONNECTADA</span>"
    fi

    echo "<div class='vlan-card'>"
    echo "  <div class='vlan-header'>"
    echo "    <div class='vlan-title'>$nom</div>"
    echo "    <div class='vlan-ip'>$ip · $estat_html</div>"
    echo "  </div>"
    echo "  <div class='actions'>"

    if [ "$estat_vlan" == "CONNECTADA" ]; then
        echo "    <a href='tallafocs-conndeconn.cgi?id=$id&accio=desconnectar'><button class='warn'>Desconnectar</button></a>"
    else
        echo "    <a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar'><button>Connectar</button></a>"
        echo "    <a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar_port_wls'><button>Connectar ports WLS</button></a>"
    fi

    echo "  </div>"
    echo "</div>"
done

/bin/cat << EOM
</body>
</html>
EOM


