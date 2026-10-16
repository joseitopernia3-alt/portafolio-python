# Scraper de precios a Excel

Descarga título, precio, calificación y disponibilidad de libros desde
[books.toscrape.com](https://books.toscrape.com) (sitio hecho para practicar
scraping) y los guarda en Excel y CSV.

*English: web scraper that extracts book titles, prices, ratings and availability into Excel/CSV.*

## Cómo usarlo
```bash
pip install -r requirements.txt
python scraper_libros.py              # 3 páginas
python scraper_libros.py --paginas 10
```
Genera `libros.xlsx` y `libros.csv`.

Incluye reintentos si falla la conexión y una pausa entre peticiones para no
saturar el sitio. Para otra página web solo hay que cambiar los selectores en
la función `extraer_libros`.

Hecho con Python, requests, BeautifulSoup y pandas.
