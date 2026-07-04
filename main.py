from flask import Flask, render_template, request
import os

app = Flask(__name__)

def result_calculate(size, lights, device):
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5   
    return size * home_coef + lights * light_coef + device * devices_coef 

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
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Сбор всех переменных из формы
    name = request.form.get('name', 'Не указано')
    email = request.form.get('email', 'Не указано')
    address = request.form.get('address', 'Не указано')
    date = request.form.get('date', 'Не указано')
    time = request.form.get('time', 'Не указано')
    password = request.form.get('password', 'Не указано')
    age = request.form.get('age', 'Не указано')

    # Формирование строки для записи в файл
    data_to_save = (
        f"--- Новая заявка ---\n"
        f"Имя: {name}\n"
        f"Email: {email}\n"
        f"Адрес: {address}\n"
        f"Дата: {date}\n"
        f"Время: {time}\n"
        f"Возраст: {age}\n"
        f"Пароль: {password}\n"  # В реальном проекте пароли НИКОГДА не хранят в открытом виде!
        f"----------------------\n\n"
    )

    # Запись в файл form.txt
    # Используем 'a' (append), чтобы добавлять новые записи, а не перезаписывать старые
    try:
        with open('form.txt', 'a', encoding='utf-8') as f:
            f.write(data_to_save)
        print("Данные успешно сохранены в form.txt")
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")

    # Передача всех переменных в шаблон
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

                            'electronics.html',
                            size = size, 
                            lights = lights                           
                           )

#Расчет
@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    return render_template('end.html', 
                            result=result_calculate(int(size),
                                                    int(lights), 
                                                    int(device)
                                                    )
                        )
app.run(debug=True)
