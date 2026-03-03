#!/bin/bash

# Este script debería manejar el guardado si recibe POST
# Por ahora mostramos el formulario

source /usr/local/JSBach/conf/variables.conf
source /usr/local/JSBach/conf/portal.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<style>
body { font-family: sans-serif; background: #0f172a; color: #e5e7eb; padding: 20px; }
h2 { border-left: 5px solid #38bdf8; padding-left: 10px; color: #7dd3fc; }
.card { background: rgba(30, 41, 59, 0.7); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
.form-group { margin-bottom: 15px; }
label { display: block; margin-bottom: 5px; color: #94a3b8; }
input, select { width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: white; }
.btn-save { background: #38bdf8; color: #0f172a; border: none; padding: 10px 20px; border-radius: 999px; font-weight: bold; cursor: pointer; margin-top: 10px; }
</style>
</head>
<body>
    <h2>Configuración General</h2>

    <form method="POST" action="portal-guardar-config.cgi">
    <div class="card">
        <div class="form-group">
            <label>Activar Portal Cautivo</label>
            <select name="ENABLED">
                <option value="1" $( [ "$ENABLED" -eq 1 ] && echo "selected" )>Activado</option>
                <option value="0" $( [ "$ENABLED" -eq 0 ] && echo "selected" )>Desactivado</option>
            </select>
        </div>

        <div class="form-group">
            <label>VLAN aplicada</label>
            <select name="VLAN_VID">
EOM

# Listar VLANs disponibles
grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF" | while read -r line; do
    vid=$(echo "$line" | cut -d';' -f2)
    name=$(echo "$line" | cut -d';' -f1)
    echo "<option value='$vid' $( [ "$vid" == "$VLAN_VID" ] && echo "selected" )>$name (VID: $vid)</option>"
done

cat << EOM
            </select>
        </div>

        <div class="form-group">
            <label>Tiempo máximo de sesión (segundos)</label>
            <input type="number" name="SESSION_TIMEOUT" value="$SESSION_TIMEOUT">
        </div>

        <div class="form-group">
            <label>Tiempo de inactividad (segundos)</label>
            <input type="number" name="IDLE_TIMEOUT" value="$IDLE_TIMEOUT">
        </div>

        <div class="form-group">
            <label>Walled Garden (IPs/dominios separados por coma)</label>
            <input type="text" name="WALLED_GARDEN" value="$WALLED_GARDEN">
        </div>
    </div>

    <h3>Personalización Visual</h3>
    <div class="card">
         <div class="form-group">
            <label>Texto de bienvenida</label>
            <input type="text" name="WELCOME_TEXT" value="$WELCOME_TEXT">
        </div>
        <div class="form-group">
            <label>Color principal (Hex)</label>
            <input type="color" name="PRIMARY_COLOR" value="$PRIMARY_COLOR">
        </div>
    </div>

    <button type="submit" class="btn-save">Guardar Configuración</button>
    </form>
</body>
</html>
EOM
