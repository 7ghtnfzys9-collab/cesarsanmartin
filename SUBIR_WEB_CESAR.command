#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
#  SUBIR_WEB_CESAR.command — www.cesarsanmartin.com — 20 de octubre de 2026
#
#  Doble clic para publicar la web.
#
#  Envía a GitHub lo que haya cambiado en esta carpeta. GitHub genera la
#  web (con lo último de YouTube e Instagram) y la publica sola en uno o
#  dos minutos. Además, la regenera cada mañana aunque no toques nada.
# ═══════════════════════════════════════════════════════════════════════

USUARIO_GITHUB="7ghtnfzys9-collab"

cd "$(dirname "$0")" || { echo "No encuentro la carpeta."; read -n 1; exit 1; }

echo "═══════════════════════════════════════════════════════"
echo "  PUBLICAR LA WEB DE CÉSAR SAN MARTÍN"
echo "═══════════════════════════════════════════════════════"
echo

[ -d .git ] || { echo "✗ Esta carpeta no es un repositorio de Git. Avisa a Claude."; echo; read -n 1; exit 1; }

# Candados que deja la máquina de Claude (no puede borrar archivos).
CANDADOS=$(find .git -maxdepth 2 -name '*.lock' 2>/dev/null)
if [ -n "$CANDADOS" ]; then
  if pgrep -x git >/dev/null; then
    echo "⚠ Hay un proceso de git en marcha. Ciérralo y vuelve a intentarlo."
    echo; read -n 1; exit 1
  fi
  echo "$CANDADOS" | while IFS= read -r C; do rm -f "$C" && echo "✓ Retirado un candado suelto ($C)"; done
fi
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null

git config credential.helper osxkeychain 2>/dev/null

# Comprobación: que la web se genere sin errores antes de enviarla.
echo "▸ Comprobando que la web se genera bien…"
if ! /usr/bin/python3 _fuente/build.py; then
  echo
  echo "✗ La web no se ha podido generar. NO se ha enviado nada. Avisa a Claude."
  echo; read -n 1; exit 1
fi
echo

echo "▸ Cambios:"
git status --short
echo
git add -A
if git diff --cached --quiet; then
  echo "  (no hay cambios nuevos que guardar)"
else
  MSG="Actualización de la web — $(date '+%-d/%m/%Y %H:%M')"
  git commit -m "$MSG" >/dev/null && echo "✓ Guardado: $MSG"
fi
echo

PENDIENTES=$(git log --oneline origin/main..HEAD 2>/dev/null | wc -l | tr -d ' ')
if [ "$PENDIENTES" = "0" ]; then
  echo "✓ No hay nada pendiente: la web ya está al día."
  echo; echo "Pulsa una tecla para cerrar."; read -n 1; exit 0
fi

echo "▸ Trayendo antes lo que haya en GitHub…"
git pull --rebase -q origin main || { echo; echo "✗ No se pudo traer lo de GitHub. Copia el mensaje y enséñaselo a Claude."; echo; read -n 1; exit 1; }
echo "▸ Enviando $PENDIENTES cambio(s) a GitHub…"
SALIDA=$(git push origin main 2>&1)
CODIGO=$?
echo "$SALIDA"
echo

if [ $CODIGO -eq 0 ]; then
  echo "═══════════════════════════════════════════════════════"
  echo "  ✓ ENVIADO"
  echo "  GitHub está publicando la web. En uno o dos minutos"
  echo "  estará al día. Avisa a Claude para que lo compruebe."
  echo "═══════════════════════════════════════════════════════"
  echo; echo "Pulsa una tecla para cerrar."; read -n 1; exit 0
fi

if echo "$SALIDA" | grep -qi "workflow"; then
  echo "═══════════════════════════════════════════════════════"
  echo "  ✗ AL TOKEN DE GITHUB LE FALTA UN PERMISO («workflow»)"
  echo "═══════════════════════════════════════════════════════"
  echo
  echo "  Esta web incluye la tarea automática que la actualiza cada día,"
  echo "  y GitHub exige un permiso más en el token para subirla."
  echo
  echo "  1. github.com → tu foto → Settings → Developer settings →"
  echo "     Personal access tokens → Tokens (classic)."
  echo "  2. Abre el token que usas y marca también la casilla «workflow»."
  echo "     Pulsa «Update token» abajo del todo."
  echo "  3. Vuelve a hacer doble clic en este archivo."
  echo
  echo "  (Si GitHub te obliga a crear un token nuevo, marca «repo» y"
  echo "   «workflow», y responde «s» la próxima vez que este archivo te"
  echo "   ofrezca olvidar las credenciales guardadas.)"
elif echo "$SALIDA" | grep -qiE "Invalid username|Authentication failed|Password authentication"; then
  echo "  ✗ GitHub ha rechazado las credenciales."
  read -p "  ¿Olvidar las credenciales guardadas de GitHub? (s/n) " R
  if [ "$R" = "s" ] || [ "$R" = "S" ]; then
    printf "protocol=https\nhost=github.com\n\n" | git credential-osxkeychain erase 2>/dev/null
    printf "protocol=https\nhost=github.com\nusername=%s\n\n" "$USUARIO_GITHUB" | git credential-osxkeychain erase 2>/dev/null
    echo "  ✓ Olvidadas. Vuelve a hacer doble clic. Usuario: $USUARIO_GITHUB"
    echo "    Contraseña: el TOKEN de GitHub (con «repo» y «workflow» marcados)."
  fi
else
  echo "✗ El envío ha fallado por otro motivo. Copia el mensaje de arriba y enséñaselo a Claude."
fi
echo; echo "Pulsa una tecla para cerrar."; read -n 1
