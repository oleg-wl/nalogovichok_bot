import datetime
from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from database.db import Database
from utils.keyboards import Keyboard
from utils.utils import ndfl as _ndfl

db = Database()
class Start:

    CHOOSE, BACK, NDFL = range(3)

    def __repr__(self) -> str:
        return "Инициализирован класс StartConv"

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_chat.id
        uname = update.effective_chat.username
        fname = update.effective_chat.first_name
        now = datetime.datetime.now()

        db._create_user(chat_id=uid, username=uname, firstname=fname, created_at=now)
        
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

    async def ndfl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # вход в секцию для расчета ндфл
        uid = update.effective_chat.id

        await context.bot.send_message(
                text="Давай посчитаем НДФЛ так если бы мы жили в 2025 году\nВведи желаемую зарплату в месяц без пробелов, например 2000000",
                chat_id=uid,
                reply_markup=Keyboard.bkb,
            )
        return self.NDFL

    async def count_ndfl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_chat.id
        #query = update.callback_query
        
        income = update.message.text

        #await query.answer()

        try:
            i = int(income)
            t = _ndfl(i)

            await context.bot.send_message(
                text=t,
                chat_id=uid,
                reply_markup=Keyboard.bkb,
            )
            return self.NDFL

        except ValueError:
            await context.bot.send_message(
                text="Введи ежемесячную зарплату без пробелов, например 2000000", chat_id=uid
            )
            return self.NDFL

        except Exception as e:
            await context.bot.send_message(
                text="Прощу прощения, произошла ошибка", chat_id=uid
            )
            logger.exception("Error: %s", exc_info=e)
            return ConversationHandler.END

    def conversation(self, entry: list[CommandHandler]) -> ConversationHandler:

        conversation = ConversationHandler(
            entry_points=entry,
            states={
                self.CHOOSE: [
                    CallbackQueryHandler(self.about, pattern="1"),
                    CallbackQueryHandler(self.howto, pattern="2"),
                    CallbackQueryHandler(self.ndfl, pattern="3")
                ],
                self.BACK: [
                    CallbackQueryHandler(self.back, pattern="back"),
                ],
                self.NDFL : [
                    MessageHandler(callback=self.count_ndfl, filters=~(filters.COMMAND)),
                    CallbackQueryHandler(self.back, pattern="back")
                    ]
            },
            fallbacks=entry,
        )
        return conversation
