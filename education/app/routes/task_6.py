from fastapi import APIRouter

from app.core import DataGenerator, DataRequest, JSONWriter, CSVWriter, YAMLWriter

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_6. 

Изучите следущие классы в модуле app.core: BaseWriter, DataGenerator

API должно принимать json, по типу:
{
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
}
В ответ на удачную генерацию файла должен приходить id для скачивания.

Добавьте реализацию методов класса DataGenerator.
Добавьте аннотации типов и (если требуется) модели в модуль app.models.

(Подумать, как переисползовать код из задания 5)
"""
@router.post("/generate_file", description="Задание_6. Конвертер")
async def generate_file(data: DataRequest):
    """Описание."""
    generator = DataGenerator()
    generator.generate(data.matrix_size)

    writer_map = {
        "json": JSONWriter(),
        "csv": CSVWriter(),
        "yaml": YAMLWriter()
    }
    if data.file_type not in writer_map:
        return {"error": "Unsupported file type"}

    writer = writer_map[data.file_type]
    file_id = generator.to_file(f"generated_file.{data.file_type}", writer)

    return {"file_id": file_id}
