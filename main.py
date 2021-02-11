import hashlib
import json


#  Класс итератора, который по каждой стране из файла countries.json ищет страницу из википедии.
# Записывает в файл пару: страна – ссылка.
class CountryGenerator:

    def __init__(self, start, end, from_file):
        self.from_file = from_file
        self.start = start - 1
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.from_file, encoding="utf-8") as f:
            self.data = json.load(f)
        self.start += 1
        self.countries = self.data[self.start].get("name").get("common")
        if len(self.data)-1 == self.start or self.start == self.end:
            raise StopIteration
        url = f"{self.countries} - "+f"https://en.wikipedia.org/wiki/{self.countries}".replace(" ", "")
        with open("countries_url.txt", "a", encoding="utf-8") as f:
            f.write(url + "\n")
        return self.countries


#  Генератор, который принимает путь к файлу. При каждой итерации возвращает md5 хеш каждой строки файла.
def my_range(file_path):
    start = 0
    try:
        while True:
            with open(file_path, "rb") as f:
                line = f.readlines()[start]
            yield hashlib.md5(line).digest()
            start += 1
    except IndexError:
        pass


my_generator = CountryGenerator(5, 15, "countries.json")

for i in my_generator:
    print(i)

print()
for i in my_range("countries_url.txt"):
    print(i)
