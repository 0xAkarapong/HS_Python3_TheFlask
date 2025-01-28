from flask import Flask, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)