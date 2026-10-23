#!/usr/bin/env python3
"""
Chequeador de contraseñas filtradas - v1

Te dice si una contraseña aparece en filtraciones conocidas (bases de datos
robadas en hackeos), usando la API publica y gratuita de HaveIBeenPwned.

LO IMPORTANTE: nunca manda tu contraseña a ningun lado. Usa "k-anonymity":
  1. Calcula el hash SHA-1 de tu contraseña.
  2. Manda al servidor SOLO los primeros 5 caracteres del hash.
  3. El servidor devuelve TODOS los hashes filtrados que empiezan con esos 5.
  4. Buscamos tu hash completo en esa lista, acá en tu maquina.
El servidor nunca ve tu contraseña, ni su hash completo, ni cual te interesa.

Uso:
    python3 chequear_pass.py                 # te la pide oculta (no se ve)
    python3 chequear_pass.py --texto         # la escribis visible (menos seguro)
"""

import sys
import hashlib
import getpass
import argparse
import urllib.request

API = "https://api.pwnedpasswords.com/range/"


def veces_filtrada(password):
    """
    Devuelve cuantas veces aparece la password en filtraciones (0 = nunca).
    """
    # Hash SHA-1 de la password, en MAYUSCULAS (formato que usa la API)
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefijo, sufijo = sha1[:5], sha1[5:]

    # Solo mandamos el prefijo de 5 caracteres
    url = API + prefijo
    with urllib.request.urlopen(url, timeout=10) as r:
        cuerpo = r.read().decode()

    # La respuesta es una lista: "SUFIJO:CANTIDAD" por linea.
    # Buscamos NUESTRO sufijo. Si esta, devolvemos su cantidad.
    for linea in cuerpo.splitlines():
        suf, cuenta = linea.split(":")
        if suf == sufijo:
            return int(cuenta)
    return 0


def main():
    p = argparse.ArgumentParser(
        description="Chequea si una contraseña aparece en filtraciones conocidas."
    )
    p.add_argument("--texto", action="store_true",
                   help="escribir la contraseña visible (por defecto va oculta)")
    args = p.parse_args()

    if args.texto:
        password = input("Contraseña a chequear: ")
    else:
        password = getpass.getpass("Contraseña a chequear (no se ve): ")

    if not password:
        print("No escribiste nada.")
        return

    try:
        veces = veces_filtrada(password)
    except Exception as e:
        print(f"No pude consultar la base de filtraciones: {e}")
        print("(Revisá tu conexion a internet.)")
        return

    print()
    if veces == 0:
        print("[OK] Esta contraseña NO aparece en filtraciones conocidas.")
        print("     (No significa que sea fuerte, solo que no fue filtrada aun.)")
    else:
        print(f"[!] FILTRADA: aparece {veces:,} veces en bases robadas.")
        print("    No la uses. Si la estás usando en algún lado, cambiala ya.")


if __name__ == "__main__":
    main()
