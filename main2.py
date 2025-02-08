# import discord
# from discord.ext import commands
# import schedule
# import time
# import csv
# import datetime
# import os
#
# intents = discord.Intents.default()
# bot = commands.Bot(command_prefix="/", intents=intents)
#
# # KÊNH DISCORD MUỐN GỬI THÔNG BÁO
# CHANNEL_ID = 1229839692489293876  # Thay bằng ID channel thực tế
#
# # HÀM ĐỌC DỮ LIỆU TỪ CSV
# def read_csv():
#     if not os.path.exists("result.csv"):
#         print("File 'result.csv' không tồn tại.")
#         return []
#     with open("result.csv", mode="r", encoding="utf-8") as f:
#         return list(csv.DictReader(f))
#
# # HÀM CHUYỂN ĐỊNH DẠNG NGÀY SANG DD/MM/YYYY
# def format_date_ddmmyyyy(date_str):
#     try:
#         return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
#     except ValueError:
#         return ""
#
# # HÀM GỬI THÔNG BÁO SINH NHẬT
# def check_and_notify_birthdays():
#     today = datetime.date.today()
#     today_mmdd = today.strftime("%m-%d")
#     birthday_list = []
#
#     data = read_csv()
#     for row in data:
#         if row["birthday"][5:] == today_mmdd:
#             formatted_date = format_date_ddmmyyyy(row["birthday"])
#             birthday_list.append(
#                 f"**{row['full_name']}** (Ban: {row['ban']}, Khóa: {row['khoa']}, Sinh ngày: {formatted_date})"
#             )
#
#     if len(birthday_list) > 0:
#         user_list_str = "\n".join(birthday_list)
#         message = (
#             f"🎉 *Hôm nay là sinh nhật của các thành viên:* 🎉\n\n"
#             f"{user_list_str}\n\n"
#             f"**@everyone** Hãy cùng gửi lời chúc mừng sinh nhật 🥳 "
#             f"cho các thành viên đặc biệt này nhé! 🌟\n\n"
#             f"**Chúc mừng sinh nhật!** 🎊🎂"
#         )
#
#         channel = bot.get_channel(CHANNEL_ID)
#         if channel:
#             bot.loop.create_task(channel.send(message))
#         print("Đã gửi thông báo sinh nhật.")
#     else:
#         print("Không có thành viên nào có sinh nhật hôm nay.")
#
# # LỆNH SLASH COMMAND
#
# @bot.tree.command(name="search", description="Tìm kiếm sinh nhật của thành viên theo tên.")
# async def search(interaction: discord.Interaction, tên: str):
#     data = read_csv()
#     results = [row for row in data if tên.lower() in row["full_name"].lower()]
#     if results:
#         message = "\n".join(
#             f"**{row['full_name']}**: {format_date_ddmmyyyy(row['birthday'])}, Ban: {row['ban']}, Khóa: {row['khoa']}"
#             for row in results
#         )
#     else:
#         message = f"Không tìm thấy thành viên nào có tên **{tên}**."
#     await interaction.response.send_message(message)
#
# @bot.tree.command(name="today", description="Tìm kiếm sinh nhật của thành viên vào ngày hôm nay.")
# async def today(interaction: discord.Interaction):
#     today_date = datetime.date.today().strftime("%m-%d")
#     data = read_csv()
#     results = [row for row in data if row["birthday"][5:] == today_date]
#     if results:
#         message = "\n".join(
#             f"**{row['full_name']}**: {format_date_ddmmyyyy(row['birthday'])}, Ban: {row['ban']}, Khóa: {row['khoa']}"
#             for row in results
#         )
#     else:
#         message = "Hôm nay không có thành viên nào sinh nhật."
#     await interaction.response.send_message(message)
#
# @bot.event
# async def on_ready():
#     print(f"{bot.user} đã sẵn sàng!")
#     try:
#         synced = await bot.tree.sync()  # Đồng bộ lệnh Slash
#         print(f"Đã đồng bộ {len(synced)} lệnh Slash Command.")
#     except Exception as e:
#         print(f"Lỗi đồng bộ lệnh: {e}")
#     schedule_jobs()
#     check_and_notify_birthdays()
#
# def schedule_jobs():
#     schedule.every().day.at("08:00").do(check_and_notify_birthdays)
#
# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# if __name__ == "__main__":
#     import threading
#     scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
#     scheduler_thread.start()
#     bot.run("MTMyODYzNzkyNTMxNDc5MzUwMw.GMT6t5.e8uLnRKqdhlFI3Poem1hubX90UM6NOb0KO39vc")
