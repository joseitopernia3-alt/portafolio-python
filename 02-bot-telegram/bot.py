"""
Bot de Telegram para un negocio pequeno: catalogo, precios y contacto.

Configuracion:
    1. Habla con @BotFather en Telegram, crea un bot con /newbot y copia el token.
    2. Define la variable de entorno TELEGRAM_TOKEN con ese token.
       Windows (PowerShell):  $env:TELEGRAM_TOKEN="tu_token"
       Linux / Mac:           export TELEGRAM_TOKEN="tu_token"
    3. Ejecuta:  python bot.py
"""
import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Datos del negocio (cambialos por los de tu cliente) ---------------------
NEGOCIO = "Tienda Ejemplo"
HORARIO = "Lunes a sabado, 9:00 am a 6:00 pm"
CONTACTO = "Escribe aqui tu telefono o enlace de contacto"

CATALOGO = {
    "camisa": {"nombre": "Camisa", "precio": 12.5, "detalle": "Algodon, tallas S a XL."},
    "pantalon": {"nombre": "Pantalon", "precio": 20.0, "detalle": "Jean, tallas 28 a 38."},
    "zapatos": {"nombre": "Zapatos", "precio": 35.0, "detalle": "Cuero sintetico, 36 a 44."},
    "gorra": {"nombre": "Gorra", "precio": 8.0, "detalle": "Ajustable, varios colores."},
}
# -----------------------------------------------------------------------------


def texto_producto(clave: str) -> str:
    p = CATALOGO[clave]
    return f"*{p['nombre']}*\nPrecio: ${p['precio']:.2f}\n{p['detalle']}"


def teclado_catalogo() -> InlineKeyboardMarkup:
    botones = [
        [InlineKeyboardButton(f"{p['nombre']} - ${p['precio']:.2f}", callback_data=clave)]
        for clave, p in CATALOGO.items()
    ]
    return InlineKeyboardMarkup(botones)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nombre = update.effective_user.first_name or "amigo"
    await update.message.reply_text(
        f"Hola {nombre}, bienvenido a {NEGOCIO}.\n\n"
        "Comandos disponibles:\n"
        "/catalogo - ver productos\n"
        "/precio <producto> - consultar un precio\n"
        "/horario - horario de atencion\n"
        "/contacto - como comunicarte con nosotros"
    )


async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Estos son nuestros productos. Toca uno para ver el detalle:",
        reply_markup=teclado_catalogo(),
    )


async def al_tocar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    consulta = update.callback_query
    await consulta.answer()
    clave = consulta.data
    if clave in CATALOGO:
        await consulta.message.reply_text(texto_producto(clave), parse_mode="Markdown")


async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usa: /precio <producto>. Ejemplo: /precio camisa")
        return
    clave = " ".join(context.args).strip().lower()
    if clave in CATALOGO:
        await update.message.reply_text(texto_producto(clave), parse_mode="Markdown")
    else:
        disponibles = ", ".join(CATALOGO)
        await update.message.reply_text(
            f"No encontre '{clave}'. Productos disponibles: {disponibles}."
        )


async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Atendemos: {HORARIO}")


async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(CONTACTO)


async def mensaje_libre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Si escriben un nombre de producto sin comando, tambien responde."""
    texto = (update.message.text or "").strip().lower()
    if texto in CATALOGO:
        await update.message.reply_text(texto_producto(texto), parse_mode="Markdown")
    else:
        await update.message.reply_text("No te entendi. Prueba con /catalogo o /start.")


def main() -> None:
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise SystemExit("Falta la variable de entorno TELEGRAM_TOKEN (ver instrucciones arriba).")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalogo", catalogo))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("horario", horario))
    app.add_handler(CommandHandler("contacto", contacto))
    app.add_handler(CallbackQueryHandler(al_tocar_producto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_libre))

    logger.info("Bot en marcha. Presiona Ctrl+C para detenerlo.")
    app.run_polling()


if __name__ == "__main__":
    main()
