from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from utils.keyboards import Keyboard


class Start:

    CHOOSE, BACK = range(2)

    def __repr__(self) -> str:
        return "Инициализирован класс StartConv"

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_chat.id
        uname = update.effective_chat.username
        msg_id = update.message.message_id 

        await context.bot.send_message(
            chat_id=uid,
            text=f"Привет {uname}, я бот Налоговичок.\nЯ могу рассказать тебе про налоговые вычеты и как их получить\nО чем ты хочешь узнать? \nили /count чтобы посчитать вычет",
            reply_markup=Keyboard.kb
        )

        return self.CHOOSE

    async def about(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_chat.id
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(
            text='Я могу рассказать тебе, <a href="https://telegra.ph/Kakie-vychety-est-01-29-2">какие бывают налоговые вычеты</a>',
            parse_mode="HTML",
            reply_markup=Keyboard.bkb,
        )
        return self.BACK

    async def howto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_chat.id
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(
            text='Я могу рассказать тебе, <a href="https://telegra.ph/Kak-poluchit-nalogovyj-vychet-02-02">как получить налоговый вычет</a>',
            parse_mode="HTML",
            reply_markup=Keyboard.bkb,
            disable_web_page_preview=False,
        )
        return self.BACK

    async def back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(
            text="Что бы ты хотел узнать?", reply_markup=Keyboard.kb, parse_mode="HTML"
        )
        return self.CHOOSE

    def conversation(self, entry: list[CommandHandler]) -> ConversationHandler:

        conversation = ConversationHandler(
            entry_points=entry,
            states={
                self.CHOOSE: [
                    CallbackQueryHandler(self.about, pattern="1"),
                    CallbackQueryHandler(self.howto, pattern="2"),
                    #CallbackQueryHandler(Count.count, pattern='/count')
                ],
                self.BACK: [
                    CallbackQueryHandler(self.back, pattern="back"),
                ],
            },
            fallbacks=entry,
        )
        return conversation
