import json
import data

content = {
    "goals": data.goals,
    "teachers": data.teachers
}

with open("data.json", 'w', encoding="utf-8") as file:
    json.dump(content, file, ensure_ascii=False)