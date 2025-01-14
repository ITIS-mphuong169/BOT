import discord
from discord.ext import commands
import schedule
import time
import csv
import datetime

intents = discord.Intents.default()
# Nếu muốn bot đọc message hay manipulate user, config intents khác
bot = commands.Bot(command_prefix="!", intents=intents)

# KÊNH DISCORD MUỐN GỬI THÔNG BÁO
CHANNEL_ID = 1137264016138453013  # thay bằng ID channel thực tế

# HÀM ĐỌC CSV VÀ XỬ LÝ
def check_and_notify_birthdays():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # Tách (day, month, year) của "ngày mai"
    tomorrow_day = tomorrow.day
    tomorrow_month = tomorrow.month
    tomorrow_year = tomorrow.year

    # Chuỗi MM-DD để so sánh
    tomorrow_mmdd = tomorrow.strftime("%m-%d")

    birthday_list = []
    with open("result.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # row["birthday"] có dạng YYYY-MM-DD
            # Cắt [5:] -> lấy "MM-DD"
            if row["birthday"][5:] == tomorrow_mmdd:
                birthday_list.append(row["full_name"])

    if len(birthday_list) > 0:
        # Tạo chuỗi danh sách tên
        # Mỗi tên trên 1 dòng: **Name**
        user_list_str = "\n".join(f"**{name}**" for name in birthday_list)

        # Tạo nội dung tin nhắn
        message = (
            f"Danh sách các thành viên có sinh nhật vào ngày mai:\n"
            f"{user_list_str}\n\n"
            f"@everyone Hãy cùng chuẩn bị chúc mừng sinh nhật "
            f"cho các thành viên có sinh nhật vào ngày mai nhé!\n\n"
            f"{tomorrow_day} tháng {tomorrow_month} năm {tomorrow_year}\n"
            f"Hãy cùng gửi lời chúc mừng sinh nhật nhé!"
        )

        # Gửi thông báo vào channel
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            # Dùng create_task để gửi async
            bot.loop.create_task(channel.send(message))

def schedule_jobs():
    # Ví dụ đặt giờ 16:20 mỗi ngày
    schedule.every().day.at("16:50").do(check_and_notify_birthdays)

@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    schedule_jobs()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Thay token bằng token MỚI reset từ Developer Portal
    # (Đừng push code này public chứa token)
    # Token (nhớ đừng push public)
    bot.run("MTMyODYzNzkyNTMxNDc5MzUwMw.Gd820K.sI1HpULfEq_qQ9n1eJ0cHTmO7O_hlD58VsOvXc")
