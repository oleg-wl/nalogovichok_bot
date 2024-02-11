from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils.utils import build_menu


class Keyboard:

    back_button = [InlineKeyboardButton("<< Вернуться", callback_data="back")]
    bkb = InlineKeyboardMarkup([back_button])

    kb = InlineKeyboardMarkup(
        build_menu(
            [
                InlineKeyboardButton("Какие вычеты есть?", callback_data="1"),
                InlineKeyboardButton("Как получить вычет?", callback_data="2"),
                #InlineKeyboardButton("Рассчитать вычет", callback_data='/count')
            ],
            1,
        )
    )


    keyboard_main = InlineKeyboardMarkup(
        build_menu(
            [
                InlineKeyboardButton(
                    "Ввести социальные вычеты", callback_data="social"
                ),
                InlineKeyboardButton(
                    "Ввести имущественные вычеты", callback_data="property"
                ),
                InlineKeyboardButton(
                    "Ввести инвестиционный вычет", callback_data="invest"
                ),
                InlineKeyboardButton(
                    ">> Рассчитать вычет", callback_data="fin"
                ),
            ],
            1,
        )
    )

    keyboard_soc = InlineKeyboardMarkup(
        build_menu(
            [
                InlineKeyboardButton("Расходы на лечение", callback_data="heal"),
                InlineKeyboardButton("Расходы на обучение", callback_data="education"),
                InlineKeyboardButton("Расходы на фитнес", callback_data="fitnes"),
                InlineKeyboardButton(
                    "Расходы на обучение детей", callback_data="child"
                ),
                InlineKeyboardButton("Выбрать другой вычет", callback_data="return"),
            ],
            1,
        )
    )
    keyboard_property = InlineKeyboardMarkup(
        build_menu(
            [
                InlineKeyboardButton(
                    "Расходы на покупку квартиры", callback_data="buy_flat"
                ),
                InlineKeyboardButton(
                    "Расходы на проценты по ипотеке", callback_data="proc"
                ),
                InlineKeyboardButton("Выбрать другой вычет", callback_data="return"),
            ],
            1,
        )
    )

    keyboard_invest = InlineKeyboardMarkup(
        build_menu(
            [
                InlineKeyboardButton(
                    "Внесенные на ИИС денежные средства", callback_data="iis"
                ),
                InlineKeyboardButton("Выбрать другой вычет", callback_data="return"),
            ],
            1,
        )
    )

    @classmethod
    def alter_keyboard(cls, t: str):

        if t == "social":
            keyboard = cls.keyboard_soc
        elif t == "property":
            keyboard = cls.keyboard_property
        elif t == "invest":
            keyboard = cls.keyboard_invest

        return keyboard

    @staticmethod
    def get_inline_button_text(button_data: str, inline) -> str:


        for row in inline:
            for button in row:
                if button.callback_data == button_data:
                    return button.text
        