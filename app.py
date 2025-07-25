from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Métodos de aproximación

# Método de Newton-Raphson
def newton_raphson(f, df, x0, tol=1e-5, max_iter=100):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = df(x)
        if dfx == 0:
            break
        x = x - fx / dfx
    return x

# Método de Bisección
def bisection_method(f, a, b, tol=1e-5, max_iter=100):
    if f(a) * f(b) >= 0:
        return None
    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        if abs(fc) < tol:
            return c
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    return (a + b) / 2

# Método de Secantes
def secant_method(f, x0, x1, tol=1e-5, max_iter=100):
    for _ in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)
        if abs(fx1) < tol:
            return x1
        denom = fx1 - fx0
        if abs(denom) < tol:
            return x1
        x2 = x1 - fx1 * (x1 - x0) / denom
        x0, x1 = x1, x2
    return x1

# Método de Regula Falsi
def regula_falsi_method(f, a, b, tol=1e-5, max_iter=100):
    if f(a) * f(b) >= 0:
        return None
    for _ in range(max_iter):
        fa = f(a)
        fb = f(b)
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        if abs(fc) < tol:
            return c
        if fa * fc < 0:
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

# Método de Euler para resolver ecuaciones diferenciales
def euler_method(f, y0, t0, tn, h):
    t = t0
    y = y0
    n = int((tn - t0) / h)
    for _ in range(n):
        y += h * f(t, y)
        t += h
    # Último paso si es necesario
    if t < tn:
        h_last = tn - t
        y += h_last * f(t, y)
    return y

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
            exact_value = math.sqrt(2)  # Valor exacto para comparación
            
            # Newton-Raphson
            if 'newton' in request.form:
                x0 = float(request.form["newton_x0"])
                root_newton = newton_raphson(f, df, x0)
                if root_newton is not None:
                    error = abs(exact_value - root_newton)
                    result = root_newton

            # Bisección
            if 'bisection' in request.form:
                a = float(request.form["bisection_a"])
                b = float(request.form["bisection_b"])
                root_bisection = bisection_method(f, a, b)
                if root_bisection is not None:
                    error_bisection = abs(exact_value - root_bisection)
                    result_bisection = root_bisection

            # Secantes
            if 'secant' in request.form:
                x0 = float(request.form["secant_x0"])
                x1 = float(request.form["secant_x1"])
                root_secant = secant_method(f, x0, x1)
                if root_secant is not None:
                    error_secant = abs(exact_value - root_secant)
                    result_secant = root_secant

            # Regula Falsi
            if 'regula_falsi' in request.form:
                a = float(request.form["regula_falsi_a"])
                b = float(request.form["regula_falsi_b"])
                root_regula_falsi = regula_falsi_method(f, a, b)
                if root_regula_falsi is not None:
                    error_regula_falsi = abs(exact_value - root_regula_falsi)
                    result_regula_falsi = root_regula_falsi

            # Trapecio
            if 'trapezoidal' in request.form:
                a = float(request.form["trapezoidal_a"])
                b = float(request.form["trapezoidal_b"])
                n = int(request.form["trapezoidal_n"])
                result_trapezoidal = trapezoidal_method(f, a, b, n)

            # Euler
            if 'euler' in request.form:
                y0 = float(request.form["euler_y0"])
                t0 = float(request.form["euler_t0"])
                tn = float(request.form["euler_tn"])
                h = float(request.form["euler_h"])
                result_euler = euler_method(f_diff, y0, t0, tn, h)
                # Solución exacta: y(t) = y0 * e^(-2t)
                exact_euler = y0 * math.exp(-2 * (tn - t0))
                error_euler = abs(exact_euler - result_euler)

        except ValueError as e:
            result = f"Error: {str(e)}"
        except Exception as e:
            result = f"Error: {str(e)}"
    
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