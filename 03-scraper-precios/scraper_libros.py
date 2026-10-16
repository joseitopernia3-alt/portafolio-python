"""
Scraper de precios: baja titulo, precio, calificacion y disponibilidad de libros
desde books.toscrape.com (un sitio creado a proposito para practicar scraping)
y los guarda en Excel y CSV.

Uso:
    python scraper_libros.py                 # 3 paginas
    python scraper_libros.py --paginas 10
"""
import argparse
import re
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/catalogue/"
PRIMERA = "https://books.toscrape.com/catalogue/page-1.html"
CABECERAS = {"User-Agent": "Mozilla/5.0 (proyecto de practica de scraping)"}
ESTRELLAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def limpiar_precio(texto: str) -> float:
    """'£51.77' (o con simbolos raros) -> 51.77"""
    numero = re.search(r"\d+(?:\.\d+)?", texto)
    return float(numero.group()) if numero else float("nan")


def extraer_libros(html: str, url_pagina: str) -> tuple[list[dict], str | None]:
    """Devuelve los libros de una pagina y la URL de la siguiente (o None)."""
    sopa = BeautifulSoup(html, "html.parser")
    libros = []
    for tarjeta in sopa.select("article.product_pod"):
        enlace = tarjeta.select_one("h3 a")
        estrellas = tarjeta.select_one("p.star-rating")
        clase = [c for c in (estrellas.get("class") or []) if c != "star-rating"] if estrellas else []
        libros.append(
            {
                "Titulo": enlace.get("title", "").strip(),
                "Precio": limpiar_precio(tarjeta.select_one("p.price_color").get_text()),
                "Calificacion": ESTRELLAS.get(clase[0]) if clase else None,
                "Disponibilidad": tarjeta.select_one("p.availability").get_text(strip=True),
                "URL": urljoin(url_pagina, enlace.get("href", "")),
            }
        )
    siguiente = sopa.select_one("li.next a")
    url_siguiente = urljoin(url_pagina, siguiente["href"]) if siguiente else None
    return libros, url_siguiente


def descargar(url: str, intentos: int = 3) -> str:
    for intento in range(1, intentos + 1):
        try:
            respuesta = requests.get(url, headers=CABECERAS, timeout=15)
            respuesta.raise_for_status()
            respuesta.encoding = "utf-8"
            return respuesta.text
        except requests.RequestException as error:
            print(f"  Intento {intento}/{intentos} fallo: {error}")
            time.sleep(2 * intento)
    raise SystemExit(f"No se pudo descargar {url}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Baja precios de libros a Excel.")
    parser.add_argument("--paginas", type=int, default=3, help="cuantas paginas bajar")
    parser.add_argument("--salida", default="libros", help="nombre base de los archivos")
    args = parser.parse_args()

    todos, url = [], PRIMERA
    for numero in range(1, args.paginas + 1):
        if not url:
            break
        print(f"Pagina {numero}: {url}")
        libros, url = extraer_libros(descargar(url), url)
        todos.extend(libros)
        time.sleep(1)  # pausa de cortesia entre peticiones

    df = pd.DataFrame(todos).drop_duplicates(subset="URL")
    df.to_excel(f"{args.salida}.xlsx", index=False)
    df.to_csv(f"{args.salida}.csv", index=False, encoding="utf-8-sig")
    print(f"\nListo: {len(df)} libros guardados en {args.salida}.xlsx y {args.salida}.csv")
    print(f"Precio promedio: {df['Precio'].mean():.2f} | mas barato: {df['Precio'].min():.2f}")


if __name__ == "__main__":
    main()
