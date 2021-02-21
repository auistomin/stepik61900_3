from flask import Flask, render_template, abort
from numpy import random
import os.path
import forms
import json


app = Flask(__name__)
app.config["SECRET_KEY"] = "bd65611d-8449-4903-8a14-af84303add38"  # str(random.randint(10000, 99999))  # set up a secret key


@app.route('/')
def render_index():

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)
    goals = data_json.get("goals")
    teachers = data_json.get("teachers")
    #keys = [teacher['id'] for teacher in teachers]
    #keys = random.choice(keys, 6, replace=False)
    #teachers = [teacher for teacher in teachers if teacher['id'] in keys]
    random.shuffle(teachers)

    return render_template("index.html", goals=goals, teachers=teachers[0:6])


@app.route('/all/')
def render_all():

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)
    goals = data_json.get("goals")
    teachers = data_json.get("teachers")

    return render_template("all.html", goals=goals, teachers=teachers, n_teachers=len(teachers))


@app.route('/goal/<goal>/')
def render_goal(goal):

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)

    goals = data_json.get("goals")
    if goal not in goals:
        abort(404)

    teachers = []
    for teacher in data_json.get('teachers'):
        if goal in set(teacher["goals"]):
            teachers.append(teacher)

    return render_template("goal.html", goals=goals, teachers=teachers, goal=goals[goal])


@app.route('/profile/<int:teacher_id>/')
def render_profile(teacher_id):

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)
    goals = data_json.get("goals")
    teachers = data_json.get('teachers')
    teachers = [teacher for teacher in teachers if teacher.get("id") == teacher_id]
    if len(teachers) == 0:
        abort(404)

    return render_template("profile.html", goals=goals, teacher=teachers[0], week_days=forms.week_days)


@app.route('/booking/<int:teacher_id>/<weekday>/<time>/', methods=['GET', 'POST'])
def render_booking(teacher_id, weekday, time):

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)
    goals = data_json.get("goals")
    teachers = data_json.get('teachers')
    teachers = [teacher for teacher in teachers if teacher.get("id") == teacher_id]
    if len(teachers) != 0:
        teacher = teachers[0]
    else:
        abort(404)

    fulltime = time + ":00"
    if not weekday in teacher['free'].keys():
        abort(404)
    elif not fulltime in teacher['free'][weekday].keys():
        abort(404)
    elif teacher['free'][weekday][fulltime] != True:
        abort(404)

    return render_template("booking.html", form=forms.BookingForm(), goals=goals, teacher=teacher, week_days=forms.week_days, weekday=weekday, time=time)


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():

    form = forms.BookingForm()
    teacher_id = form.teacher.data
    weekday = form.weekday.data
    time = form.time.data
    name = form.name.data
    phone = form.phone.data

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)
    goals = data_json.get("goals")
    teachers = data_json.get('teachers')
    teachers = [teacher for teacher in teachers if str(teacher.get("id")) == teacher_id]
    if len(teachers) != 0:
        teacher = teachers[0]
    else:
        abort(404)

    fulltime = time + ":00"
    if not weekday in teacher['free'].keys():
        abort(404)
    elif not fulltime in teacher['free'][weekday].keys():
        abort(404)
    elif teacher['free'][weekday][fulltime] != True:
        abort(404)

    if not form.validate_on_submit():
        return render_template("booking.html", form=form, goals=goals, teacher=teacher, week_days=forms.week_days, weekday=weekday, time=time)

    if not os.path.exists('booking.json'):
        booking_json = []
    else:
        with open("booking.json", "r", encoding="utf-8") as file:
            booking_json = json.load(file)
    booking_json.append({"teacher_id": teacher_id, "weekday": weekday, "time": time + ':00', "phone": phone, "name": name})
    with open("booking.json", "w", encoding="utf-8") as file:
        json.dump(booking_json, file, ensure_ascii=False)

    return render_template("booking_done.html", goals=goals, weekday=forms.week_days[weekday], time=time, name=name, phone=phone)


@app.route('/request/', methods=["POST", "GET"])
def render_request():

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)
    goals = data_json.get("goals")

    return render_template("request.html", form=forms.RequestForm(), goals=goals)


@app.route('/request_done/', methods=['POST'])
def render_request_done():

    with open("data.json", encoding="utf-8") as file:
        data_json = json.load(file)
    goals = data_json.get("goals")

    form = forms.RequestForm()
    goal = form.goal.data
    time = form.time.data
    name = form.name.data
    phone = form.phone.data
    if not form.validate_on_submit():
        return render_template("request.html", form=form, goals=goals)

    if not os.path.exists('request.json'):
        request_json = []
    else:
        with open("request.json", "r", encoding="utf-8") as file:
            request_json = json.load(file)
    request_json.append({"goal": goal, "time": time, "phone": phone, "name": name})
    with open("request.json", "w", encoding="utf-8") as file:
        json.dump(request_json, file, ensure_ascii=False)

    return render_template("request_done.html", goals=goals, goal=goals[goal]['title'], time=forms.week_times[time], name=name, phone=phone)


@app.route('/302/')
def render_302():
    return render_template('302.html')


@app.errorhandler(404)
def render_404(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()