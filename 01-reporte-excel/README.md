# Reporte automático de ventas en Excel

Une todos los archivos Excel/CSV de una carpeta, limpia los datos y genera un
reporte con resumen, totales por producto, vendedor y mes, y gráficos.

*English: merges all Excel/CSV sales files in a folder, cleans the data and builds a formatted Excel report with summary tables and charts.*

## Qué hace
- Lee todos los `.xlsx` y `.csv` de una carpeta
- Quita filas vacías, espacios sobrantes y datos inválidos
- Crea el Excel `reporte_ventas.xlsx` con las hojas: Resumen, Por producto, Por vendedor, Por mes y Datos

## Cómo usarlo
```bash
pip install -r requirements.txt
python generar_datos_demo.py        # crea datos de ejemplo en la carpeta "datos"
python reporte_ventas.py            # genera reporte_ventas.xlsx
python reporte_ventas.py mi_carpeta -o salida.xlsx
```
Columnas requeridas en los archivos: `Fecha, Producto, Cantidad, Precio_Unitario, Vendedor`.

Opción `--quitar-duplicados`: elimina filas totalmente repetidas (útil si hay archivos duplicados).

Hecho con Python, pandas y openpyxl.
