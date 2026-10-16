"""Genera archivos de ventas de ejemplo (datos inventados) para probar el reporte."""
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)

PRODUCTOS = {
    "Camisa": 12.5,
    "Pantalon": 20.0,
    "Zapatos": 35.0,
    "Gorra": 8.0,
    "Bolso": 25.0,
}
VENDEDORES = ["Ana", "Luis", "Maria"]

carpeta = Path("datos")
carpeta.mkdir(exist_ok=True)

for mes in (1, 2, 3):
    filas = []
    for _ in range(40):
        producto = random.choice(list(PRODUCTOS))
        filas.append(
            {
                "Fecha": date(2026, mes, 1) + timedelta(days=random.randint(0, 27)),
                "Producto": producto,
                "Cantidad": random.randint(1, 6),
                "Precio_Unitario": PRODUCTOS[producto],
                "Vendedor": random.choice(VENDEDORES),
            }
        )
    pd.DataFrame(filas).to_excel(carpeta / f"ventas_mes_{mes}.xlsx", index=False)

print(f"Listo: archivos de ejemplo creados en la carpeta '{carpeta}'.")
