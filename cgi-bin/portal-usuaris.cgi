#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<style>
body { font-family: sans-serif; background: #0f172a; color: #e5e7eb; padding: 20px; }
h2 { border-left: 5px solid #38bdf8; padding-left: 10px; color: #7dd3fc; }
.card { background: rgba(30, 41, 59, 0.7); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px; border-bottom: 1px solid #334155; text-align: left; }
.btn { border: none; padding: 8px 15px; border-radius: 6px; cursor: pointer; font-weight: bold; }
.btn-add { background: #38bdf8; color: #0f172a; margin-bottom: 15px; }
.btn-del { background: #ef4444; color: white; }
</style>
</head>
<body>
    <h2>Gestión de Usuarios del Portal</h2>
    
    <button class="btn btn-add">Crear Nuevo Usuario</button>

    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>Usuario</th>
                    <th>Expiración</th>
                    <th>Límite BW</th>
                    <th>Disp. Máx.</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
EOM

while IFS=: read -r user salt hash expiry bw limit; do
    [[ "$user" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$user" ]] && continue
    
    echo "<tr>
            <td>$user</td>
            <td>$( [ "$expiry" == "0" ] && echo "Nunca" || echo "$expiry" )</td>
            <td>$( [ "$bw" == "0" ] && echo "Sin límite" || echo "$bw Mbps" )</td>
            <td>$( [ "$limit" == "0" ] && echo "Ilimitado" || echo "$limit" )</td>
            <td>
                <button class='btn'>Editar</button>
                <button class='btn btn-del'>Eliminar</button>
            </td>
          </tr>"
done < /usr/local/JSBach/conf/portal_users.conf

cat << EOM
            </tbody>
        </table>
    </div>
</body>
</html>
EOM
