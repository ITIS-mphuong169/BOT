import discord
from discord.ext import commands
import schedule
import time
import csv
import datetime

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

CHANNEL_ID = 1095712215111303253

notified_today = None

def read_csv():
    with open("result.csv", mode="r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# @bot.event
# async def on_ready():
#     print(f"{bot.user} is now running!")
#     try:
#         synced = await bot.tree.sync()  # Đồng bộ lệnh Slash Command
#         print(f"Đã đồng bộ {len(synced)} lệnh Slash Command.")
#     except Exception as e:
#         print(f"Lỗi đồng bộ lệnh: {e}")
#
#     # Kiểm tra kênh
#     channel = bot.get_channel(CHANNEL_ID)
#     if channel:
#         print(f"Bot đã tìm thấy kênh: {channel.name}")
#         # Gửi thông báo ngay lập tức
#         message = (
#             f"🎉 **Chúc Mừng Năm Mới!** 🎉\n\n"
#             f"Chào năm {datetime.date.today().year} với nhiều niềm vui, thành công, và hạnh phúc!\n"
#             f"**@everyone**, hãy cùng nhau tận hưởng khoảnh khắc đặc biệt này nhé! 🌟🎆\n\n"
#             f"**Chúc tất cả mọi người một năm mới thật tuyệt vời!** 🥳✨"
#         )
#         await channel.send(message)
#         print("Đã gửi lời chúc mừng năm mới.")
#     else:
#         print(f"Không tìm thấy kênh với ID: {CHANNEL_ID}")


#THÔNG BÁO SINH NHẬT
def check_and_notify_birthdays():
    global notified_today
    today = datetime.date.today()
    today_mmdd = today.strftime("%d/%m")

    # Kiểm tra nếu đã gửi thông báo hôm nay
    if notified_today == today:
        print("Thông báo đã được gửi hôm nay.")
        return

    birthday_list = []
    data = read_csv()
    for row in data:
        birthday = row["birthday"].strip()
        if birthday[:5] == today_mmdd:
            birthday_list.append(
                f"**{row['full_name']}** (Ban: {row['ban']}, Khóa: {row['khoa']}, Sinh ngày: {birthday})"
            )

    if len(birthday_list) > 0:
        user_list_str = "\n".join(birthday_list)
        message = (
            f"🎉 *Hôm nay là sinh nhật của các thành viên:* 🎉\n\n"
            f"{user_list_str}\n\n"
            f"**@everyone** Hãy cùng gửi lời chúc mừng sinh nhật 🥳 "
            f"cho các thành viên đặc biệt này nhé! 🌟\n\n"
            f"**Chúc mừng sinh nhật!** 🎊🎂 "
        )

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            bot.loop.create_task(channel.send(message))
            notified_today = today
            print("Đã gửi thông báo sinh nhật.")
    else:
        print("Hôm nay không có sinh nhật.")


# Lên lịch chạy tự động
def schedule_jobs():
    schedule.every().day.at("08:00").do(check_and_notify_birthdays)  # Đúng 8h sáng chạy


# LỆNH SLASH COMMAND
# Lệnh /search <tên>
@bot.tree.command(name="search", description="Tìm kiếm sinh nhật của thành viên theo tên.")
async def search(interaction: discord.Interaction, tên: str):
    data = read_csv()
    results = [row for row in data if tên.lower() in row["full_name"].lower()]
    if results:
        message = "\n".join(f"**{row['full_name']}**: {row['birthday']}" for row in results)
    else:
        message = f"Không tìm thấy thành viên nào có tên **{tên}**."
    await interaction.response.send_message(message)


# Lệnh /birthday <ngày/tháng>
@bot.tree.command(name="birthday", description="Tìm kiếm sinh nhật theo ngày/tháng.")
async def birthday(interaction: discord.Interaction, ngày_tháng: str):
    try:
        day, month = map(int, ngày_tháng.split("/"))
        formatted_date = f"{day:02}/{month:02}"
        data = read_csv()
        results = [row for row in data if row["birthday"][:5] == formatted_date]
        if results:
            message = "\n".join(f"**{row['full_name']}**: {row['birthday']}" for row in results)
        else:
            message = f"Không có thành viên nào có sinh nhật vào ngày **{ngày_tháng}**."
    except ValueError:
        message = "Vui lòng nhập đúng định dạng ngày/tháng (VD: 20/01)."
    await interaction.response.send_message(message)

# Lệnh /helpme
@bot.tree.command(name="helpme", description="Hiển thị tất cả các lệnh hiện có.")
async def helpme(interaction: discord.Interaction):
    commands_list = """
    **Danh sách các lệnh hiện có:**
    - `/search <tên>`: Tìm kiếm sinh nhật của thành viên theo tên.
    - `/birthday <ngày/tháng>`: Tìm kiếm sinh nhật theo ngày/tháng.
    - `/today`: Tìm kiếm sinh nhật của thành viên vào ngày hôm nay.
    - `/info_name <tên>`: Tìm kiếm thông tin của thành viên theo tên.
    - `/info_cohort <khóa>`: Tìm kiếm thông tin của các thành viên theo khóa.
    - `/info_department <ban>`: Tìm kiếm thông tin của các thành viên theo ban.
    - `/all_birthdays`: Hiển thị danh sách sinh nhật của tất cả các thành viên.
    - `/department_birthdays <ban>`: Tìm kiếm sinh nhật của các thành viên thuộc ban cụ thể.
    - `/cohort_birthdays <khóa>`: Tìm kiếm sinh nhật của các thành viên thuộc khóa cụ thể.
    - `/helpme`: Hiển thị tất cả các lệnh hiện có.
    """
    await interaction.response.send_message(commands_list)


# Lệnh /today
@bot.tree.command(name="today", description="Tìm kiếm sinh nhật của thành viên vào ngày hôm nay.")
async def today(interaction: discord.Interaction):
    today_date = datetime.date.today().strftime("%d/%m")
    data = read_csv()
    results = [row for row in data if row["birthday"][:5] == today_date]
    if results:
        message = "\n".join(f"**{row['full_name']}**: {row['birthday']}" for row in results)
    else:
        message = "Hôm nay không có thành viên nào sinh nhật."
    await interaction.response.send_message(message)


# Lệnh /info_name <tên>
@bot.tree.command(name="info_name", description="Tìm kiếm thông tin của thành viên theo tên.")
async def info_name(interaction: discord.Interaction, tên: str):
    data = read_csv()
    results = [row for row in data if tên.lower() in row["full_name"].lower()]
    if results:
        message = "\n".join(
            f"**{row['full_name']}** (Ban: {row['ban']}, Khóa: {row['khoa']}, Sinh ngày: {row['birthday']})"
            for row in results
        )
    else:
        message = f"Không tìm thấy thành viên nào có tên **{tên}**."
    await interaction.response.send_message(message)


# Lệnh /info_cohort <khóa>
@bot.tree.command(name="info_cohort", description="Tìm kiếm thông tin của các thành viên theo khóa.")
async def info_cohort(interaction: discord.Interaction, khóa: str):
    data = read_csv()
    results = [row for row in data if row["khoa"].lower() == khóa.lower()]
    if results:
        message = "\n".join(
            f"**{row['full_name']}** (Ban: {row['ban']}, Sinh ngày: {row['birthday']})"
            for row in results
        )
    else:
        message = f"Không tìm thấy thành viên nào thuộc khóa **{khóa}**."
    await interaction.response.send_message(message)


# Lệnh /info_department <ban>
@bot.tree.command(name="info_department", description="Tìm kiếm thông tin của các thành viên theo ban.")
async def info_department(interaction: discord.Interaction, ban: str):
    data = read_csv()
    results = [row for row in data if row["ban"].lower() == ban.lower()]
    if results:
        message = "\n".join(
            f"**{row['full_name']}** (Khóa: {row['khoa']}, Sinh ngày: {row['birthday']})"
            for row in results
        )
    else:
        message = f"Không tìm thấy thành viên nào thuộc ban **{ban}**."
    await interaction.response.send_message(message)


@bot.tree.command(name="all_birthdays", description="Hiển thị danh sách sinh nhật của tất cả các thành viên.")
async def all_birthdays(interaction: discord.Interaction):
    data = read_csv()
    if data:
        # Tạo danh sách các dòng để gửi
        message_parts = []
        current_message = ""

        for row in data:
            line = f"**{row['full_name']}**: {row['birthday']}\n"
            # Kiểm tra nếu dòng hiện tại + dòng mới vượt quá 2000 ký tự
            if len(current_message) + len(line) > 2000:
                message_parts.append(current_message)  # Lưu phần hiện tại
                current_message = line  # Bắt đầu phần mới
            else:
                current_message += line  # Thêm dòng vào phần hiện tại

        # Thêm phần còn lại nếu có
        if current_message:
            message_parts.append(current_message)

        # Gửi từng phần
        for part in message_parts:
            await interaction.channel.send(part)

        # Xác nhận với người dùng rằng tin nhắn đã được gửi
        await interaction.response.send_message("Danh sách sinh nhật đã được gửi thành công!")
    else:
        await interaction.response.send_message("Không có dữ liệu thành viên.")


# Lệnh /department_birthdays <ban>
@bot.tree.command(name="department_birthdays", description="Tìm kiếm sinh nhật của các thành viên thuộc ban cụ thể.")
async def department_birthdays(interaction: discord.Interaction, ban: str):
    data = read_csv()
    results = [row for row in data if row["ban"].lower() == ban.lower()]
    if results:
        message = "\n".join(f"**{row['full_name']}**: {row['birthday']}" for row in results)
    else:
        message = f"Không có thành viên nào thuộc ban **{ban}**."
    await interaction.response.send_message(message)


# Lệnh /cohort_birthdays <khóa>
@bot.tree.command(name="cohort_birthdays", description="Tìm kiếm sinh nhật của các thành viên thuộc khóa cụ thể.")
async def cohort_birthdays(interaction: discord.Interaction, khóa: str):
    data = read_csv()
    results = [row for row in data if row["khoa"].lower() == khóa.lower()]
    if results:
        message = "\n".join(f"**{row['full_name']}**: {row['birthday']}" for row in results)
    else:
        message = f"Không có thành viên nào thuộc khóa **{khóa}**."
    await interaction.response.send_message(message)


# SỰ KIỆN KHI BOT SẴN SÀNG
@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()  # Đồng bộ lệnh Slash Command
        print(f"Đã đồng bộ {len(synced)} lệnh Slash Command.")
    except Exception as e:
        print(f"Lỗi đồng bộ lệnh: {e}")
    schedule_jobs()  # Lên lịch chạy tự động
    print("Lịch trình thông báo đã được thiết lập.")


# CHẠY SCHEDULE TRONG THREAD KHÁC
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    bot.run("MTMyODYzNzkyNTMxNDc5MzUwMw.GMT6t5.e8uLnRKqdhlFI3Poem1hubX90UM6NOb0KO39vc")
