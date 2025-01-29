from flask import Flask, request, render_template, url_for
import matplotlib.pyplot as plt
from math import sin, cos, sqrt
import numpy as np
import io
import base64

app = Flask(__name__)

functions = {
    "sin": sin,
    "cos": cos,
    "x_squared": lambda x: x**2,
    "sqrt_x": sqrt,
}

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/sum_of_squares')
def sum_of_squares():
    try:
        num1 = int(request.args.get('num1'))
        num2 = int(request.args.get('num2'))
        result = num1**2 + num2**2
        return f"The sum of squares of {num1} and {num2} is: {result}"
    except ValueError:
        return "Invalid input. Please enter valid integers."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/plot", methods=["GET", "POST"])
def plot():
    plot_url = None
    if request.method == "POST":
        try:
            x_from = float(request.form['x_from'])
            x_to = float(request.form['x_to'])
            function_name = request.form.get('function')
            color = request.form.get('color') or '#0000FF'

            if not function_name:
                return "Please select a function."

            x = np.linspace(x_from, x_to, 100)

            plt.figure()

            if function_name in functions:
                func = functions[function_name]

                if function_name == "sqrt_x":
                    x_safe = np.where(x >= 0, x, 0)
                    y = func(x_safe)
                else:
                    y = func(x)

                plt.plot(x, y, color=color, label=function_name)

            plt.xlabel("x")
            plt.ylabel("y")
            plt.title("Plot of " + function_name)
            plt.legend()

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

            return render_template("plotter.html", plot_url=plot_url, functions=functions)

        except ValueError:
            return "Invalid input. Please enter valid numbers for the interval."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template("plotter.html", plot_url=plot_url, functions=functions)

if __name__ == '__main__':
    app.run(debug=True)