#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# https://docs.python-telegram-bot.org/en/v20.6/examples.conversationbot2.html

import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
from art import art

from source.start import Start
from source.count import Count

logger = logging.getLogger(__name__)
# Инициализировать объекты отдельных веток
s = Start()
c = Count()

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id

    msg = 'Основные команды\n/start - основное меню\n/count - примерный расчет вычета\n/info - информация о проекте'

    await context.bot.send_message(
        chat_id=uid, text=msg, disable_web_page_preview=True
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    uid = update.effective_chat.id
    msg = f'Спасибо, что заглянул{art("heart bold")}\nПри создании бота я хотел собрать для тебя в одном месте основную информацию по личным налогам и простым языком рассказать, как получить налоговый вычет.\nНадеюсь, информация оказалась для тебя полезна и ты смог без труда получить приятный бонус в виде налогового вычета. Если есть проблемы или предложения, обязательно пиши мне в <a href="ВК">ВК</a> или <a href="телеграм">Телегу</a> .'

    await context.bot.send_message(
        chat_id=uid, text=msg, parse_mode="HTML", disable_web_page_preview=False)
    
def main(token: str):
      
    app = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", s.start)
    start_conv = s.conversation(entry=[start_handler])

    start_count = CommandHandler("count", c.count)
    conv_count = c.conversation(entry=[start_count])

    start_ndfl = CommandHandler('ndfl')
    conv_ndfl = n.conversation(entry=[start_ndfl])

    help_handler = CommandHandler("help", help)

    info_handler = CommandHandler("info", info)

    app.add_handlers([start_conv, conv_count, conv_ndfl, help_handler, info_handler])

    app.run_polling()
