from flask import Flask, render_template, request
import cmath  # для работы с комплексными числами
import math   # для работы с действительными числами
import re     # для работы с регулярными выражениями

app = Flask(__name__)

# Данные для языков
languages = {
    "ru": {
        "title": "Извлечение квадратного корня",
        "input_placeholder": "Введите число, например, 2+3j , -4 или sin(2*pi/3)",
        "precision_placeholder": "Введите точность (необязательно)",
        "submit": "Рассчитать",
        "result_label": "Результат",
        "error": "Введите латинскую букву в квадрате, корректное число или тригонометрическое выражение.",
        "undefined": "Неопределенно",
        "precision_error": "Ошибка: в строке точность введите неотрицательное число.",
        "support": "Почта техподдержки сайта",
        "email": "tdpopov@edu.hse.ru",
        "instruction_button": "Инструкция",
        "instruction": "<ul>"
                       "<li>Введите латинскую букву в квадрате, корректное число или тригонометрическое выражение.</li>"
                       "<li>Примеры:</li>"
                       "<ul>"
                       "<li>Простое число: 4</li>"
                       "<li>Комплексное число: 2+3j</li>"
                       "<li>Отрицательное число: -4</li>"
                       "<li>Тригонометрическое выражение: sin(2*pi/3)</li>"
                       "<li>Переменная в квадрате: t^2</li>"
                       "</ul>"
                       "</ul>",
    },
    "en": {
        "title": "Extracting the square root",
        "input_placeholder": "Enter a number, e.g., 2+3j , -4 or sin(2*pi/3)",
        "precision_placeholder": "Enter precision (optional)",
        "submit": "Calculate",
        "result_label": "Result",
        "error": "Enter a Latin letter in the square, a valid number, or a trigonometric expression.",
        "undefined": "Undefined",
        "precision_error": "Error: Please enter a non-negative number in the precision field.",
        "support": "Technical Support mail site",
        "email": "tdpopov@edu.hse.ru",
        "instruction_button": "Instructions",
        "instruction": "<ul>"
                       "<li>Enter a Latin letter in the square, a valid number, or a trigonometric expression.</li>"
                       "<li>Examples:</li>"
                       "<ul>"
                       "<li>Simple number: 4</li>"
                       "<li>Complex number: 2+3j</li>"
                       "<li>Negative number: -4</li>"
                       "<li>Trigonometric expression: sin(2*pi/3)</li>"
                       "<li>Variable squared: t^2</li>"
                       "</ul>"
                       "</ul>",
    },
    "es": {
        "title": "Extracción de raíz cuadrada",
        "input_placeholder": "Ingrese un número, p.ej., 2+3j , -4 o sin(2*pi/3)",
        "precision_placeholder": "Ingrese la precisión (opcional)",
        "submit": "Calcular",
        "result_label": "Resultado",
        "error": "Escriba la letra Latina en el cuadrado, un número válido o una expresión trigonométrica.",
        "undefined": "Indefinido",
        "precision_error": "Error: Ingrese un número no negativo en el campo de precisión.",
        "support": "Soporte del sitio web",
        "email": "tdpopov@edu.hse.ru",
        "instruction_button": "Instrucciones",
        "instruction": "<ul>"
                       "<li>Escriba la letra Latina en el cuadrado, un número válido o una expresión trigonométrica.</li>"
                       "<li>Ejemplos:</li>"
                       "<ul>"
                       "<li>Número simple: 4</li>"
                       "<li>Número complejo: 2+3j</li>"
                       "<li>Número negativo: -4</li>"
                       "<li>Expresión trigonométrica: sin(2*pi/3)</li>"
                       "<li>Variable al cuadrado: t^2</li>"
                       "</ul>"
                       "</ul>",
    }
}


def near_zero(value, threshold=1e-10):
    """Проверяем, является ли число близким к нулю."""
    return abs(value) < threshold


def process_input(input_value, language):
    """Обрабатываем ввод: преобразуем ^ в ** и обрабатываем переменные."""
    input_value = input_value.replace("^", "**")
    
    if re.match(r"^[a-zA-Z]\*\*2$", input_value):
        variable = input_value[0]
        return f"±{variable}"
    
    # Проверка на неопределенные выражения
    if input_value == "tan(pi/2)" or input_value == "ctg(pi)":
        return language["undefined"]
    
    # Выполняем вычисление
    try:
        return str(eval(input_value, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "ctg": lambda x: 1 / math.tan(x), "pi": math.pi, "e": math.e}))
    except ZeroDivisionError:
        return language["undefined"]


@app.route("/", methods=["GET", "POST"])
@app.route("/<lang>", methods=["GET", "POST"])
def index(lang="ru"):
    result = None
    language = languages.get(lang, languages["ru"])

    if request.method == "POST":
        try:
            input_value = request.form.get("number")
            precision_value = request.form.get("precision")

            # Проверка на правильность точности
            if precision_value:
                if not precision_value.isdigit() or int(precision_value) < 0:
                    return render_template("index.html", result=language["precision_error"], lang=lang, language=language)

            precision = int(precision_value) if precision_value else None

            processed_value = process_input(input_value, language)
            
            if processed_value == language["undefined"]:
                result = processed_value
            elif "±" in processed_value:
                result = f"√{input_value} = {processed_value}"
            else:
                complex_number = complex(processed_value)
                
                if near_zero(complex_number.real):
                    complex_number = complex(0, complex_number.imag)
                if near_zero(complex_number.imag):
                    complex_number = complex(complex_number.real, 0)
                
                is_real = complex_number.imag == 0

                if is_real and complex_number.real < 0:
                    root1 = cmath.sqrt(complex_number)
                    root2 = -root1
                else:
                    root1 = cmath.sqrt(complex_number)
                    root2 = -root1

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

                # Проверка для 0, если корень 0, результат просто 0
                if complex_number == 0:
                    result = "√0 = 0"
                elif is_real:
                    result = f"√{input_value} = ±{format_complex(root1)}"
                else:
                    result = f"√{input_value} = ±({format_complex(root1)})"
            
        except ValueError:
            result = language["error"]
        except Exception as e:
            result = language["error"]

    return render_template("index.html", result=result, lang=lang, language=language)


if __name__ == "__main__":
    app.run(debug=True)
