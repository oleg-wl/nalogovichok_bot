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

def ndfl(month: int):
    # функция для расчета новой прогрессии НДФЛ

    if isinstance(month, int):
        gross = month * 12

        gross13 = 
        gross15 = gross13 - 2400000
        gross18 = gross15 - 5000000
        gross20 = gross18
        gross22 = 50000000 - gross20

        
        if gross <= 2400000:
            
            tax = gross * 0.13
            net = gross - tax
            salary = net / 12
            eff_tax = tax / 12

        