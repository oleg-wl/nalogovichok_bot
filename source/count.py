# ~~~~~~~~~~~~~~~~
# Модуль в котором реализована логика ConversationHandler бота для расчета
# размера налогового вычета
# ~~~~~~~~~~~~~~~~

import logging
import re

from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from utils.utils import sum_costs, count_intro
from .start import Start
from utils.keyboards import Keyboard

logger = logging.getLogger(__name__)


class Count(Start):
    START_COUNT, VYCHET, SUM, END = range(3, 7)

    def __repr__(self) -> str:
        return "Инициализирован класс count"

    async def count(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_chat.id
        name = update.effective_chat.username
        text = count_intro.format(name)

        await context.bot.send_message(
            chat_id=uid, text=text, reply_markup=Keyboard.keyboard_main
        )

        return self.START_COUNT

    async def ret(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        query = update.callback_query
        name = update.effective_chat.username
        text = count_intro.format(name)

        await query.answer()

        await query.edit_message_text(text=text, reply_markup=Keyboard.keyboard_main)
        return self.START_COUNT

    async def test(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        query = update.callback_query
        t = query.data
        self.kb = Keyboard.alter_keyboard(t=t)

        await query.answer()

        await query.edit_message_text(text="Какой вычет считаем?", reply_markup=self.kb)
        return self.VYCHET

    async def choose(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        query = update.callback_query
        await query.answer()
        
        # Название расхода из inline кнопки
        button_data = update.callback_query.data.lower()
        inline = query.message.reply_markup.inline_keyboard
        
        cost_type = Keyboard.get_inline_button_text(button_data=button_data, inline=inline)
        
        text = "Отлично, считаем {}. Введи сумму в формате целого числа".format(
            cost_type
        )
        context.user_data["type"] = cost_type.lower()

        
        await query.edit_message_text(text=text, reply_markup=Keyboard.bkb)
        return self.SUM

    async def add_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_chat.id
        msg = update.message.text

        try:
            c = int(msg)
            t = context.user_data["type"]

            context.user_data[t] = c
            context.user_data.pop("type")

            await context.bot.send_message(
                text="Принято,  %s = %d " % (t, c),
                chat_id=uid,
                reply_markup=self.kb,
            )
            return self.VYCHET

        except ValueError:
            await context.bot.send_message(
                text="Пожалуйста введи целое число, например 120000", chat_id=uid
            )
            return self.SUM

        except Exception as e:
            await context.bot.send_message(
                text="Прощу прощения, произошла ошибка", chat_id=uid
            )
            logger.exception("Error: %s", exc_info=e)
            return ConversationHandler.END

    async def fin(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_chat.id

        for k, v in context.user_data.items():
            logger.debug(f"{k}-{v}")
        sum = sum_costs(context.user_data)
        for k, v in sum.items():
            logger.debug(f"{k}-{v}")

        msg = "Всего можно заявить к вычету:\nРасходы на лечение, обучение, фитнес: {soc:.0f}\nРасходы на обучение детей: {edu:.0f}\nРасходы на покупку квартиры: {im:.0f}\nРасходы на проценты по ипотеке: {per:.0f}\nИнвестиционный вычет по ИИС: {inv:.0f}".format(
            **sum
        )

        await context.bot.send_message(chat_id=uid, text=msg)
        return ConversationHandler.END

    def conversation(self, entry: list[CommandHandler]) -> ConversationHandler:

        conversation = ConversationHandler(
            entry_points=entry,
            states={
                self.START_COUNT: [
                    CallbackQueryHandler(
                        self.test, pattern=re.compile(r"[social|invest|property]")
                    ),
                    CallbackQueryHandler(callback=self.fin, pattern='fin')
                ],
                self.VYCHET: [
                    CallbackQueryHandler(self.choose, pattern=re.compile(r"\b(?!return)\w+")),
                    CallbackQueryHandler(self.ret, pattern="return"),
                ],
                self.SUM: [
                    CallbackQueryHandler(self.ret, pattern="back"),
                    MessageHandler(callback=self.add_data, filters=~(filters.COMMAND)),
                ],
            },
            fallbacks=entry,
        )
        return conversation
