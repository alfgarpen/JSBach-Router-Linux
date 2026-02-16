#!/bin/bash

source /usr/local/JSBach/conf/variables.conf 2>/dev/null

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
  margin: 20px 0;
  width: 100%;
  background: rgba(15, 23, 42, 0.9);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 22px rgba(0,0,0,0.6);
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
</style>
</head>
<body>
<h2>Taula de MACs dels Switches</h2>

<table>
  <thead>
    <tr>
      <th>Switch</th>
      <th>MAC Address</th>
      <th>Port</th>
      <th>VLAN</th>
    </tr>
  </thead>
  <tbody>
EOM

if [ -x "$DIR/$PROJECTE/$DIR_SCRIPTS/switch" ]; then
    echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/switch macs)"
else
    echo "<tr><td colspan='4'>Error: No s'ha trobat l'script del switch.</td></tr>"
fi

cat << EOM
  </tbody>
</table>
</body>
</html>
EOM
