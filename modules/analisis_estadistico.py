import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class AnalisisEstadistico:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        self.df_productos = None
        self.datos_analisis = None
        
        self.canvas.delete("all")
        self.cargar_productos()
        self.crear_interfaz()
    
    def cargar_productos(self):
        query = """
        SELECT DISTINCT p.id_producto, p.nombre_producto, p.unidad_medida 
        FROM producto p
        INNER JOIN oferta o ON p.id_producto = o.id_producto
        WHERE p.activo = TRUE
        ORDER BY p.nombre_producto;
        """
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            self.df_productos = pd.DataFrame(resultados, columns=['id', 'nombre', 'unidad'])
            self.df_productos['display'] = (self.df_productos['nombre'] + ' (' + 
                                            self.df_productos['unidad'] + ')')
        
        print(f"✓ Productos con ofertas: {len(self.df_productos) if self.df_productos is not None else 0}")
    
    def crear_interfaz(self):
        self.canvas.create_text(450, 30, text="ANÁLISIS ESTADÍSTICO", 
                               font=("Arial", 20, "bold"), fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, 
                               text="Estudio de tendencias, volatilidad y patrones de precios", 
                               font=("Arial", 11), fill="#94a3b8")
        
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        self.canvas.create_rectangle(50, 90, 850, 160, fill="#1e293b", outline="#8b5cf6", width=2)
        
        self.canvas.create_text(450, 105, text="SELECCIONAR PRODUCTO PARA ANALIZAR", 
                               font=("Arial", 12, "bold"), fill="#8b5cf6")
        
        if self.df_productos is None or len(self.df_productos) == 0:
            self.canvas.create_text(450, 130, 
                                   text="⚠️  No hay productos con ofertas registradas", 
                                   font=("Arial", 11, "bold"), fill="#f59e0b")
            self.crear_boton_volver()
            return
        
        self.canvas.create_text(310, 135, text="Producto:", font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="e")
        
        self.combo_producto = ttk.Combobox(self.frame_principal,
            values=self.df_productos['display'].tolist(),
            state="readonly", font=("Arial", 10), width=32)
        self.combo_producto.place(x=320, y=125)
        
        self.btn_analizar = tk.Button(self.frame_principal, text="📊 Analizar",
            font=("Arial", 10, "bold"), bg="#8b5cf6", fg="white",
            activebackground="#7c3aed", relief=tk.FLAT, cursor="hand2",
            padx=20, pady=6, command=self.analizar_producto)
        self.btn_analizar.place(x=600, y=125)
        
        self.canvas.create_rectangle(50, 175, 850, 270, fill="#1e293b", outline="#10b981", width=2)
        
        self.canvas.create_text(450, 190, text="ESTADÍSTICAS PRINCIPALES", 
                               font=("Arial", 11, "bold"), fill="#10b981")
        
        card_config = np.array([
            ['actual', '💰 Precio Actual', '#3b82f6'],
            ['promedio', '📊 Precio Promedio', '#10b981'],
            ['minimo', '⬇️ Precio Mínimo', '#06b6d4'],
            ['maximo', '⬆️ Precio Máximo', '#dc2626']
        ], dtype=object)
        
        card_width = 155
        card_height = 50
        card_y = 225
        total_width = 4 * card_width + 3 * 25
        start_x = (900 - total_width) / 2 + card_width / 2
        spacing = card_width + 25
        
        for i, (key, titulo, color) in enumerate(card_config):
            x = start_x + i * spacing
            self.crear_tarjeta_stat(x, card_y, card_width, card_height, 
                                   titulo, "---", color, f"card_{key}")
        
        self.canvas.create_rectangle(50, 285, 850, 350, fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(450, 300, text="VISUALIZACIÓN DE DATOS", 
                               font=("Arial", 11, "bold"), fill="#06b6d4")
        
        self.btn_grafico_evolucion = tk.Button(self.frame_principal,
            text="📈 Ver Evolución de Precios", font=("Arial", 10, "bold"),
            bg="#06b6d4", fg="white", activebackground="#0891b2",
            relief=tk.FLAT, cursor="hand2", padx=25, pady=8,
            state=tk.DISABLED, command=self.mostrar_grafico_evolucion)
        self.btn_grafico_evolucion.place(x=345, y=318)
        
        self.canvas.create_rectangle(50, 365, 850, 530, fill="#1e293b", outline="#f59e0b", width=2)
        
        self.canvas.create_text(450, 380, text="INFORMACIÓN DETALLADA", 
                               font=("Arial", 11, "bold"), fill="#f59e0b")
        
        info_config = np.array([
            ['volatilidad', 410, '📉 Volatilidad:', 'Seleccione un producto'],
            ['tendencia', 436, '📈 Tendencia:', '---'],
            ['mercados', 462, '🏪 Mercados:', '---'],
            ['fecha', 488, '🕐 Actualización:', '---'],
            ['rango', 514, '💹 Rango:', '---']
        ], dtype=object)
        
        label_x = 100
        value_x = 250
        
        for key, y, label_text, default_value in info_config:
            self.canvas.create_text(label_x, int(y), text=label_text, 
                                   font=("Arial", 10, "bold"), fill="#e2e8f0", anchor="w")
            self.canvas.create_text(value_x, int(y), text=default_value, 
                                   font=("Arial", 9), fill="#94a3b8", anchor="w",
                                   tags=f"info_{key}", width=550)
        
        self.crear_boton_volver()
    
    def crear_tarjeta_stat(self, x, y, width, height, titulo, valor, color, tag):
        self.canvas.create_rectangle(x - width/2, y - height/2, 
                                     x + width/2, y + height/2,
                                     fill="#0f172a", outline=color, width=2,
                                     tags=f"{tag}_bg")
        
        self.canvas.create_text(x, y - 13, text=titulo, font=("Arial", 9, "bold"), 
                               fill=color, tags=f"{tag}_titulo")
        
        self.canvas.create_text(x, y + 10, text=valor, font=("Arial", 15, "bold"), 
                               fill="#e2e8f0", tags=f"{tag}_valor")
    
    def analizar_producto(self):
        if not self.combo_producto.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        id_producto = self.get_id_from_combo()
        
        query_actual = """
        SELECT o.precio, o.fecha_actualizacion, m.nombre_mercado
        FROM oferta o
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        WHERE o.id_producto = %s
        ORDER BY o.fecha_actualizacion DESC;
        """
        
        resultados_actuales = execute_query(query_actual, (id_producto,), fetch=True)
        
        if not resultados_actuales:
            messagebox.showinfo("Sin datos", "No hay ofertas registradas para este producto")
            return
        
        df_actuales = pd.DataFrame(resultados_actuales, columns=['precio', 'fecha', 'mercado'])
        df_actuales['precio'] = pd.to_numeric(df_actuales['precio'])
        
        precios_actuales = df_actuales['precio'].tolist()
        mercados = df_actuales['mercado'].tolist()
        fecha_reciente = df_actuales.iloc[0]['fecha']
        precio_actual = float(df_actuales.iloc[0]['precio'])
        
        query_historial = """
        SELECT observaciones, fecha_registro
        FROM historial_p
        WHERE id_producto = %s 
        AND observaciones LIKE 'Precio actualizado%%'
        ORDER BY fecha_registro DESC;
        """
        
        resultados_historial = execute_query(query_historial, (id_producto,), fetch=True)
        
        precios_historicos = []
        if resultados_historial:
            df_historial = pd.DataFrame(resultados_historial, columns=['observacion', 'fecha'])
            
            for _, row in df_historial.iterrows():
                observacion = row['observacion']
                try:
                    if "de " in observacion and " a " in observacion:
                        inicio = observacion.find("de ") + 3
                        fin = observacion.find(" a ", inicio)
                        precio_str = observacion[inicio:fin].strip()
                        precio = float(precio_str)
                        precios_historicos.append(precio)
                except (ValueError, IndexError):
                    continue
        
        todos_precios = precios_historicos + precios_actuales
        
        if not todos_precios:
            todos_precios = precios_actuales
        
        precios_array = np.array(todos_precios)
        precio_promedio = np.mean(precios_array)
        precio_minimo = np.min(precios_array)
        precio_maximo = np.max(precios_array)
        
        if len(precios_array) > 1:
            volatilidad = np.std(precios_array)
            volatilidad_porcentaje = (volatilidad / precio_promedio) * 100
        else:
            volatilidad = 0
            volatilidad_porcentaje = 0
        
        if precio_actual < precio_promedio * 0.95:
            tendencia = "BAJISTA (por debajo del promedio)"
            color_tendencia = "#10b981"
        elif precio_actual > precio_promedio * 1.05:
            tendencia = "ALCISTA (por encima del promedio)"
            color_tendencia = "#dc2626"
        else:
            tendencia = "ESTABLE (cerca del promedio)"
            color_tendencia = "#f59e0b"
        
        self.canvas.itemconfig("card_actual_valor", text=f"{precio_actual:.2f} Bs")
        self.canvas.itemconfig("card_promedio_valor", text=f"{precio_promedio:.2f} Bs")
        self.canvas.itemconfig("card_minimo_valor", text=f"{precio_minimo:.2f} Bs")
        self.canvas.itemconfig("card_maximo_valor", text=f"{precio_maximo:.2f} Bs")
        
        volatilidad_texto = f"{volatilidad:.2f} Bs ({volatilidad_porcentaje:.1f}%)"
        if volatilidad_porcentaje < 5:
            volatilidad_texto += " - BAJA volatilidad ✓"
        elif volatilidad_porcentaje < 15:
            volatilidad_texto += " - Volatilidad MODERADA"
        else:
            volatilidad_texto += " - ALTA volatilidad ⚠️"
        
        self.canvas.itemconfig("info_volatilidad", text=volatilidad_texto, fill="#e2e8f0")
        self.canvas.itemconfig("info_tendencia", text=tendencia, fill=color_tendencia)
        
        mercados_unicos = list(set(mercados))
        mercados_texto = f"{len(mercados_unicos)} mercado(s): {', '.join(mercados_unicos[:3])}"
        if len(mercados_unicos) > 3:
            mercados_texto += "..."
        
        self.canvas.itemconfig("info_mercados", text=mercados_texto, fill="#e2e8f0")
        self.canvas.itemconfig("info_fecha", 
                              text=fecha_reciente.strftime("%d/%m/%Y %H:%M"), 
                              fill="#e2e8f0")
        
        diferencia = precio_maximo - precio_minimo
        self.canvas.itemconfig("info_rango", 
                              text=f"{diferencia:.2f} Bs (diferencia min-max)", 
                              fill="#e2e8f0")
        
        self.datos_analisis = {
            'id_producto': int(id_producto),
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
        
        self.btn_grafico_evolucion.config(state=tk.NORMAL)
        alertas = self.generar_alertas_automaticas(
            id_producto, 
            self.combo_producto.get(),
            precio_actual,
            precio_promedio,
            volatilidad_porcentaje
        )
    
        # Mostrar alertas generadas
        if alertas:
            alertas_texto = "\n\n".join([msg for _, msg in alertas])
            messagebox.showinfo("⚠️ Alertas Generadas", 
                f"✓ Análisis completado\n\n"
                f"Se generaron {len(alertas)} alerta(s):\n\n{alertas_texto}")
        else:
            messagebox.showinfo("Análisis Completo", 
                f"✓ Análisis estadístico completado\n\n"
                f"No se detectaron condiciones especiales.")
        messagebox.showinfo("Análisis Completo", 
            f"✓ Análisis estadístico completado\n\n"
            f"Producto: {self.combo_producto.get()}\n"
            f"Precios analizados: {len(todos_precios)}\n"
            f"  • Históricos: {len(precios_historicos)}\n"
            f"  • Actuales: {len(precios_actuales)}")
    
    def mostrar_grafico_evolucion(self):
        if not self.datos_analisis:
            messagebox.showwarning("Advertencia", "Primero debe analizar un producto")
            return
        
        id_producto = self.datos_analisis['id_producto']
        nombre_producto = self.datos_analisis['nombre_producto']
        
        query_temporal = """
        SELECT observaciones, fecha_registro
        FROM historial_p
        WHERE id_producto = %s 
        AND observaciones LIKE 'Precio actualizado%%'
        ORDER BY fecha_registro ASC;
        """
        
        historial = execute_query(query_temporal, (id_producto,), fetch=True)
        
        query_actuales = """
        SELECT precio, fecha_actualizacion
        FROM oferta
        WHERE id_producto = %s
        ORDER BY fecha_actualizacion ASC;
        """
        
        actuales = execute_query(query_actuales, (id_producto,), fetch=True)
        
        puntos_temporales = []
        
        if historial:
            df_hist = pd.DataFrame(historial, columns=['observacion', 'fecha'])
            
            for _, row in df_hist.iterrows():
                observacion = row['observacion']
                fecha = row['fecha']
                
                try:
                    if " a " in observacion and " Bs" in observacion:
                        inicio_nuevo = observacion.find(" a ") + 3
                        fin_nuevo = observacion.find(" Bs", inicio_nuevo)
                        precio_nuevo_str = observacion[inicio_nuevo:fin_nuevo].strip()
                        precio_nuevo = float(precio_nuevo_str)
                        puntos_temporales.append((fecha, precio_nuevo))
                except (ValueError, IndexError):
                    continue
        
        if actuales:
            df_actuales = pd.DataFrame(actuales, columns=['precio', 'fecha'])
            for _, row in df_actuales.iterrows():
                puntos_temporales.append((row['fecha'], float(row['precio'])))
        
        if len(puntos_temporales) < 1:
            messagebox.showinfo("Información", 
                "No hay suficientes datos temporales para generar el gráfico.\n\n"
                "Actualice los precios varias veces para ver la evolución.")
            return
        
        puntos_temporales = sorted(set(puntos_temporales), key=lambda x: x[0])
        
        if len(puntos_temporales) < 2:
            messagebox.showinfo("Información", 
                "No hay suficientes cambios de precio para mostrar evolución.\n\n"
                f"Datos encontrados: {len(puntos_temporales)} punto(s)\n"
                "Se necesitan al menos 2 actualizaciones en momentos diferentes.")
            return
        
        df_puntos = pd.DataFrame(puntos_temporales, columns=['fecha', 'precio'])
        fechas_ordenadas = df_puntos['fecha'].tolist()
        precios_ordenados = df_puntos['precio'].tolist()
        
        ventana_grafico = tk.Toplevel(self.frame_principal)
        ventana_grafico.title(f"Evolución de Precios - {nombre_producto}")
        ventana_grafico.geometry("900x600")
        ventana_grafico.configure(bg="#0a0f1e")
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0a0f1e')
        ax.set_facecolor('#1e293b')
        
        ax.plot(fechas_ordenadas, precios_ordenados, 
               color='#06b6d4', linewidth=2, marker='o', markersize=6,
               markerfacecolor='#06b6d4', markeredgecolor='white', markeredgewidth=1.5)
        
        ax.set_title(f'Evolución de Precios - {nombre_producto}', 
                    fontsize=16, fontweight='bold', color='#e2e8f0', pad=20)
        ax.set_xlabel('Fecha', fontsize=12, color='#94a3b8')
        ax.set_ylabel('Precio (Bs)', fontsize=12, color='#94a3b8')
        
        ax.grid(True, alpha=0.2, color='#475569', linestyle='--')
        ax.tick_params(colors='#94a3b8')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        promedio = self.datos_analisis['precio_promedio']
        ax.axhline(y=promedio, color='#10b981', linestyle='--', linewidth=2, 
                  label=f'Promedio: {promedio:.2f} Bs', alpha=0.7)
        ax.legend(loc='best', facecolor='#1e293b', edgecolor='#475569', 
                 labelcolor='#e2e8f0')
        
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_botones = tk.Frame(ventana_grafico, bg="#0a0f1e")
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        btn_guardar = tk.Button(frame_botones, text="💾 Guardar Gráfico",
            font=("Arial", 10, "bold"), bg="#10b981", fg="white",
            activebackground="#059669", relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6,
            command=lambda: self.guardar_grafico(fig, nombre_producto, "evolucion"))
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        btn_cerrar = tk.Button(frame_botones, text="✕ Cerrar",
            font=("Arial", 10, "bold"), bg="#475569", fg="white",
            activebackground="#334155", relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6, command=ventana_grafico.destroy)
        btn_cerrar.pack(side=tk.RIGHT, padx=5)
    def guardar_grafico(self, figura, nombre_producto, tipo_grafico):
        nombre_limpio = nombre_producto.replace(" ", "_").replace("(", "").replace(")", "")
        nombre_archivo = f"grafico_{tipo_grafico}_{nombre_limpio}.png"
        
        try:
            figura.savefig(nombre_archivo, dpi=300, facecolor='#0a0f1e', 
                          edgecolor='none', bbox_inches='tight')
            messagebox.showinfo("Éxito", 
                f"Gráfico guardado correctamente:\n{nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el gráfico:\n{e}")
    
    def get_id_from_combo(self):
        if self.df_productos is None:
            return None
        valor_seleccionado = self.combo_producto.get()
        match = self.df_productos[self.df_productos['display'] == valor_seleccionado]
        return int(match.iloc[0]['id']) if len(match) > 0 else None
    def generar_alertas_automaticas(self, id_producto, nombre_producto, precio_actual, 
                                precio_promedio, volatilidad_porcentaje):
        """Genera alertas automáticas basadas en el análisis"""
    
        alertas_generadas = []
    
        # ALERTA 1: Precio muy por debajo del promedio (oportunidad de compra)
        if precio_actual < precio_promedio * 0.85:  # 15% o más bajo
            diferencia = ((precio_promedio - precio_actual) / precio_promedio) * 100
            mensaje = (f"🟢 OPORTUNIDAD DE COMPRA: {nombre_producto} está {diferencia:.1f}% "
                    f"por debajo del precio promedio ({precio_actual:.2f} Bs vs {precio_promedio:.2f} Bs)")
            self.insertar_alerta(1, mensaje, "precio_bajo", id_producto)
            alertas_generadas.append(("precio_bajo", mensaje))
    
        # ALERTA 2: Precio muy por encima del promedio (advertencia)
        elif precio_actual > precio_promedio * 1.15:  # 15% o más alto
            diferencia = ((precio_actual - precio_promedio) / precio_promedio) * 100
            mensaje = (f"🔴 PRECIO ELEVADO: {nombre_producto} está {diferencia:.1f}% "
                    f"por encima del precio promedio ({precio_actual:.2f} Bs vs {precio_promedio:.2f} Bs)")
            self.insertar_alerta(1, mensaje, "precio_alto", id_producto)
            alertas_generadas.append(("precio_alto", mensaje))
    
        # ALERTA 3: Alta volatilidad
        if volatilidad_porcentaje > 20:
            mensaje = (f"⚠️ ALTA VOLATILIDAD: {nombre_producto} presenta variaciones de "
                    f"{volatilidad_porcentaje:.1f}%, lo que indica precios inestables")
            self.insertar_alerta(1, mensaje, "volatilidad_alta", id_producto)
            alertas_generadas.append(("volatilidad", mensaje))
    
        # ALERTA 4: Precio estable (información positiva)
        elif volatilidad_porcentaje < 5:
            mensaje = (f"✅ PRECIO ESTABLE: {nombre_producto} tiene baja volatilidad "
                    f"({volatilidad_porcentaje:.1f}%), ideal para planificación")
            self.insertar_alerta(1, mensaje, "precio_estable", id_producto)
            alertas_generadas.append(("estable", mensaje))
    
        return alertas_generadas

    def insertar_alerta(self, id_usuario, mensaje, tipo_alerta, id_producto=None):
        """Inserta una alerta en la base de datos"""
        query = """
        INSERT INTO alerta (id_usuario, mensaje, tipo_alerta, leida)
        VALUES (%s, %s, %s, FALSE);
        """
        execute_query(query, (id_usuario, mensaje, tipo_alerta))
    
    def crear_boton_volver(self):
        self.btn_volver = tk.Button(self.frame_principal, text="← Volver al Menú",
            font=("Arial", 11, "bold"), bg="#475569", fg="white",
            activebackground="#334155", relief=tk.FLAT, cursor="hand2",
            padx=25, pady=8, command=self.volver)
        self.btn_volver.place(x=380, y=555)
    
    def volver(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()