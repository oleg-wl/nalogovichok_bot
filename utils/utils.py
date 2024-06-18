def build_menu(buttons: list, n_cols: int,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


count_intro = '{}, я помогу рассчитать размер основных налоговых вычетов и подсказать тебе примерную сумму налога к возврату по расходам за 2023 год\nПо очереди выбери расходы на услуги и введи сумму расхода в виде целого числа\n\nКогда закончишь нажми кнопку Рассчитать\nЕсли ошибся, выбери расход и введи сумму повторно\nДа прибудет с тобой сила'


def sum_costs(costs: dict) -> dict:

    soc, edu, im, inv, per = 0, 0, 0, 0, 0
    
    for k, v in costs.items():
        if k in ['расходы на обучение', 'расходы на лечение', 'расходы на фитнес']:
            soc += v
        elif k in ['расходы на обучение детей']:
            edu += v
        elif k in ['расходы на покупку квартиры']:
            im +=v
        elif k in ['расходы на проценты по ипотеке']:
            per += v
        elif k in ['внесенные на иис денежные средства']:
            inv += v

    soc = soc*0.13 if soc < 120000 else 120000*0.13    
    edu = edu*0.13 if edu < 50000 else 50000*0.13    
    im = im*0.13 if im < 2000000 else 2000000*0.13    
    per = per*0.13 if per < 3000000 else 3000000*0.13    
    inv = inv*0.13 if inv < 400000 else 400000*0.13    

    return {'soc':soc, 'edu':edu, 'im':im, 'per':per, 'inv':inv}

def ndfl(month: int) -> str:
    """
    функция принимает месячный доход и возвращает соответтсвующий прогрессивный ндфл

    :param int month: зарплата
    :return str: сообщение ответ бота
    """
    def net(g: int, t: float): return g - t

    if isinstance(month, int):
        income = month * 12 # вся зп

        gross13 = 2400000*0.13
        gross15 = 2600000*0.15
        gross18 = 15000000*0.18
        gross20 = 30000000*0.20

        if income <= 2400000:
            tax = income * 0.13
            net = net(income, tax)
            rates = '13%'

        elif income <= 5000000:
            tax = gross13 + (income - 2400000) * 0.15
            net = net(income, tax)
            rates = '13%, 15%'

        elif income <= 20000000:
            tax = gross13 + gross15 + (income - 5000000) * 0.18
            net = net(income, tax)
            rates = '13%, 15%, 18%'

        elif income <= 50000000:
            tax = gross13 + gross15 + gross18 + (income - 20000000) * 0.20
            net = net(income, tax)
            rates = '13%, 15%, 18%, 20%'

        else:
            tax = gross13 + gross15 + gross18 + gross20 + (income - 50000000) * 0.22
            net = net(income, tax)
            rates = 'так я и поверил'

        er = tax / income * 100
        
        return 'Сумма НДФЛ за год: {0:,.0f}. На руки за год ты получишь: {1:,.0f}\nНалоговые ставки: {2}\nЭффективная ставка: {3}%'.format(round(tax,0), round(net,0), rates, round(er, 2)).replace(',',' ')  
    else: return 'Введи ежемесячную зарплату без пробелов, например 2000000'