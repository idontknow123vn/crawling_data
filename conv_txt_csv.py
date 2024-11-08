import ast
import csv

# Đọc dữ liệu từ file TXT
with open('hotel.txt', 'r', encoding='utf-8') as txt_file:
    lines = txt_file.readlines()

# Chuyển từng dòng thành dictionary
data = [ast.literal_eval(line.strip()) for line in lines]

# Lấy tên các cột từ keys của dictionary đầu tiên
fieldnames = data[0].keys()

# Ghi dữ liệu vào file CSV
with open('hotels.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()  # Ghi dòng tiêu đề
    writer.writerows(data)  # Ghi các dòng dữ liệu