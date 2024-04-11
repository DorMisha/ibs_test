import csv
import json
import random
from abc import ABC, abstractmethod
from io import StringIO

import yaml
from fastapi import UploadFile, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel

import pandas as pd


def convert_arabic_to_roman(number: int) -> str:
    roman_numerals = {
        1: "I", 4: "IV", 5: "V", 9: "IX",
        10: "X", 40: "XL", 50: "L", 90: "XC",
        100: "C", 400: "CD", 500: "D", 900: "CM",
        1000: "M"
    }
    result = ""
    for value, numeral in sorted(roman_numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result



def convert_roman_to_arabic(number: str) -> int:
    roman_numerals = {
        "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000
    }
    total = 0
    prev_value = 0
    for numeral in number:
        value = roman_numerals[numeral]
        if prev_value < value:
            total += value - 2 * prev_value
        else:
            total += value
        prev_value = value
    return total


def average_age_by_position(file: UploadFile) -> Dict[str, float]:
    try:
        df = pd.read_csv(file.file)
        if not all(col in df.columns for col in ["Имя", "Возраст", "Должность"]):
            raise HTTPException(status_code=400,
                                detail="Invalid file format. Columns should be: 'Имя', 'Возраст', 'Должность'")

        avg_age_by_position = df.groupby('Должность')['Возраст'].mean().to_dict()
        return avg_age_by_position
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


"""
Задание_6.
Дан класс DataGenerator, который имеет два метода: generate(), to_file()
Метод generate генерирует данные формата list[list[int, str, float]] и записывает результат в
переменную класса data
Метод to_file сохраняет значение переменной generated_data по пути path c помощью метода
write, классов JSONWritter, CSVWritter, YAMLWritter.

Допишите реализацию методов и классов.
"""

class DataRequest(BaseModel):
    file_type: str
    matrix_size: int

class BaseWriter(ABC):
    """Абстрактный класс с методом write для генерации файла"""

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в json формате"""
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        json_data = json.dumps(data)
        buffer = StringIO(json_data)
        return buffer


class CSVWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в csv формате"""
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        output = StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerows(data)
        output.seek(0)
        return output


class YAMLWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате"""
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        yaml_data = yaml.dump(data)
        buffer = StringIO(yaml_data)
        return buffer




class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id: Optional[str] = None

    def generate(self, matrix_size: int) -> None:
        """Генерирует матрицу данных заданного размера."""
        if matrix_size < 4 or matrix_size > 15:
            raise ValueError("Matrix size should be in range from 4 to 15")

        data = []
        for _ in range(matrix_size):
            row = []
            for _ in range(matrix_size):
                row.append([random.randint(1,100), random.choice(['a', 'b', 'c']), round(random.uniform(1.0, 10.0), 2)])
            data.append(row)

        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> Optional[str]:
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """
        if not self.data:
            raise Exception("No data to write")

        file_stream = writer.write(self.data)
        with open(path, "w") as file:
            file.write(file_stream.getvalue())

        self.file_id = "some_generated_id"
        return self.file_id
