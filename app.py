from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Métodos de aproximación

# Método de Newton-Raphson
def newton_raphson(f, df, x0, tol=1e-5, max_iter=100):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(fx) < tol:
            return x
        x = x - fx / dfx
    return x

# Método de Bisección
def bisection_method(f, a, b, tol=1e-5, max_iter=100):
    if f(a) * f(b) > 0:
        return None  # No hay raíz entre a y b
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2

# Método de Secantes
def secant_method(f, x0, x1, tol=1e-5, max_iter=100):
    for _ in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)
        if abs(fx1 - fx0) < tol:
            return x1
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        if abs(f(x2)) < tol:
            return x2
        x0, x1 = x1, x2
    return x1

# Método de Regula Falsi
def regula_falsi_method(f, a, b, tol=1e-5, max_iter=100):
    if f(a) * f(b) > 0:
        return None  # No hay raíz entre a y b
    for _ in range(max_iter):
        c = b - f(b)*(b - a) / (f(b) - f(a))
        if abs(f(c)) < tol:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c

# Método de Trapecio
def trapezoidal_method(f, a, b, n):
    h = (b - a) / n
    sum_val = (f(a) + f(b)) / 2
    for i in range(1, n):
        sum_val += f(a + i * h)
    return sum_val * h

# Función de ejemplo: f(x) = x^2 - 2 (Raíz en sqrt(2))
def f(x):
    return x**2 - 2

# Derivada de la función: f'(x) = 2x
def df(x):
    return 2*x

# Función para la ecuación diferencial: dy/dt = -2y
def f_diff(t, y):
    return -2 * y

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    result_bisection = None
    error_bisection = None
    result_secant = None
    error_secant = None
    result_regula_falsi = None
    error_regula_falsi = None
    result_trapezoidal = None
    error_trapezoidal = None
    result_euler = None
    error_euler = None

    if request.method == "POST":
        try:
            # Selección de métodos y validación de entrada
            if 'newton' in request.form:
                x0 = float(request.form["x0"])
                root_newton = newton_raphson(f, df, x0)
                exact_value = math.sqrt(2)
                error = abs(exact_value - root_newton)
                result = root_newton

            if 'bisection' in request.form:
                a = float(request.form["a"])
                b = float(request.form["b"])
                root_bisection = bisection_method(f, a, b)
                if root_bisection is not None:
                    error_bisection = abs(exact_value - root_bisection)
                result_bisection = root_bisection

            if 'secant' in request.form:
                x0 = float(request.form["x0"])
                x1 = float(request.form["x1"])
                root_secant = secant_method(f, x0, x1)
                error_secant = abs(exact_value - root_secant)
                result_secant = root_secant

            if 'regula_falsi' in request.form:
                a = float(request.form["a"])
                b = float(request.form["b"])
                root_regula_falsi = regula_falsi_method(f, a, b)
                error_regula_falsi = abs(exact_value - root_regula_falsi)
                result_regula_falsi = root_regula_falsi

            if 'trapezoidal' in request.form:
                a = float(request.form["a"])
                b = float(request.form["b"])
                n = int(request.form["n"])
                result_trapezoidal = trapezoidal_method(f, a, b, n)

            if 'euler' in request.form:
                y0 = float(request.form["y0"])
                t0 = float(request.form["t0"])
                tn = float(request.form["tn"])
                h = float(request.form["h"])
                result_euler = euler_method(f_diff, y0, t0, tn, h)
                error_euler = abs(result_euler - 1)  # Comparar con valor real para y(tn)

        except ValueError:
            result = "Error: Por favor ingresa un valor numérico válido."
    
    return render_template("index.html", 
                           result=result, 
                           error=error,
                           result_bisection=result_bisection,
                           error_bisection=error_bisection,
                           result_secant=result_secant,
                           error_secant=error_secant,
                           result_regula_falsi=result_regula_falsi,
                           error_regula_falsi=error_regula_falsi,
                           result_trapezoidal=result_trapezoidal,
                           error_trapezoidal=error_trapezoidal,
                           result_euler=result_euler,
                           error_euler=error_euler)

if __name__ == "__main__":
    app.run(debug=True)
