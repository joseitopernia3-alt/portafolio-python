# Bot de Telegram para un negocio pequeño

Bot con catálogo de productos, consulta de precios, horario y contacto.
Fácil de adaptar: solo se editan los datos del negocio al inicio de `bot.py`.

*English: simple Telegram bot for a small business (catalog, prices, hours, contact). Easy to customize.*

## Comandos
`/start` · `/catalogo` (con botones) · `/precio camisa` · `/horario` · `/contacto`

## Cómo usarlo
1. En Telegram, habla con **@BotFather**, escribe `/newbot` y copia el token.
2. Instala y ejecuta:
```bash
pip install -r requirements.txt
# Windows (PowerShell)
$env:TELEGRAM_TOKEN="tu_token"
# Linux / Mac
export TELEGRAM_TOKEN="tu_token"

python bot.py
```
El token nunca va escrito dentro del código; se lee de una variable de entorno.

Hecho con Python y python-telegram-bot.
