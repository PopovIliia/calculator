from flask import Flask, request, render_template
import cmath

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Получаем число из формы
            number_str = request.form['number']
            
            # Преобразуем введенное значение в комплексное число
            number = complex(number_str)
            
            # Вычисляем квадратный корень комплексного числа
            result = cmath.sqrt(number)
        except ValueError:
            result = "Введите корректное число"
        except Exception as e:
            result = f"Ошибка: {str(e)}"
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

