from flask import Flask, request, render_template
import matplotlib.pyplot as plt
from math import sin, cos, sqrt
import numpy as np
app = Flask(__name__)

functions = {
    "sin": sin,
    "cos": cos,
    "x_squared": lambda x: x**2,
    "sqrt_x": sqrt,
}

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
    if request.method == "POST":
        xleft = float(request.form.get("xleft"))
        xright = float(request.form.get("xright"))

        x = np.linspace(xleft, xright, 100)
        y = np.sin(x)

        plt.plot(x, y)

        image_name = f"static/images/plot.png"
        plt.savefig(image_name)
        plt.close()
        return render_template("plotter.html", image_path=image_name)
    else:
        return render_template("plotter.html")

if __name__ == '__main__':
    app.run(debug=True)