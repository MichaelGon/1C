import os
import hashlib

# Функция для получения хэш-суммы файла
def get_file_hash(filename):
    hasher = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Функция для сравнения файлов
def compare_files(file1, file2, threshold):
    hash1 = get_file_hash(file1)
    hash2 = get_file_hash(file2)
    if hash1 == hash2:
        return 'identical', f"{file1} - {file2}"
    else:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            data1 = f1.read()
            data2 = f2.read()
            similarity = sum(1 for a, b in zip(data1, data2) if a == b) / max(len(data1), len(data2)) #Разумнее всего здесь переделывать содержимое каждого из файлов в строку и решать классическую задачу на поиск НОП двух строк.
            if similarity >= threshold:
                return 'similar'
            else:
                return 'different'

# Функция для сравнения директорий
def compare_directories(dir1, dir2, threshold):
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))
    identical_files = []
    similar_files = []
    different_files1 = []
    different_files2 = []
    for file1 in files1:
        for file2 in files2:
            if get_file_hash(os.path.join(dir1, file1)) == get_file_hash(os.path.join(dir2, file2)):
                result, message = compare_files(os.path.join(dir1, file1), os.path.join(dir2, file2), threshold)
                if result == 'identical':
                    identical_files.append(f"{file1} - {file2}")
                elif result == 'similar':
                    similar_files.append(f"{file1} - {file2} - {message}")
    for file in files1 - files2:
        different_files1.append(f"{os.path.join(dir1, file)} - есть в директории 1, но нет в директории 2\n")
    for file in files2 - files1:
        different_files2.append(f"- {os.path.join(dir2, file)} - есть в директории 2, но нет в директории 1\n")
    return identical_files, similar_files, different_files1, different_files2


# Пример использования функции
dir1 = input('Введите первую директорию:')
dir2 = input('Введите вторую директорию:')
threshold = float(input('Введите сходство: '))
identical_files, similar_files, different_files1, different_files2 = compare_directories(dir1, dir2, threshold)
print('Identical files:', *identical_files, end='\n', sep='\n')
print('----------------')
print('Similar files:', *similar_files, end='\n', sep='\n')
print('-----------------')
print(*different_files1, end='\n', sep='\n')
print('-----------------')
print(*different_files2, end='\n', sep='\n')
