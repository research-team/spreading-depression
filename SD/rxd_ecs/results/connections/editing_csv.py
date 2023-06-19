import csv

# Открываем исходный файл CSV для чтения
with open('connections.csv', 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    data = list(reader)

# Изменяем данные в файле CSV
for row in data:
    # Редактируем значения в нужных столбцах
    if row[0] == '1':
        row[0] = 'A'
    if row[0] == '0':
        row[0] = 'N'
    if row[0] == '-1':
        row[0] = 'G'

#Открываем файл CSV для записи обновленных данных
with open('con_new.csv', 'w', newline='') as file:
    writer = csv.writer(file, elimiter='\t')
    writer.writerows(data)

print("Файл успешно обновлен.")