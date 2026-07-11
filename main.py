from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
DATA_FILE = 'user_data.json'

def result_calculate(size, lights, device):
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5
    return size * home_coef + lights * light_coef + device * devices_coef

def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_user_data(data):
    # Не сохраняем пароль и время
    safe_data = {k: v for k, v in data.items() if k not in ('password', 'time','date')}
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(safe_data, f, ensure_ascii=False, indent=2)
        print("Данные успешно сохранены в user_data.json")
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<size>')
def lights(size):
    return render_template('lights.html', size=size)

@app.route('/<size>/<lights>')
def electronics(size, lights):
    return render_template('electronics.html', size=size, lights=lights)

@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    return render_template('end.html',
                           result=result_calculate(int(size), int(lights), int(device)))

@app.route('/form')
def form():
    # Загружаем сохранённые данные
    user_data = load_user_data()
    return render_template('form.html', user=user_data)

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    address = request.form.get('address', '')
    date = request.form.get('date', '')
    time = request.form.get('time', '')
    password = request.form.get('password', '')
    age = request.form.get('age', '')

    # Формируем строку для текстового файла (как раньше)
    data_to_save = (
        f"--- Новая заявка ---\n"
        f"Имя: {name}\n"
        f"Email: {email}\n"
        f"Адрес: {address}\n"
        f"Дата: {date}\n"
        f"Время: {time}\n"
        f"Возраст: {age}\n"
        f"Пароль: {password}\n"
        f"----------------------\n\n"
    )

    try:
        with open('form.txt', 'a', encoding='utf-8') as f:
            f.write(data_to_save)
        print("Данные успешно сохранены в form.txt")
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")

    # Сохраняем основные данные в JSON (без пароля и времени)
    save_user_data({
        'name': name,
        'email': email,
        'address': address,
        'date': date,
        'age': age,
        'password': password,
        'time': time
    })

    return render_template('form_result.html',
                           name=name,
                           email=email,
                           address=address,
                           date=date,
                           time=time,
                           password=password,
                           age=age)

if __name__ == '__main__':
    app.run(debug=True)
