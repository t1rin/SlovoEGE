import os

from json import loads, dumps


def _path(path:str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def json_read(path: str) -> dict:
    json_data = None
    with open(_path(path), "r", encoding="utf-8") as file:
        json_data = loads(file.read())
    return json_data

def json_write(path: str, data: dict) -> None:
    with open(_path(path), "w", encoding="utf-8") as file:
        file.write(dumps(data, ensure_ascii=False, indent=4))

def json_file_checking() -> None:
    if not os.path.isfile(_path("data.json")):
        data = {"words": [], "letters": [["а", "о"],["о", "е"],["у","ю"],["и","ы"],["и","е"],["б","п"],["д","т"],["г","к"],["ж","ш"],["з","с"],["ъ","ь"]]}
        json_write("data.json", data)
    if not os.path.isfile(_path("statistic.json")):
        data = {"questions": 0, "right_answers": 0,"errors": {}}
        json_write("statistic.json", data)

def from_wrd_to_question(word: str) -> tuple:
    parts = word.split("_")
    wrd = parts[0] + ".." + parts[2]
    ltr = parts[1]
    return wrd, ltr

def similar_ltrs(all_ltrs: list[list], ltr: str) -> list:
    similar = set()
    for couple in all_ltrs:
        if ltr in couple:
            similar.update(couple)
    return list(similar)






