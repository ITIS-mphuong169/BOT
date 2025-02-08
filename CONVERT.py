import csv
from datetime import datetime

input_file = "birthdays.csv"  # File đầu vào chứa dữ liệu gốc
output_file = "result.csv"    # File đầu ra có thêm cột khóa

def convert_date_vn_to_ddmmyyyy(date_str):
    """
    Chuyển 'dd/mm/yyyy' => 'dd/mm/yyyy' nếu hợp lệ.
    Nếu không parse được, trả về "" (chuỗi rỗng).
    """
    date_str = date_str.strip().strip(",")
    if not date_str:
        return ""
    parts = date_str.split("/")
    if len(parts) == 3:
        dd, mm, yyyy = parts
        dd = dd.zfill(2)
        mm = mm.zfill(2)
        yyyy = yyyy.strip(",").strip()
        try:
            # Kiểm tra lại ngày, tháng, năm có hợp lệ không
            new_date = datetime.strptime(f"{dd}/{mm}/{yyyy}", "%d/%m/%Y")
            return new_date.strftime("%d/%m/%Y")  # Trả về ngày theo định dạng dd/mm/yyyy
        except ValueError:
            return ""  # Nếu không hợp lệ, trả về chuỗi rỗng
    return ""

def extract_khoa_from_lop(lop_str):
    """
    Trích xuất khóa từ 3 ký tự đầu tiên của mã lớp.
    Nếu không hợp lệ hoặc trống, trả về "Không rõ".
    """
    lop_str = lop_str.strip() if lop_str else ""
    return lop_str[:3] if lop_str[:3].isalnum() else ""

with open(input_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", encoding="utf-8", newline="") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = ["STT", "full_name", "birthday", "ban", "chuc_vu", "khoa"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        stt = row["STT"].strip()
        full_name = row["Họ và tên"].strip()
        raw_birthday = row["ngày sinh"]
        # Chuyển ngày sinh sang định dạng dd/mm/yyyy
        vn_birthday = convert_date_vn_to_ddmmyyyy(raw_birthday)
        ban = row["Ban"].strip() if "Ban" in row else "Không rõ"
        chuc_vu = row["Chức vụ"].strip() if "Chức vụ" in row else "Không rõ"
        lop = row["Lớp"] if "Lớp" in row else ""
        khoa = extract_khoa_from_lop(lop)

        writer.writerow({
            "STT": stt,
            "full_name": full_name,
            "birthday": vn_birthday,  # Ghi ngày theo định dạng dd/mm/yyyy
            "ban": ban,
            "chuc_vu": chuc_vu,
            "khoa": khoa
        })

print("Done! Check 'result.csv'")
