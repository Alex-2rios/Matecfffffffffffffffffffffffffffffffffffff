from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Entorno seguro para evaluación de funciones
safe_dict = {
    'abs': abs, 'max': max, 'min': min, 'pow': pow, 'round': round,
    'math': math, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'exp': math.exp, 'log': math.log, 'log10': math.log10, 'sqrt': math.sqrt,
    'pi': math.pi, 'e': math.e
}
safe_dict['__builtins__'] = {}

# Métodos de aproximación

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    iterations = []
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        if abs(dfx) < 1e-15:
            return None, iterations, "Derivada cero"
            
        x_new = x - fx / dfx
        error = abs(x_new - x)
        iterations.append({
            'iteration': i+1,
            'x': x,
            'f(x)': fx,
            "f'(x)": dfx,
            'x_new': x_new,
            'error': error
        })
        
        if error < tol or abs(fx) < tol:
            return x_new, iterations, None
            
        x = x_new
        
    return x, iterations, "Máximas iteraciones alcanzadas"

def bisection_method(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) > 0:
        return None, [], "No hay cambio de signo en el intervalo"
    
    iterations = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        fa = f(a)
        fb = f(b)
        error = abs(b - a) / 2
        
        iterations.append({
            'iteration': i+1,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
            'error': error
        })
        
        if abs(fc) < tol or error < tol:
            return c, iterations, None
            
        if fa * fc < 0:
            b = c
        else:
            a = c
            
    return (a + b) / 2, iterations, "Máximas iteraciones alcanzadas"

def secant_method(f, x0, x1, tol=1e-6, max_iter=100):
    iterations = []
    for i in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)
        
        if abs(fx1 - fx0) < 1e-15:
            return None, iterations, "División por cero"
            
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x2 - x1)
        
        iterations.append({
            'iteration': i+1,
            'x0': x0,
            'x1': x1,
            'f(x0)': fx0,
            'f(x1)': fx1,
            'x2': x2,
            'error': error
        })
        
        if abs(fx1) < tol or error < tol:
            return x2, iterations, None
            
        x0, x1 = x1, x2
        
    return x1, iterations, "Máximas iteraciones alcanzadas"

def regula_falsi_method(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) > 0:
        return None, [], "No hay cambio de signo en el intervalo"
    
    iterations = []
    for i in range(max_iter):
        fa = f(a)
        fb = f(b)
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        error = abs(fc)
        
        iterations.append({
            'iteration': i+1,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
            'error': error
        })
        
        if abs(fc) < tol:
            return c, iterations, None
            
        if fa * fc < 0:
            b = c
        else:
            a = c
            
    return c, iterations, "Máximas iteraciones alcanzadas"

def trapezoidal_method(f, a, b, n):
    h = (b - a) / n
    result = (f(a) + f(b)) / 2
    points = [a]
    values = [f(a)]
    
    for i in range(1, n):
        x = a + i * h
        result += f(x)
        points.append(x)
        values.append(f(x))
        
    points.append(b)
    values.append(f(b))
    return result * h, points, values

def euler_method(f, y0, t0, tn, h):
    t = t0
    y = y0
    n = int((tn - t0) / h)
    points = [t0]
    values = [y0]
    
    for i in range(n):
        y += h * f(t, y)
        t += h
        points.append(t)
        values.append(y)
    
    # Último paso si es necesario
    if t < tn:
        h_last = tn - t
        y += h_last * f(t, y)
        t = tn
        points.append(t)
        values.append(y)
        
    return y, points, values

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    function_expression = "x**2 - 2"
    derivative_expression = "2*x"
    edo_expression = "-2*y"
    
    if request.method == "POST":
        try:
            # Obtener expresiones
            function_expression = request.form.get("function", "x**2 - 2")
            derivative_expression = request.form.get("derivative", "2*x")
            edo_expression = request.form.get("edo", "-2*y")
            
            # Crear funciones
            f = lambda x: eval(function_expression, {'x': x, **safe_dict})
            df = lambda x: eval(derivative_expression, {'x': x, **safe_dict})
            f_edo = lambda t, y: eval(edo_expression, {'t': t, 'y': y, **safe_dict})
            
            # Procesar métodos seleccionados
            if 'newton' in request.form:
                x0 = float(request.form["newton_x0"])
                tol = float(request.form.get("newton_tol", 1e-6))
                root, iterations, error_msg = newton_raphson(f, df, x0, tol)
                results['newton'] = {
                    'root': root,
                    'iterations': iterations,
                    'error': abs(f(root)) if root is not None else None,
                    'error_msg': error_msg
                }
                
            if 'bisection' in request.form:
                a = float(request.form["bisection_a"])
                b = float(request.form["bisection_b"])
                tol = float(request.form.get("bisection_tol", 1e-6))
                root, iterations, error_msg = bisection_method(f, a, b, tol)
                results['bisection'] = {
                    'root': root,
                    'iterations': iterations,
                    'error': abs(f(root)) if root is not None else None,
                    'error_msg': error_msg
                }
                
            if 'secant' in request.form:
                x0 = float(request.form["secant_x0"])
                x1 = float(request.form["secant_x1"])
                tol = float(request.form.get("secant_tol", 1e-6))
                root, iterations, error_msg = secant_method(f, x0, x1, tol)
                results['secant'] = {
                    'root': root,
                    'iterations': iterations,
                    'error': abs(f(root)) if root is not None else None,
                    'error_msg': error_msg
                }
                
            if 'regula_falsi' in request.form:
                a = float(request.form["regula_falsi_a"])
                b = float(request.form["regula_falsi_b"])
                tol = float(request.form.get("regula_falsi_tol", 1e-6))
                root, iterations, error_msg = regula_falsi_method(f, a, b, tol)
                results['regula_falsi'] = {
                    'root': root,
                    'iterations': iterations,
                    'error': abs(f(root)) if root is not None else None,
                    'error_msg': error_msg
                }
                
            if 'trapezoidal' in request.form:
                a = float(request.form["trapezoidal_a"])
                b = float(request.form["trapezoidal_b"])
                n = int(request.form["trapezoidal_n"])
                result, points, values = trapezoidal_method(f, a, b, n)
                results['trapezoidal'] = {
                    'result': result,
                    'points': points,
                    'values': values
                }
                
            if 'euler' in request.form:
                y0 = float(request.form["euler_y0"])
                t0 = float(request.form["euler_t0"])
                tn = float(request.form["euler_tn"])
                h = float(request.form["euler_h"])
                result, points, values = euler_method(f_edo, y0, t0, tn, h)
                # Solución exacta para EDO simple
                if edo_expression == "-2*y":
                    exact = y0 * math.exp(-2 * (tn - t0))
                    error = abs(result - exact)
                else:
                    exact = None
                    error = None
                    
                results['euler'] = {
                    'result': result,
                    'points': points,
                    'values': values,
                    'exact': exact,
                    'error': error
                }
                
        except Exception as e:
            import traceback
            results['error'] = f"Error: {str(e)}<br>{traceback.format_exc()}"
    
    return render_template("index.html", results=results, 
                           function=function_expression,
                           derivative=derivative_expression,
                           edo=edo_expression)

if __name__ == "__main__":
    app.run(debug=True)