from flask import Flask, render_template, request
import cmath  # для работы с комплексными числами
import math   # для работы с действительными числами
import re     # для работы с регулярными выражениями

app = Flask(__name__)

# Данные для языков
languages = {
    "ru": {
        "title": "Квадратный корень числа",
        "input_placeholder": "Введите число, например, 2+3j или -4 или sin(3*pi/2)",
        "precision_placeholder": "Введите точность (необязательно)",
        "submit": "Рассчитать",
        "result_label": "Результат",
        "error": "Пожалуйста, введите корректное число.",
        "support": "Почта техподдержки сайта",
        "email": "tdpopov@edu.hse.ru",
    },
    "en": {
        "title": "Square Root of a Number",
        "input_placeholder": "Enter a number, e.g., 2+3j or -4 or sin(3*pi/2)",
        "precision_placeholder": "Enter precision (optional)",
        "submit": "Calculate",
        "result_label": "Result",
        "error": "Please enter a valid number.",
        "support": "Technical Support mail site",
        "email": "tdpopov@edu.hse.ru",
    },
    "es": {
        "title": "Raíz Cuadrada de un Número",
        "input_placeholder": "Ingrese un número, p.ej., 2+3j o -4 o sin(3*pi/2)",
        "precision_placeholder": "Ingrese la precisión (opcional)",
        "submit": "Calcular",
        "result_label": "Resultado",
        "error": "Por favor, ingrese un número válido.",
        "support": "Soporte del sitio web",
        "email": "tdpopov@edu.hse.ru",
    }
}

def near_zero(value, threshold=1e-10):
    """Проверяем, является ли число близким к нулю."""
    return abs(value) < threshold

def process_input(input_value):
    """Обрабатываем ввод: преобразуем ^ в ** и обрабатываем переменные."""
    # Заменяем ^ на ** для операций возведения в степень
    input_value = input_value.replace("^", "**")
    
    # Проверка на наличие переменной в выражении
    if re.match(r"^[a-zA-Z]\*\*2$", input_value):  # Обрабатываем выражения вида a^2
        variable = input_value[0]  # Извлекаем переменную
        return f"±{variable}"
    
    # Если это обычное число или выражение
    return str(eval(input_value, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "ctg": lambda x: 1 / math.tan(x), "pi": math.pi, "e": math.e}))

@app.route("/", methods=["GET", "POST"])
@app.route("/<lang>", methods=["GET", "POST"])
def index(lang="ru"):
    result = None
    language = languages.get(lang, languages["ru"])

    if request.method == "POST":
        try:
            input_value = request.form.get("number")
            precision_value = request.form.get("precision")
            precision = int(precision_value) if precision_value else None

            # Обрабатываем вводимое выражение
            processed_value = process_input(input_value)
            
            # Если результат это переменная (±a), сразу выводим его
            if "±" in processed_value:
                result = f"√{input_value} = {processed_value}"
            else:
                # Преобразуем строку в комплексное число
                complex_number = complex(processed_value)
                
                # Проверка на малые значения, близкие к нулю
                if near_zero(complex_number.real):
                    complex_number = complex(0, complex_number.imag)
                if near_zero(complex_number.imag):
                    complex_number = complex(complex_number.real, 0)
                
                is_real = complex_number.imag == 0

                # Для отрицательных действительных чисел выводим комплексный корень
                if is_real and complex_number.real < 0:
                    root1 = cmath.sqrt(complex_number)
                    root2 = -root1
                else:
                    root1 = cmath.sqrt(complex_number)
                    root2 = -root1

                # Форматируем результат
                def format_complex(number):
                    real = number.real if precision is None else round(number.real, precision)
                    imag = number.imag if precision is None else round(number.imag, precision)

                    if near_zero(real):
                        real = 0
                    if near_zero(imag):
                        imag = 0

                    if imag == 0:
                        return f"{real}"
                    elif real == 0:
                        return f"{imag}j"
                    else:
                        sign = "+" if imag > 0 else "-"
                        return f"{real}{sign}{abs(imag)}j"

                if is_real:
                    result = f"√{input_value} = ±{format_complex(root1)}"
                else:
                    result = f"√{input_value} = {format_complex(root1)}"
            
        except ValueError:
            result = language["error"]
        except Exception as e:
            result = f"Ошибка: {str(e)}"

    return render_template("index.html", result=result, lang=lang, language=language)

if __name__ == "__main__":
    app.run(debug=True)
