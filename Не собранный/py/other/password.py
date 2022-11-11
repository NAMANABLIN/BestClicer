alhb_eng = 'qwertyuiopasdfghjklzxcvbnm'
numbers = '0123456789'


def check_login(login):
    if login == '':
        return 'Не введён логин'
    elif len(login) < 4:
        return 'В логине мало символов'
    return 'ОК'


def check_password(password, password2=None):
    num = False
    capital_let = False
    lowercase_let = False

    if password == '':
        return 'Первый пароль'
    elif password2 is not None:
        if password2 == '':
            return 'Второй пароль не введён'
        elif password != password2:
            return 'Пароли не совпадают'
    if len(password) < 8:
        return 'В пароле меньше 8 символов'
    elif ''.join(password.split(' ')) != password:
        return 'Лишний/e пробел/ы'
    for i, let in enumerate(password):
        if let in numbers:
            num = True
        elif let.lower() in alhb_eng:
            if let in alhb_eng:
                lowercase_let = True
            elif let in alhb_eng.upper():
                capital_let = True
        else:
            return 'Не подходящий/e символ/ы'
    if num and lowercase_let and capital_let:
        return 'ОК'
    elif not num:
        return 'Нет цифр'
    elif not lowercase_let:
        return 'Нет строчных букв'
    elif not capital_let:
        return 'Нет заглавных букв'
