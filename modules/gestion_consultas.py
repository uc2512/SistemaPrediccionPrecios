import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database.connection import execute_query
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GestionConsultas:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        self.canvas.delete("all")
        self.crear_interfaz_principal()
    
    def crear_interfaz_principal(self):
        """Crea el menú principal de consultas y reportes"""
        # Header
        self.canvas.create_text(450, 30,
            text="🔍 CONSULTAS Y REPORTES",
            font=("Arial", 20, "bold"),
            fill="#e2e8f0")
        
        self.canvas.create_text(450, 55,
            text="Búsqueda avanzada y generación de reportes",
            font=("Arial", 11),
            fill="#94a3b8")
        
        # Línea divisoria
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        # === SECCIÓN DE BÚSQUEDAS ===
        self.canvas.create_rectangle(50, 95, 430, 480,
            fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(240, 115,
            text="🔎 BÚSQUEDAS",
            font=("Arial", 13, "bold"),
            fill="#06b6d4")
        
        # Tarjetas de búsqueda
        y_busqueda = 160
        spacing = 70
        
        self.crear_boton_consulta(
            240, y_busqueda,
            "🛒 Buscar Producto",
            "Ver precios en todos los mercados",
            "#10b981",
            self.buscar_producto
        )
        
        self.crear_boton_consulta(
            240, y_busqueda + spacing,
            "🏪 Consultar Mercado",
            "Ver todos los productos de un mercado",
            "#8b5cf6",
            self.consultar_mercado
        )
        
        self.crear_boton_consulta(
            240, y_busqueda + spacing*2,
            "💰 Filtrar por Precio",
            "Buscar ofertas en un rango de precio",
            "#f59e0b",
            self.filtrar_por_precio
        )
        
        self.crear_boton_consulta(
            240, y_busqueda + spacing*3,
            "🏆 Rankings",
            "Top productos y mejores mercados",
            "#ec4899",
            self.ver_rankings
        )
        
        # === SECCIÓN DE REPORTES ===
        self.canvas.create_rectangle(470, 95, 850, 480,
            fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(660, 115,
            text="📊 REPORTES",
            font=("Arial", 13, "bold"),
            fill="#06b6d4")
        
        y_reporte = 160
        
        self.crear_boton_consulta(
            660, y_reporte,
            "📄 Reporte General",
            "Todos los productos con precios",
            "#3b82f6",
            self.reporte_general
        )
        
        self.crear_boton_consulta(
            660, y_reporte + spacing,
            "📈 Comparar Mercados",
            "Comparativa de precios entre mercados",
            "#06b6d4",
            self.comparar_mercados
        )
        
        self.crear_boton_consulta(
            660, y_reporte + spacing*2,
            "📅 Historial de Cambios",
            "Ver cambios de precio en el tiempo",
            "#8b5cf6",
            self.historial_cambios
        )
        
        self.crear_boton_consulta(
            660, y_reporte + spacing*3,
            "💾 Exportar Datos",
            "Guardar reportes en CSV/Excel",
            "#10b981",
            self.exportar_datos
        )
        
        # === ESTADÍSTICAS RÁPIDAS ===
        self.canvas.create_rectangle(50, 500, 850, 540,
            fill="#1e293b", outline="#334155", width=1)
        
        # Obtener estadísticas
        self.mostrar_estadisticas_rapidas()
        
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
        self.btn_volver.place(x=380, y=560)
    
    def crear_boton_consulta(self, x, y, titulo, descripcion, color, comando):
        """Crea un botón de consulta estilizado"""
        rect_id = self.canvas.create_rectangle(x-160, y-25, x+160, y+25,
            fill="#0f172a", outline=color, width=2,
            tags=f"btn_{x}_{y}")
        
        self.canvas.create_text(x, y-8,
            text=titulo,
            font=("Arial", 11, "bold"),
            fill="#e2e8f0",
            tags=f"btn_{x}_{y}")
        
        self.canvas.create_text(x, y+10,
            text=descripcion,
            font=("Arial", 8),
            fill="#64748b",
            tags=f"btn_{x}_{y}")
        
        self.canvas.tag_bind(f"btn_{x}_{y}", "<Button-1>", lambda e: comando())
        self.canvas.tag_bind(f"btn_{x}_{y}", "<Enter>", 
            lambda e: self.hover_boton_enter(rect_id, color))
        self.canvas.tag_bind(f"btn_{x}_{y}", "<Leave>", 
            lambda e: self.hover_boton_leave(rect_id, color))
        
        self.canvas.tag_bind(f"btn_{x}_{y}", "<Enter>", 
            lambda e: self.canvas.config(cursor="hand2"), add="+")
        self.canvas.tag_bind(f"btn_{x}_{y}", "<Leave>", 
            lambda e: self.canvas.config(cursor=""), add="+")
    
    def hover_boton_enter(self, rect_id, color):
        self.canvas.itemconfig(rect_id, fill="#1e3a5f", width=3)
    
    def hover_boton_leave(self, rect_id, color):
        self.canvas.itemconfig(rect_id, fill="#0f172a", width=2)
    
    def mostrar_estadisticas_rapidas(self):
        """Muestra estadísticas rápidas del sistema"""
        query_productos = "SELECT COUNT(*) FROM producto WHERE activo = TRUE;"
        productos = execute_query(query_productos, fetch=True)
        num_productos = productos[0][0] if productos else 0
        
        query_mercados = "SELECT COUNT(*) FROM mercado WHERE activo = TRUE;"
        mercados = execute_query(query_mercados, fetch=True)
        num_mercados = mercados[0][0] if mercados else 0
        
        query_ofertas = "SELECT COUNT(*) FROM oferta;"
        ofertas = execute_query(query_ofertas, fetch=True)
        num_ofertas = ofertas[0][0] if ofertas else 0
        
        query_precio = "SELECT AVG(precio) FROM oferta;"
        precio = execute_query(query_precio, fetch=True)
        precio_prom = precio[0][0] if precio and precio[0][0] else 0
        
        stats_text = (f"📊 Sistema: {num_productos} productos | "
                     f"{num_mercados} mercados | "
                     f"{num_ofertas} ofertas registradas | "
                     f"Precio promedio: {precio_prom:.2f} Bs")
        
        self.canvas.create_text(450, 520,
            text=stats_text,
            font=("Arial", 10),
            fill="#94a3b8")
    
    # ========== FUNCIONES DE BÚSQUEDA ==========
    
    def buscar_producto(self):
        """Busca un producto y muestra todos sus precios"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Buscar Producto")
        ventana.geometry("800x500")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana,
            text="🛒 BUSCAR PRODUCTO",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        frame_busqueda = tk.Frame(ventana, bg="#1e293b")
        frame_busqueda.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_busqueda,
            text="Nombre del producto:",
            font=("Arial", 10),
            bg="#1e293b", fg="#e2e8f0").pack(side=tk.LEFT, padx=10)
        
        entry_buscar = tk.Entry(frame_busqueda,
            font=("Arial", 10),
            bg="#0f172a", fg="white",
            width=30)
        entry_buscar.pack(side=tk.LEFT, padx=5)
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(frame_resultados,
            columns=("Producto", "Mercado", "Precio", "Stock"),
            show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("Producto", text="Producto")
        tree.heading("Mercado", text="Mercado")
        tree.heading("Precio", text="Precio (Bs)")
        tree.heading("Stock", text="Stock")
        
        tree.column("Producto", width=250)
        tree.column("Mercado", width=250)
        tree.column("Precio", width=100, anchor="e")
        tree.column("Stock", width=80, anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana,
            text="",
            font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def ejecutar_busqueda():
            termino = entry_buscar.get().strip()
            if not termino:
                messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
                return
            
            tree.delete(*tree.get_children())
            
            query = """
            SELECT 
                p.nombre_producto,
                p.unidad_medida,
                m.nombre_mercado,
                m.ciudad,
                o.precio,
                o.stock
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE LOWER(p.nombre_producto) LIKE LOWER(%s)
            ORDER BY o.precio ASC;
            """
            
            resultados = execute_query(query, (f"%{termino}%",), fetch=True)
            
            if resultados:
                for fila in resultados:
                    producto = f"{fila[0]} ({fila[1]})"
                    mercado = f"{fila[2]} - {fila[3]}" if fila[3] else fila[2]
                    precio = f"{fila[4]:.2f}"
                    stock = fila[5] if fila[5] else "N/A"
                    
                    tree.insert("", tk.END, values=(producto, mercado, precio, stock))
                
                precios = [float(fila[4]) for fila in resultados]
                precio_min = min(precios)
                precio_max = max(precios)
                precio_prom = sum(precios) / len(precios)
                
                stats = (f"Se encontraron {len(resultados)} ofertas | "
                        f"Precio mínimo: {precio_min:.2f} Bs | "
                        f"Precio máximo: {precio_max:.2f} Bs | "
                        f"Promedio: {precio_prom:.2f} Bs")
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(
                    text=f"No se encontraron resultados para '{termino}'",
                    fg="#f59e0b"
                )
        
        btn_buscar = tk.Button(frame_busqueda,
            text="🔍 Buscar",
            font=("Arial", 10, "bold"),
            bg="#10b981", fg="white",
            command=ejecutar_busqueda,
            padx=15, pady=5)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        entry_buscar.bind("<Return>", lambda e: ejecutar_busqueda())
        
        tk.Button(ventana,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def consultar_mercado(self):
        """Muestra todos los productos de un mercado seleccionado"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Consultar Mercado")
        ventana.geometry("800x550")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana,
            text="🏪 CONSULTAR MERCADO",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        # Frame de selección
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_seleccion,
            text="Seleccione un mercado:",
            font=("Arial", 10),
            bg="#1e293b", fg="#e2e8f0").pack(side=tk.LEFT, padx=10)
        
        # Cargar mercados
        query_mercados = """
        SELECT id_mercado, nombre_mercado, ciudad 
        FROM mercado 
        WHERE activo = TRUE 
        ORDER BY nombre_mercado;
        """
        mercados = execute_query(query_mercados, fetch=True)
        
        if not mercados:
            tk.Label(ventana,
                text="⚠️ No hay mercados registrados",
                font=("Arial", 11),
                bg="#0a0f1e", fg="#f59e0b").pack(pady=20)
            tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                     bg="#475569", fg="white", padx=20, pady=5).pack()
            return
        
        mercados_dict = {f"{m[1]} - {m[2]}": m[0] for m in mercados}
        
        combo_mercado = ttk.Combobox(frame_seleccion,
            values=list(mercados_dict.keys()),
            state="readonly",
            font=("Arial", 10),
            width=40)
        combo_mercado.pack(side=tk.LEFT, padx=5)
        if mercados_dict:
            combo_mercado.current(0)
        
        # Frame para resultados
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(frame_resultados,
            columns=("Producto", "Categoría", "Precio", "Stock", "Última Actualización"),
            show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("Producto", text="Producto")
        tree.heading("Categoría", text="Categoría")
        tree.heading("Precio", text="Precio (Bs)")
        tree.heading("Stock", text="Stock")
        tree.heading("Última Actualización", text="Última Actualización")
        
        tree.column("Producto", width=200)
        tree.column("Categoría", width=120)
        tree.column("Precio", width=100, anchor="e")
        tree.column("Stock", width=80, anchor="center")
        tree.column("Última Actualización", width=150, anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana,
            text="",
            font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def consultar():
            seleccion = combo_mercado.get()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un mercado")
                return
            
            id_mercado = mercados_dict[seleccion]
            tree.delete(*tree.get_children())
            
            query = """
            SELECT 
                p.nombre_producto,
                p.unidad_medida,
                p.categoria,
                o.precio,
                o.stock,
                o.fecha_actualizacion
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            WHERE o.id_mercado = %s
            ORDER BY p.nombre_producto;
            """
            
            resultados = execute_query(query, (id_mercado,), fetch=True)
            
            if resultados:
                for fila in resultados:
                    producto = f"{fila[0]} ({fila[1]})"
                    categoria = fila[2] if fila[2] else "Sin categoría"
                    precio = f"{fila[3]:.2f}"
                    stock = fila[4] if fila[4] else "N/A"
                    fecha = fila[5].strftime("%d/%m/%Y %H:%M") if fila[5] else "N/A"
                    
                    tree.insert("", tk.END, values=(producto, categoria, precio, stock, fecha))
                
                precios = [float(fila[3]) for fila in resultados]
                total_productos = len(resultados)
                precio_prom = sum(precios) / len(precios)
                
                stats = (f"Total: {total_productos} productos | "
                        f"Precio promedio: {precio_prom:.2f} Bs")
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(
                    text="Este mercado no tiene productos registrados",
                    fg="#f59e0b"
                )
        
        btn_consultar = tk.Button(frame_seleccion,
            text="🔍 Consultar",
            font=("Arial", 10, "bold"),
            bg="#8b5cf6", fg="white",
            command=consultar,
            padx=15, pady=5)
        btn_consultar.pack(side=tk.LEFT, padx=5)
        
        # Cargar automáticamente el primer mercado
        consultar()
        
        tk.Button(ventana,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def filtrar_por_precio(self):
        """Filtra ofertas por rango de precio"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Filtrar por Precio")
        ventana.geometry("800x550")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana,
            text="💰 FILTRAR POR RANGO DE PRECIO",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        # Frame de filtros
        frame_filtros = tk.Frame(ventana, bg="#1e293b")
        frame_filtros.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_filtros,
            text="Precio mínimo (Bs):",
            font=("Arial", 10),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        entry_min = tk.Entry(frame_filtros,
            font=("Arial", 10),
            bg="#0f172a", fg="white",
            width=15)
        entry_min.grid(row=0, column=1, padx=5, pady=5)
        entry_min.insert(0, "0")
        
        tk.Label(frame_filtros,
            text="Precio máximo (Bs):",
            font=("Arial", 10),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        entry_max = tk.Entry(frame_filtros,
            font=("Arial", 10),
            bg="#0f172a", fg="white",
            width=15)
        entry_max.grid(row=0, column=3, padx=5, pady=5)
        entry_max.insert(0, "1000")
        
        # Frame para resultados
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(frame_resultados,
            columns=("Producto", "Mercado", "Precio", "Stock"),
            show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("Producto", text="Producto")
        tree.heading("Mercado", text="Mercado")
        tree.heading("Precio", text="Precio (Bs)")
        tree.heading("Stock", text="Stock")
        
        tree.column("Producto", width=250)
        tree.column("Mercado", width=250)
        tree.column("Precio", width=120, anchor="e")
        tree.column("Stock", width=100, anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana,
            text="",
            font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def filtrar():
            try:
                precio_min = float(entry_min.get())
                precio_max = float(entry_max.get())
                
                if precio_min < 0 or precio_max < 0:
                    messagebox.showwarning("Advertencia", "Los precios deben ser positivos")
                    return
                
                if precio_min > precio_max:
                    messagebox.showwarning("Advertencia", 
                        "El precio mínimo no puede ser mayor que el máximo")
                    return
                
            except ValueError:
                messagebox.showwarning("Advertencia", "Ingrese valores numéricos válidos")
                return
            
            tree.delete(*tree.get_children())
            
            query = """
            SELECT 
                p.nombre_producto,
                p.unidad_medida,
                m.nombre_mercado,
                m.ciudad,
                o.precio,
                o.stock
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE o.precio BETWEEN %s AND %s
            ORDER BY o.precio ASC;
            """
            
            resultados = execute_query(query, (precio_min, precio_max), fetch=True)
            
            if resultados:
                for fila in resultados:
                    producto = f"{fila[0]} ({fila[1]})"
                    mercado = f"{fila[2]} - {fila[3]}" if fila[3] else fila[2]
                    precio = f"{fila[4]:.2f}"
                    stock = fila[5] if fila[5] else "N/A"
                    
                    tree.insert("", tk.END, values=(producto, mercado, precio, stock))
                
                stats = (f"Se encontraron {len(resultados)} ofertas entre "
                        f"{precio_min:.2f} Bs y {precio_max:.2f} Bs")
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(
                    text=f"No se encontraron ofertas en el rango especificado",
                    fg="#f59e0b"
                )
        
        btn_filtrar = tk.Button(frame_filtros,
            text="🔍 Filtrar",
            font=("Arial", 10, "bold"),
            bg="#f59e0b", fg="white",
            command=filtrar,
            padx=20, pady=5)
        btn_filtrar.grid(row=0, column=4, padx=10, pady=5)
        
        # Filtrar automáticamente al iniciar
        filtrar()
        
        tk.Button(ventana,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def ver_rankings(self):
        """Muestra rankings de productos (más caros/baratos)"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Rankings de Productos")
        ventana.geometry("900x600")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana,
            text="🏆 RANKINGS DE PRODUCTOS",
            font=("Arial", 16, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        # Frame principal con dos columnas
        frame_rankings = tk.Frame(ventana, bg="#0a0f1e")
        frame_rankings.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # === COLUMNA IZQUIERDA: MÁS CAROS ===
        frame_caros = tk.Frame(frame_rankings, bg="#1e293b")
        frame_caros.grid(row=0, column=0, padx=10, sticky="nsew")
        
        tk.Label(frame_caros,
            text="🔴 TOP 10 PRODUCTOS MÁS CAROS",
            font=("Arial", 12, "bold"),
            bg="#1e293b", fg="#dc2626").pack(pady=10)
        
        scrollbar_caros = ttk.Scrollbar(frame_caros, orient=tk.VERTICAL)
        scrollbar_caros.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_caros = ttk.Treeview(frame_caros,
            columns=("Pos", "Producto", "Precio"),
            show="headings",
            height=15,
            yscrollcommand=scrollbar_caros.set)
        scrollbar_caros.config(command=tree_caros.yview)
        
        tree_caros.heading("Pos", text="#")
        tree_caros.heading("Producto", text="Producto")
        tree_caros.heading("Precio", text="Precio (Bs)")
        
        tree_caros.column("Pos", width=40, anchor="center")
        tree_caros.column("Producto", width=250)
        tree_caros.column("Precio", width=100, anchor="e")
        
        tree_caros.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # === COLUMNA DERECHA: MÁS BARATOS ===
        frame_baratos = tk.Frame(frame_rankings, bg="#1e293b")
        frame_baratos.grid(row=0, column=1, padx=10, sticky="nsew")
        
        tk.Label(frame_baratos,
            text="🟢 TOP 10 PRODUCTOS MÁS BARATOS",
            font=("Arial", 12, "bold"),
            bg="#1e293b", fg="#10b981").pack(pady=10)
        
        scrollbar_baratos = ttk.Scrollbar(frame_baratos, orient=tk.VERTICAL)
        scrollbar_baratos.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_baratos = ttk.Treeview(frame_baratos,
            columns=("Pos", "Producto", "Precio"),
            show="headings",
            height=15,
            yscrollcommand=scrollbar_baratos.set)
        scrollbar_baratos.config(command=tree_baratos.yview)
        
        tree_baratos.heading("Pos", text="#")
        tree_baratos.heading("Producto", text="Producto")
        tree_baratos.heading("Precio", text="Precio (Bs)")
        
        tree_baratos.column("Pos", width=40, anchor="center")
        tree_baratos.column("Producto", width=250)
        tree_baratos.column("Precio", width=100, anchor="e")
        
        tree_baratos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar grid para que se expanda
        frame_rankings.grid_columnconfigure(0, weight=1)
        frame_rankings.grid_columnconfigure(1, weight=1)
        frame_rankings.grid_rowconfigure(0, weight=1)
        
        # Cargar datos
        # MÁS CAROS
        query_caros = """
        SELECT 
            p.nombre_producto,
            p.unidad_medida,
            m.nombre_mercado,
            o.precio
        FROM oferta o
        INNER JOIN producto p ON o.id_producto = p.id_producto
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        ORDER BY o.precio DESC
        LIMIT 10;
        """
        
        resultados_caros = execute_query(query_caros, fetch=True)
        
        if resultados_caros:
            for i, fila in enumerate(resultados_caros, 1):
                producto = f"{fila[0]} ({fila[1]}) - {fila[2]}"
                precio = f"{fila[3]:.2f}"
                tree_caros.insert("", tk.END, values=(i, producto, precio))
        
        # MÁS BARATOS
        query_baratos = """
        SELECT 
            p.nombre_producto,
            p.unidad_medida,
            m.nombre_mercado,
            o.precio
        FROM oferta o
        INNER JOIN producto p ON o.id_producto = p.id_producto
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        ORDER BY o.precio ASC
        LIMIT 10;
        """
        
        resultados_baratos = execute_query(query_baratos, fetch=True)
        
        if resultados_baratos:
            for i, fila in enumerate(resultados_baratos, 1):
                producto = f"{fila[0]} ({fila[1]}) - {fila[2]}"
                precio = f"{fila[3]:.2f}"
                tree_baratos.insert("", tk.END, values=(i, producto, precio))
        
        # Botón cerrar
        tk.Button(ventana,
            text="Cerrar",
            font=("Arial", 11, "bold"),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=30, pady=8).pack(pady=15)
    
    # ========== FUNCIONES DE REPORTES ==========
    
    def reporte_general(self):
        """Genera reporte general de todos los productos con sus precios"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Reporte General")
        ventana.geometry("1000x600")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana,
            text="📄 REPORTE GENERAL DE PRODUCTOS",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        # Frame para tabla
        frame_tabla = tk.Frame(ventana, bg="#1e293b")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(frame_tabla,
            columns=("Producto", "Categoría", "Mercado", "Ciudad", "Precio", "Stock", "Fecha"),
            show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("Producto", text="Producto")
        tree.heading("Categoría", text="Categoría")
        tree.heading("Mercado", text="Mercado")
        tree.heading("Ciudad", text="Ciudad")
        tree.heading("Precio", text="Precio (Bs)")
        tree.heading("Stock", text="Stock")
        tree.heading("Fecha", text="Última Actualización")
        
        tree.column("Producto", width=180)
        tree.column("Categoría", width=100)
        tree.column("Mercado", width=150)
        tree.column("Ciudad", width=100)
        tree.column("Precio", width=90, anchor="e")
        tree.column("Stock", width=70, anchor="center")
        tree.column("Fecha", width=140, anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Label de estadísticas
        label_stats = tk.Label(ventana,
            text="Cargando datos...",
            font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        # Consultar todos los datos
        query = """
        SELECT 
            p.nombre_producto,
            p.unidad_medida,
            p.categoria,
            m.nombre_mercado,
            m.ciudad,
            o.precio,
            o.stock,
            o.fecha_actualizacion
        FROM oferta o
        INNER JOIN producto p ON o.id_producto = p.id_producto
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        ORDER BY p.nombre_producto, m.nombre_mercado;
        """
        
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            for fila in resultados:
                producto = f"{fila[0]} ({fila[1]})"
                categoria = fila[2] if fila[2] else "Sin categoría"
                mercado = fila[3]
                ciudad = fila[4] if fila[4] else "N/A"
                precio = f"{fila[5]:.2f}"
                stock = fila[6] if fila[6] else "N/A"
                fecha = fila[7].strftime("%d/%m/%Y %H:%M") if fila[7] else "N/A"
                
                tree.insert("", tk.END, values=(producto, categoria, mercado, ciudad, precio, stock, fecha))
            
            total_registros = len(resultados)
            precios = [float(fila[5]) for fila in resultados]
            precio_prom = sum(precios) / len(precios)
            precio_min = min(precios)
            precio_max = max(precios)
            
            stats = (f"Total: {total_registros} registros | "
                    f"Promedio: {precio_prom:.2f} Bs | "
                    f"Mín: {precio_min:.2f} Bs | "
                    f"Máx: {precio_max:.2f} Bs")
            label_stats.config(text=stats, fg="#10b981")
        else:
            label_stats.config(text="No hay datos para mostrar", fg="#f59e0b")
        
        # Botones
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones,
            text="💾 Exportar a CSV",
            font=("Arial", 10, "bold"),
            bg="#10b981", fg="white",
            command=lambda: self.exportar_tabla_csv(resultados, "reporte_general"),
            padx=15, pady=6).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=6).pack(side=tk.LEFT, padx=5)
    
    def comparar_mercados(self):
        """Compara precios entre dos mercados seleccionados"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Comparar Mercados")
        ventana.geometry("1000x650")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana,
            text="📈 COMPARAR PRECIOS ENTRE MERCADOS",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        # Frame de selección
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=10)
        
        # Cargar mercados
        query_mercados = """
        SELECT id_mercado, nombre_mercado, ciudad 
        FROM mercado 
        WHERE activo = TRUE 
        ORDER BY nombre_mercado;
        """
        mercados = execute_query(query_mercados, fetch=True)
        
        if not mercados or len(mercados) < 2:
            tk.Label(ventana,
                text="⚠️ Se necesitan al menos 2 mercados registrados para comparar",
                font=("Arial", 11),
                bg="#0a0f1e", fg="#f59e0b").pack(pady=20)
            tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                     bg="#475569", fg="white", padx=20, pady=5).pack()
            return
        
        mercados_dict = {f"{m[1]} - {m[2]}": m[0] for m in mercados}
        
        tk.Label(frame_seleccion,
            text="Mercado 1:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        combo_mercado1 = ttk.Combobox(frame_seleccion,
            values=list(mercados_dict.keys()),
            state="readonly",
            font=("Arial", 10),
            width=35)
        combo_mercado1.grid(row=0, column=1, padx=5, pady=5)
        if mercados_dict:
            combo_mercado1.current(0)
        
        tk.Label(frame_seleccion,
            text="Mercado 2:",
            font=("Arial", 10, "bold"),
            bg="#1e293b", fg="#e2e8f0").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        combo_mercado2 = ttk.Combobox(frame_seleccion,
            values=list(mercados_dict.keys()),
            state="readonly",
            font=("Arial", 10),
            width=35)
        combo_mercado2.grid(row=0, column=3, padx=5, pady=5)
        if len(mercados_dict) > 1:
            combo_mercado2.current(1)
        
        # Frame para resultados
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(frame_resultados,
            columns=("Producto", "Mercado1", "Mercado2", "Diferencia"),
            show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("Producto", text="Producto")
        tree.heading("Mercado1", text="Mercado 1 (Bs)")
        tree.heading("Mercado2", text="Mercado 2 (Bs)")
        tree.heading("Diferencia", text="Diferencia")
        
        tree.column("Producto", width=300)
        tree.column("Mercado1", width=150, anchor="e")
        tree.column("Mercado2", width=150, anchor="e")
        tree.column("Diferencia", width=200, anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana,
            text="",
            font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def comparar():
            sel1 = combo_mercado1.get()
            sel2 = combo_mercado2.get()
            
            if not sel1 or not sel2:
                messagebox.showwarning("Advertencia", "Seleccione ambos mercados")
                return
            
            if sel1 == sel2:
                messagebox.showwarning("Advertencia", "Seleccione mercados diferentes")
                return
            
            id_mercado1 = mercados_dict[sel1]
            id_mercado2 = mercados_dict[sel2]
            
            tree.delete(*tree.get_children())
            
            query = """
            SELECT 
                p.nombre_producto,
                p.unidad_medida,
                o1.precio as precio_m1,
                o2.precio as precio_m2
            FROM producto p
            LEFT JOIN oferta o1 ON p.id_producto = o1.id_producto AND o1.id_mercado = %s
            LEFT JOIN oferta o2 ON p.id_producto = o2.id_producto AND o2.id_mercado = %s
            WHERE o1.precio IS NOT NULL AND o2.precio IS NOT NULL
            ORDER BY p.nombre_producto;
            """
            
            resultados = execute_query(query, (id_mercado1, id_mercado2), fetch=True)
            
            if resultados:
                total_diferencia = 0
                mercado1_mas_barato = 0
                mercado2_mas_barato = 0
                
                for fila in resultados:
                    producto = f"{fila[0]} ({fila[1]})"
                    precio_m1 = float(fila[2])
                    precio_m2 = float(fila[3])
                    diferencia = precio_m2 - precio_m1
                    total_diferencia += abs(diferencia)
                    
                    if precio_m1 < precio_m2:
                        mercado1_mas_barato += 1
                        dif_texto = f"▼ {abs(diferencia):.2f} Bs (M1 más barato)"
                        tag = "mas_barato_m1"
                    elif precio_m1 > precio_m2:
                        mercado2_mas_barato += 1
                        dif_texto = f"▲ {abs(diferencia):.2f} Bs (M2 más barato)"
                        tag = "mas_barato_m2"
                    else:
                        dif_texto = "= Igual precio"
                        tag = "igual"
                    
                    tree.insert("", tk.END, values=(
                        producto,
                        f"{precio_m1:.2f}",
                        f"{precio_m2:.2f}",
                        dif_texto
                    ), tags=(tag,))
                
                # Aplicar colores
                tree.tag_configure("mas_barato_m1", foreground="#10b981")
                tree.tag_configure("mas_barato_m2", foreground="#3b82f6")
                tree.tag_configure("igual", foreground="#94a3b8")
                
                promedio_dif = total_diferencia / len(resultados)
                stats = (f"Productos comparados: {len(resultados)} | "
                        f"M1 más barato: {mercado1_mas_barato} | "
                        f"M2 más barato: {mercado2_mas_barato} | "
                        f"Diferencia promedio: {promedio_dif:.2f} Bs")
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(
                    text="No hay productos en común entre ambos mercados",
                    fg="#f59e0b"
                )
        
        btn_comparar = tk.Button(frame_seleccion,
            text="🔍 Comparar",
            font=("Arial", 10, "bold"),
            bg="#06b6d4", fg="white",
            command=comparar,
            padx=20, pady=5)
        btn_comparar.grid(row=0, column=4, padx=10, pady=5)
        
        # Comparar automáticamente al iniciar
        comparar()
        
        tk.Button(ventana,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def historial_cambios(self):
        """Muestra historial de cambios de precio usando historial_p"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Historial de Cambios")
        ventana.geometry("1000x600")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana,
            text="📅 HISTORIAL DE CAMBIOS DE PRECIO",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        # Frame de filtros
        frame_filtros = tk.Frame(ventana, bg="#1e293b")
        frame_filtros.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_filtros,
            text="Filtrar por producto (opcional):",
            font=("Arial", 10),
            bg="#1e293b", fg="#e2e8f0").pack(side=tk.LEFT, padx=10)
        
        # Cargar productos
        query_productos = """
        SELECT DISTINCT p.id_producto, p.nombre_producto, p.unidad_medida
        FROM producto p
        INNER JOIN historial_p h ON p.id_producto = h.id_producto
        ORDER BY p.nombre_producto;
        """
        productos = execute_query(query_productos, fetch=True)
        
        productos_dict = {"Todos los productos": None}
        if productos:
            for p in productos:
                productos_dict[f"{p[1]} ({p[2]})"] = p[0]
        
        combo_producto = ttk.Combobox(frame_filtros,
            values=list(productos_dict.keys()),
            state="readonly",
            font=("Arial", 10),
            width=40)
        combo_producto.pack(side=tk.LEFT, padx=5)
        combo_producto.current(0)
        
        # Frame para resultados
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(frame_resultados,
            columns=("Fecha", "Producto", "Cambio", "Fuente"),
            show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("Fecha", text="Fecha y Hora")
        tree.heading("Producto", text="Producto")
        tree.heading("Cambio", text="Descripción del Cambio")
        tree.heading("Fuente", text="Fuente")
        
        tree.column("Fecha", width=150, anchor="center")
        tree.column("Producto", width=200)
        tree.column("Cambio", width=450)
        tree.column("Fuente", width=120, anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana,
            text="",
            font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def cargar_historial():
            seleccion = combo_producto.get()
            id_producto = productos_dict[seleccion]
            
            tree.delete(*tree.get_children())
            
            if id_producto is None:
                # Mostrar todo el historial
                query = """
                SELECT 
                    h.fecha_registro,
                    p.nombre_producto,
                    p.unidad_medida,
                    h.observaciones,
                    h.fuente
                FROM historial_p h
                INNER JOIN producto p ON h.id_producto = p.id_producto
                ORDER BY h.fecha_registro DESC
                LIMIT 200;
                """
                resultados = execute_query(query, fetch=True)
            else:
                # Mostrar historial de un producto específico
                query = """
                SELECT 
                    h.fecha_registro,
                    p.nombre_producto,
                    p.unidad_medida,
                    h.observaciones,
                    h.fuente
                FROM historial_p h
                INNER JOIN producto p ON h.id_producto = p.id_producto
                WHERE h.id_producto = %s
                ORDER BY h.fecha_registro DESC;
                """
                resultados = execute_query(query, (id_producto,), fetch=True)
            
            if resultados:
                for fila in resultados:
                    fecha = fila[0].strftime("%d/%m/%Y %H:%M:%S") if fila[0] else "N/A"
                    producto = f"{fila[1]} ({fila[2]})"
                    cambio = fila[3] if fila[3] else "Sin descripción"
                    fuente = fila[4] if fila[4] else "N/A"
                    
                    tree.insert("", tk.END, values=(fecha, producto, cambio, fuente))
                
                stats = f"Se encontraron {len(resultados)} cambios registrados"
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(
                    text="No hay cambios registrados",
                    fg="#f59e0b"
                )
        
        btn_cargar = tk.Button(frame_filtros,
            text="🔍 Buscar",
            font=("Arial", 10, "bold"),
            bg="#8b5cf6", fg="white",
            command=cargar_historial,
            padx=15, pady=5)
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        # Cargar automáticamente al iniciar
        cargar_historial()
        
        tk.Button(ventana,
            text="Cerrar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def exportar_datos(self):
        """Exporta datos a CSV/Excel"""
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Exportar Datos")
        ventana.geometry("400x300")
        ventana.configure(bg="#0a0f1e")
        
        tk.Label(ventana,
            text="💾 EXPORTAR DATOS",
            font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        tk.Label(ventana,
            text="Seleccione qué datos desea exportar:",
            font=("Arial", 10),
            bg="#0a0f1e", fg="#94a3b8").pack(pady=5)
        
        opciones = [
            ("Todas las ofertas actuales", "ofertas"),
            ("Todos los productos", "productos"),
            ("Todos los mercados", "mercados"),
            ("Historial de cambios", "historial")
        ]
        
        var_opcion = tk.StringVar(value="ofertas")
        
        frame_opciones = tk.Frame(ventana, bg="#0a0f1e")
        frame_opciones.pack(pady=10)
        
        for texto, valor in opciones:
            rb = tk.Radiobutton(frame_opciones,
                text=texto,
                variable=var_opcion,
                value=valor,
                font=("Arial", 10),
                bg="#0a0f1e", fg="#e2e8f0",
                selectcolor="#1e293b",
                activebackground="#0a0f1e",
                activeforeground="#10b981")
            rb.pack(anchor="w", pady=3)
        
        def exportar_csv():
            opcion = var_opcion.get()
            
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"{opcion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not archivo:
                return
            
            if opcion == "ofertas":
                query = """
                SELECT 
                    p.nombre_producto,
                    p.unidad_medida,
                    m.nombre_mercado,
                    m.ciudad,
                    o.precio,
                    o.stock,
                    o.fecha_actualizacion
                FROM oferta o
                INNER JOIN producto p ON o.id_producto = p.id_producto
                INNER JOIN mercado m ON o.id_mercado = m.id_mercado
                ORDER BY p.nombre_producto;
                """
                headers = ["Producto", "Unidad", "Mercado", "Ciudad", "Precio", "Stock", "Fecha"]
            
            elif opcion == "productos":
                query = """
                SELECT 
                    nombre_producto,
                    categoria,
                    unidad_medida,
                    descripcion
                FROM producto
                WHERE activo = TRUE
                ORDER BY nombre_producto;
                """
                headers = ["Producto", "Categoría", "Unidad", "Descripción"]
            
            elif opcion == "mercados":
                query = """
                SELECT 
                    nombre_mercado,
                    ciudad,
                    departamento,
                    direccion
                FROM mercado
                WHERE activo = TRUE
                ORDER BY nombre_mercado;
                """
                headers = ["Mercado", "Ciudad", "Departamento", "Dirección"]
            
            else:  # historial
                query = """
                SELECT 
                    p.nombre_producto,
                    h.fecha_registro,
                    h.stock,
                    h.fuente,
                    h.observaciones
                FROM historial_p h
                INNER JOIN producto p ON h.id_producto = p.id_producto
                ORDER BY h.fecha_registro DESC
                LIMIT 1000;
                """
                headers = ["Producto", "Fecha", "Stock", "Fuente", "Observaciones"]
            
            datos = execute_query(query, fetch=True)
            
            if not datos:
                messagebox.showwarning("Sin datos", "No hay datos para exportar")
                return
            
            try:
                with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(datos)
                
                messagebox.showinfo("Éxito", 
                    f"✓ Archivo exportado correctamente\n\n"
                    f"Registros: {len(datos)}\n"
                    f"Ubicación: {archivo}")
                ventana.destroy()
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
        
        tk.Button(ventana,
            text="💾 Exportar a CSV",
            font=("Arial", 11, "bold"),
            bg="#10b981", fg="white",
            command=exportar_csv,
            padx=30, pady=8).pack(pady=15)
        
        tk.Button(ventana,
            text="Cancelar",
            font=("Arial", 10),
            bg="#475569", fg="white",
            command=ventana.destroy,
            padx=20, pady=5).pack()
    
    def exportar_tabla_csv(self, datos, nombre_base):
        """Función auxiliar para exportar cualquier tabla a CSV"""
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar")
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"{nombre_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not archivo:
            return
        
        try:
            with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # Escribir headers (basados en el primer elemento)
                if nombre_base == "reporte_general":
                    headers = ["Producto", "Unidad", "Categoría", "Mercado", "Ciudad", "Precio", "Stock", "Fecha"]
                else:
                    headers = [f"Columna_{i+1}" for i in range(len(datos[0]))]
                
                writer.writerow(headers)
                writer.writerows(datos)
            
            messagebox.showinfo("Éxito", 
                f"✓ Archivo exportado correctamente\n\n"
                f"Registros: {len(datos)}\n"
                f"Ubicación: {archivo}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
    
    def volver(self):
        """Vuelve al menú principal"""
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()