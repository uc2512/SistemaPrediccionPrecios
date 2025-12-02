import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query
from datetime import datetime, timedelta
import math
import pandas as pd
import numpy as np

class GestionPredicciones:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        self.df_productos = None
        self.df_mercados = None
        
        self.canvas.delete("all")
        self.cargar_datos_iniciales()
        self.crear_interfaz_principal()
    
    def cargar_datos_iniciales(self):
        query_productos = """
        SELECT id_producto, nombre_producto, unidad_medida
        FROM producto WHERE activo = TRUE ORDER BY nombre_producto;
        """
        productos = execute_query(query_productos, fetch=True)
        if productos:
            self.df_productos = pd.DataFrame(productos, columns=['id', 'nombre', 'unidad'])
            self.df_productos['display'] = (self.df_productos['nombre'] + ' (' + 
                                            self.df_productos['unidad'] + ')')
        
        query_mercados = """
        SELECT id_mercado, nombre_mercado, ciudad
        FROM mercado WHERE activo = TRUE ORDER BY nombre_mercado;
        """
        mercados = execute_query(query_mercados, fetch=True)
        if mercados:
            self.df_mercados = pd.DataFrame(mercados, columns=['id', 'nombre', 'ciudad'])
            self.df_mercados['display'] = self.df_mercados.apply(
                lambda x: f"{x['nombre']}" + (f" - {x['ciudad']}" if pd.notna(x['ciudad']) else ""),
                axis=1
            )
    
    def crear_interfaz_principal(self):
        self.canvas.create_text(450, 30, text="🔮 PREDICCIONES DE PRECIOS",
            font=("Arial", 20, "bold"), fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, text="Proyección inteligente basada en datos históricos",
            font=("Arial", 11), fill="#94a3b8")
        
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        if self.df_productos is None or len(self.df_productos) == 0:
            self.mostrar_sin_datos()
            return
        
        self.canvas.create_text(450, 110, text="MODELOS DE PREDICCIÓN DISPONIBLES",
            font=("Arial", 13, "bold"), fill="#f59e0b")
        
        modelos_config = np.array([
            [240, 170, '📈', 'Tendencia Lineal', 'Predicción simple basada en regresión lineal', '#10b981'],
            [660, 170, '📊', 'Media Móvil', 'Promedio ponderado de precios recientes', '#3b82f6'],
            [240, 250, '🔄', 'Análisis Estacional', 'Detecta patrones que se repiten en el tiempo', '#8b5cf6'],
            [660, 250, '📉', 'Suavizado Exponencial', 'Mayor peso a datos más recientes', '#f59e0b']
        ], dtype=object)
        
        comandos = [self.prediccion_lineal, self.prediccion_media_movil,
                   self.prediccion_estacional, self.prediccion_exponencial]
        
        for i, (x, y, icono, titulo, desc, color) in enumerate(modelos_config):
            self.crear_tarjeta_modelo(int(x), int(y), icono, titulo, desc, color, comandos[i])
        
        self.canvas.create_rectangle(50, 380, 850, 500, fill="#1e293b", outline="#334155", width=2)
        
        self.canvas.create_text(450, 400, text="⚙️ OPCIONES AVANZADAS",
            font=("Arial", 12, "bold"), fill="#64748b")
        
        opciones_config = np.array([
            [200, 435, '🎯 Comparar Modelos', 'Evalúa qué modelo predice mejor', '#06b6d4'],
            [450, 435, '🔍 Detección de Anomalías', 'Identifica picos inusuales', '#ec4899'],
            [700, 435, '📊 Historial vs Predicción', 'Gráfico comparativo completo', '#8b5cf6']
        ], dtype=object)
        
        comandos_avanzados = [self.comparar_modelos, self.detectar_anomalias, self.grafico_comparativo]
        
        for i, (x, y, titulo, desc, color) in enumerate(opciones_config):
            self.crear_boton_opcion(int(x), int(y), titulo, desc, color, comandos_avanzados[i])
        
        self.canvas.create_rectangle(50, 515, 850, 545, fill="#1e293b", outline="#334155", width=1)
        
        self.mostrar_estadisticas_prediccion()
        
        self.btn_volver = tk.Button(self.frame_principal, text="← Volver al Menú",
            font=("Arial", 11, "bold"), bg="#475569", fg="white",
            activebackground="#334155", relief=tk.FLAT, cursor="hand2",
            padx=20, pady=8, command=self.volver)
        self.btn_volver.place(x=380, y=565)
    
    def crear_tarjeta_modelo(self, x, y, icono, titulo, descripcion, color, comando):
        tag = f"modelo_{x}_{y}"
        
        rect_id = self.canvas.create_rectangle(x-180, y-25, x+180, y+25,
            fill="#0f172a", outline=color, width=2, tags=tag)
        
        self.canvas.create_text(x-140, y, text=icono, font=("Arial", 20),
            fill=color, tags=tag)
        
        self.canvas.create_text(x-20, y-8, text=titulo, font=("Arial", 11, "bold"),
            fill="#e2e8f0", anchor="w", tags=tag)
        
        self.canvas.create_text(x-20, y+10, text=descripcion, font=("Arial", 8),
            fill="#64748b", anchor="w", tags=tag)
        
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: comando())
        self.canvas.tag_bind(tag, "<Enter>", 
            lambda e: self.canvas.itemconfig(rect_id, fill="#1e3a5f", width=3))
        self.canvas.tag_bind(tag, "<Leave>", 
            lambda e: self.canvas.itemconfig(rect_id, fill="#0f172a", width=2))
        self.canvas.tag_bind(tag, "<Enter>", 
            lambda e: self.canvas.config(cursor="hand2"), add="+")
        self.canvas.tag_bind(tag, "<Leave>", 
            lambda e: self.canvas.config(cursor=""), add="+")
    
    def crear_boton_opcion(self, x, y, titulo, descripcion, color, comando):
        tag = f"opcion_{x}_{y}"
        
        rect_id = self.canvas.create_rectangle(x-110, y-22, x+110, y+22,
            fill="#0f172a", outline=color, width=1, tags=tag)
        
        self.canvas.create_text(x, y-8, text=titulo, font=("Arial", 9, "bold"),
            fill="#e2e8f0", tags=tag)
        
        self.canvas.create_text(x, y+8, text=descripcion, font=("Arial", 7),
            fill="#64748b", tags=tag)
        
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: comando())
        self.canvas.tag_bind(tag, "<Enter>", 
            lambda e: self.canvas.itemconfig(rect_id, outline=color, width=2))
        self.canvas.tag_bind(tag, "<Leave>", 
            lambda e: self.canvas.itemconfig(rect_id, outline=color, width=1))
        self.canvas.tag_bind(tag, "<Enter>", 
            lambda e: self.canvas.config(cursor="hand2"), add="+")
        self.canvas.tag_bind(tag, "<Leave>", 
            lambda e: self.canvas.config(cursor=""), add="+")
    
    def mostrar_estadisticas_prediccion(self):
        query = "SELECT COUNT(*) FROM historial_p;"
        result = execute_query(query, fetch=True)
        num_historial = result[0][0] if result else 0
        
        query2 = "SELECT COUNT(*) FROM oferta;"
        result2 = execute_query(query2, fetch=True)
        num_ofertas = result2[0][0] if result2 else 0
        
        if num_historial < 5:
            capacidad = "⚠️ Datos insuficientes"
            color = "#f59e0b"
        elif num_historial < 20:
            capacidad = "✓ Predicción básica disponible"
            color = "#3b82f6"
        else:
            capacidad = "✓ Predicción avanzada disponible"
            color = "#10b981"
        
        stats_text = (f"📊 Sistema: {num_ofertas} ofertas actuales | "
                     f"{num_historial} registros históricos | {capacidad}")
        
        self.canvas.create_text(450, 530, text=stats_text, font=("Arial", 9), fill=color)
    
    def mostrar_sin_datos(self):
        self.canvas.create_rectangle(200, 200, 700, 350, fill="#1e293b", outline="#f59e0b", width=2)
        
        self.canvas.create_text(450, 240, text="⚠️ DATOS INSUFICIENTES",
            font=("Arial", 16, "bold"), fill="#f59e0b")
        
        mensajes = [
            "Para realizar predicciones necesitas:",
            "• Al menos 1 producto registrado",
            "• Al menos 5 registros de precios históricos"
        ]
        
        for i, msg in enumerate(mensajes):
            self.canvas.create_text(450, 280 + i*25, text=msg,
                font=("Arial", 11 if i == 0 else 10),
                fill="#94a3b8" if i == 0 else "#e2e8f0", anchor="center")
        
        btn_volver = tk.Button(self.frame_principal, text="← Volver al Menú",
            font=("Arial", 11, "bold"), bg="#475569", fg="white",
            command=self.volver, padx=20, pady=8)
        btn_volver.place(x=380, y=400)
    
    def obtener_datos_historicos(self, id_producto, id_mercado=None):
        if id_mercado is None:
            query = """
            WITH todos_precios AS (
                SELECT 
                    h.fecha_registro::timestamp as fecha_completa,
                    NULLIF(
                        REGEXP_REPLACE(
                            SUBSTRING(h.observaciones FROM 'a ([0-9]+\\.?[0-9]*) Bs'),
                            '[^0-9.]', '', 'g'
                        ),
                        ''
                    )::DECIMAL(10,2) as precio_nuevo,
                    NULLIF(
                        REGEXP_REPLACE(
                            SUBSTRING(h.observaciones FROM 'de ([0-9]+\\.?[0-9]*) a'),
                            '[^0-9.]', '', 'g'
                        ),
                        ''
                    )::DECIMAL(10,2) as precio_viejo
                FROM historial_p h
                WHERE h.id_producto = %s
                  AND h.fecha_registro >= CURRENT_DATE - INTERVAL '90 days'
                  AND h.observaciones IS NOT NULL
            ),
            precios_expandidos AS (
                SELECT fecha_completa, precio_viejo as precio
                FROM todos_precios
                WHERE precio_viejo IS NOT NULL
                
                UNION ALL
                
                SELECT fecha_completa, precio_nuevo as precio
                FROM todos_precios
                WHERE precio_nuevo IS NOT NULL
                
                UNION ALL
                
                SELECT o.fecha_actualizacion, o.precio
                FROM oferta o
                WHERE o.id_producto = %s
            )
            SELECT fecha_completa::date as fecha, precio
            FROM precios_expandidos
            WHERE precio > 0
            ORDER BY fecha_completa;
            """
            params = (id_producto, id_producto)
        else:
            query = """
            WITH todos_precios AS (
                SELECT 
                    h.fecha_registro::timestamp as fecha_completa,
                    NULLIF(
                        REGEXP_REPLACE(
                            SUBSTRING(h.observaciones FROM 'a ([0-9]+\\.?[0-9]*) Bs'),
                            '[^0-9.]', '', 'g'
                        ),
                        ''
                    )::DECIMAL(10,2) as precio_nuevo,
                    NULLIF(
                        REGEXP_REPLACE(
                            SUBSTRING(h.observaciones FROM 'de ([0-9]+\\.?[0-9]*) a'),
                            '[^0-9.]', '', 'g'
                        ),
                        ''
                    )::DECIMAL(10,2) as precio_viejo,
                    h.observaciones
                FROM historial_p h
                WHERE h.id_producto = %s
                  AND h.fecha_registro >= CURRENT_DATE - INTERVAL '90 days'
                  AND h.observaciones IS NOT NULL
            ),
            precios_mercado AS (
                SELECT fecha_completa, precio_viejo as precio
                FROM todos_precios tp
                INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                WHERE m.id_mercado = %s AND precio_viejo IS NOT NULL
                
                UNION ALL
                
                SELECT fecha_completa, precio_nuevo as precio
                FROM todos_precios tp
                INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                WHERE m.id_mercado = %s AND precio_nuevo IS NOT NULL
                
                UNION ALL
                
                SELECT o.fecha_actualizacion, o.precio
                FROM oferta o
                WHERE o.id_producto = %s AND o.id_mercado = %s
            )
            SELECT fecha_completa::date as fecha, precio
            FROM precios_mercado
            WHERE precio > 0
            ORDER BY fecha_completa;
            """
            params = (id_producto, id_mercado, id_mercado, id_producto, id_mercado)
        
        datos = execute_query(query, params, fetch=True)
        
        if datos:
            df = pd.DataFrame(datos, columns=['fecha', 'precio'])
            df['precio'] = pd.to_numeric(df['precio'])
            return df
        return None
    def prediccion_lineal(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Tendencia Lineal")
        ventana.geometry("900x650")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="📈 PREDICCIÓN POR TENDENCIA LINEAL",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana, text="Proyección futura basada en regresión lineal de datos históricos",
            font=("Arial", 10), bg="#0a0f1e", fg="#94a3b8").pack()
        
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        labels_config = np.array([
            ['Producto:', 0, 0], ['Mercado:', 0, 2], ['Días a predecir:', 1, 0]
        ], dtype=object)
        
        for texto, row, col in labels_config:
            tk.Label(frame_seleccion, text=texto, font=("Arial", 10, "bold"),
                bg="#1e293b", fg="#e2e8f0").grid(row=int(row), column=int(col), 
                padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=self.df_productos['display'].tolist(),
            state="readonly", font=("Arial", 10), width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        mercados_lista = ["Todos los mercados"] + self.df_mercados['display'].tolist()
        combo_mercado = ttk.Combobox(frame_seleccion, values=mercados_lista,
            state="readonly", font=("Arial", 10), width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        spin_dias = tk.Spinbox(frame_seleccion, from_=1, to=90,
            font=("Arial", 10), width=10, bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=350)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)
        
        canvas_grafico = tk.Canvas(frame_resultados, bg="#0f172a",
            highlightthickness=0, height=200)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        label_resultado = tk.Text(frame_texto, font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8", wrap=tk.WORD, height=8,
            yscrollcommand=scrollbar.set)
        label_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=label_resultado.yview)
        
        label_resultado.insert("1.0", "Selecciona un producto y presiona 'Calcular Predicción'")
        
        def calcular_prediccion():
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            id_producto = self.get_id_from_combo(combo_producto, self.df_productos)
            dias_futuro = int(spin_dias.get())
            
            id_mercado = None
            if combo_mercado.get() != "Todos los mercados":
                id_mercado = self.get_id_from_combo(combo_mercado, self.df_mercados)
            
            df_datos = self.obtener_datos_historicos(id_producto, id_mercado)
            
            if df_datos is None or len(df_datos) < 3:
                messagebox.showwarning("Datos insuficientes",
                    "Se necesitan al menos 3 registros históricos para predecir.\n\n"
                    f"Registros encontrados: {len(df_datos) if df_datos is not None else 0}")
                return
            
            n = len(df_datos)
            precios = df_datos['precio'].values
            
            x = np.arange(n)
            suma_x = np.sum(x)
            suma_y = np.sum(precios)
            suma_xy = np.sum(x * precios)
            suma_x2 = np.sum(x ** 2)
            
            m = (n * suma_xy - suma_x * suma_y) / (n * suma_x2 - suma_x ** 2)
            b = (suma_y - m * suma_x) / n
            
            precio_actual = float(df_datos.iloc[-1]['precio'])
            fecha_actual = df_datos.iloc[-1]['fecha']
            
            precio_predicho = m * (n + dias_futuro - 1) + b
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            
            if m > 0.1:
                tendencia = "ALCISTA 📈"
            elif m < -0.1:
                tendencia = "BAJISTA 📉"
            else:
                tendencia = "ESTABLE ➡️"
            
            errores = precios - (m * x + b)
            mse = np.mean(errores ** 2)
            std_error = np.sqrt(mse)
            
            resultado_texto = f"""
📊 RESULTADOS DE LA PREDICCIÓN

Producto: {combo_producto.get()}
Mercado: {combo_mercado.get()}
Período analizado: {n} días de datos históricos

════════════════════════════════════════════════

📍 SITUACIÓN ACTUAL
   Precio actual: {precio_actual:.2f} Bs
   Fecha: {fecha_actual.strftime('%d/%m/%Y')}

🔮 PREDICCIÓN PARA {dias_futuro} DÍAS
   Precio estimado: {precio_predicho:.2f} Bs
   Fecha proyectada: {fecha_futura.strftime('%d/%m/%Y')}
   
   Rango probable: {precio_predicho - std_error:.2f} - {precio_predicho + std_error:.2f} Bs

════════════════════════════════════════════════

📈 ANÁLISIS DE TENDENCIA
   Tendencia: {tendencia}
   Cambio diario promedio: {m:.3f} Bs/día
   Cambio esperado total: {(precio_predicho - precio_actual):.2f} Bs
   Cambio porcentual: {((precio_predicho - precio_actual) / precio_actual * 100):.1f}%

════════════════════════════════════════════════

⚙️ INFORMACIÓN TÉCNICA
   Modelo: Regresión Lineal Simple
   Ecuación: y = {m:.4f}x + {b:.2f}
   Error estándar: ±{std_error:.2f} Bs
   Nivel de confianza: {"Alto" if std_error < 2 else "Medio" if std_error < 5 else "Bajo"}
            """
            if std_error < 2:
                nivel_confianza = 85.0
            elif std_error < 5:
                nivel_confianza = 65.0
            else:
                nivel_confianza = 40.0
    
    
            self.guardar_prediccion(
                id_producto=id_producto,
                precio_estimado=precio_predicho,
                nivel_confianza=nivel_confianza,
                tendencia=tendencia.split()[0],  # "ALCISTA", "BAJISTA", o "ESTABLE"
                fecha_objetivo=fecha_futura,
                modelo_usado="Regresión Lineal"
            )
            label_resultado.delete("1.0", tk.END)
            label_resultado.insert("1.0", resultado_texto)
            label_resultado.config(fg="#e2e8f0")
            
            canvas_grafico.delete("all")
            self.dibujar_grafico_simple(canvas_grafico, df_datos, m, b, dias_futuro, precio_predicho)
        
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="🔮 Calcular Predicción",
            font=("Arial", 11, "bold"), bg="#10b981", fg="white",
            command=calcular_prediccion, padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    
    def dibujar_grafico_simple(self, canvas, df_datos, m, b, dias_futuro, precio_final):
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 400
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 400
        
        margin = 60
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        precios = df_datos['precio'].values
        todos_precios = np.append(precios, precio_final)
        
        precio_min = np.min(todos_precios) * 0.95
        precio_max = np.max(todos_precios) * 1.05
        rango_precio = precio_max - precio_min
        
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)
        
        canvas.create_text(width/2, height-20, text="Tiempo (días)",
            font=("Arial", 10), fill="#94a3b8")
        
        canvas.create_text(20, height/2, text="Precio (Bs)",
            font=("Arial", 10), fill="#94a3b8", angle=90)
        
        n_datos = len(df_datos)
        total_puntos = n_datos + dias_futuro
        
        puntos_historicos = []
        for i in range(n_datos):
            x = margin + (i / total_puntos) * graph_width
            precio = precios[i]
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos_historicos.append((x, y))
            
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="#3b82f6", outline="")
        
        if len(puntos_historicos) > 1:
            for i in range(len(puntos_historicos)-1):
                canvas.create_line(puntos_historicos[i], puntos_historicos[i+1],
                    fill="#3b82f6", width=2)
        
        x_pred = margin + ((n_datos + dias_futuro - 1) / total_puntos) * graph_width
        y_pred = height - margin - ((precio_final - precio_min) / rango_precio) * graph_height
        
        if puntos_historicos:
            canvas.create_line(puntos_historicos[-1], (x_pred, y_pred),
                fill="#10b981", width=2, dash=(5, 5))
            
            canvas.create_oval(x_pred-5, y_pred-5, x_pred+5, y_pred+5,
                fill="#10b981", outline="#064e3b", width=2)
            
            canvas.create_text(x_pred, y_pred-15, text=f"{precio_final:.2f} Bs",
                font=("Arial", 9, "bold"), fill="#10b981")
        
        legend_x = width - margin - 150
        legend_y = margin + 20
        
        canvas.create_rectangle(legend_x-10, legend_y-15, legend_x+140, legend_y+35,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_line(legend_x, legend_y, legend_x+20, legend_y,
            fill="#3b82f6", width=2)
        canvas.create_text(legend_x+30, legend_y, text="Histórico",
            font=("Arial", 9), fill="#e2e8f0", anchor="w")
        
        canvas.create_line(legend_x, legend_y+20, legend_x+20, legend_y+20,
            fill="#10b981", width=2, dash=(5, 5))
        canvas.create_text(legend_x+30, legend_y+20, text="Predicción",
            font=("Arial", 9), fill="#e2e8f0", anchor="w")
    def prediccion_media_movil(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Media Móvil")
        ventana.geometry("900x700")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="📊 PREDICCIÓN POR MEDIA MÓVIL",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana, text="Promedio de los últimos N días para proyectar el futuro",
            font=("Arial", 10), bg="#0a0f1e", fg="#94a3b8").pack()
        
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        labels = ['Producto:', 'Mercado:', 'Ventana (días):', 'Días a predecir:']
        rows = [0, 0, 1, 2]
        cols = [0, 2, 0, 0]
        
        for texto, row, col in zip(labels, rows, cols):
            tk.Label(frame_seleccion, text=texto, font=("Arial", 10, "bold"),
                bg="#1e293b", fg="#e2e8f0").grid(row=row, column=col, padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=self.df_productos['display'].tolist(),
            state="readonly", font=("Arial", 10), width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        mercados_lista = ["Todos los mercados"] + self.df_mercados['display'].tolist()
        combo_mercado = ttk.Combobox(frame_seleccion, values=mercados_lista,
            state="readonly", font=("Arial", 10), width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        spin_ventana = tk.Spinbox(frame_seleccion, from_=3, to=30,
            font=("Arial", 10), width=10, bg="#0f172a", fg="white")
        spin_ventana.delete(0, tk.END)
        spin_ventana.insert(0, "7")
        spin_ventana.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(frame_seleccion, text="(Últimos N días para calcular el promedio)",
            font=("Arial", 8, "italic"), bg="#1e293b", fg="#64748b").grid(
            row=1, column=2, columnspan=2, sticky="w")
        
        spin_dias = tk.Spinbox(frame_seleccion, from_=1, to=90,
            font=("Arial", 10), width=10, bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=320)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)
        
        canvas_grafico = tk.Canvas(frame_resultados, bg="#0f172a",
            highlightthickness=0, height=180)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_resultado = tk.Text(frame_texto, font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8", wrap=tk.WORD, height=6,
            yscrollcommand=scrollbar.set)
        text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_resultado.yview)
        
        text_resultado.insert("1.0", "Selecciona un producto y presiona 'Calcular Predicción'")
        
        def calcular_media_movil():
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            id_producto = self.get_id_from_combo(combo_producto, self.df_productos)
            dias_futuro = int(spin_dias.get())
            ventana_dias = int(spin_ventana.get())
            
            id_mercado = None
            if combo_mercado.get() != "Todos los mercados":
                id_mercado = self.get_id_from_combo(combo_mercado, self.df_mercados)
            
            df_datos = self.obtener_datos_historicos(id_producto, id_mercado)
            
            if df_datos is None or len(df_datos) < ventana_dias:
                messagebox.showwarning("Datos insuficientes",
                    f"Se necesitan al menos {ventana_dias} registros para calcular la media móvil.\n\n"
                    f"Registros encontrados: {len(df_datos) if df_datos is not None else 0}")
                return
            
            precios = df_datos['precio'].values
            ultimos_precios = precios[-ventana_dias:]
            
            media_movil = np.mean(ultimos_precios)
            
            precio_actual = float(df_datos.iloc[-1]['precio'])
            fecha_actual = df_datos.iloc[-1]['fecha']
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            
            promedio = np.mean(precios)
            volatilidad = np.std(precios)
            
            if volatilidad < 1:
                confianza = "Alta"
            elif volatilidad < 3:
                confianza = "Media"
            else:
                confianza = "Baja"
            
            resultado_texto = f"""
📊 RESULTADOS - MEDIA MÓVIL SIMPLE

Producto: {combo_producto.get()}
Mercado: {combo_mercado.get()}
Ventana de análisis: {ventana_dias} días
Total de datos históricos: {len(df_datos)}

════════════════════════════════════════════════

📍 SITUACIÓN ACTUAL
   Precio actual: {precio_actual:.2f} Bs
   Fecha: {fecha_actual.strftime('%d/%m/%Y')}
   
   Últimos {ventana_dias} precios:
   {', '.join([f'{p:.2f}' for p in ultimos_precios])} Bs

🔮 PREDICCIÓN PARA {dias_futuro} DÍAS
   Precio estimado (media móvil): {media_movil:.2f} Bs
   Fecha proyectada: {fecha_futura.strftime('%d/%m/%Y')}
   
   Rango probable: {media_movil - volatilidad:.2f} - {media_movil + volatilidad:.2f} Bs

════════════════════════════════════════════════

📈 ANÁLISIS
   Cambio esperado: {(media_movil - precio_actual):.2f} Bs
   Cambio porcentual: {((media_movil - precio_actual) / precio_actual * 100):.1f}%
   
   Tendencia: {"📈 ALCISTA" if media_movil > precio_actual else "📉 BAJISTA" if media_movil < precio_actual else "➡️ ESTABLE"}
   
   Volatilidad: ±{volatilidad:.2f} Bs
   Nivel de confianza: {confianza}

════════════════════════════════════════════════

⚙️ INFORMACIÓN TÉCNICA
   Modelo: Media Móvil Simple (SMA)
   Fórmula: SMA = Σ(precios últimos {ventana_dias} días) / {ventana_dias}
   Precio min histórico: {np.min(precios):.2f} Bs
   Precio max histórico: {np.max(precios):.2f} Bs
   Promedio general: {promedio:.2f} Bs

💡 INTERPRETACIÓN:
   La media móvil simple asume que el precio futuro será
   el promedio de los últimos {ventana_dias} días. Este modelo
   funciona mejor en mercados estables sin tendencias fuertes.
            """
            if confianza == "Alta":
                nivel_conf_num = 80.0
            elif confianza == "Media":
                nivel_conf_num = 60.0
            else:
                nivel_conf_num = 35.0
    
            
            if media_movil > precio_actual * 1.02:
                tend = "ALCISTA"
            elif media_movil < precio_actual * 0.98:
                tend = "BAJISTA"
            else:
                tend = "ESTABLE"
    
    
            self.guardar_prediccion(
                id_producto=id_producto,
                precio_estimado=media_movil,
                nivel_confianza=nivel_conf_num,
                tendencia=tend,
                fecha_objetivo=fecha_futura,
                modelo_usado=f"Media Móvil (ventana={ventana_dias}d)"
            )
            text_resultado.delete("1.0", tk.END)
            text_resultado.insert("1.0", resultado_texto)
            text_resultado.config(fg="#e2e8f0")
            
            canvas_grafico.delete("all")
            self.dibujar_grafico_media_movil(canvas_grafico, df_datos, media_movil, 
                                            ventana_dias, dias_futuro)
        
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="📊 Calcular Predicción",
            font=("Arial", 11, "bold"), bg="#3b82f6", fg="white",
            command=calcular_media_movil, padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    
    def dibujar_grafico_media_movil(self, canvas, df_datos, media_movil, ventana_dias, dias_futuro):
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 200
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 200
        
        margin = 50
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        precios = df_datos['precio'].values
        todos_precios = np.append(precios, media_movil)
        
        precio_min = np.min(todos_precios) * 0.95
        precio_max = np.max(todos_precios) * 1.05
        rango_precio = precio_max - precio_min
        
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)
        
        canvas.create_text(width/2, height-15, text="Tiempo",
            font=("Arial", 9), fill="#94a3b8")
        canvas.create_text(15, height/2, text="Precio",
            font=("Arial", 9), fill="#94a3b8", angle=90)
        
        n_datos = len(df_datos)
        puntos = []
        for i in range(n_datos):
            x = margin + (i / (n_datos + dias_futuro)) * graph_width
            precio = precios[i]
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos.append((x, y))
            
            if i >= n_datos - ventana_dias:
                canvas.create_oval(x-4, y-4, x+4, y+4, fill="#f59e0b", outline="")
            else:
                canvas.create_oval(x-2, y-2, x+2, y+2, fill="#64748b", outline="")
        
        if len(puntos) > 1:
            for i in range(len(puntos)-1):
                color = "#f59e0b" if i >= n_datos - ventana_dias - 1 else "#64748b"
                canvas.create_line(puntos[i], puntos[i+1], fill=color, width=2)
        
        x_pred = margin + ((n_datos + dias_futuro - 1) / (n_datos + dias_futuro)) * graph_width
        y_pred = height - margin - ((media_movil - precio_min) / rango_precio) * graph_height
        
        if puntos:
            canvas.create_line(puntos[-1], (x_pred, y_pred),
                fill="#3b82f6", width=2, dash=(5, 5))
            canvas.create_oval(x_pred-5, y_pred-5, x_pred+5, y_pred+5,
                fill="#3b82f6", outline="#1e40af", width=2)
            canvas.create_text(x_pred, y_pred-12, text=f"{media_movil:.2f} Bs",
                font=("Arial", 8, "bold"), fill="#3b82f6")
        
        legend_x = width - margin - 120
        legend_y = margin + 15
        
        canvas.create_rectangle(legend_x-5, legend_y-10, legend_x+115, legend_y+40,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_oval(legend_x, legend_y-3, legend_x+6, legend_y+3,
            fill="#64748b", outline="")
        canvas.create_text(legend_x+15, legend_y, text="Histórico",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_oval(legend_x, legend_y+12, legend_x+6, legend_y+18,
            fill="#f59e0b", outline="")
        canvas.create_text(legend_x+15, legend_y+15, text=f"Ventana ({ventana_dias}d)",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_line(legend_x, legend_y+30, legend_x+15, legend_y+30,
            fill="#3b82f6", width=2, dash=(3, 3))
        canvas.create_text(legend_x+20, legend_y+30, text="Predicción",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
    def prediccion_estacional(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Análisis Estacional")
        ventana.geometry("900x700")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="🔄 ANÁLISIS ESTACIONAL",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana, text="Detecta patrones que se repiten en ciclos de tiempo",
            font=("Arial", 10), bg="#0a0f1e", fg="#94a3b8").pack()
        
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        labels = ['Producto:', 'Mercado:', 'Ciclo a analizar:', 'Días a predecir:']
        rows = [0, 0, 1, 2]
        cols = [0, 2, 0, 0]
        
        for texto, row, col in zip(labels, rows, cols):
            tk.Label(frame_seleccion, text=texto, font=("Arial", 10, "bold"),
                bg="#1e293b", fg="#e2e8f0").grid(row=row, column=col, padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=self.df_productos['display'].tolist(),
            state="readonly", font=("Arial", 10), width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        mercados_lista = ["Todos los mercados"] + self.df_mercados['display'].tolist()
        combo_mercado = ttk.Combobox(frame_seleccion, values=mercados_lista,
            state="readonly", font=("Arial", 10), width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        combo_ciclo = ttk.Combobox(frame_seleccion,
            values=["Semanal (7 días)", "Quincenal (15 días)", "Mensual (30 días)"],
            state="readonly", font=("Arial", 10), width=25)
        combo_ciclo.current(0)
        combo_ciclo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(frame_seleccion, text="(Patrón que se repite cada N días)",
            font=("Arial", 8, "italic"), bg="#1e293b", fg="#64748b").grid(
            row=1, column=2, columnspan=2, sticky="w")
        
        spin_dias = tk.Spinbox(frame_seleccion, from_=1, to=90,
            font=("Arial", 10), width=10, bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        frame_info = tk.Frame(ventana, bg="#1a1f2e")
        frame_info.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(frame_info, text="💡 ¿Qué es el Análisis Estacional?",
            font=("Arial", 9, "bold"), bg="#1a1f2e", fg="#8b5cf6").pack(anchor="w", padx=10, pady=5)
        
        info_text = """    Este modelo busca patrones repetitivos en los precios:
    • Semanal: ¿Los lunes son más caros? ¿Los domingos más baratos?
    • Quincenal: ¿Sube a mitad de mes cuando la gente cobra?
    • Mensual: ¿Ciclos relacionados con cosechas o temporadas?
    
    La predicción se basa en promedios de cada día del ciclo."""
        
        tk.Label(frame_info, text=info_text, font=("Arial", 8),
            bg="#1a1f2e", fg="#94a3b8", justify=tk.LEFT).pack(anchor="w", padx=20)
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=320)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)
        
        canvas_grafico = tk.Canvas(frame_resultados, bg="#0f172a",
            highlightthickness=0, height=180)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_resultado = tk.Text(frame_texto, font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8", wrap=tk.WORD, height=6,
            yscrollcommand=scrollbar.set)
        text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_resultado.yview)
        
        text_resultado.insert("1.0", "Selecciona un producto y presiona 'Analizar Estacionalidad'")
        
        def calcular_estacional():
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            id_producto = self.get_id_from_combo(combo_producto, self.df_productos)
            dias_futuro = int(spin_dias.get())
            
            ciclo_texto = combo_ciclo.get()
            ciclos_info = {
                "Semanal (7 días)": (7, "Semanal", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]),
                "Quincenal (15 días)": (15, "Quincenal", [f"Día {i+1}" for i in range(15)]),
                "Mensual (30 días)": (30, "Mensual", [f"Día {i+1}" for i in range(30)])
            }
            
            longitud_ciclo, nombre_ciclo, dias_nombres = ciclos_info[ciclo_texto]
            
            id_mercado = None
            if combo_mercado.get() != "Todos los mercados":
                id_mercado = self.get_id_from_combo(combo_mercado, self.df_mercados)
            
            df_datos = self.obtener_datos_historicos(id_producto, id_mercado)
            
            if df_datos is None or len(df_datos) < longitud_ciclo:
                messagebox.showwarning("Datos insuficientes",
                    f"Se necesitan al menos {longitud_ciclo} registros para análisis {nombre_ciclo.lower()}.\n\n"
                    f"Registros encontrados: {len(df_datos) if df_datos is not None else 0}")
                return
            
            precios = df_datos['precio'].values
            
            promedios_dict = {}
            for i, precio in enumerate(precios):
                posicion = i % longitud_ciclo
                if posicion not in promedios_dict:
                    promedios_dict[posicion] = []
                promedios_dict[posicion].append(precio)
            
            patron_estacional = {}
            promedio_general = np.mean(precios)
            
            for pos in range(longitud_ciclo):
                if pos in promedios_dict and len(promedios_dict[pos]) > 0:
                    patron_estacional[pos] = np.mean(promedios_dict[pos])
                else:
                    patron_estacional[pos] = promedio_general
            
            precio_actual = float(df_datos.iloc[-1]['precio'])
            fecha_actual = df_datos.iloc[-1]['fecha']
            posicion_actual = (len(df_datos) - 1) % longitud_ciclo
            
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            posicion_futura = (len(df_datos) + dias_futuro - 1) % longitud_ciclo
            precio_predicho = patron_estacional[posicion_futura]
            
            varianzas = []
            for pos in range(longitud_ciclo):
                if pos in promedios_dict and len(promedios_dict[pos]) > 1:
                    varianzas.append(np.std(promedios_dict[pos]))
            
            variabilidad = np.mean(varianzas) if len(varianzas) > 0 else 1.0
            
            rango_precios = np.max(precios) - np.min(precios)
            valores_patron = np.array(list(patron_estacional.values()))
            rango_patron = np.max(valores_patron) - np.min(valores_patron)
            
            fuerza_patron = (rango_patron / rango_precios * 100) if rango_precios > 0 else 0
            
            if fuerza_patron > 15:
                interpretacion = "PATRÓN FUERTE detectado"
                confianza = "Alta"
            elif fuerza_patron > 5:
                interpretacion = "PATRÓN MODERADO detectado"
                confianza = "Media"
            else:
                interpretacion = "PATRÓN DÉBIL o inexistente"
                confianza = "Baja"
            
            pos_max = max(patron_estacional, key=patron_estacional.get)
            pos_min = min(patron_estacional, key=patron_estacional.get)
            
            tendencia = "ALCISTA 📈" if precio_predicho > precio_actual * 1.02 else "BAJISTA 📉" if precio_predicho < precio_actual * 0.98 else "ESTABLE ➡️"
            
            resultado_texto = f"""
🔄 RESULTADOS - ANÁLISIS ESTACIONAL {nombre_ciclo.upper()}

Producto: {combo_producto.get()}
Mercado: {combo_mercado.get()}
Tipo de ciclo: {nombre_ciclo} ({longitud_ciclo} días)
Datos históricos: {len(df_datos)} registros

════════════════════════════════════════════════

📊 PATRÓN DETECTADO
   {interpretacion}
   Fuerza del patrón: {fuerza_patron:.1f}%
   Variabilidad: ±{variabilidad:.2f} Bs
   Nivel de confianza: {confianza}

📍 SITUACIÓN ACTUAL
   Precio actual: {precio_actual:.2f} Bs
   Fecha: {fecha_actual.strftime('%d/%m/%Y')}
   Posición en el ciclo: {dias_nombres[posicion_actual] if posicion_actual < len(dias_nombres) else f"Día {posicion_actual+1}"}
   Precio esperado hoy: {patron_estacional[posicion_actual]:.2f} Bs
   Desviación: {(precio_actual - patron_estacional[posicion_actual]):.2f} Bs

🔮 PREDICCIÓN PARA {dias_futuro} DÍAS
   Precio estimado: {precio_predicho:.2f} Bs
   Fecha proyectada: {fecha_futura.strftime('%d/%m/%Y')}
   Posición en el ciclo: {dias_nombres[posicion_futura] if posicion_futura < len(dias_nombres) else f"Día {posicion_futura+1}"}
   
   Rango probable: {precio_predicho - variabilidad:.2f} - {precio_predicho + variabilidad:.2f} Bs
   
   Tendencia: {tendencia}
   Cambio esperado: {(precio_predicho - precio_actual):.2f} Bs ({((precio_predicho - precio_actual) / precio_actual * 100):.1f}%)

════════════════════════════════════════════════

📈 ANÁLISIS DEL PATRÓN {nombre_ciclo.upper()}

   Día MÁS CARO del ciclo:
   • {dias_nombres[pos_max] if pos_max < len(dias_nombres) else f"Día {pos_max+1}"}: {patron_estacional[pos_max]:.2f} Bs (promedio)
   
   Día MÁS BARATO del ciclo:
   • {dias_nombres[pos_min] if pos_min < len(dias_nombres) else f"Día {pos_min+1}"}: {patron_estacional[pos_min]:.2f} Bs (promedio)
   
   Diferencia máxima: {(patron_estacional[pos_max] - patron_estacional[pos_min]):.2f} Bs

════════════════════════════════════════════════

⚙️ INFORMACIÓN TÉCNICA
   Modelo: Descomposición Estacional Simple
   Método: Promedio por posición en el ciclo
   
   Precio min histórico: {np.min(precios):.2f} Bs
   Precio max histórico: {np.max(precios):.2f} Bs
   Promedio general: {promedio_general:.2f} Bs

💡 INTERPRETACIÓN:
   {"Este producto muestra un patrón claro que se repite" if fuerza_patron > 15 else "El patrón es débil, los precios varían más por" if fuerza_patron > 5 else "No hay patrón estacional significativo. Los precios"}
   {"cada " + nombre_ciclo.lower() + ". Usa este patrón para planificar" if fuerza_patron > 15 else "otros factores que por el ciclo " + nombre_ciclo.lower() + "." if fuerza_patron > 5 else "parecen variar por razones no cíclicas."}
   {"compras en días baratos y ventas en días caros." if fuerza_patron > 15 else "Considera otros modelos de predicción." if fuerza_patron > 5 else ""}
            """
            if confianza == "Alta":
                nivel_conf_num = 75.0
            elif confianza == "Media":
                nivel_conf_num = 55.0
            else:
                nivel_conf_num = 30.0
    
            
            tend = tendencia.split()[0]  
    
            
            self.guardar_prediccion(
                id_producto=id_producto,
                precio_estimado=precio_predicho,
                nivel_confianza=nivel_conf_num,
                tendencia=tend,
                fecha_objetivo=fecha_futura,
                modelo_usado=f"Análisis Estacional ({nombre_ciclo})"
            )
            text_resultado.delete("1.0", tk.END)
            text_resultado.insert("1.0", resultado_texto)
            text_resultado.config(fg="#e2e8f0")
            
            canvas_grafico.delete("all")
            self.dibujar_grafico_estacional(canvas_grafico, df_datos, patron_estacional, 
                                           longitud_ciclo, dias_nombres, precio_predicho, 
                                           posicion_futura, dias_futuro)
        
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="🔄 Analizar Estacionalidad",
            font=("Arial", 11, "bold"), bg="#8b5cf6", fg="white",
            command=calcular_estacional, padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    def dibujar_grafico_estacional(self, canvas, df_datos, patron, longitud_ciclo, nombres_dias, precio_pred, pos_pred, dias_futuro):
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 180
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 180
        
        margin = 50
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        precios_patron = list(patron.values())
        precios_patron.append(precio_pred)
        
        precio_min = np.min(precios_patron) * 0.95
        precio_max = np.max(precios_patron) * 1.05
        rango_precio = precio_max - precio_min
        
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)
        
        canvas.create_text(width/2, height-15, text="Posición en el ciclo",
            font=("Arial", 9), fill="#94a3b8")
        canvas.create_text(15, height/2, text="Precio",
            font=("Arial", 9), fill="#94a3b8", angle=90)
        
        canvas.create_text(width/2, margin-25, 
            text=f"Patrón Estacional (Ciclo: {longitud_ciclo} días)",
            font=("Arial", 10, "bold"), fill="#8b5cf6")
        
        puntos_patron = []
        for pos in range(longitud_ciclo):
            x = margin + (pos / longitud_ciclo) * graph_width
            precio = patron[pos]
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos_patron.append((x, y))
            
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="#8b5cf6", outline="")
        
        if len(puntos_patron) > 1:
            for i in range(len(puntos_patron)):
                inicio = puntos_patron[i]
                fin = puntos_patron[(i+1) % longitud_ciclo]
                canvas.create_line(inicio, fin, fill="#8b5cf6", width=2)
        
        x_pred = margin + (pos_pred / longitud_ciclo) * graph_width
        y_pred = height - margin - ((precio_pred - precio_min) / rango_precio) * graph_height
        
        canvas.create_oval(x_pred-6, y_pred-6, x_pred+6, y_pred+6,
            fill="#10b981", outline="#064e3b", width=2)
        
        canvas.create_text(x_pred, y_pred-15, text=f"{precio_pred:.2f} Bs",
            font=("Arial", 8, "bold"), fill="#10b981")
        
        pos_max = max(patron, key=patron.get)
        pos_min = min(patron, key=patron.get)
        
        x_max = margin + (pos_max / longitud_ciclo) * graph_width
        y_max = height - margin - ((patron[pos_max] - precio_min) / rango_precio) * graph_height
        
        x_min = margin + (pos_min / longitud_ciclo) * graph_width
        y_min = height - margin - ((patron[pos_min] - precio_min) / rango_precio) * graph_height
        
        canvas.create_text(x_max, y_max+15, text="↑ MÁX",
            font=("Arial", 7, "bold"), fill="#dc2626")
        
        canvas.create_text(x_min, y_min-15, text="↓ MÍN",
            font=("Arial", 7, "bold"), fill="#10b981")
        
        legend_x = width - margin - 90
        legend_y = margin + 10
        
        canvas.create_rectangle(legend_x-5, legend_y-8, legend_x+85, legend_y+30,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_oval(legend_x, legend_y-2, legend_x+6, legend_y+4,
            fill="#8b5cf6", outline="")
        canvas.create_text(legend_x+15, legend_y, text="Patrón",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_oval(legend_x-1, legend_y+13, legend_x+7, legend_y+21,
            fill="#10b981", outline="#064e3b", width=1)
        canvas.create_text(legend_x+15, legend_y+17, text="Predicción",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
    
    def prediccion_exponencial(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Suavizado Exponencial")
        ventana.geometry("900x700")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="📉 PREDICCIÓN POR SUAVIZADO EXPONENCIAL",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana, text="Mayor peso a datos recientes para predicciones más precisas",
            font=("Arial", 10), bg="#0a0f1e", fg="#94a3b8").pack()
        
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        labels = ['Producto:', 'Mercado:', 'Factor α (alpha):', 'Días a predecir:']
        rows = [0, 0, 1, 2]
        cols = [0, 2, 0, 0]
        
        for texto, row, col in zip(labels, rows, cols):
            tk.Label(frame_seleccion, text=texto, font=("Arial", 10, "bold"),
                bg="#1e293b", fg="#e2e8f0").grid(row=row, column=col, padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=self.df_productos['display'].tolist(),
            state="readonly", font=("Arial", 10), width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        mercados_lista = ["Todos los mercados"] + self.df_mercados['display'].tolist()
        combo_mercado = ttk.Combobox(frame_seleccion, values=mercados_lista,
            state="readonly", font=("Arial", 10), width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        frame_alpha = tk.Frame(frame_seleccion, bg="#1e293b")
        frame_alpha.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        alpha_var = tk.DoubleVar(value=0.3)
        
        scale_alpha = tk.Scale(frame_alpha, from_=0.1, to=0.9, resolution=0.1,
            orient=tk.HORIZONTAL, variable=alpha_var, bg="#0f172a", fg="white",
            highlightthickness=0, length=150)
        scale_alpha.pack(side=tk.LEFT)
        
        label_alpha_val = tk.Label(frame_alpha, text=f"α = {alpha_var.get():.1f}",
            font=("Arial", 9), bg="#1e293b", fg="#f59e0b")
        label_alpha_val.pack(side=tk.LEFT, padx=5)
        
        def update_alpha_label(*args):
            label_alpha_val.config(text=f"α = {alpha_var.get():.1f}")
        
        alpha_var.trace("w", update_alpha_label)
        
        tk.Label(frame_seleccion, text="Bajo: más suave | Alto: más reactivo",
            font=("Arial", 8, "italic"), bg="#1e293b", fg="#64748b").grid(
            row=1, column=2, columnspan=2, sticky="w")
        
        spin_dias = tk.Spinbox(frame_seleccion, from_=1, to=90,
            font=("Arial", 10), width=10, bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        frame_info = tk.Frame(ventana, bg="#1a1f2e")
        frame_info.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(frame_info, text="💡 ¿Qué es Alpha (α)?",
            font=("Arial", 9, "bold"), bg="#1a1f2e", fg="#f59e0b").pack(anchor="w", padx=10, pady=5)
        
        info_text = """    Alpha controla cuánto peso se da a los datos recientes:
    • α bajo (0.1-0.3): Predicción más suave, menos sensible a cambios bruscos
    • α medio (0.4-0.6): Balance entre estabilidad y reactividad
    • α alto (0.7-0.9): Muy reactivo, sigue de cerca los últimos cambios"""
        
        tk.Label(frame_info, text=info_text, font=("Arial", 8),
            bg="#1a1f2e", fg="#94a3b8", justify=tk.LEFT).pack(anchor="w", padx=20)
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=320)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)
        
        canvas_grafico = tk.Canvas(frame_resultados, bg="#0f172a",
            highlightthickness=0, height=180)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_resultado = tk.Text(frame_texto, font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8", wrap=tk.WORD, height=6,
            yscrollcommand=scrollbar.set)
        text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_resultado.yview)
        
        text_resultado.insert("1.0", "Selecciona un producto y presiona 'Calcular Predicción'")
        
        def calcular_exponencial():
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            id_producto = self.get_id_from_combo(combo_producto, self.df_productos)
            dias_futuro = int(spin_dias.get())
            alpha = alpha_var.get()
            
            id_mercado = None
            if combo_mercado.get() != "Todos los mercados":
                id_mercado = self.get_id_from_combo(combo_mercado, self.df_mercados)
            
            df_datos = self.obtener_datos_historicos(id_producto, id_mercado)
            
            if df_datos is None or len(df_datos) < 3:
                messagebox.showwarning("Datos insuficientes",
                    f"Se necesitan al menos 3 registros históricos.\n\n"
                    f"Registros encontrados: {len(df_datos) if df_datos is not None else 0}")
                return
            
            precios = df_datos['precio'].values
            
            S = [precios[0]]
            
            for i in range(1, len(precios)):
                S_t = alpha * precios[i] + (1 - alpha) * S[-1]
                S.append(S_t)
            
            precio_predicho = S[-1]
            
            precio_actual = float(df_datos.iloc[-1]['precio'])
            fecha_actual = df_datos.iloc[-1]['fecha']
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            
            errores = np.abs(precios - np.array(S))
            mae = np.mean(errores)
            
            promedio = np.mean(precios)
            volatilidad = np.std(precios)
            
            tendencia = "ALCISTA 📈" if precio_predicho > precio_actual * 1.02 else "BAJISTA 📉" if precio_predicho < precio_actual * 0.98 else "ESTABLE ➡️"
            
            confianza = "Alta" if mae < 1 else "Media" if mae < 3 else "Baja"
            
            reactividad = alpha * 100
            
            resultado_texto = f"""
📉 RESULTADOS - SUAVIZADO EXPONENCIAL SIMPLE

Producto: {combo_producto.get()}
Mercado: {combo_mercado.get()}
Parámetro Alpha (α): {alpha:.1f} ({reactividad:.0f}% reactivo)
Datos históricos: {len(df_datos)} registros

════════════════════════════════════════════════

📍 SITUACIÓN ACTUAL
   Precio real actual: {precio_actual:.2f} Bs
   Precio suavizado: {S[-1]:.2f} Bs
   Fecha: {fecha_actual.strftime('%d/%m/%Y')}

🔮 PREDICCIÓN PARA {dias_futuro} DÍAS
   Precio estimado: {precio_predicho:.2f} Bs
   Fecha proyectada: {fecha_futura.strftime('%d/%m/%Y')}
   
   Rango probable: {precio_predicho - mae:.2f} - {precio_predicho + mae:.2f} Bs

════════════════════════════════════════════════

📈 ANÁLISIS DE TENDENCIA
   Tendencia: {tendencia}
   Cambio esperado: {(precio_predicho - precio_actual):.2f} Bs
   Cambio porcentual: {((precio_predicho - precio_actual) / precio_actual * 100):.1f}%
   
   Volatilidad histórica: ±{volatilidad:.2f} Bs

════════════════════════════════════════════════

⚙️ INFORMACIÓN TÉCNICA
   Modelo: Suavizado Exponencial Simple (SES)
   Fórmula: S_t = α·Y_t + (1-α)·S_(t-1)
   
   Error medio absoluto: {mae:.2f} Bs
   Nivel de confianza: {confianza}
   
   Precio min histórico: {np.min(precios):.2f} Bs
   Precio max histórico: {np.max(precios):.2f} Bs
   Promedio general: {promedio:.2f} Bs

════════════════════════════════════════════════

💡 INTERPRETACIÓN DEL ALPHA (α = {alpha:.1f}):
   {"• Alta reactividad: La predicción se ajusta rápidamente" if alpha > 0.6 else "• Media reactividad: Balance entre estabilidad y cambio" if alpha > 0.3 else "• Baja reactividad: Predicción suave y estable"}
   {"  a los últimos cambios de precio." if alpha > 0.6 else "  entre datos recientes e históricos." if alpha > 0.3 else "  que ignora fluctuaciones pequeñas."}
   {"• Ideal para mercados volátiles" if alpha > 0.6 else "• Útil para la mayoría de casos" if alpha > 0.3 else "• Mejor para mercados estables"}
            """
            if confianza == "Alta":
                nivel_conf_num = 82.0
            elif confianza == "Media":
                nivel_conf_num = 62.0
            else:
                nivel_conf_num = 38.0
    
    
            tend = tendencia.split()[0]  
    
            
            self.guardar_prediccion(
                id_producto=id_producto,
                precio_estimado=precio_predicho,
                nivel_confianza=nivel_conf_num,
                tendencia=tend,
                fecha_objetivo=fecha_futura,
                modelo_usado=f"Suavizado Exponencial (α={alpha:.1f})"
            )
            text_resultado.delete("1.0", tk.END)
            text_resultado.insert("1.0", resultado_texto)
            text_resultado.config(fg="#e2e8f0")
            
            canvas_grafico.delete("all")
            self.dibujar_grafico_exponencial(canvas_grafico, df_datos, S, precio_predicho, dias_futuro, alpha)
        
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="📉 Calcular Predicción",
            font=("Arial", 11, "bold"), bg="#f59e0b", fg="white",
            command=calcular_exponencial, padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    def dibujar_grafico_exponencial(self, canvas, df_datos, valores_suavizados, precio_pred, dias_futuro, alpha):
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 180
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 180
        
        margin = 50
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        precios_reales = df_datos['precio'].values
        todos_precios = np.append(np.append(precios_reales, valores_suavizados), precio_pred)
        
        precio_min = np.min(todos_precios) * 0.95
        precio_max = np.max(todos_precios) * 1.05
        rango_precio = precio_max - precio_min
        
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)
        
        canvas.create_text(width/2, height-15, text="Tiempo",
            font=("Arial", 9), fill="#94a3b8")
        canvas.create_text(15, height/2, text="Precio",
            font=("Arial", 9), fill="#94a3b8", angle=90)
        
        canvas.create_text(width/2, margin-25, text=f"Suavizado Exponencial (α = {alpha:.1f})",
            font=("Arial", 10, "bold"), fill="#f59e0b")
        
        n_datos = len(df_datos)
        
        puntos_reales = []
        for i in range(n_datos):
            x = margin + (i / (n_datos + dias_futuro)) * graph_width
            precio = precios_reales[i]
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos_reales.append((x, y))
            
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="#64748b", outline="")
        
        if len(puntos_reales) > 1:
            for i in range(len(puntos_reales)-1):
                canvas.create_line(puntos_reales[i], puntos_reales[i+1],
                    fill="#64748b", width=1, dash=(2, 2))
        
        puntos_suavizados = []
        for i in range(len(valores_suavizados)):
            x = margin + (i / (n_datos + dias_futuro)) * graph_width
            precio_s = valores_suavizados[i]
            y = height - margin - ((precio_s - precio_min) / rango_precio) * graph_height
            puntos_suavizados.append((x, y))
            
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="#f59e0b", outline="")
        
        if len(puntos_suavizados) > 1:
            for i in range(len(puntos_suavizados)-1):
                canvas.create_line(puntos_suavizados[i], puntos_suavizados[i+1],
                    fill="#f59e0b", width=2)
        
        x_pred = margin + ((n_datos + dias_futuro - 1) / (n_datos + dias_futuro)) * graph_width
        y_pred = height - margin - ((precio_pred - precio_min) / rango_precio) * graph_height
        
        if puntos_suavizados:
            canvas.create_line(puntos_suavizados[-1], (x_pred, y_pred),
                fill="#10b981", width=2, dash=(5, 5))
            canvas.create_oval(x_pred-5, y_pred-5, x_pred+5, y_pred+5,
                fill="#10b981", outline="#064e3b", width=2)
            canvas.create_text(x_pred, y_pred-12, text=f"{precio_pred:.2f} Bs",
                font=("Arial", 8, "bold"), fill="#10b981")
        
        legend_x = width - margin - 110
        legend_y = margin + 10
        
        canvas.create_rectangle(legend_x-5, legend_y-8, legend_x+105, legend_y+45,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_line(legend_x, legend_y, legend_x+15, legend_y,
            fill="#64748b", width=1, dash=(2, 2))
        canvas.create_text(legend_x+20, legend_y, text="Real",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_line(legend_x, legend_y+15, legend_x+15, legend_y+15,
            fill="#f59e0b", width=2)
        canvas.create_text(legend_x+20, legend_y+15, text="Suavizado",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_line(legend_x, legend_y+30, legend_x+15, legend_y+30,
            fill="#10b981", width=2, dash=(5, 5))
        canvas.create_text(legend_x+20, legend_y+30, text="Predicción",
            font=("Arial", 8), fill="#e2e8f0", anchor="w")
    
    def comparar_modelos(self):
        messagebox.showinfo("En desarrollo",
            "🎯 Comparación de Modelos\n\n"
            "Esta herramienta evaluará la precisión\n"
            "de diferentes modelos y recomendará el mejor.\n\n"
            "Próximamente disponible...")
    
    def detectar_anomalias(self):
        messagebox.showinfo("En desarrollo",
            "🔍 Detección de Anomalías\n\n"
            "Este módulo identificará picos inusuales\n"
            "o valores atípicos en el historial.\n\n"
            "Próximamente disponible...")
    
    def grafico_comparativo(self):
        messagebox.showinfo("En desarrollo",
            "📊 Gráfico Comparativo\n\n"
            "Visualización completa del historial\n"
            "comparado con las predicciones futuras.\n\n"
            "Próximamente disponible...")
    def guardar_prediccion(self, id_producto, precio_estimado, nivel_confianza, 
                      tendencia, fecha_objetivo, modelo_usado):
        
        query = """
        INSERT INTO prediccion (precio_estimado, nivel_confianza, tendencia, 
                           fecha_objetivo, modelo_usado)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_prediccion;
        """
    
        resultado = execute_query(query, (precio_estimado, nivel_confianza, 
                                         tendencia, fecha_objetivo, modelo_usado), 
                                 fetch=True)
    
        if resultado:
            id_pred = resultado[0][0]
            print(f"✓ Predicción guardada con ID: {id_pred}")
    
    def get_id_from_combo(self, combo, df):
        if df is None:
            return None
        valor = combo.get()
        match = df[df['display'] == valor]
        return int(match.iloc[0]['id']) if len(match) > 0 else None
    
    def volver(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()