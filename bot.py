import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    WebAppInfo, MenuButtonWebApp,
)
from telegram.ext import (
    Application, CommandHandler, ContextTypes, filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]          # токен от @BotFather
WEBAPP_URL = os.environ["WEBAPP_URL"]        # https-ссылка на index.html
# ID разрешённых пользователей через запятую, например: "123456,789012"
ALLOWED = {int(x) for x in os.environ.get("ALLOWED_IDS", "").split(",") if x.strip()}

# Фильтр: отвечаем только тебе и другу
only_me = filters.User(user_id=ALLOWED) if ALLOWED else filters.ALL


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await update.message.reply_text("Привет! Жми кнопку, чтобы открыть игры.", reply_markup=kb)


async def my_id(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # Работает для всех: нужна, чтобы узнать свой ID и вписать в ALLOWED_IDS
    await update.message.reply_text(f"Твой ID: {update.effective_user.id}")


async def post_init(app: Application):
    # Кнопка «Игры» рядом с полем ввода
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Игры", web_app=WebAppInfo(url=WEBAPP_URL))
    )


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("id", my_id))
    app.add_handler(CommandHandler("start", start, filters=only_me))
    app.run_polling()


if __name__ == "__main__":
    main()
