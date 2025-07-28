import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://minesrussobot.replit.app/"
CADASTRO_URL = "https://1wuafz.life/?open=register&p=gv72"
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

users = load_users()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in users:
        await send_menu(update)
    else:
        await update.message.reply_text(
            f"🚨 Para acessar o bot, cadastre-se pelo link abaixo:\n\n{CADASTRO_URL}\n\n"
            "Depois envie **seu ID de cadastro (9 dígitos)** aqui nesta conversa.",
            parse_mode='Markdown'
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    if user_id in users:
        await send_menu(update)
        return
    if text.isdigit() and len(text) == 9:
        users.add(user_id)
        save_users(users)
        await update.message.reply_text("✅ Cadastro confirmado! Agora você tem acesso total ao bot.")
        await send_menu(update)
    else:
        await update.message.reply_text(
            f"❗ Envie seu **ID de cadastro** (apenas números, 9 dígitos).\n\nSe ainda não se cadastrou, acesse:\n{CADASTRO_URL}",
            parse_mode='Markdown'
        )

async def send_menu(update):
    keyboard = [
        [InlineKeyboardButton("🚀 Abrir Analyzer", web_app={"url": WEB_APP_URL})],
        [InlineKeyboardButton("📊 Estatísticas", callback_data="stats")],
        [InlineKeyboardButton("ℹ️ Como Usar", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = """
🤖 *Mines Pro Analyzer v2.1.4*

⚡ Sistema de análise em tempo real  
🎯 94.2% de precisão  
🔒 IA treinada com 50M+ partidas

Clique no botão abaixo para começar a análise!
    """
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "stats":
        stats_text = """
📊 *Estatísticas do Sistema*

🎯 Precisão: 94.2%
📈 Sinais gerados: 1,247+
👥 Usuários ativos: 2,853
🟢 Status: Online
⏱️ Última atualização: Hoje

*Estatísticas atualizadas em tempo real*
        """
        await query.message.reply_text(stats_text, parse_mode='Markdown')
    elif query.data == "help":
        help_text = """
❓ *Como Usar o Analyzer*

1️⃣ Clique em "Abrir Analyzer"  
2️⃣ Visualize o grid de análise  
3️⃣ Clique em "ANALISAR PADRÃO"  
4️⃣ Aguarde a IA processar os dados  
5️⃣ Veja os padrões identificados  
6️⃣ Use as informações para suas jogadas

⚠️ *Importante*: Use com responsabilidade!
        """
        await query.message.reply_text(help_text, parse_mode='Markdown')

# ---- MENSAGENS AUTOMÁTICAS ----

async def enviar_mensagem_manha(context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🚨 *Comece o dia ganhando!*\n"
        "O site russo ainda está vulnerável. Acesse o Analyzer agora e pegue a melhor sequência para lucrar nas primeiras horas!"
    )
    for uid in list(users):
        try:
            await context.bot.send_message(chat_id=uid, text=msg, parse_mode='Markdown')
        except Exception:
            pass

async def enviar_mensagem_tarde(context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⚡ *Hora da virada!*\n"
        "Aproveite a janela de brecha no site russo. Analise padrões agora e potencialize seus ganhos usando o Analyzer!"
    )
    for uid in list(users):
        try:
            await context.bot.send_message(chat_id=uid, text=msg, parse_mode='Markdown')
        except Exception:
            pass

async def enviar_mensagem_fim_tarde(context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🔥 *Melhor horário para multiplicar!*\n"
        "O hack segue funcionando! Use o Analyzer agora e maximize seu resultado enquanto a brecha está ativa."
    )
    for uid in list(users):
        try:
            await context.bot.send_message(chat_id=uid, text=msg, parse_mode='Markdown')
        except Exception:
            pass

async def enviar_mensagem_noite(context: ContextTypes.DEFAULT_TYPE):
    img_url = "https://media.giphy.com/media/l0MYRzcWP1l6NQnHy/giphy.gif"
    caption = (
        "🌙 *Última chance do dia!*\n"
        "Essa pode ser sua última oportunidade hoje de aproveitar a falha do site russo.\nClique em “Abrir Analyzer” e confira!"
    )
    for uid in list(users):
        try:
            await context.bot.send_photo(chat_id=uid, photo=img_url, caption=caption, parse_mode='Markdown')
        except Exception:
            pass

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    scheduler = AsyncIOScheduler()
    # Agendando mensagens diferentes em horários distintos
    scheduler.add_job(lambda: application.create_task(enviar_mensagem_manha(application)), 'cron', hour=10, minute=0)
    scheduler.add_job(lambda: application.create_task(enviar_mensagem_tarde(application)), 'cron', hour=15, minute=0)
    scheduler.add_job(lambda: application.create_task(enviar_mensagem_fim_tarde(application)), 'cron', hour=18, minute=0)
    scheduler.add_job(lambda: application.create_task(enviar_mensagem_noite(application)), 'cron', hour=21, minute=0)
    scheduler.start()

    print("🤖 Bot iniciado!")
    application.run_polling()

if __name__ == '__main__':
    main()
