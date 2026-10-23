# chequear-contraseñas

Script de Python que te dice si una contraseña aparece en filtraciones conocidas (bases de datos robadas en hackeos), usando la API pública y gratuita de [HaveIBeenPwned](https://haveibeenpwned.com/).

Complemento del [gestor de contraseñas](https://github.com/acostanoemi/gestor-contrasenas): ese las guarda, este te avisa si alguna ya está quemada y conviene cambiarla.

## Lo importante: nunca manda tu contraseña

Usa una técnica llamada **k-anonymity**:

1. Calcula el hash SHA-1 de tu contraseña.
2. Manda al servidor **solo los primeros 5 caracteres** del hash.
3. El servidor devuelve todos los hashes filtrados que empiezan con esos 5.
4. Busca tu hash completo en esa lista, **en tu máquina**.

El servidor nunca ve tu contraseña, ni su hash completo, ni cuál de los cientos de resultados te interesaba. Averiguás lo que querías sin revelar nada.

## Requisitos

Solo Python 3 (usa `hashlib` y `urllib`, ambos incluidos). Necesita conexión a internet.

## Uso

```bash
python3 chequear_pass.py                      # una, oculta (no se ve al tipear)
python3 chequear_pass.py --texto              # una, visible
python3 chequear_pass.py --archivo claves.txt # varias, una por línea
```

Te dice si cada contraseña fue filtrada y cuántas veces apareció en bases robadas. Con `--archivo` chequea una lista entera y muestra un resumen (sin imprimir las contraseñas completas).

## Nota

Que una contraseña no esté filtrada no significa que sea fuerte, solo que no apareció (todavía) en una filtración conocida. Para contraseñas fuertes, usá un generador (el gestor de contraseñas tiene uno).

## Roadmap

- [x] v1: chequear una contraseña contra HaveIBeenPwned (k-anonymity)
- [x] v2: chequear varias de una (desde un archivo)
- [x] v3: integrado en el gestor de contraseñas (comando `check` revisa todo el vault)
