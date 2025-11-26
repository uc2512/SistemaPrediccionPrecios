import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query
from datetime import datetime, timedelta
import math

class GestionPredicciones:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        # Diccionarios de datos
        self.productos_dict = {}
        self.mercados_dict = {}
        
        self.canvas.delete("all")
        self.cargar_datos_iniciales()
        self.crear_interfaz_principal()
    
    def cargar_datos_iniciales(self):
        """Carga productos y mercados disponibles"""
        # Cargar productos
        query_productos = """
        SELECT id_producto, nombre_producto, unidad_medida
        FROM producto
        WHERE activo = TRUE
        ORDER BY nombre_producto;
        """
        productos = execute_query(query_productos, fetch=True)
        if productos:
            for p in productos:
                self.productos_dict[p[0]] = f"{p[1]} ({p[2]})"
        
        # Cargar mercados
        query_mercados = """
        SELECT id_mercado, nombre_mercado, ciudad
        FROM mercado
        WHERE activo = TRUE
        ORDER BY nombre_mercado;
        """
        mercados = execute_query(query_mercados, fetch=True)
        if mercados:
            for m in mercados:
                nombre = f"{m[1]}"
                if m[2]:
                    nombre += f" - {m[2]}"
                self.mercados_dict[m[0]] = nombre
    
    def crear_interfaz_principal(self):
        """Crea el menú principal de predicciones"""
        # Header
        self.canvas.create_text(450, 30,
            text="🔮 PREDICCIONES DE PRECIOS",
            font=("Arial", 20, "bold"),
            fill="#e2e8f0")
        
        self.canvas.create_text(450, 55,
            text="Proyección inteligente basada en datos históricos",
            font=("Arial", 11),
            fill="#94a3b8")
        
        # Línea divisoria
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        # Verificar si hay datos suficientes
        if not self.productos_dict:
            self.mostrar_sin_datos()
            return
        
        # === TARJETAS DE MODELOS DE PREDICCIÓN ===
        self.canvas.create_text(450, 110,
            text="MODELOS DE PREDICCIÓN DISPONIBLES",
            font=("Arial", 13, "bold"),
            fill="#f59e0b")
        
        y_modelos = 170
        spacing = 80
        
        # Modelo 1: Tendencia Lineal
        self.crear_tarjeta_modelo(
            240, y_modelos,
            "📈",
            "Tendencia Lineal",
            "Predicción simple basada en regresión lineal",
            "#10b981",
            self.prediccion_lineal
        )
        
        # Modelo 2: Media Móvil
        self.crear_tarjeta_modelo(
            660, y_modelos,
            "📊",
            "Media Móvil",
            "Promedio ponderado de precios recientes",
            "#3b82f6",
            self.prediccion_media_movil
        )
        
        # Modelo 3: Estacionalidad
        self.crear_tarjeta_modelo(
            240, y_modelos + spacing,
            "🔄",
            "Análisis Estacional",
            "Detecta patrones que se repiten en el tiempo",
            "#8b5cf6",
            self.prediccion_estacional
        )
        
        # Modelo 4: Suavizado Exponencial
        self.crear_tarjeta_modelo(
            660, y_modelos + spacing,
            "📉",
            "Suavizado Exponencial",
            "Mayor peso a datos más recientes",
            "#f59e0b",
            self.prediccion_exponencial
        )
        
        # === OPCIONES AVANZADAS ===
        self.canvas.create_rectangle(50, 380, 850, 500,
            fill="#1e293b", outline="#334155", width=2)
        
        self.canvas.create_text(450, 400,
            text="⚙️ OPCIONES AVANZADAS",
            font=("Arial", 12, "bold"),
            fill="#64748b")
        
        y_opciones = 435
        
        self.crear_boton_opcion(200, y_opciones, "🎯 Comparar Modelos",
            "Evalúa qué modelo predice mejor", "#06b6d4", self.comparar_modelos)
        
        self.crear_boton_opcion(450, y_opciones, "🔍 Detección de Anomalías",
            "Identifica picos inusuales", "#ec4899", self.detectar_anomalias)
        
        self.crear_boton_opcion(700, y_opciones, "📊 Historial vs Predicción",
            "Gráfico comparativo completo", "#8b5cf6", self.grafico_comparativo)
        
        # === ESTADÍSTICAS RÁPIDAS ===
        self.canvas.create_rectangle(50, 515, 850, 545,
            fill="#1e293b", outline="#334155", width=1)
        
        self.mostrar_estadisticas_prediccion()
        
        # Botón Volver
        self.btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Menú",
            font=("Arial", 11, "bold"),
            bg="#475569", fg="white",
            activebackground="#334155",
            relief=tk.FLAT, cursor="hand2",
            padx=20, pady=8,
            command=self.volver
        )
        self.btn_volver.place(x=380, y=565)
    
    def crear_tarjeta_modelo(self, x, y, icono, titulo, descripcion, color, comando):
        """Crea una tarjeta de modelo de predicción"""
        tag = f"modelo_{x}_{y}"
        
        # Fondo
        rect_id = self.canvas.create_rectangle(x-180, y-25, x+180, y+25,
            fill="#0f172a", outline=color, width=2, tags=tag)
        
        # Icono
        self.canvas.create_text(x-140, y,
            text=icono,
            font=("Arial", 20),
            fill=color, tags=tag)
        
        # Título
        self.canvas.create_text(x-20, y-8,
            text=titulo,
            font=("Arial", 11, "bold"),
            fill="#e2e8f0",
            anchor="w", tags=tag)
        
        # Descripción
        self.canvas.create_text(x-20, y+10,
            text=descripcion,
            font=("Arial", 8),
            fill="#64748b",
            anchor="w", tags=tag)
        
        # Eventos
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
        """Crea un botón de opción avanzada"""
        tag = f"opcion_{x}_{y}"
        
        rect_id = self.canvas.create_rectangle(x-110, y-22, x+110, y+22,
            fill="#0f172a", outline=color, width=1, tags=tag)
        
        self.canvas.create_text(x, y-8,
            text=titulo,
            font=("Arial", 9, "bold"),
            fill="#e2e8f0", tags=tag)
        
        self.canvas.create_text(x, y+8,
            text=descripcion,
            font=("Arial", 7),
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
        """Muestra estadísticas sobre capacidad de predicción"""
        # Contar registros en historial
        query = "SELECT COUNT(*) FROM historial_p;"
        result = execute_query(query, fetch=True)
        num_historial = result[0][0] if result else 0
        
        # Contar ofertas activas
        query2 = "SELECT COUNT(*) FROM oferta;"
        result2 = execute_query(query2, fetch=True)
        num_ofertas = result2[0][0] if result2 else 0
        
        # Determinar capacidad de predicción
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
        
        self.canvas.create_text(450, 530,
            text=stats_text,
            font=("Arial", 9),
            fill=color)
    
    def mostrar_sin_datos(self):
        """Muestra mensaje cuando no hay datos suficientes"""
        self.canvas.create_rectangle(200, 200, 700, 350,
            fill="#1e293b", outline="#f59e0b", width=2)
        
        self.canvas.create_text(450, 240,
            text="⚠️ DATOS INSUFICIENTES",
            font=("Arial", 16, "bold"),
            fill="#f59e0b")
        
        self.canvas.create_text(450, 280,
            text="Para realizar predicciones necesitas:",
            font=("Arial", 11),
            fill="#94a3b8")
        
        self.canvas.create_text(450, 305,
            text="• Al menos 1 producto registrado",
            font=("Arial", 10),
            fill="#e2e8f0", anchor="center")
        
        self.canvas.create_text(450, 325,
            text="• Al menos 5 registros de precios históricos",
            font=("Arial", 10),
            fill="#e2e8f0", anchor="center")
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Menú",
            font=("Arial", 11, "bold"),
            bg="#475569", fg="white",
            command=self.volver,
            padx=20, pady=8
        )
        btn_volver.place(x=380, y=400)
    
    # ========== MODELOS DE PREDICCIÓN ==========
    
    def prediccion_lineal(self):
        """Predicción usando regresión lineal simple"""
        # Crear ventana de predicción
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Tendencia Lineal")
        ventana.geometry("900x650")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        # Header
        tk.Label(ventana,
            text="📈 PREDICCIÓN POR TENDENCIA LINEAL",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana,
            text="Proyección futura basada en regresión lineal de datos históricos",
            font=("Arial", 10),
            bg="#0a0f1e", fg="#94a3b8").pack()
        
        # Frame de selección
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        # Seleccionar producto
        tk.Label(frame_seleccion,
            text="Producto:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=list(self.productos_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        # Seleccionar mercado (opcional)
        tk.Label(frame_seleccion,
            text="Mercado:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        mercados_lista = ["Todos los mercados"] + list(self.mercados_dict.values())
        combo_mercado = ttk.Combobox(frame_seleccion,
            values=mercados_lista,
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        # Días a predecir
        tk.Label(frame_seleccion,
            text="Días a predecir:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        spin_dias = tk.Spinbox(frame_seleccion,
            from_=1, to=90,
            font=("Arial", 10),
            width=10,
            bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Frame de resultados (CON ALTURA FIJA)
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=350)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)  # ✅ Evita que crezca
        
        # Canvas para gráfico simple
        canvas_grafico = tk.Canvas(frame_resultados,
            bg="#0f172a",
            highlightthickness=0,
            height=200)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        # Label de resultados (CON SCROLL SI ES NECESARIO)
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        label_resultado = tk.Text(frame_texto,
            font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8",
            wrap=tk.WORD,
            height=8,
            yscrollcommand=scrollbar.set)
        label_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=label_resultado.yview)
        
        label_resultado.insert("1.0", "Selecciona un producto y presiona 'Calcular Predicción'")
        
        def calcular_prediccion():
            """Calcula la predicción lineal"""
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            # Obtener ID del producto
            id_producto = self.get_id_from_combo(combo_producto, self.productos_dict)
            dias_futuro = int(spin_dias.get())
            
            # ✅ CONSULTA CORREGIDA - Obtiene TODOS los precios del historial
            if combo_mercado.get() == "Todos los mercados":
                query = """
                WITH todos_precios AS (
                    -- Intentar extraer el precio NUEVO (después de "a")
                    SELECT 
                        h.fecha_registro::timestamp as fecha_completa,
                        NULLIF(
                            REGEXP_REPLACE(
                                SUBSTRING(h.observaciones FROM 'a ([0-9]+\\.?[0-9]*) Bs'),
                                '[^0-9.]', '', 'g'
                            ),
                            ''
                        )::DECIMAL(10,2) as precio_nuevo,
                        -- Intentar extraer el precio VIEJO (antes de "de")
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
                    -- Crear 2 filas por cada cambio: precio viejo y nuevo
                    SELECT fecha_completa, precio_viejo as precio
                    FROM todos_precios
                    WHERE precio_viejo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT fecha_completa, precio_nuevo as precio
                    FROM todos_precios
                    WHERE precio_nuevo IS NOT NULL
                    
                    UNION ALL
                    
                    -- Agregar precio actual
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_expandidos
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_producto)
            else:
                id_mercado = self.get_id_from_combo(combo_mercado, self.mercados_dict)
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
                    SELECT 
                        fecha_completa,
                        precio_viejo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_viejo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        fecha_completa,
                        precio_nuevo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_nuevo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                      AND o.id_mercado = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_mercado
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_mercado, id_mercado, id_producto, id_mercado)
            
            datos = execute_query(query, params, fetch=True)
            
            if not datos or len(datos) < 3:
                messagebox.showwarning("Datos insuficientes",
                    "Se necesitan al menos 3 registros históricos para predecir.\n\n"
                    f"Registros encontrados: {len(datos) if datos else 0}")
                return
            
            # Calcular regresión lineal
            n = len(datos)
            suma_x = sum(range(n))
            suma_y = sum(float(d[1]) for d in datos)
            suma_xy = sum(i * float(d[1]) for i, d in enumerate(datos))
            suma_x2 = sum(i**2 for i in range(n))
            
            # Pendiente (m) e intersección (b) de y = mx + b
            m = (n * suma_xy - suma_x * suma_y) / (n * suma_x2 - suma_x**2)
            b = (suma_y - m * suma_x) / n
            
            # Precio actual (último dato)
            precio_actual = float(datos[-1][1])
            fecha_actual = datos[-1][0]
            
            # Predicción futura
            precio_predicho = m * (n + dias_futuro - 1) + b
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            
            # Calcular tendencia
            if m > 0.1:
                tendencia = "ALCISTA 📈"
                color_tend = "#10b981"
            elif m < -0.1:
                tendencia = "BAJISTA 📉"
                color_tend = "#dc2626"
            else:
                tendencia = "ESTABLE ➡️"
                color_tend = "#3b82f6"
            
            # Calcular margen de error (desviación estándar simplificada)
            errores = [float(d[1]) - (m * i + b) for i, d in enumerate(datos)]
            mse = sum(e**2 for e in errores) / n
            std_error = math.sqrt(mse)
            
            # Mostrar resultados
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
            
            label_resultado.delete("1.0", tk.END)
            label_resultado.insert("1.0", resultado_texto)
            label_resultado.config(fg="#e2e8f0")
            
            # Dibujar gráfico simple en canvas
            canvas_grafico.delete("all")
            self.dibujar_grafico_simple(canvas_grafico, datos, m, b, dias_futuro, precio_predicho)
        
        # Botones
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones,
            text="🔮 Calcular Predicción",
            font=("Arial", 11, "bold"),
            bg="#10b981", fg="white",
            command=calcular_prediccion,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    
    def dibujar_grafico_simple(self, canvas, datos, m, b, dias_futuro, precio_final):
        """Dibuja un gráfico simple de la predicción"""
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 400
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 400
        
        margin = 60
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        # Fondo del gráfico
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        # Encontrar rango de precios
        precios = [float(d[1]) for d in datos]
        precios.append(precio_final)
        
        precio_min = min(precios) * 0.95
        precio_max = max(precios) * 1.05
        rango_precio = precio_max - precio_min
        
        # Dibujar ejes
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)  # Eje X
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)  # Eje Y
        
        # Labels
        canvas.create_text(width/2, height-20,
            text="Tiempo (días)",
            font=("Arial", 10),
            fill="#94a3b8")
        
        canvas.create_text(20, height/2,
            text="Precio (Bs)",
            font=("Arial", 10),
            fill="#94a3b8",
            angle=90)
        
        # Dibujar datos históricos
        n_datos = len(datos)
        total_puntos = n_datos + dias_futuro
        
        puntos_historicos = []
        for i, dato in enumerate(datos):
            x = margin + (i / total_puntos) * graph_width
            precio = float(dato[1])
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos_historicos.append((x, y))
            
            # Punto
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="#3b82f6", outline="")
        
        # Línea histórica
        if len(puntos_historicos) > 1:
            for i in range(len(puntos_historicos)-1):
                canvas.create_line(puntos_historicos[i], puntos_historicos[i+1],
                    fill="#3b82f6", width=2)
        
        # Dibujar predicción
        x_pred = margin + ((n_datos + dias_futuro - 1) / total_puntos) * graph_width
        y_pred = height - margin - ((precio_final - precio_min) / rango_precio) * graph_height
        
        # Línea de predicción
        if puntos_historicos:
            canvas.create_line(puntos_historicos[-1], (x_pred, y_pred),
                fill="#10b981", width=2, dash=(5, 5))
            
            # Punto predicho
            canvas.create_oval(x_pred-5, y_pred-5, x_pred+5, y_pred+5,
                fill="#10b981", outline="#064e3b", width=2)
            
            # Label predicción
            canvas.create_text(x_pred, y_pred-15,
                text=f"{precio_final:.2f} Bs",
                font=("Arial", 9, "bold"),
                fill="#10b981")
        
        # Leyenda
        legend_x = width - margin - 150
        legend_y = margin + 20
        
        canvas.create_rectangle(legend_x-10, legend_y-15, legend_x+140, legend_y+35,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_line(legend_x, legend_y, legend_x+20, legend_y,
            fill="#3b82f6", width=2)
        canvas.create_text(legend_x+30, legend_y,
            text="Histórico",
            font=("Arial", 9),
            fill="#e2e8f0",
            anchor="w")
        
        canvas.create_line(legend_x, legend_y+20, legend_x+20, legend_y+20,
            fill="#10b981", width=2, dash=(5, 5))
        canvas.create_text(legend_x+30, legend_y+20,
            text="Predicción",
            font=("Arial", 9),
            fill="#e2e8f0",
            anchor="w")
    
    def prediccion_media_movil(self):
        """Predicción usando media móvil simple"""
        # Crear ventana
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Media Móvil")
        ventana.geometry("900x650")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        # Header
        tk.Label(ventana,
            text="📊 PREDICCIÓN POR MEDIA MÓVIL",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana,
            text="Promedio de los últimos N días para proyectar el futuro",
            font=("Arial", 10),
            bg="#0a0f1e", fg="#94a3b8").pack()
        
        # Frame de selección
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        # Producto
        tk.Label(frame_seleccion,
            text="Producto:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=list(self.productos_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        # Mercado
        tk.Label(frame_seleccion,
            text="Mercado:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        mercados_lista = ["Todos los mercados"] + list(self.mercados_dict.values())
        combo_mercado = ttk.Combobox(frame_seleccion,
            values=mercados_lista,
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        # Ventana de días (cuántos días promediar)
        tk.Label(frame_seleccion,
            text="Ventana (días):",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        spin_ventana = tk.Spinbox(frame_seleccion,
            from_=3, to=30,
            font=("Arial", 10),
            width=10,
            bg="#0f172a", fg="white")
        spin_ventana.delete(0, tk.END)
        spin_ventana.insert(0, "7")  # 7 días por defecto
        spin_ventana.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(frame_seleccion,
            text="(Últimos N días para calcular el promedio)",
            font=("Arial", 8, "italic"),
            bg="#1e293b", fg="#64748b").grid(row=1, column=2, columnspan=2, sticky="w")
        
        # Días a predecir
        tk.Label(frame_seleccion,
            text="Días a predecir:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        spin_dias = tk.Spinbox(frame_seleccion,
            from_=1, to=90,
            font=("Arial", 10),
            width=10,
            bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Frame de resultados
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=350)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)
        
        # Canvas para gráfico
        canvas_grafico = tk.Canvas(frame_resultados,
            bg="#0f172a",
            highlightthickness=0,
            height=200)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        # Text widget para resultados
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_resultado = tk.Text(frame_texto,
            font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8",
            wrap=tk.WORD,
            height=8,
            yscrollcommand=scrollbar.set)
        text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_resultado.yview)
        
        text_resultado.insert("1.0", "Selecciona un producto y presiona 'Calcular Predicción'")
        
        def calcular_media_movil():
            """Calcula la predicción por media móvil"""
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            id_producto = self.get_id_from_combo(combo_producto, self.productos_dict)
            dias_futuro = int(spin_dias.get())
            ventana_dias = int(spin_ventana.get())
            
            # Obtener datos históricos (misma consulta que predicción lineal)
            if combo_mercado.get() == "Todos los mercados":
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
                    
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_expandidos
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_producto)
            else:
                id_mercado = self.get_id_from_combo(combo_mercado, self.mercados_dict)
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
                    SELECT 
                        fecha_completa,
                        precio_viejo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_viejo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        fecha_completa,
                        precio_nuevo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_nuevo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                      AND o.id_mercado = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_mercado
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_mercado, id_mercado, id_producto, id_mercado)
            
            datos = execute_query(query, params, fetch=True)
            
            if not datos or len(datos) < ventana_dias:
                messagebox.showwarning("Datos insuficientes",
                    f"Se necesitan al menos {ventana_dias} registros para calcular la media móvil.\n\n"
                    f"Registros encontrados: {len(datos) if datos else 0}")
                return
            
            # Calcular media móvil de los últimos N días
            precios = [float(d[1]) for d in datos]
            ultimos_precios = precios[-ventana_dias:]  # Últimos N días
            
            media_movil = sum(ultimos_precios) / ventana_dias
            
            # Precio actual
            precio_actual = float(datos[-1][1])
            fecha_actual = datos[-1][0]
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            
            # Calcular volatilidad (desviación estándar)
            promedio = sum(precios) / len(precios)
            varianza = sum((p - promedio) ** 2 for p in precios) / len(precios)
            volatilidad = math.sqrt(varianza)
            
            # Determinar confianza
            if volatilidad < 1:
                confianza = "Alta"
                color_conf = "#10b981"
            elif volatilidad < 3:
                confianza = "Media"
                color_conf = "#f59e0b"
            else:
                confianza = "Baja"
                color_conf = "#dc2626"
            
            # Mostrar resultados
            resultado_texto = f"""
📊 RESULTADOS - MEDIA MÓVIL SIMPLE

Producto: {combo_producto.get()}
Mercado: {combo_mercado.get()}
Ventana de análisis: {ventana_dias} días
Total de datos históricos: {len(datos)}

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
   Precio min histórico: {min(precios):.2f} Bs
   Precio max histórico: {max(precios):.2f} Bs
   Promedio general: {promedio:.2f} Bs

💡 INTERPRETACIÓN:
   La media móvil simple asume que el precio futuro será
   el promedio de los últimos {ventana_dias} días. Este modelo
   funciona mejor en mercados estables sin tendencias fuertes.
            """
            
            text_resultado.delete("1.0", tk.END)
            text_resultado.insert("1.0", resultado_texto)
            text_resultado.config(fg="#e2e8f0")
            
            # Dibujar gráfico
            canvas_grafico.delete("all")
            self.dibujar_grafico_media_movil(canvas_grafico, datos, media_movil, ventana_dias, dias_futuro)
        
        # Botones
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones,
            text="📊 Calcular Predicción",
            font=("Arial", 11, "bold"),
            bg="#3b82f6", fg="white",
            command=calcular_media_movil,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    
    def dibujar_grafico_media_movil(self, canvas, datos, media_movil, ventana_dias, dias_futuro):
        """Dibuja gráfico de media móvil"""
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 200
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 200
        
        margin = 50
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        # Fondo
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        # Rango de precios
        precios = [float(d[1]) for d in datos]
        precios.append(media_movil)
        
        precio_min = min(precios) * 0.95
        precio_max = max(precios) * 1.05
        rango_precio = precio_max - precio_min
        
        # Ejes
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)
        
        # Labels
        canvas.create_text(width/2, height-15,
            text="Tiempo", font=("Arial", 9), fill="#94a3b8")
        canvas.create_text(15, height/2,
            text="Precio", font=("Arial", 9), fill="#94a3b8", angle=90)
        
        # Dibujar datos históricos
        n_datos = len(datos)
        puntos = []
        for i, dato in enumerate(datos):
            x = margin + (i / (n_datos + dias_futuro)) * graph_width
            precio = float(dato[1])
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos.append((x, y))
            
            # Resaltar últimos ventana_dias días
            if i >= n_datos - ventana_dias:
                canvas.create_oval(x-4, y-4, x+4, y+4, fill="#f59e0b", outline="")
            else:
                canvas.create_oval(x-2, y-2, x+2, y+2, fill="#64748b", outline="")
        
        # Línea histórica
        if len(puntos) > 1:
            for i in range(len(puntos)-1):
                color = "#f59e0b" if i >= n_datos - ventana_dias - 1 else "#64748b"
                canvas.create_line(puntos[i], puntos[i+1], fill=color, width=2)
        
        # Línea de predicción (horizontal)
        x_pred = margin + ((n_datos + dias_futuro - 1) / (n_datos + dias_futuro)) * graph_width
        y_pred = height - margin - ((media_movil - precio_min) / rango_precio) * graph_height
        
        if puntos:
            canvas.create_line(puntos[-1], (x_pred, y_pred),
                fill="#3b82f6", width=2, dash=(5, 5))
            canvas.create_oval(x_pred-5, y_pred-5, x_pred+5, y_pred+5,
                fill="#3b82f6", outline="#1e40af", width=2)
            canvas.create_text(x_pred, y_pred-12,
                text=f"{media_movil:.2f} Bs",
                font=("Arial", 8, "bold"),
                fill="#3b82f6")
        
        # Leyenda
        legend_x = width - margin - 120
        legend_y = margin + 15
        
        canvas.create_rectangle(legend_x-5, legend_y-10, legend_x+115, legend_y+40,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_oval(legend_x, legend_y-3, legend_x+6, legend_y+3,
            fill="#64748b", outline="")
        canvas.create_text(legend_x+15, legend_y,
            text="Histórico", font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_oval(legend_x, legend_y+12, legend_x+6, legend_y+18,
            fill="#f59e0b", outline="")
        canvas.create_text(legend_x+15, legend_y+15,
            text=f"Ventana ({ventana_dias}d)", font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_line(legend_x, legend_y+30, legend_x+15, legend_y+30,
            fill="#3b82f6", width=2, dash=(3, 3))
        canvas.create_text(legend_x+20, legend_y+30,
            text="Predicción", font=("Arial", 8), fill="#e2e8f0", anchor="w")
    
    def prediccion_estacional(self):
        """Análisis de patrones estacionales"""
        # Crear ventana
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Análisis Estacional")
        ventana.geometry("900x700")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        # Header
        tk.Label(ventana,
            text="🔄 ANÁLISIS ESTACIONAL",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana,
            text="Detecta patrones que se repiten en ciclos de tiempo",
            font=("Arial", 10),
            bg="#0a0f1e", fg="#94a3b8").pack()
        
        # Frame de selección
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        # Producto
        tk.Label(frame_seleccion,
            text="Producto:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=list(self.productos_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        # Mercado
        tk.Label(frame_seleccion,
            text="Mercado:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        mercados_lista = ["Todos los mercados"] + list(self.mercados_dict.values())
        combo_mercado = ttk.Combobox(frame_seleccion,
            values=mercados_lista,
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        # Tipo de ciclo
        tk.Label(frame_seleccion,
            text="Ciclo a analizar:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        combo_ciclo = ttk.Combobox(frame_seleccion,
            values=["Semanal (7 días)", "Quincenal (15 días)", "Mensual (30 días)"],
            state="readonly",
            font=("Arial", 10),
            width=25)
        combo_ciclo.current(0)
        combo_ciclo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(frame_seleccion,
            text="(Patrón que se repite cada N días)",
            font=("Arial", 8, "italic"),
            bg="#1e293b", fg="#64748b").grid(row=1, column=2, columnspan=2, sticky="w")
        
        # Días a predecir
        tk.Label(frame_seleccion,
            text="Días a predecir:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        spin_dias = tk.Spinbox(frame_seleccion,
            from_=1, to=90,
            font=("Arial", 10),
            width=10,
            bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Explicación
        frame_info = tk.Frame(ventana, bg="#1a1f2e")
        frame_info.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(frame_info,
            text="💡 ¿Qué es el Análisis Estacional?",
            font=("Arial", 9, "bold"),
            bg="#1a1f2e", fg="#8b5cf6").pack(anchor="w", padx=10, pady=5)
        
        info_text = """    Este modelo busca patrones repetitivos en los precios:
    • Semanal: ¿Los lunes son más caros? ¿Los domingos más baratos?
    • Quincenal: ¿Sube a mitad de mes cuando la gente cobra?
    • Mensual: ¿Ciclos relacionados con cosechas o temporadas?
    
    La predicción se basa en promedios de cada día del ciclo."""
        
        tk.Label(frame_info,
            text=info_text,
            font=("Arial", 8),
            bg="#1a1f2e", fg="#94a3b8",
            justify=tk.LEFT).pack(anchor="w", padx=20)
        
        # Frame de resultados
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=320)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)
        
        # Canvas para gráfico
        canvas_grafico = tk.Canvas(frame_resultados,
            bg="#0f172a",
            highlightthickness=0,
            height=180)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        # Text widget para resultados
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_resultado = tk.Text(frame_texto,
            font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8",
            wrap=tk.WORD,
            height=6,
            yscrollcommand=scrollbar.set)
        text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_resultado.yview)
        
        text_resultado.insert("1.0", "Selecciona un producto y presiona 'Analizar Estacionalidad'")
        
        def calcular_estacional():
            """Calcula la predicción estacional"""
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            id_producto = self.get_id_from_combo(combo_producto, self.productos_dict)
            dias_futuro = int(spin_dias.get())
            
            # Determinar longitud del ciclo
            ciclo_texto = combo_ciclo.get()
            if "Semanal" in ciclo_texto:
                longitud_ciclo = 7
                nombre_ciclo = "Semanal"
                dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            elif "Quincenal" in ciclo_texto:
                longitud_ciclo = 15
                nombre_ciclo = "Quincenal"
                dias_nombres = [f"Día {i+1}" for i in range(15)]
            else:  # Mensual
                longitud_ciclo = 30
                nombre_ciclo = "Mensual"
                dias_nombres = [f"Día {i+1}" for i in range(30)]
            
            # Obtener datos históricos
            if combo_mercado.get() == "Todos los mercados":
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
                    
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_expandidos
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_producto)
            else:
                id_mercado = self.get_id_from_combo(combo_mercado, self.mercados_dict)
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
                    SELECT 
                        fecha_completa,
                        precio_viejo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_viejo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        fecha_completa,
                        precio_nuevo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_nuevo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                      AND o.id_mercado = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_mercado
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_mercado, id_mercado, id_producto, id_mercado)
            
            datos = execute_query(query, params, fetch=True)
            
            if not datos or len(datos) < longitud_ciclo:
                messagebox.showwarning("Datos insuficientes",
                    f"Se necesitan al menos {longitud_ciclo} registros para análisis {nombre_ciclo.lower()}.\n\n"
                    f"Registros encontrados: {len(datos) if datos else 0}")
                return
            
            # Calcular promedio por posición en el ciclo
            from collections import defaultdict
            promedios_ciclo = defaultdict(list)
            
            for i, dato in enumerate(datos):
                posicion_ciclo = i % longitud_ciclo
                precio = float(dato[1])
                promedios_ciclo[posicion_ciclo].append(precio)
            
            # Calcular promedio de cada posición
            patron_estacional = {}
            for pos in range(longitud_ciclo):
                if pos in promedios_ciclo and promedios_ciclo[pos]:
                    patron_estacional[pos] = sum(promedios_ciclo[pos]) / len(promedios_ciclo[pos])
                else:
                    # Si no hay datos para esa posición, usar el promedio general
                    todos_precios = [float(d[1]) for d in datos]
                    patron_estacional[pos] = sum(todos_precios) / len(todos_precios)
            
            # Precio actual
            precio_actual = float(datos[-1][1])
            fecha_actual = datos[-1][0]
            posicion_actual = (len(datos) - 1) % longitud_ciclo
            
            # Predecir para días futuros
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            posicion_futura = (len(datos) + dias_futuro - 1) % longitud_ciclo
            precio_predicho = patron_estacional[posicion_futura]
            
            # Calcular variabilidad del patrón
            varianzas = []
            for pos in range(longitud_ciclo):
                if pos in promedios_ciclo and len(promedios_ciclo[pos]) > 1:
                    prom = patron_estacional[pos]
                    var = sum((p - prom) ** 2 for p in promedios_ciclo[pos]) / len(promedios_ciclo[pos])
                    varianzas.append(math.sqrt(var))
            
            variabilidad = sum(varianzas) / len(varianzas) if varianzas else 1.0
            
            # Determinar si el patrón es fuerte
            precios_todos = [float(d[1]) for d in datos]
            rango_precios = max(precios_todos) - min(precios_todos)
            rango_patron = max(patron_estacional.values()) - min(patron_estacional.values())
            
            fuerza_patron = (rango_patron / rango_precios * 100) if rango_precios > 0 else 0
            
            if fuerza_patron > 15:
                interpretacion = "PATRÓN FUERTE detectado"
                color_patron = "#10b981"
                confianza = "Alta"
            elif fuerza_patron > 5:
                interpretacion = "PATRÓN MODERADO detectado"
                color_patron = "#f59e0b"
                confianza = "Media"
            else:
                interpretacion = "PATRÓN DÉBIL o inexistente"
                color_patron = "#dc2626"
                confianza = "Baja"
            
            # Encontrar día más caro y más barato del ciclo
            pos_max = max(patron_estacional, key=patron_estacional.get)
            pos_min = min(patron_estacional, key=patron_estacional.get)
            
            # Determinar tendencia
            if precio_predicho > precio_actual * 1.02:
                tendencia = "ALCISTA 📈"
            elif precio_predicho < precio_actual * 0.98:
                tendencia = "BAJISTA 📉"
            else:
                tendencia = "ESTABLE ➡️"
            
            # Mostrar resultados
            resultado_texto = f"""
🔄 RESULTADOS - ANÁLISIS ESTACIONAL {nombre_ciclo.upper()}

Producto: {combo_producto.get()}
Mercado: {combo_mercado.get()}
Tipo de ciclo: {nombre_ciclo} ({longitud_ciclo} días)
Datos históricos: {len(datos)} registros

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
   
   Precio min histórico: {min(precios_todos):.2f} Bs
   Precio max histórico: {max(precios_todos):.2f} Bs
   Promedio general: {sum(precios_todos)/len(precios_todos):.2f} Bs

💡 INTERPRETACIÓN:
   {"Este producto muestra un patrón claro que se repite" if fuerza_patron > 15 else "El patrón es débil, los precios varían más por" if fuerza_patron > 5 else "No hay patrón estacional significativo. Los precios"}
   {"cada " + nombre_ciclo.lower() + ". Usa este patrón para planificar" if fuerza_patron > 15 else "otros factores que por el ciclo " + nombre_ciclo.lower() + "." if fuerza_patron > 5 else "parecen variar por razones no cíclicas."}
   {"compras en días baratos y ventas en días caros." if fuerza_patron > 15 else "Considera otros modelos de predicción." if fuerza_patron > 5 else ""}
            """
            
            text_resultado.delete("1.0", tk.END)
            text_resultado.insert("1.0", resultado_texto)
            text_resultado.config(fg="#e2e8f0")
            
            # Dibujar gráfico
            canvas_grafico.delete("all")
            self.dibujar_grafico_estacional(canvas_grafico, datos, patron_estacional, 
                                           longitud_ciclo, dias_nombres, precio_predicho, 
                                           posicion_futura, dias_futuro)
        
        # Botones
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones,
            text="🔄 Analizar Estacionalidad",
            font=("Arial", 11, "bold"),
            bg="#8b5cf6", fg="white",
            command=calcular_estacional,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    
    def dibujar_grafico_estacional(self, canvas, datos, patron, longitud_ciclo, nombres_dias, precio_pred, pos_pred, dias_futuro):
        """Dibuja gráfico del patrón estacional"""
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 180
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 180
        
        margin = 50
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        # Fondo
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        # Rango de precios
        precios_patron = list(patron.values())
        precios_patron.append(precio_pred)
        
        precio_min = min(precios_patron) * 0.95
        precio_max = max(precios_patron) * 1.05
        rango_precio = precio_max - precio_min
        
        # Ejes
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)
        
        # Labels
        canvas.create_text(width/2, height-15,
            text="Posición en el ciclo", font=("Arial", 9), fill="#94a3b8")
        canvas.create_text(15, height/2,
            text="Precio", font=("Arial", 9), fill="#94a3b8", angle=90)
        
        # Título
        canvas.create_text(width/2, margin-25,
            text=f"Patrón Estacional (Ciclo: {longitud_ciclo} días)",
            font=("Arial", 10, "bold"),
            fill="#8b5cf6")
        
        # Dibujar patrón estacional
        puntos_patron = []
        for pos in range(longitud_ciclo):
            x = margin + (pos / longitud_ciclo) * graph_width
            precio = patron[pos]
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos_patron.append((x, y))
            
            # Punto morado
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="#8b5cf6", outline="")
        
        # Línea del patrón
        if len(puntos_patron) > 1:
            for i in range(len(puntos_patron)):
                inicio = puntos_patron[i]
                fin = puntos_patron[(i+1) % longitud_ciclo]
                canvas.create_line(inicio, fin, fill="#8b5cf6", width=2)
        
        # Marcar posición de predicción
        x_pred = margin + (pos_pred / longitud_ciclo) * graph_width
        y_pred = height - margin - ((precio_pred - precio_min) / rango_precio) * graph_height
        
        # Círculo grande para predicción
        canvas.create_oval(x_pred-6, y_pred-6, x_pred+6, y_pred+6,
            fill="#10b981", outline="#064e3b", width=2)
        
        canvas.create_text(x_pred, y_pred-15,
            text=f"{precio_pred:.2f} Bs",
            font=("Arial", 8, "bold"),
            fill="#10b981")
        
        # Marcar picos (máx y mín)
        pos_max = max(patron, key=patron.get)
        pos_min = min(patron, key=patron.get)
        
        x_max = margin + (pos_max / longitud_ciclo) * graph_width
        y_max = height - margin - ((patron[pos_max] - precio_min) / rango_precio) * graph_height
        
        x_min = margin + (pos_min / longitud_ciclo) * graph_width
        y_min = height - margin - ((patron[pos_min] - precio_min) / rango_precio) * graph_height
        
        # Etiquetas para máx/mín
        canvas.create_text(x_max, y_max+15,
            text="↑ MÁX",
            font=("Arial", 7, "bold"),
            fill="#dc2626")
        
        canvas.create_text(x_min, y_min-15,
            text="↓ MÍN",
            font=("Arial", 7, "bold"),
            fill="#10b981")
        
        # Leyenda
        legend_x = width - margin - 90
        legend_y = margin + 10
        
        canvas.create_rectangle(legend_x-5, legend_y-8, legend_x+85, legend_y+30,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_oval(legend_x, legend_y-2, legend_x+6, legend_y+4,
            fill="#8b5cf6", outline="")
        canvas.create_text(legend_x+15, legend_y,
            text="Patrón", font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_oval(legend_x-1, legend_y+13, legend_x+7, legend_y+21,
            fill="#10b981", outline="#064e3b", width=1)
        canvas.create_text(legend_x+15, legend_y+17,
            text="Predicción", font=("Arial", 8), fill="#e2e8f0", anchor="w")
    
    def prediccion_exponencial(self):
        """Predicción con suavizado exponencial simple"""
        # Crear ventana
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Predicción - Suavizado Exponencial")
        ventana.geometry("900x700")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        # Header
        tk.Label(ventana,
            text="📉 PREDICCIÓN POR SUAVIZADO EXPONENCIAL",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana,
            text="Mayor peso a datos recientes para predicciones más precisas",
            font=("Arial", 10),
            bg="#0a0f1e", fg="#94a3b8").pack()
        
        # Frame de selección
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=15)
        
        # Producto
        tk.Label(frame_seleccion,
            text="Producto:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        combo_producto = ttk.Combobox(frame_seleccion,
            values=list(self.productos_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_producto.grid(row=0, column=1, padx=10, pady=5)
        
        # Mercado
        tk.Label(frame_seleccion,
            text="Mercado:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        mercados_lista = ["Todos los mercados"] + list(self.mercados_dict.values())
        combo_mercado = ttk.Combobox(frame_seleccion,
            values=mercados_lista,
            state="readonly",
            font=("Arial", 10),
            width=30)
        combo_mercado.current(0)
        combo_mercado.grid(row=0, column=3, padx=10, pady=5)
        
        # Alpha (factor de suavizado)
        tk.Label(frame_seleccion,
            text="Factor α (alpha):",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # Slider para alpha
        frame_alpha = tk.Frame(frame_seleccion, bg="#1e293b")
        frame_alpha.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        alpha_var = tk.DoubleVar(value=0.3)
        
        scale_alpha = tk.Scale(frame_alpha,
            from_=0.1, to=0.9,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=alpha_var,
            bg="#0f172a", fg="white",
            highlightthickness=0,
            length=150)
        scale_alpha.pack(side=tk.LEFT)
        
        label_alpha_val = tk.Label(frame_alpha,
            text=f"α = {alpha_var.get():.1f}",
            font=("Arial", 9),
            bg="#1e293b", fg="#f59e0b")
        label_alpha_val.pack(side=tk.LEFT, padx=5)
        
        def update_alpha_label(*args):
            label_alpha_val.config(text=f"α = {alpha_var.get():.1f}")
        
        alpha_var.trace("w", update_alpha_label)
        
        tk.Label(frame_seleccion,
            text="Bajo: más suave | Alto: más reactivo",
            font=("Arial", 8, "italic"),
            bg="#1e293b", fg="#64748b").grid(row=1, column=2, columnspan=2, sticky="w")
        
        # Días a predecir
        tk.Label(frame_seleccion,
            text="Días a predecir:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        spin_dias = tk.Spinbox(frame_seleccion,
            from_=1, to=90,
            font=("Arial", 10),
            width=10,
            bg="#0f172a", fg="white")
        spin_dias.delete(0, tk.END)
        spin_dias.insert(0, "30")
        spin_dias.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Explicación del parámetro alpha
        frame_info = tk.Frame(ventana, bg="#1a1f2e")
        frame_info.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(frame_info,
            text="💡 ¿Qué es Alpha (α)?",
            font=("Arial", 9, "bold"),
            bg="#1a1f2e", fg="#f59e0b").pack(anchor="w", padx=10, pady=5)
        
        info_text = """    Alpha controla cuánto peso se da a los datos recientes:
    • α bajo (0.1-0.3): Predicción más suave, menos sensible a cambios bruscos
    • α medio (0.4-0.6): Balance entre estabilidad y reactividad
    • α alto (0.7-0.9): Muy reactivo, sigue de cerca los últimos cambios"""
        
        tk.Label(frame_info,
            text=info_text,
            font=("Arial", 8),
            bg="#1a1f2e", fg="#94a3b8",
            justify=tk.LEFT).pack(anchor="w", padx=20)
        
        # Frame de resultados
        frame_resultados = tk.Frame(ventana, bg="#1e293b", height=320)
        frame_resultados.pack(fill=tk.BOTH, padx=20, pady=10)
        frame_resultados.pack_propagate(False)
        
        # Canvas para gráfico
        canvas_grafico = tk.Canvas(frame_resultados,
            bg="#0f172a",
            highlightthickness=0,
            height=180)
        canvas_grafico.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        # Text widget para resultados
        frame_texto = tk.Frame(frame_resultados, bg="#1e293b")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_resultado = tk.Text(frame_texto,
            font=("Courier", 9),
            bg="#1e293b", fg="#94a3b8",
            wrap=tk.WORD,
            height=6,
            yscrollcommand=scrollbar.set)
        text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_resultado.yview)
        
        text_resultado.insert("1.0", "Selecciona un producto y presiona 'Calcular Predicción'")
        
        def calcular_exponencial():
            """Calcula la predicción por suavizado exponencial"""
            if not combo_producto.get():
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            id_producto = self.get_id_from_combo(combo_producto, self.productos_dict)
            dias_futuro = int(spin_dias.get())
            alpha = alpha_var.get()
            
            # Obtener datos históricos (misma consulta que otros modelos)
            if combo_mercado.get() == "Todos los mercados":
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
                    
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_expandidos
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_producto)
            else:
                id_mercado = self.get_id_from_combo(combo_mercado, self.mercados_dict)
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
                    SELECT 
                        fecha_completa,
                        precio_viejo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_viejo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        fecha_completa,
                        precio_nuevo as precio
                    FROM todos_precios tp
                    INNER JOIN mercado m ON tp.observaciones LIKE '%%' || m.nombre_mercado || '%%'
                    WHERE m.id_mercado = %s AND precio_nuevo IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        o.fecha_actualizacion,
                        o.precio
                    FROM oferta o
                    WHERE o.id_producto = %s
                      AND o.id_mercado = %s
                )
                SELECT 
                    fecha_completa::date as fecha,
                    precio
                FROM precios_mercado
                WHERE precio > 0
                ORDER BY fecha_completa;
                """
                params = (id_producto, id_mercado, id_mercado, id_producto, id_mercado)
            
            datos = execute_query(query, params, fetch=True)
            
            if not datos or len(datos) < 3:
                messagebox.showwarning("Datos insuficientes",
                    f"Se necesitan al menos 3 registros históricos.\n\n"
                    f"Registros encontrados: {len(datos) if datos else 0}")
                return
            
            # Aplicar suavizado exponencial simple
            precios = [float(d[1]) for d in datos]
            
            # Inicializar con el primer valor
            S = [precios[0]]  # Lista de valores suavizados
            
            # Calcular valores suavizados: S_t = α * Y_t + (1-α) * S_(t-1)
            for i in range(1, len(precios)):
                S_t = alpha * precios[i] + (1 - alpha) * S[-1]
                S.append(S_t)
            
            # La predicción es el último valor suavizado
            precio_predicho = S[-1]
            
            # Precio actual
            precio_actual = precios[-1]
            fecha_actual = datos[-1][0]
            fecha_futura = fecha_actual + timedelta(days=dias_futuro)
            
            # Calcular error medio absoluto (MAE)
            errores = [abs(precios[i] - S[i]) for i in range(len(precios))]
            mae = sum(errores) / len(errores)
            
            # Calcular volatilidad
            promedio = sum(precios) / len(precios)
            varianza = sum((p - promedio) ** 2 for p in precios) / len(precios)
            volatilidad = math.sqrt(varianza)
            
            # Determinar tendencia
            if precio_predicho > precio_actual * 1.02:
                tendencia = "ALCISTA 📈"
                color_tend = "#10b981"
            elif precio_predicho < precio_actual * 0.98:
                tendencia = "BAJISTA 📉"
                color_tend = "#dc2626"
            else:
                tendencia = "ESTABLE ➡️"
                color_tend = "#3b82f6"
            
            # Determinar confianza
            if mae < 1:
                confianza = "Alta"
            elif mae < 3:
                confianza = "Media"
            else:
                confianza = "Baja"
            
            # Calcular % de reactividad
            reactividad = alpha * 100
            
            # Mostrar resultados
            resultado_texto = f"""
📉 RESULTADOS - SUAVIZADO EXPONENCIAL SIMPLE

Producto: {combo_producto.get()}
Mercado: {combo_mercado.get()}
Parámetro Alpha (α): {alpha:.1f} ({reactividad:.0f}% reactivo)
Datos históricos: {len(datos)} registros

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
   
   Precio min histórico: {min(precios):.2f} Bs
   Precio max histórico: {max(precios):.2f} Bs
   Promedio general: {promedio:.2f} Bs

════════════════════════════════════════════════

💡 INTERPRETACIÓN DEL ALPHA (α = {alpha:.1f}):
   {"• Alta reactividad: La predicción se ajusta rápidamente" if alpha > 0.6 else "• Media reactividad: Balance entre estabilidad y cambio" if alpha > 0.3 else "• Baja reactividad: Predicción suave y estable"}
   {"  a los últimos cambios de precio." if alpha > 0.6 else "  entre datos recientes e históricos." if alpha > 0.3 else "  que ignora fluctuaciones pequeñas."}
   {"• Ideal para mercados volátiles" if alpha > 0.6 else "• Útil para la mayoría de casos" if alpha > 0.3 else "• Mejor para mercados estables"}
            """
            
            text_resultado.delete("1.0", tk.END)
            text_resultado.insert("1.0", resultado_texto)
            text_resultado.config(fg="#e2e8f0")
            
            # Dibujar gráfico
            canvas_grafico.delete("all")
            self.dibujar_grafico_exponencial(canvas_grafico, datos, S, precio_predicho, dias_futuro, alpha)
        
        # Botones
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones,
            text="📉 Calcular Predicción",
            font=("Arial", 11, "bold"),
            bg="#f59e0b", fg="white",
            command=calcular_exponencial,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    
    def dibujar_grafico_exponencial(self, canvas, datos, valores_suavizados, precio_pred, dias_futuro, alpha):
        """Dibuja gráfico del suavizado exponencial"""
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 180
        
        if width <= 1:
            width = 800
        if height <= 1:
            height = 180
        
        margin = 50
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        # Fondo
        canvas.create_rectangle(margin, margin, width-margin, height-margin,
            fill="#1a1f2e", outline="#334155")
        
        # Datos
        precios_reales = [float(d[1]) for d in datos]
        todos_precios = precios_reales + [precio_pred]
        
        precio_min = min(todos_precios) * 0.95
        precio_max = max(todos_precios) * 1.05
        rango_precio = precio_max - precio_min
        
        # Ejes
        canvas.create_line(margin, height-margin, width-margin, height-margin,
            fill="#64748b", width=2)
        canvas.create_line(margin, margin, margin, height-margin,
            fill="#64748b", width=2)
        
        # Labels
        canvas.create_text(width/2, height-15,
            text="Tiempo", font=("Arial", 9), fill="#94a3b8")
        canvas.create_text(15, height/2,
            text="Precio", font=("Arial", 9), fill="#94a3b8", angle=90)
        
        # Título con alpha
        canvas.create_text(width/2, margin-25,
            text=f"Suavizado Exponencial (α = {alpha:.1f})",
            font=("Arial", 10, "bold"),
            fill="#f59e0b")
        
        n_datos = len(datos)
        
        # Dibujar precios reales
        puntos_reales = []
        for i in range(n_datos):
            x = margin + (i / (n_datos + dias_futuro)) * graph_width
            precio = precios_reales[i]
            y = height - margin - ((precio - precio_min) / rango_precio) * graph_height
            puntos_reales.append((x, y))
            
            # Puntos pequeños grises
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="#64748b", outline="")
        
        # Línea de precios reales
        if len(puntos_reales) > 1:
            for i in range(len(puntos_reales)-1):
                canvas.create_line(puntos_reales[i], puntos_reales[i+1],
                    fill="#64748b", width=1, dash=(2, 2))
        
        # Dibujar valores suavizados
        puntos_suavizados = []
        for i in range(len(valores_suavizados)):
            x = margin + (i / (n_datos + dias_futuro)) * graph_width
            precio_s = valores_suavizados[i]
            y = height - margin - ((precio_s - precio_min) / rango_precio) * graph_height
            puntos_suavizados.append((x, y))
            
            # Puntos naranjas
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="#f59e0b", outline="")
        
        # Línea suavizada
        if len(puntos_suavizados) > 1:
            for i in range(len(puntos_suavizados)-1):
                canvas.create_line(puntos_suavizados[i], puntos_suavizados[i+1],
                    fill="#f59e0b", width=2)
        
        # Predicción
        x_pred = margin + ((n_datos + dias_futuro - 1) / (n_datos + dias_futuro)) * graph_width
        y_pred = height - margin - ((precio_pred - precio_min) / rango_precio) * graph_height
        
        if puntos_suavizados:
            canvas.create_line(puntos_suavizados[-1], (x_pred, y_pred),
                fill="#10b981", width=2, dash=(5, 5))
            canvas.create_oval(x_pred-5, y_pred-5, x_pred+5, y_pred+5,
                fill="#10b981", outline="#064e3b", width=2)
            canvas.create_text(x_pred, y_pred-12,
                text=f"{precio_pred:.2f} Bs",
                font=("Arial", 8, "bold"),
                fill="#10b981")
        
        # Leyenda
        legend_x = width - margin - 110
        legend_y = margin + 10
        
        canvas.create_rectangle(legend_x-5, legend_y-8, legend_x+105, legend_y+45,
            fill="#1a1f2e", outline="#334155")
        
        canvas.create_line(legend_x, legend_y, legend_x+15, legend_y,
            fill="#64748b", width=1, dash=(2, 2))
        canvas.create_text(legend_x+20, legend_y,
            text="Real", font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_line(legend_x, legend_y+15, legend_x+15, legend_y+15,
            fill="#f59e0b", width=2)
        canvas.create_text(legend_x+20, legend_y+15,
            text="Suavizado", font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
        canvas.create_line(legend_x, legend_y+30, legend_x+15, legend_y+30,
            fill="#10b981", width=2, dash=(5, 5))
        canvas.create_text(legend_x+20, legend_y+30,
            text="Predicción", font=("Arial", 8), fill="#e2e8f0", anchor="w")
        
    
    def comparar_modelos(self):
        """Compara diferentes modelos de predicción"""
        messagebox.showinfo("En desarrollo",
            "🎯 Comparación de Modelos\n\n"
            "Esta herramienta evaluará la precisión\n"
            "de diferentes modelos y recomendará el mejor.\n\n"
            "Próximamente disponible...")
    
    def detectar_anomalias(self):
        """Detecta precios anormales en el historial"""
        messagebox.showinfo("En desarrollo",
            "🔍 Detección de Anomalías\n\n"
            "Este módulo identificará picos inusuales\n"
            "o valores atípicos en el historial.\n\n"
            "Próximamente disponible...")
    
    def grafico_comparativo(self):
        """Muestra gráfico histórico vs predicción"""
        messagebox.showinfo("En desarrollo",
            "📊 Gráfico Comparativo\n\n"
            "Visualización completa del historial\n"
            "comparado con las predicciones futuras.\n\n"
            "Próximamente disponible...")
    
    
    
    def get_id_from_combo(self, combo, diccionario):
        """Obtiene el ID a partir del valor seleccionado"""
        valor = combo.get()
        for id_item, nombre in diccionario.items():
            if nombre == valor:
                return id_item
        return None
    
    def volver(self):
        """Vuelve al menú principal"""
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()