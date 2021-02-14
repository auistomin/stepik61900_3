from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, StringField, RadioField
from wtforms.validators import InputRequired, Length, Regexp
from wtforms.fields.html5 import TelField
import json

week_days = {
    "mon": "Понедельник",
    "tue": "Вторник",
    "wed": "Среда",
    "thu": "Четверг",
    "fri": "Пятница",
    "sat": "Суббота",
    "sun": "Воскресенье"
}
week_times = {
    "time12": "1-2 часа в неделю",
    "time35": "3-5 часов в неделю",
    "time57": "5-7 часов в неделю",
    "time710": "7-10 часов в неделю"
}

goal_select = []
with open("data.json", "r", encoding="utf-8") as file:
    data_json = json.load(file)
goals = data_json.get("goals")
for key, value in goals.items():
    goal_select.append((key, value['title']))

time_select = []
for key, value in week_times.items():
    time_select.append((key, value))


class BookingForm(FlaskForm):
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()
    clientName = StringField("Вас зовут", validators=[InputRequired("Введите ваше имя"), Length(min=2, message="Имя должно быть не менее 2 символов")])
    clientPhone = TelField("Ваш телефон", validators=[InputRequired("Введите ваш номер телефона"), Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message="Номер телефона имеет некорректный формат")])
    submit = SubmitField("Записаться на пробный урок")

class RequestForm(FlaskForm):
    clientGoal = RadioField('Какая цель занятий?', choices=goal_select, default="travel")
    clientTime = RadioField('Сколько времени есть?', choices=time_select, default="time12")
    clientName = StringField("Вас зовут", validators=[InputRequired("Введите ваше имя"), Length(min=2, message="Имя должно быть не менее 2 символов")])
    clientPhone = TelField("Ваш телефон", validators=[InputRequired("Введите ваш номер телефона"), Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message="Номер телефона имеет некорректный формат")])
    submit = SubmitField("Найдите мне преподавателя")