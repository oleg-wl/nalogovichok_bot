import logging

from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from utils.utils import ndfl as _ndfl
from .start import Start
from utils.keyboards import Keyboard

logger = logging.getLogger(__name__)

class Ndfl(Start):
    msg = 'текст'

    def __repr__(self) -> str:
        return "Инициализирован объект класса ndfl"

    START, BACK = range(1)

    async def start_conv(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_chat.id
        name = update.effective_chat.username
        text = self.msg

    await context.bot.send_message(
        chat_id=uid, text=text, reply_markup=Keyboard.bkb
    )

    return self.START

    async def ndfl(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_chat.id
        income = update.message.text

        try:
            i = int(income)
            t = _ndfl(i)

            await context.bot.send_message(
                text=t,
                chat_id=uid,
                reply_markup=Keyboard.bkb,
            )
            return self.START

        except ValueError:
            await context.bot.send_message(
                text="Введи ежемесячную зарплату без пробелов, например 2000000", chat_id=uid
            )
            return self.START

        except Exception as e:
            await context.bot.send_message(
                text="Прощу прощения, произошла ошибка", chat_id=uid
            )
            logger.exception("Error: %s", exc_info=e)
            return ConversationHandler.END

        