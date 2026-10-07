from datetime import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN ='8917954401:AAGpG_rSZZ2IiR6vfgjEz0yEwBvVdsb_l0g'



# Твой Telegram ID.
# Пока оставь 0 — после запуска я покажу, как узнать ID.
MY_CHAT_ID = 0

schedule = {
    0: [
        "Английский язык",
        "Узбекский язык",
        "История",
        "Русский язык",
        "Биология",
        "Английский язык",
    ],
    1: [
        "Английский язык",
        "Математика",
        "Узбекский язык",
        "Математика",
        "Русский язык",
    ],
    2: [
        "Английский язык",
        "Русский язык",
        "Математика",
        "Биология",
        "Информатика",
    ],
    3: [
        "Математика",
        "Английский язык",
        "Английский язык",
        "Информатика",
        "Информатика",
    ],
    4: [
        "Математика",
        "История",
        "Физическая культура",
        "Узбекский язык",
        "Математика",
    ],
    5: [
        "Русский язык",
        "Математика",
    ],
}

days = {
    0: "ПОНЕДЕЛЬНИК",
    1: "ВТОРНИК",
    2: "СРЕДА",
    3: "ЧЕТВЕРГ",
    4: "ПЯТНИЦА",
    5: "СУББОТА",
    6: "ВОСКРЕСЕНЬЕ",
}


def make_schedule(day):
    if day == 6:
        return "😴 Сегодня воскресенье. Уроков нет!"

    lessons = schedule.get(day)

    if not lessons:
        return "😴 Сегодня уроков нет!"

    text = f"📚 РАСПИСАНИЕ НА {days[day]}\n\n"

    for number, lesson in enumerate(lessons, 1):
        text += f"{number}. {lesson}\n"

    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я твой бот расписания 📚\n\n"
        "/today — расписание на сегодня\n"
        "/schedule — расписание на сегодня\n"
        "/week — всё расписание"
    )


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime

    day = datetime.now().weekday()
    await update.message.reply_text(make_schedule(day))


async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📚 РАСПИСАНИЕ НА НЕДЕЛЮ\n\n"

    for day in range(6):
        text += make_schedule(day) + "\n\n"

    await update.message.reply_text(text)


async def send_morning_schedule(context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime

    if MY_CHAT_ID == 0:
        print("⚠️ MY_CHAT_ID ещё не указан!")
        return

    day = datetime.now().weekday()
    text = "🌅 ДОБРОЕ УТРО!\n\n" + make_schedule(day)

    await context.bot.send_message(
        chat_id=MY_CHAT_ID,
        text=text
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("schedule", today))
app.add_handler(CommandHandler("week", week))

# Автоматическая отправка каждый день в 07:00
app.job_queue.run_daily(
    send_morning_schedule,
    time=time(hour=7, minute=0),
)

print("✅ БОТ ЗАПУЩЕН!")
print("⏰ Автоматическая отправка: каждый день в 07:00")

app.run_polling()