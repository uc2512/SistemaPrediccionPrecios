import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query
import statistics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class AnalisisEstadistico:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        # Variables para almacenar datos
        self.productos_dict = {}  # {id_producto: "Nombre (unidad)"}
        self.datos_analisis = None  # Almacenará los datos del producto seleccionado
        
        self.canvas.delete("all")
        self.cargar_productos()
        self.crear_interfaz()
    
    def cargar_productos(self):
        """Carga productos que tienen ofertas registradas"""
        query = """
        SELECT DISTINCT p.id_producto, p.nombre_producto, p.unidad_medida 
        FROM producto p
        INNER JOIN oferta o ON p.id_producto = o.id_producto
        WHERE p.activo = TRUE
        ORDER BY p.nombre_producto;
        """
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            for fila in resultados:
                id_prod = fila[0]
                nombre = f"{fila[1]} ({fila[2]})"
                self.productos_dict[id_prod] = nombre
        
        print(f"✓ Productos con ofertas: {len(self.productos_dict)}")
    
    def crear_interfaz(self):
        """Crea la interfaz del módulo de análisis estadístico"""
        
        # Header
        self.canvas.create_text(450, 30, 
                               text="📈 ANÁLISIS ESTADÍSTICO", 
                               font=("Arial", 20, "bold"), 
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, 
                               text="Estudio de tendencias, volatilidad y patrones de precios", 
                               font=("Arial", 11), 
                               fill="#94a3b8")
        
        # Línea divisoria
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        # === SECCIÓN SELECTOR ===
        self.canvas.create_rectangle(50, 90, 850, 160, 
                                     fill="#1e293b", outline="#8b5cf6", width=2)
        
        self.canvas.create_text(450, 105, 
                               text="SELECCIONAR PRODUCTO PARA ANALIZAR", 
                               font=("Arial", 12, "bold"), 
                               fill="#8b5cf6")
        
        # Verificar si hay productos
        if not self.productos_dict:
            self.canvas.create_text(450, 130, 
                                   text="⚠️  No hay productos con ofertas registradas", 
                                   font=("Arial", 11, "bold"), 
                                   fill="#f59e0b")
            self.crear_boton_volver()
            return
        
        # Combobox de productos
        self.canvas.create_text(250, 135, 
                               text="Producto:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="e")
        
        self.combo_producto = ttk.Combobox(
            self.frame_principal,
            values=list(self.productos_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=35
        )
        self.combo_producto.place(x=270, y=125)
        
        # Botón Analizar
        self.btn_analizar = tk.Button(
            self.frame_principal,
            text="📊 Analizar",
            font=("Arial", 10, "bold"),
            bg="#8b5cf6", fg="white",
            activebackground="#7c3aed",
            relief=tk.FLAT, cursor="hand2",
            padx=25, pady=6,
            command=self.analizar_producto
        )
        self.btn_analizar.place(x=610, y=125)
        
        # === SECCIÓN ESTADÍSTICAS PRINCIPALES ===
        self.canvas.create_rectangle(50, 175, 850, 265, 
                                     fill="#1e293b", outline="#10b981", width=2)
        
        self.canvas.create_text(450, 190, 
                               text="ESTADÍSTICAS PRINCIPALES", 
                               font=("Arial", 11, "bold"), 
                               fill="#10b981")
        
        # Tarjetas de estadísticas (4 columnas)
        card_y = 222
        card_width = 160
        card_height = 55
        spacing = 188
        
        # Tarjeta 1: Precio Actual
        x1 = 140
        self.crear_tarjeta_stat(x1, card_y, card_width, card_height, 
                               "💰 Precio Actual", "---", "#3b82f6", "card_actual")
        
        # Tarjeta 2: Precio Promedio
        x2 = x1 + spacing
        self.crear_tarjeta_stat(x2, card_y, card_width, card_height, 
                               "📊 Precio Promedio", "---", "#10b981", "card_promedio")
        
        # Tarjeta 3: Precio Mínimo
        x3 = x2 + spacing
        self.crear_tarjeta_stat(x3, card_y, card_width, card_height, 
                               "⬇️ Precio Mínimo", "---", "#06b6d4", "card_minimo")
        
        # Tarjeta 4: Precio Máximo
        x4 = x3 + spacing
        self.crear_tarjeta_stat(x4, card_y, card_width, card_height, 
                               "⬆️ Precio Máximo", "---", "#dc2626", "card_maximo")
        
        # === SECCIÓN GRÁFICOS ===
        self.canvas.create_rectangle(50, 280, 850, 345, 
                                     fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(450, 295, 
                               text="VISUALIZACIÓN DE DATOS", 
                               font=("Arial", 10, "bold"), 
                               fill="#06b6d4")
        
        # Botón para gráfico de evolución
        self.btn_grafico_evolucion = tk.Button(
            self.frame_principal,
            text="📈 Ver Evolución de Precios",
            font=("Arial", 10, "bold"),
            bg="#06b6d4", fg="white",
            activebackground="#0891b2",
            relief=tk.FLAT, cursor="hand2",
            padx=20, pady=8,
            state=tk.DISABLED,  # Deshabilitado hasta que se analice
            command=self.mostrar_grafico_evolucion
        )
        self.btn_grafico_evolucion.place(x=330, y=315)
        
        # === SECCIÓN INFORMACIÓN ADICIONAL (ahora más abajo) ===
        self.canvas.create_rectangle(50, 360, 850, 510, 
                                     fill="#1e293b", outline="#f59e0b", width=2)
        
        self.canvas.create_text(450, 375, 
                               text="INFORMACIÓN DETALLADA", 
                               font=("Arial", 11, "bold"), 
                               fill="#f59e0b")
        
        # Área de información
        info_y = 405
        info_spacing = 35
        
        self.canvas.create_text(120, info_y, 
                               text="📉 Volatilidad:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.label_volatilidad = self.canvas.create_text(270, info_y, 
                               text="Seleccione un producto para analizar", 
                               font=("Arial", 10), 
                               fill="#94a3b8", anchor="w",
                               tags="info_volatilidad")
        
        self.canvas.create_text(120, info_y + info_spacing, 
                               text="📈 Tendencia:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.label_tendencia = self.canvas.create_text(270, info_y + info_spacing, 
                               text="---", 
                               font=("Arial", 10), 
                               fill="#94a3b8", anchor="w",
                               tags="info_tendencia")
        
        self.canvas.create_text(120, info_y + info_spacing*2, 
                               text="🏪 Mercados:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.label_mercados = self.canvas.create_text(270, info_y + info_spacing*2, 
                               text="---", 
                               font=("Arial", 10), 
                               fill="#94a3b8", anchor="w",
                               tags="info_mercados")
        
        self.canvas.create_text(120, info_y + info_spacing*3, 
                               text="🕐 Última actualización:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.label_fecha = self.canvas.create_text(270, info_y + info_spacing*3, 
                               text="---", 
                               font=("Arial", 10), 
                               fill="#94a3b8", anchor="w",
                               tags="info_fecha")
        
        self.canvas.create_text(120, info_y + info_spacing*4, 
                               text="💹 Rango de precios:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.label_rango = self.canvas.create_text(270, info_y + info_spacing*4, 
                               text="---", 
                               font=("Arial", 10), 
                               fill="#94a3b8", anchor="w",
                               tags="info_rango")
        
        # Crear botón volver
        self.crear_boton_volver()
    
    def crear_tarjeta_stat(self, x, y, width, height, titulo, valor, color, tag):
        """Crea una tarjeta de estadística"""
        # Fondo
        self.canvas.create_rectangle(x - width/2, y - height/2, 
                                     x + width/2, y + height/2,
                                     fill="#0f172a", outline=color, width=2,
                                     tags=f"{tag}_bg")
        
        # Título
        self.canvas.create_text(x, y - 15, 
                               text=titulo, 
                               font=("Arial", 9, "bold"), 
                               fill=color,
                               tags=f"{tag}_titulo")
        
        # Valor
        self.canvas.create_text(x, y + 10, 
                               text=valor, 
                               font=("Arial", 16, "bold"), 
                               fill="#e2e8f0",
                               tags=f"{tag}_valor")
    
    def analizar_producto(self):
        """Realiza el análisis estadístico del producto seleccionado"""
        if not self.combo_producto.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        # Obtener ID del producto
        id_producto = self.get_id_from_combo(self.combo_producto, self.productos_dict)
        
        # Consultar precios ACTUALES (de ofertas)
        query_actual = """
        SELECT 
            o.precio,
            o.fecha_actualizacion,
            m.nombre_mercado
        FROM oferta o
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        WHERE o.id_producto = %s
        ORDER BY o.fecha_actualizacion DESC;
        """
        
        resultados_actuales = execute_query(query_actual, (id_producto,), fetch=True)
        
        if not resultados_actuales:
            messagebox.showinfo("Sin datos", "No hay ofertas registradas para este producto")
            return
        
        # Extraer precios actuales
        precios_actuales = [float(fila[0]) for fila in resultados_actuales]
        mercados = [fila[2] for fila in resultados_actuales]
        fecha_reciente = resultados_actuales[0][1]
        precio_actual = precios_actuales[0]  # El más reciente
        
        # Consultar HISTORIAL de precios (para cálculos estadísticos)
        query_historial = """
        SELECT observaciones, fecha_registro
        FROM historial_p
        WHERE id_producto = %s 
        AND observaciones LIKE 'Precio actualizado%%'
        ORDER BY fecha_registro DESC;
        """
        
        resultados_historial = execute_query(query_historial, (id_producto,), fetch=True)
        
        # Extraer precios del historial manualmente (más seguro)
        precios_historicos = []
        if resultados_historial:
            for fila in resultados_historial:
                observacion = fila[0]
                # Formato: "Precio actualizado de 50.00 a 45.00 Bs en Mercado"
                try:
                    if "de " in observacion and " a " in observacion:
                        # Extraer el precio "de X"
                        inicio = observacion.find("de ") + 3
                        fin = observacion.find(" a ", inicio)
                        precio_str = observacion[inicio:fin].strip()
                        precio = float(precio_str)
                        precios_historicos.append(precio)
                except (ValueError, IndexError) as e:
                    print(f"No se pudo extraer precio de: {observacion}")
                    continue
        
        # Lista completa de precios para análisis (históricos + actuales)
        todos_precios = precios_historicos + precios_actuales
        
        # Si solo hay precios actuales (sin historial), usar solo esos
        if not todos_precios:
            todos_precios = precios_actuales
        
        print(f"Debug: Precios históricos: {precios_historicos}")
        print(f"Debug: Precios actuales: {precios_actuales}")
        print(f"Debug: Total precios para análisis: {todos_precios}")
        
        # Calcular estadísticas con TODOS los precios (históricos + actuales)
        precio_promedio = statistics.mean(todos_precios)
        precio_minimo = min(todos_precios)
        precio_maximo = max(todos_precios)
        
        # Volatilidad (desviación estándar)
        if len(todos_precios) > 1:
            volatilidad = statistics.stdev(todos_precios)
            volatilidad_porcentaje = (volatilidad / precio_promedio) * 100
        else:
            volatilidad = 0
            volatilidad_porcentaje = 0
        
        # Determinar tendencia (comparar precio actual con promedio)
        if precio_actual < precio_promedio * 0.95:
            tendencia = "📉 BAJISTA (por debajo del promedio)"
            color_tendencia = "#10b981"
        elif precio_actual > precio_promedio * 1.05:
            tendencia = "📈 ALCISTA (por encima del promedio)"
            color_tendencia = "#dc2626"
        else:
            tendencia = "➡️ ESTABLE (cerca del promedio)"
            color_tendencia = "#f59e0b"
        
        # Actualizar tarjetas
        self.canvas.itemconfig("card_actual_valor", text=f"{precio_actual:.2f} Bs")
        self.canvas.itemconfig("card_promedio_valor", text=f"{precio_promedio:.2f} Bs")
        self.canvas.itemconfig("card_minimo_valor", text=f"{precio_minimo:.2f} Bs")
        self.canvas.itemconfig("card_maximo_valor", text=f"{precio_maximo:.2f} Bs")
        
        # Actualizar información adicional
        volatilidad_texto = f"{volatilidad:.2f} Bs ({volatilidad_porcentaje:.1f}%)"
        if volatilidad_porcentaje < 5:
            volatilidad_texto += " - BAJA volatilidad ✓"
        elif volatilidad_porcentaje < 15:
            volatilidad_texto += " - Volatilidad MODERADA"
        else:
            volatilidad_texto += " - ALTA volatilidad ⚠️"
        
        self.canvas.itemconfig("info_volatilidad", text=volatilidad_texto, fill="#e2e8f0")
        self.canvas.itemconfig("info_tendencia", text=tendencia, fill=color_tendencia)
        self.canvas.itemconfig("info_mercados", 
                              text=f"{len(set(mercados))} mercado(s): {', '.join(set(mercados))}", 
                              fill="#e2e8f0")
        self.canvas.itemconfig("info_fecha", 
                              text=fecha_reciente.strftime("%d/%m/%Y %H:%M"), 
                              fill="#e2e8f0")
        
        diferencia = precio_maximo - precio_minimo
        self.canvas.itemconfig("info_rango", 
                              text=f"{diferencia:.2f} Bs (diferencia entre min y max)", 
                              fill="#e2e8f0")
        
        # Guardar datos para los gráficos
        self.datos_analisis = {
            'id_producto': id_producto,
            'nombre_producto': self.combo_producto.get(),
            'precios_historicos': precios_historicos,
            'precios_actuales': precios_actuales,
            'todos_precios': todos_precios,
            'mercados': mercados,
            'precio_actual': precio_actual,
            'precio_promedio': precio_promedio,
            'precio_minimo': precio_minimo,
            'precio_maximo': precio_maximo
        }
        
        # Habilitar botón de gráfico
        self.btn_grafico_evolucion.config(state=tk.NORMAL)
        
        # Mensaje de éxito
        messagebox.showinfo("Análisis Completo", 
            f"✓ Análisis estadístico completado\n\n"
            f"Producto: {self.combo_producto.get()}\n"
            f"Precios analizados: {len(todos_precios)}\n"
            f"  • Históricos: {len(precios_historicos)}\n"
            f"  • Actuales: {len(precios_actuales)}")
    
    def mostrar_grafico_evolucion(self):
        """Genera y muestra el gráfico de evolución de precios en el tiempo"""
        if not self.datos_analisis:
            messagebox.showwarning("Advertencia", "Primero debe analizar un producto")
            return
        
        id_producto = self.datos_analisis['id_producto']
        nombre_producto = self.datos_analisis['nombre_producto']
        
        # Obtener datos temporales del historial con TODAS las transiciones
        query_temporal = """
        SELECT observaciones, fecha_registro
        FROM historial_p
        WHERE id_producto = %s 
        AND observaciones LIKE 'Precio actualizado%%'
        ORDER BY fecha_registro ASC;
        """
        
        historial = execute_query(query_temporal, (id_producto,), fetch=True)
        
        # Obtener precios actuales con fechas
        query_actuales = """
        SELECT precio, fecha_actualizacion
        FROM oferta
        WHERE id_producto = %s
        ORDER BY fecha_actualizacion ASC;
        """
        
        actuales = execute_query(query_actuales, (id_producto,), fetch=True)
        
        # Construir serie temporal
        puntos_temporales = []  # Lista de (fecha, precio)
        
        # Procesar historial - SOLO el precio NUEVO (el "a Y")
        for fila in historial:
            observacion = fila[0]
            fecha = fila[1]
            
            try:
                # Extraer SOLO el precio nuevo (el "a Y")
                if " a " in observacion and " Bs" in observacion:
                    inicio_nuevo = observacion.find(" a ") + 3
                    fin_nuevo = observacion.find(" Bs", inicio_nuevo)
                    precio_nuevo_str = observacion[inicio_nuevo:fin_nuevo].strip()
                    precio_nuevo = float(precio_nuevo_str)
                    
                    puntos_temporales.append((fecha, precio_nuevo))
            except (ValueError, IndexError) as e:
                print(f"Error procesando: {observacion}")
                continue
        
        # Agregar precios actuales (pueden ser actualizaciones sin historial)
        for fila in actuales:
            precio = float(fila[0])
            fecha = fila[1]
            puntos_temporales.append((fecha, precio))
        
        # Verificar que hay datos suficientes
        if len(puntos_temporales) < 1:
            messagebox.showinfo("Información", 
                "No hay suficientes datos temporales para generar el gráfico.\n\n"
                "Actualice los precios varias veces para ver la evolución.")
            return
        
        # Ordenar por fecha y eliminar duplicados (mismo timestamp)
        puntos_temporales = sorted(set(puntos_temporales), key=lambda x: x[0])
        
        # Si hay muy pocos puntos únicos
        if len(puntos_temporales) < 2:
            messagebox.showinfo("Información", 
                "No hay suficientes cambios de precio para mostrar evolución.\n\n"
                f"Datos encontrados: {len(puntos_temporales)} punto(s)\n"
                "Se necesitan al menos 2 actualizaciones en momentos diferentes.")
            return
        
        fechas_ordenadas = [p[0] for p in puntos_temporales]
        precios_ordenados = [p[1] for p in puntos_temporales]
        
        print(f"Debug - Puntos en el gráfico: {len(puntos_temporales)}")
        for fecha, precio in puntos_temporales:
            print(f"  {fecha.strftime('%d/%m/%Y %H:%M:%S')} → {precio:.2f} Bs")
        
        # Crear ventana para el gráfico
        ventana_grafico = tk.Toplevel(self.frame_principal)
        ventana_grafico.title(f"Evolución de Precios - {nombre_producto}")
        ventana_grafico.geometry("900x600")
        ventana_grafico.configure(bg="#0a0f1e")
        
        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0a0f1e')
        ax.set_facecolor('#1e293b')
        
        # Configurar gráfico
        ax.plot(fechas_ordenadas, precios_ordenados, 
               color='#06b6d4', linewidth=2, marker='o', markersize=6,
               markerfacecolor='#06b6d4', markeredgecolor='white', markeredgewidth=1.5)
        
        # Títulos y etiquetas
        ax.set_title(f'Evolución de Precios - {nombre_producto}', 
                    fontsize=16, fontweight='bold', color='#e2e8f0', pad=20)
        ax.set_xlabel('Fecha', fontsize=12, color='#94a3b8')
        ax.set_ylabel('Precio (Bs)', fontsize=12, color='#94a3b8')
        
        # Configurar colores del grid
        ax.grid(True, alpha=0.2, color='#475569', linestyle='--')
        ax.tick_params(colors='#94a3b8')
        
        # Rotar fechas para mejor legibilidad
        plt.xticks(rotation=45, ha='right')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Agregar línea del promedio
        promedio = self.datos_analisis['precio_promedio']
        ax.axhline(y=promedio, color='#10b981', linestyle='--', linewidth=2, 
                  label=f'Promedio: {promedio:.2f} Bs', alpha=0.7)
        ax.legend(loc='best', facecolor='#1e293b', edgecolor='#475569', 
                 labelcolor='#e2e8f0')
        
        # Incrustar gráfico en ventana Tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para botones
        frame_botones = tk.Frame(ventana_grafico, bg="#0a0f1e")
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        # Botón para guardar gráfico
        btn_guardar = tk.Button(
            frame_botones,
            text="💾 Guardar Gráfico",
            font=("Arial", 10, "bold"),
            bg="#10b981", fg="white",
            activebackground="#059669",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6,
            command=lambda: self.guardar_grafico(fig, nombre_producto, "evolucion")
        )
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Botón cerrar
        btn_cerrar = tk.Button(
            frame_botones,
            text="✕ Cerrar",
            font=("Arial", 10, "bold"),
            bg="#475569", fg="white",
            activebackground="#334155",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6,
            command=ventana_grafico.destroy
        )
        btn_cerrar.pack(side=tk.RIGHT, padx=5)
    
    def guardar_grafico(self, figura, nombre_producto, tipo_grafico):
        """Guarda el gráfico como imagen PNG"""
        # Limpiar nombre del producto para nombre de archivo
        nombre_limpio = nombre_producto.replace(" ", "_").replace("(", "").replace(")", "")
        nombre_archivo = f"grafico_{tipo_grafico}_{nombre_limpio}.png"
        
        try:
            figura.savefig(nombre_archivo, dpi=300, facecolor='#0a0f1e', 
                          edgecolor='none', bbox_inches='tight')
            messagebox.showinfo("Éxito", 
                f"Gráfico guardado correctamente:\n{nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el gráfico:\n{e}")
    
    def get_id_from_combo(self, combo, diccionario):
        """Obtiene el ID a partir del valor seleccionado en el combobox"""
        valor_seleccionado = combo.get()
        for id_item, nombre in diccionario.items():
            if nombre == valor_seleccionado:
                return id_item
        return None
    
    def crear_boton_volver(self):
        """Crea el botón de volver"""
        self.btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Menú",
            font=("Arial", 11, "bold"),
            bg="#475569", fg="white",
            activebackground="#334155",
            relief=tk.FLAT, cursor="hand2",
            padx=25, pady=8,
            command=self.volver
        )
        self.btn_volver.place(x=380, y=540)
    
    def volver(self):
        """Vuelve al menú principal"""
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()