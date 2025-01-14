import csv
from datetime import datetime

input_file = "birthdays.csv"  # file chứa bảng to đùng mà bạn cung cấp
output_file = "result.csv"   # file CSV kết quả chỉ có (full_name,birthday)

def convert_date_vn_to_iso(date_str):
    """
    Thử chuyển 'dd/mm/yyyy' => 'yyyy-mm-dd'.
    Nếu không parse được, trả về "" (chuỗi rỗng) hoặc None tùy ý.
    """
    # Loại bỏ khoảng trắng, dấu phẩy,... thừa
    date_str = date_str.strip().strip(",")

    # Nếu date_str rỗng, trả None
    if not date_str:
        return None

    # Một số dòng có thể ghi '14/1/1997', '8/2/1999', '1998', '2710/1999' (lỗi) ...
    # Ta cố gắng tách bằng dấu '/'.
    parts = date_str.split("/")
    if len(parts) == 3:
        # parts = [dd, mm, yyyy]
        dd, mm, yyyy = parts
        # Bổ sung '0' nếu cần:
        if len(dd) == 1: dd = "0" + dd
        if len(mm) == 1: mm = "0" + mm

        # Nhiều trường hợp yyyy = '1997,' (dính dấu phẩy cuối => bỏ)
        yyyy = yyyy.strip(",").strip()

        # Giả sử yyyy có 4 chữ số => parse datetime
        try:
            new_date = datetime.strptime(f"{dd}/{mm}/{yyyy}", "%d/%m/%Y")
            return new_date.strftime("%Y-%m-%d")
        except ValueError:
            # Parse thất bại => trả None
            return None

    # Nếu file có nhiều kiểu sai, ta đành chịu, return None
    return None

with open(input_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", encoding="utf-8", newline="") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = ["full_name", "birthday"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Lấy tên từ cột "Họ và tên"
        full_name = row["Họ và tên"].strip()

        # Lấy ngày sinh từ cột "ngày sinh"
        raw_birthday = row["ngày sinh"]
        iso_birthday = convert_date_vn_to_iso(raw_birthday)  # Trả về 'YYYY-MM-DD' hoặc None

        # Nếu iso_birthday = None => bạn muốn ghi trống hay bỏ qua tuỳ
        if iso_birthday is None:
            iso_birthday = ""  # hoặc continue nếu bạn muốn skip

        # Ghi ra file CSV
        writer.writerow({
            "full_name": full_name,
            "birthday": iso_birthday
        })

print("Done! Check 'result.csv'")
