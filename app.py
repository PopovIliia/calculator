from flask import Flask, request, render_template
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            number = float(request.form['number'])
            result = math.sqrt(number)
        except ValueError:
            result = "Введите корректное число"
        except Exception as e:
            result = f"Ошибка: {str(e)}"
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
