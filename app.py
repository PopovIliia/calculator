from flask import Flask, render_template, request
import cmath  # для работы с комплексными числами
import math   # для работы с действительными числами

app = Flask(__name__)

# Данные для языков
languages = {
    "ru": {
        "title": "Квадратный корень числа",
        "input_placeholder": "Введите число, например, 2+3j или -4",
        "precision_placeholder": "Введите точность (необязательно)",
        "submit": "Рассчитать",
        "result_label": "Результат",
        "error": "Пожалуйста, введите корректное число.",
        "support": "Почта техподдержки сайта",
        "email": "tdpopov@edu.hse.ru",
    },
    "en": {
        "title": "Square Root of a Number",
        "input_placeholder": "Enter a number, e.g., 2+3j or -4",
        "precision_placeholder": "Enter precision (optional)",
        "submit": "Calculate",
        "result_label": "Result",
        "error": "Please enter a valid number.",
        "support": "Technical Support mail site",
        "email": "tdpopov@edu.hse.ru",
    },
    "es": {
        "title": "Raíz Cuadrada de un Número",
        "input_placeholder": "Ingrese un número, p.ej., 2+3j o -4",
        "precision_placeholder": "Ingrese la precisión (opcional)",
        "submit": "Calcular",
        "result_label": "Resultado",
        "error": "Por favor, ingrese un número válido.",
        "support": "Soporte del sitio web",
        "email": "tdpopov@edu.hse.ru",
    }
}

@app.route("/", methods=["GET", "POST"])
@app.route("/<lang>", methods=["GET", "POST"])
def index(lang="ru"):
    result = None
    language = languages.get(lang, languages["ru"])

    if request.method == "POST":
        try:
            input_value = request.form.get("number")
            precision_value = request.form.get("precision")
            # Если точность не указана, не округляем, выводим максимальное количество знаков
            precision = int(precision_value) if precision_value else None

            # Преобразуем строку в число (комплексное или реальное)
            complex_number = complex(input_value)
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
                if imag == 0:  # Действительное число
                    return f"{real}"
                elif real == 0:  # Только мнимая часть
                    return f"{imag}j"
                else:  # Комплексное число
                    sign = "+" if imag > 0 else "-"
                    return f"{real}{sign}{abs(imag)}j"

            # Форматируем результат
            if is_real:  # Для действительных чисел показываем ±
                result = f"√{input_value} = ±{format_complex(root1)}"
            else:  # Для комплексных чисел показываем только один корень
                result = f"√{input_value} = {format_complex(root1)}"
            
        except ValueError:
            result = language["error"]
        except Exception as e:
            result = f"Ошибка: {str(e)}"

    return render_template("index.html", result=result, lang=lang, language=language)

if __name__ == "__main__":
    app.run(debug=True)
