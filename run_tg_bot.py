#!/usr/bin/env python

from environs import Env

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from run_dialogflow import create_api_key, detect_intent_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def send_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    create_api_key()

    dialogflow_response = detect_intent_text(
        session_id=update.message.chat.id,
        text=update.message.text,
    )

    await update.message.reply_text(dialogflow_response)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    tg_token = env.str("TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(tg_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_msg))
    application.run_polling()
