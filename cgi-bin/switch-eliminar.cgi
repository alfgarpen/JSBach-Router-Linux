#!/bin/bash

source /usr/local/JSBach/conf/variables.conf 2>/dev/null
CONF_FILE="/usr/local/JSBach/conf/switchs.conf"

# Check if we are deleting
delete_ip=$(echo "$QUERY_STRING" | sed -n 's/^.*delete_ip=\([^&]*\).*$/\1/p')

if [ -n "$delete_ip" ]; then
    if [ -x "$DIR/$PROJECTE/$DIR_SCRIPTS/switch" ]; then
        result=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/switch eliminar "$delete_ip")
        if [[ "$result" == *"OK"* ]]; then
               # Redirect back to self to refresh list
            echo "Content-Type:text/html;charset=utf-8"
            echo ""
            echo "<html><head><meta http-equiv='refresh' content='0; url=/cgi-bin/switch-eliminar.cgi'></head></html>"
            exit 0
        fi
        # If error, flow down to show error
    fi
fi

# Display current list with delete buttons

echo "Content-Type:text/html;charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  color: #7dd3fc;
  margin-bottom: 20px;
}

table {
  border-collapse: collapse;
  margin: 20px auto;
  width: 90%;
  background: rgba(15, 23, 42, 0.9);
  border-radius: 12px;
  overflow: hidden;
}

td, th {
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 10px 14px;
  text-align: left;
}

th {
  background: rgba(2, 6, 23, 0.95);
  color: #38bdf8;
  font-weight: 600;
}

.del-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 12px;
}

.del-btn:hover {
  background: #dc2626;
}
</style>
</head>
<body>
<h2>Eliminar Switch</h2>

<table>
  <thead>
    <tr>
      <th>Nom</th>
      <th>IP</th>
      <th>Acció</th>
    </tr>
  </thead>
  <tbody>
EOM

if [ -f "$CONF_FILE" ]; then
    while IFS=";" read -r nombre ip usuario pass; do
        [[ "$nombre" =~ ^#.*$ ]] && continue
        [[ -z "$nombre" ]] && continue

        echo "<tr>"
        echo "<td>$nombre</td>"
        echo "<td>$ip</td>"
        echo "<td><a href='/cgi-bin/switch-eliminar.cgi?delete_ip=$ip' class='del-btn' onclick=\"return confirm('Segur que vols eliminar aquest switch?');\">Eliminar</a></td>"
        echo "</tr>"
    done < "$CONF_FILE"
else
    echo "<tr><td colspan='3'>No hi ha switches configurats.</td></tr>"
fi

cat << EOM
  </tbody>
</table>

<div style="text-align:center; margin-top:20px;">
  <a href="/cgi-bin/switch-menu.cgi" style="color: #38bdf8; text-decoration:none;">Tornar al menú</a>
</div>

</body>
</html>
EOM
