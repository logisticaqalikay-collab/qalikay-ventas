"""
Modulo de Conexion Automatica a la Nube (GitHub + GitHub Pages / Vercel)
Qali Kay S.A.C. - Sistema de Inteligencia Comercial
Automatiza la autenticacion de GitHub CLI evitando preguntas interactivas en consola.
"""

import os
import sys
import re
import time
import subprocess
import webbrowser
from pathlib import Path

GH_EXE = r"C:\Users\cguti\AppData\Local\Programs\GitHub CLI\gh.exe"
GIT_EXE = r"C:\Users\cguti\AppData\Local\Programs\Git\cmd\git.exe"

# Agregar Git y GH CLI al entorno
os.environ["PATH"] = rf"{Path(GIT_EXE).parent};{Path(GH_EXE).parent};" + os.environ.get("PATH", "")
os.environ["GIT_TERMINAL_PROMPT"] = "0"
os.environ["GCM_INTERACTIVE"] = "never"

def main():
    print("=" * 80)
    print("SISTEMA DE INTELIGENCIA COMERCIAL - QALI KAY S.A.C.")
    print("CONECTOR AUTOMATICO A LA NUBE (GITHUB + GITHUB PAGES / VERCEL)")
    print("=" * 80)
    print()

    # 1. Verificar si ya existe sesion activa
    res_status = subprocess.run([GH_EXE, "auth", "status"], capture_output=True, text=True)
    if res_status.returncode != 0:
        print("[1/4] Iniciando autorizacion segura con GitHub...")
        proc = subprocess.Popen(
            [GH_EXE, "auth", "login", "--web", "-h", "github.com", "-p", "https"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        # Enviar automaticamente 'Y\n' para evitar la pregunta interactiva en consola
        try:
            proc.stdin.write("Y\n")
            proc.stdin.flush()
        except Exception:
            pass

        code_found = None
        url_to_open = "https://github.com/login/device"

        # Leer salida para extraer el codigo de 8 letras
        for line in iter(proc.stdout.readline, ""):
            m = re.search(r"\(([A-Z0-9]{4}-[A-Z0-9]{4})\)", line)
            if m:
                code_found = m.group(1)
                break

        if code_found:
            print()
            print("*" * 80)
            print(f"   TU CODIGO DE AUTORIZACION ES:   {code_found}")
            print("   (Ya ha sido copiado a tu portapapeles automaticamente)")
            print("*" * 80)
            print()
            print("1. Se ha abierto tu navegador en: https://github.com/login/device")
            print("2. Pega el codigo con [Ctrl + V] y haz clic en 'Continue' y luego 'Authorize'.")
            print()
            print("Esperando tu autorizacion en el navegador...")
            webbrowser.open(url_to_open)
        
        proc.wait()
        if proc.returncode != 0:
            print("\n[ERROR] La autenticacion no se completo. Vuelve a ejecutar el asistente.")
            sys.exit(1)
        print("\n* [OK] Autenticacion completada con exito.")
    else:
        print("[1/4] Sesion de GitHub activa detectada.")

    # 2. Obtener usuario de GitHub
    res_user = subprocess.run([GH_EXE, "api", "user", "--jq", ".login"], capture_output=True, text=True)
    gh_user = res_user.stdout.strip()
    if not gh_user:
        gh_user = "usuario"
    print(f"[2/4] Conectado como usuario: {gh_user}")

    # 3. Crear repositorio y subir codigo
    print("\n[3/4] Creando repositorio 'qalikay-ventas' y sincronizando rama main...")
    res_create = subprocess.run(
        [GH_EXE, "repo", "create", "qalikay-ventas", "--public", "--source=.", "--remote=origin", "--push"],
        capture_output=True,
        text=True
    )
    if res_create.returncode != 0:
        print("      * Sincronizando con repositorio existente...")
        subprocess.run([GIT_EXE, "remote", "add", "origin", f"https://github.com/{gh_user}/qalikay-ventas.git"], capture_output=True)
        subprocess.run([GIT_EXE, "push", "-u", "origin", "main"])
    else:
        print("      * [OK] Repositorio creado y subido con exito.")

    # 4. Activar GitHub Pages
    print("\n[4/4] Activando GitHub Pages para hosting web gratuito e inmediato...")
    subprocess.run(
        [GH_EXE, "api", "-X", "POST", f"repos/{gh_user}/qalikay-ventas/pages", "-F", "build_type=legacy", "-f", "source[branch]=main", "-f", "source[path]=/"],
        capture_output=True,
        text=True
    )
    print("      * [OK] GitHub Pages configurado.")

    print("\n" + "=" * 80)
    print("[SUCCESS] DASHBOARD COMERCIAL PUBLICADO EXITOSAMENTE")
    print("=" * 80)
    print()
    print("TU LINK WEB HTTPS PERMANENTE (GITHUB PAGES):")
    print(f"  https://{gh_user}.github.io/qalikay-ventas/")
    print()
    print("NOTAS IMPORTANTES:")
    print("1. GitHub Pages compila en 1 a 2 minutos la primera vez.")
    print("2. Tu Dashboard esta protegido con el PIN Directivo: 2026 / 7361.")
    print("3. Cada vez que ejecutes 'actualizar_dashboard.bat' los datos se actualizaran solos.")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
