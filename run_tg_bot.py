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
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def send_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    env = Env()
    env.read_env()

    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')

    create_api_key(dialogflow_project_id)

    dialogflow_response = detect_intent_text(
        project_id=dialogflow_project_id,
        session_id='16121996',
        text=update.message.text,
    )
    """Echo the user message."""
    await update.message.reply_text(dialogflow_response)


def main() -> None:
    env = Env()
    env.read_env()

    tg_token = env.str("TELEGRAM_BOT_TOKEN")

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(tg_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_msg))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
