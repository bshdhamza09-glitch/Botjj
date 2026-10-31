import os, sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ['BOT_TOKEN']
ADMIN_ID = int(os.environ['ADMIN_ID'])
EMAIL = os.environ['BASE_GMAIL'].strip().lower()
if not EMAIL.endswith('@gmail.com') or '+' in EMAIL.split('@')[0]:
    raise ValueError('BASE_GMAIL must be a regular @gmail.com address')
DB = os.environ.get('DB_PATH', '/data/aliases.db')
os.makedirs(os.path.dirname(DB) or '.', exist_ok=True)
with sqlite3.connect(DB) as c:
    c.execute('CREATE TABLE IF NOT EXISTS aliases (id INTEGER PRIMARY KEY AUTOINCREMENT, address TEXT UNIQUE NOT NULL)')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.effective_message.reply_text('غير مصرح لك باستخدام البوت.')
        return
    kb = InlineKeyboardMarkup([[InlineKeyboardButton('إنشاء عنوان جديد', callback_data='new')], [InlineKeyboardButton('آخر 10 عناوين', callback_data='list')]])
    await update.effective_message.reply_text('مولّد عناوين Gmail البديلة. هذه ليست حسابات مستقلة ولا كلمات سر منفصلة.', reply_markup=kb)

async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.from_user.id != ADMIN_ID:
        return
    with sqlite3.connect(DB) as c:
        if q.data == 'new':
            cursor = c.execute('INSERT INTO aliases(address) VALUES (?)', ('pending',)) if False else None
            next_id = c.execute("SELECT COALESCE(MAX(id),0)+1 FROM aliases").fetchone()[0]
            local = EMAIL.split('@')[0]
            alias = f'{local}+{next_id:06d}@gmail.com'
            c.execute('INSERT INTO aliases(address) VALUES (?)', (alias,))
            msg = f'العنوان الجديد:\n{alias}\n\nالرسائل تصل إلى {EMAIL}. هذا عنوان بديل وليس حساب Google جديداً.'
        else:
            rows = c.execute('SELECT address FROM aliases ORDER BY id DESC LIMIT 10').fetchall()
            msg = '\n'.join(x[0] for x in rows) if rows else 'لا توجد عناوين بعد.'
    await q.message.reply_text(msg)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(click))
app.run_polling()
