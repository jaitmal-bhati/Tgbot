import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

# ---------- Configuration ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")          # Set in hosting platform
OWNER_ID  = int(os.getenv("OWNER_ID")) # Your Telegram numeric chat_id

# ---------- Handlers ----------
async def forward_to_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Forward every message (text, photo, etc.) from any user to the owner.
    """
    if update.effective_chat.id != OWNER_ID:
        await context.bot.forward_message(
            chat_id=OWNER_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )

async def relay_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    When the owner replies to a forwarded message,
    send the reply text back to the original sender.
    """
    if update.effective_chat.id == OWNER_ID and update.message.reply_to_message:
        fwd_user = update.message.reply_to_message.forward_from
        if fwd_user:  # ensures original sender is available
            await context.bot.send_message(
                chat_id=fwd_user.id,
                text=update.message.text
            )

# ---------- Main ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Forward everything you receive to the owner
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_to_owner))
    # Owner replies are relayed back to the original user
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, relay_reply))

    print("Bot is running…")
    app.run_polling()

if __name__ == "__main__":
    main()
