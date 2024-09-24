import csv
import sys

def main():
    # Проверяем, что переданы три аргумента
    if len(sys.argv) != 4:
        print("Usage: python task.py <csv_file_path> <row_num> <col_num>")
        return

    # Получаем аргументы
    csv_file_path = sys.argv[1]
    row_num = int(sys.argv[2])
    col_num = int(sys.argv[3])

    # Открываем файл и получаем значение
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i == row_num:
                    print(row[col_num])
                    return
        print("Row or column not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
