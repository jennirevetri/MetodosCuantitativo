import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pulp import *
import os

class OptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")  # Establece el tamaño de la ventana a 800x600 píxeles

        self.root.title("Optimización y Programación Entera")
        
        # Crear un menú
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Crear el menú de opciones
        self.problem_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Problemas", menu=self.problem_menu)
        self.problem_menu.add_command(label="Programación Binaria", command=self.programacion_binaria)
        self.problem_menu.add_command(label="Programación Entera Mixta", command=self.programacion_entera_mixta)
        self.problem_menu.add_command(label="Programación Entera Pura", command=self.programacion_entera_pura)
        self.problem_menu.add_command(label="Problema de la Mochila", command=self.problema_de_la_mochila)
        self.problem_menu.add_command(label="Panadería (Programación Entera Mixta)", command=self.panaderia)
        self.problem_menu.add_command(label="Programación Entera (Ramificación y Cortes)", command=self.programacion_entera_ramificacion_cortes)

        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        # Variables para almacenar los parámetros del problema
        self.params = {}
        
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def save_output(self, output):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(output)
            messagebox.showinfo("Guardado", f"El resultado ha sido guardado en {file_path}")
    
    def display_output(self, output):
        self.clear_frame()
        text_box = tk.Text(self.frame, wrap=tk.WORD, width=80, height=20)
        text_box.insert(tk.END, output)
        text_box.config(state=tk.DISABLED)
        text_box.pack(pady=10)
        save_button = ttk.Button(self.frame, text="Guardar Resultado", command=lambda: self.save_output(output))
        save_button.pack(pady=5)
    
    def programacion_binaria(self):
        self.clear_frame()
        
        # Crear widgets de entrada para los parámetros
        tk.Label(self.frame, text="Función Objetivo:").grid(row=0, column=0, pady=2, sticky="e")
        tk.Label(self.frame, text="Coeficientes (separados por comas):").grid(row=1, column=0, pady=2, sticky="e")
        self.obj_coef = tk.Entry(self.frame)
        self.obj_coef.grid(row=1, column=1, pady=2)
        
        tk.Label(self.frame, text="Restricciones:").grid(row=2, column=0, pady=2, sticky="e")
        self.restricciones = tk.Text(self.frame, height=5, width=40)
        self.restricciones.grid(row=2, column=1, pady=2)
        
        tk.Label(self.frame, text="Lado derecho de las restricciones (separados por comas):").grid(row=3, column=0, pady=2, sticky="e")
        self.restr_rhs = tk.Entry(self.frame)
        self.restr_rhs.grid(row=3, column=1, pady=2)
        
        tk.Label(self.frame, text="Tipos de restricciones (<=, =, >= separados por comas):").grid(row=4, column=0, pady=2, sticky="e")
        self.restr_types = tk.Entry(self.frame)
        self.restr_types.grid(row=4, column=1, pady=2)
        
        solve_button = ttk.Button(self.frame, text="Resolver", command=self.solve_programacion_binaria)
        solve_button.grid(row=5, column=1, pady=10)
    
    def solve_programacion_binaria(self):
        # Leer los parámetros del problema
        obj_coef = list(map(int, self.obj_coef.get().split(',')))
        restricciones = [list(map(int, row.split(','))) for row in self.restricciones.get("1.0", tk.END).strip().split('\n')]
        restr_rhs = list(map(int, self.restr_rhs.get().split(',')))
        restr_types = self.restr_types.get().split(',')
        
        # Crear el problema de minimización
        prob = LpProblem("Programacion_Binaria", LpMinimize)
        
        # Definir las variables de decisión (binarias)
        variables = [LpVariable(f'x{i}', cat='Binary') for i in range(len(obj_coef))]
        
        # Definir la función objetivo
        prob += lpSum([obj_coef[i] * variables[i] for i in range(len(obj_coef))]), "Función Objetivo"
        
        # Definir las restricciones
        for i in range(len(restricciones)):
            if restr_types[i] == "<=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) <= restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == "=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) == restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == ">=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) >= restr_rhs[i], f"Restriccion_{i+1}"
        
        # Resolver el problema
        prob.solve()
        
        # Mostrar resultados
        output = f"Estado de la solución: {LpStatus[prob.status]}\n"
        for v in variables:
            output += f"{v.name} = {v.varValue}\n"
        output += f"Valor óptimo de la función objetivo: {value(prob.objective)}"
        
        self.display_output(output)
    
    def programacion_entera_mixta(self):
        self.clear_frame()
        
        # Crear widgets de entrada para los parámetros
        tk.Label(self.frame, text="Función Objetivo:").grid(row=0, column=0, pady=2, sticky="e")
        tk.Label(self.frame, text="Coeficientes (separados por comas):").grid(row=1, column=0, pady=2, sticky="e")
        self.obj_coef_mixta = tk.Entry(self.frame)
        self.obj_coef_mixta.grid(row=1, column=1, pady=2)
        
        tk.Label(self.frame, text="Variables (enteras, separadas por comas):").grid(row=2, column=0, pady=2, sticky="e")
        self.var_ent_mixta = tk.Entry(self.frame)
        self.var_ent_mixta.grid(row=2, column=1, pady=2)
        
        tk.Label(self.frame, text="Restricciones:").grid(row=3, column=0, pady=2, sticky="e")
        self.restricciones_mixta = tk.Text(self.frame, height=5, width=40)
        self.restricciones_mixta.grid(row=3, column=1, pady=2)
        
        tk.Label(self.frame, text="Lado derecho de las restricciones (separados por comas):").grid(row=4, column=0, pady=2, sticky="e")
        self.restr_rhs_mixta = tk.Entry(self.frame)
        self.restr_rhs_mixta.grid(row=4, column=1, pady=2)
        
        tk.Label(self.frame, text="Tipos de restricciones (<=, =, >= separados por comas):").grid(row=5, column=0, pady=2, sticky="e")
        self.restr_types_mixta = tk.Entry(self.frame)
        self.restr_types_mixta.grid(row=5, column=1, pady=2)
        
        solve_button = ttk.Button(self.frame, text="Resolver", command=self.solve_programacion_entera_mixta)
        solve_button.grid(row=6, column=1, pady=10)
    
    def solve_programacion_entera_mixta(self):
        # Leer los parámetros del problema
        obj_coef = list(map(int, self.obj_coef_mixta.get().split(',')))
        var_ent = list(map(int, self.var_ent_mixta.get().split(',')))
        restricciones = [list(map(int, row.split(','))) for row in self.restricciones_mixta.get("1.0", tk.END).strip().split('\n')]
        restr_rhs = list(map(int, self.restr_rhs_mixta.get().split(',')))
        restr_types = self.restr_types_mixta.get().split(',')
        
        # Crear el problema de maximización
        prob = LpProblem("Programacion_Entera_Mixta", LpMaximize)
        
        # Definir las variables de decisión (mixtas)
        variables = []
        for i in range(len(obj_coef)):
            if i in var_ent:
                variables.append(LpVariable(f'x{i}', lowBound=0, cat='Integer'))
            else:
                variables.append(LpVariable(f'x{i}', lowBound=0))
        
        # Definir la función objetivo
        prob += lpSum([obj_coef[i] * variables[i] for i in range(len(obj_coef))]), "Función Objetivo"
        
        # Definir las restricciones
        for i in range(len(restricciones)):
            if restr_types[i] == "<=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) <= restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == "=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) == restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == ">=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) >= restr_rhs[i], f"Restriccion_{i+1}"
        
        # Resolver el problema
        prob.solve()
        
        # Mostrar resultados
        output = f"Estado de la solución: {LpStatus[prob.status]}\n"
        for v in variables:
            output += f"{v.name} = {v.varValue}\n"
        output += f"Valor óptimo de la función objetivo: {value(prob.objective)}"
        
        self.display_output(output)
    
    def programacion_entera_pura(self):
        self.clear_frame()
        
        # Crear widgets de entrada para los parámetros
        tk.Label(self.frame, text="Función Objetivo:").grid(row=0, column=0, pady=2, sticky="e")
        tk.Label(self.frame, text="Coeficientes (separados por comas):").grid(row=1, column=0, pady=2, sticky="e")
        self.obj_coef_pura = tk.Entry(self.frame)
        self.obj_coef_pura.grid(row=1, column=1, pady=2)
        
        tk.Label(self.frame, text="Restricciones:").grid(row=2, column=0, pady=2, sticky="e")
        self.restricciones_pura = tk.Text(self.frame, height=5, width=40)
        self.restricciones_pura.grid(row=2, column=1, pady=2)
        
        tk.Label(self.frame, text="Lado derecho de las restricciones (separados por comas):").grid(row=3, column=0, pady=2, sticky="e")
        self.restr_rhs_pura = tk.Entry(self.frame)
        self.restr_rhs_pura.grid(row=3, column=1, pady=2)
        
        tk.Label(self.frame, text="Tipos de restricciones (<=, =, >= separados por comas):").grid(row=4, column=0, pady=2, sticky="e")
        self.restr_types_pura = tk.Entry(self.frame)
        self.restr_types_pura.grid(row=4, column=1, pady=2)
        
        solve_button = ttk.Button(self.frame, text="Resolver", command=self.solve_programacion_entera_pura)
        solve_button.grid(row=5, column=1, pady=10)
    
    def solve_programacion_entera_pura(self):
        # Leer los parámetros del problema
        obj_coef = list(map(int, self.obj_coef_pura.get().split(',')))
        restricciones = [list(map(int, row.split(','))) for row in self.restricciones_pura.get("1.0", tk.END).strip().split('\n')]
        restr_rhs = list(map(int, self.restr_rhs_pura.get().split(',')))
        restr_types = self.restr_types_pura.get().split(',')
        
        # Crear el problema de maximización
        prob = LpProblem("Programacion_Entera_Pura", LpMaximize)
        
        # Definir las variables de decisión (enteras)
        variables = [LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(len(obj_coef))]
        
        # Definir la función objetivo
        prob += lpSum([obj_coef[i] * variables[i] for i in range(len(obj_coef))]), "Función Objetivo"
        
        # Definir las restricciones
        for i in range(len(restricciones)):
            if restr_types[i] == "<=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) <= restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == "=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) == restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == ">=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) >= restr_rhs[i], f"Restriccion_{i+1}"
        
        # Resolver el problema
        prob.solve()
        
        # Mostrar resultados
        output = f"Estado de la solución: {LpStatus[prob.status]}\n"
        for v in variables:
            output += f"{v.name} = {v.varValue}\n"
        output += f"Valor óptimo de la función objetivo: {value(prob.objective)}"
        
        self.display_output(output)
    
    def problema_de_la_mochila(self):
        self.clear_frame()
        
        # Crear widgets de entrada para los parámetros
        tk.Label(self.frame, text="Pesos de los objetos (separados por comas):").grid(row=0, column=0, pady=2, sticky="e")
        self.pesos = tk.Entry(self.frame)
        self.pesos.grid(row=0, column=1, pady=2)
        
        tk.Label(self.frame, text="Valores de los objetos (separados por comas):").grid(row=1, column=0, pady=2, sticky="e")
        self.valores = tk.Entry(self.frame)
        self.valores.grid(row=1, column=1, pady=2)
        
        tk.Label(self.frame, text="Capacidad máxima de la mochila:").grid(row=2, column=0, pady=2, sticky="e")
        self.capacidad = tk.Entry(self.frame)
        self.capacidad.grid(row=2, column=1, pady=2)
        
        solve_button = ttk.Button(self.frame, text="Resolver", command=self.solve_problema_de_la_mochila)
        solve_button.grid(row=3, column=1, pady=10)
    
    def solve_problema_de_la_mochila(self):
        # Leer los parámetros del problema
        pesos = list(map(int, self.pesos.get().split(',')))
        valores = list(map(int, self.valores.get().split(',')))
        capacidad = int(self.capacidad.get())
        
        # Crear el problema de maximización
        problema_mochila = LpProblem("Problema_de_la_Mochila", LpMaximize)
        
        # Definir las variables de decisión (0 o 1 para cada objeto)
        n = len(pesos)
        x = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(n)]
        
        # Definir la función objetivo (maximizar el valor total)
        problema_mochila += lpSum([valores[i] * x[i] for i in range(n)]), "Valor_total"
        
        # Definir la restricción de capacidad de la mochila
        problema_mochila += lpSum([pesos[i] * x[i] for i in range(n)]) <= capacidad, "Capacidad_mochila"
        
        # Resolver el problema
        problema_mochila.solve()
        
        # Mostrar resultados
        output = f"Estado de la solución: {LpStatus[problema_mochila.status]}\n"
        for i in range(n):
            output += f"Objeto {i+1}: {'Seleccionado' if x[i].varValue == 1 else 'No seleccionado'} (Peso: {pesos[i]}, Valor: {valores[i]})\n"
        
        valor_total = sum(valores[i] * x[i].varValue for i in range(n))
        peso_total = sum(pesos[i] * x[i].varValue for i in range(n))
        
        output += f"\nValor total en la mochila: {valor_total}\n"
        output += f"Peso total en la mochila: {peso_total}"
        
        self.display_output(output)
    
    def panaderia(self):
        self.clear_frame()
        
        # Crear widgets de entrada para los parámetros
        tk.Label(self.frame, text="Capacidades máximas de los hornos (separados por comas):").grid(row=0, column=0, pady=2, sticky="e")
        self.capacidades_hornos = tk.Entry(self.frame)
        self.capacidades_hornos.grid(row=0, column=1, pady=2)
        
        tk.Label(self.frame, text="Costes diarios de los hornos (separados por comas):").grid(row=1, column=0, pady=2, sticky="e")
        self.costes_diarios = tk.Entry(self.frame)
        self.costes_diarios.grid(row=1, column=1, pady=2)
        
        tk.Label(self.frame, text="Costes de hornear una barra en cada horno (separados por comas):").grid(row=2, column=0, pady=2, sticky="e")
        self.costes_barras = tk.Entry(self.frame)
        self.costes_barras.grid(row=2, column=1, pady=2)
        
        tk.Label(self.frame, text="Número total de barras a hornear:").grid(row=3, column=0, pady=2, sticky="e")
        self.barras = tk.Entry(self.frame)
        self.barras.grid(row=3, column=1, pady=2)
        
        solve_button = ttk.Button(self.frame, text="Resolver", command=self.solve_panaderia)
        solve_button.grid(row=4, column=1, pady=10)
    
    def solve_panaderia(self):
        # Leer los parámetros del problema
        capacidades_hornos = list(map(int, self.capacidades_hornos.get().split(',')))
        costes_diarios = list(map(int, self.costes_diarios.get().split(',')))
        costes_barras = list(map(float, self.costes_barras.get().split(',')))
        barras = int(self.barras.get())
        
        # Crear el problema de minimización
        prob = LpProblem("Problema_Panaderia", LpMinimize)
        
        # Definir las variables de decisión
        n = len(capacidades_hornos)
        x = [LpVariable(f"x_{i+1}", lowBound=0) for i in range(n)]  # Variables continuas para el número de barras
        
        # Definir la función objetivo (minimizar el coste total)
        prob += lpSum([costes_diarios[i] + costes_barras[i] * x[i] for i in range(n)]), "Coste_total"
        
        # Definir las restricciones
        prob += lpSum(x) == barras, "Total_barras"
        for i in range(n):
            prob += x[i] <= capacidades_hornos[i], f"Capacidad_horno_{i+1}"
        
        # Resolver el problema
        prob.solve()
        
        # Mostrar resultados
        output = f"Estado de la solución: {LpStatus[prob.status]}\n"
        for i in range(n):
            output += f"Horno {i+1}: {x[i].varValue} barras\n"
        
        output += f"\nCoste total: {value(prob.objective)}"
        
        self.display_output(output)

    def programacion_entera_ramificacion_cortes(self):
        self.clear_frame()
        tk.Label(self.frame, text="Función Objetivo:").grid(row=0, column=0, pady=2, sticky="e")
        tk.Label(self.frame, text="Coeficientes (separados por comas):").grid(row=1, column=0, pady=2, sticky="e")
        self.obj_coef_ramificacion = tk.Entry(self.frame)
        self.obj_coef_ramificacion.grid(row=1, column=1, pady=2)
        
        tk.Label(self.frame, text="Restricciones:").grid(row=2, column=0, pady=2, sticky="e")
        self.restricciones_ramificacion = tk.Text(self.frame, height=5, width=40)
        self.restricciones_ramificacion.grid(row=2, column=1, pady=2)
        
        tk.Label(self.frame, text="Lado derecho de las restricciones (separados por comas):").grid(row=3, column=0, pady=2, sticky="e")
        self.restr_rhs_ramificacion = tk.Entry(self.frame)
        self.restr_rhs_ramificacion.grid(row=3, column=1, pady=2)
        
        tk.Label(self.frame, text="Tipos de restricciones (<=, =, >= separados por comas):").grid(row=4, column=0, pady=2, sticky="e")
        self.restr_types_ramificacion = tk.Entry(self.frame)
        self.restr_types_ramificacion.grid(row=4, column=1, pady=2)
        
        solve_button = ttk.Button(self.frame, text="Resolver", command=self.solve_programacion_entera_ramificacion_cortes)
        solve_button.grid(row=5, column=1, pady=10)

# Definir el método solve_programacion_entera_ramificacion_cortes
    def solve_programacion_entera_ramificacion_cortes(self):
        # Leer los parámetros del problema
        obj_coef = list(map(int, self.obj_coef_ramificacion.get().split(',')))
        restricciones = [list(map(int, row.split(','))) for row in self.restricciones_ramificacion.get("1.0", tk.END).strip().split('\n')]
        restr_rhs = list(map(int, self.restr_rhs_ramificacion.get().split(',')))
        restr_types = self.restr_types_ramificacion.get().split(',')
        
        # Crear el problema de maximización
        prob = LpProblem("Programacion_Entera_Ramificacion_Cortes", LpMaximize)
        
        # Definir las variables de decisión (enteras)
        variables = [LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(len(obj_coef))]
        
        # Definir la función objetivo
        prob += lpSum([obj_coef[i] * variables[i] for i in range(len(obj_coef))]), "Función Objetivo"
        
        # Definir las restricciones
        for i in range(len(restricciones)):
            if restr_types[i] == "<=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) <= restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == "=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) == restr_rhs[i], f"Restriccion_{i+1}"
            elif restr_types[i] == ">=":
                prob += lpSum([restricciones[i][j] * variables[j] for j in range(len(obj_coef))]) >= restr_rhs[i], f"Restriccion_{i+1}"
        
        # Resolver el problema
        prob.solve()
        
        # Mostrar resultados
        output = f"Estado de la solución: {LpStatus[prob.status]}\n"
        for v in variables:
            output += f"{v.name} = {v.varValue}\n"
        output += f"Valor óptimo de la función objetivo: {value(prob.objective)}"
        
        self.display_output(output)
    
    def display_output(self, output):
        self.clear_frame()
        text_box = tk.Text(self.frame, wrap=tk.WORD)
        text_box.insert(tk.END, output)
        text_box.grid(row=0, column=0, padx=10, pady=10)
        
        save_button = ttk.Button(self.frame, text="Guardar resultado", command=lambda: self.save_output(output))
        save_button.grid(row=1, column=0, pady=10)
    
    def save_output(self, output):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(output)
    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()
