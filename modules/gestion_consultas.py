import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database.connection import execute_query
from datetime import datetime
import csv
import pandas as pd
import numpy as np

class GestionConsultas:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        self.canvas.delete("all")
        self.crear_interfaz_principal()
    
    def crear_interfaz_principal(self):
        self.canvas.create_text(450, 30, text="🔍 CONSULTAS Y REPORTES",
            font=("Arial", 20, "bold"), fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, text="Búsqueda avanzada y generación de reportes",
            font=("Arial", 11), fill="#94a3b8")
        
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        self.canvas.create_rectangle(50, 95, 430, 480, fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(240, 115, text="🔎 BÚSQUEDAS", font=("Arial", 13, "bold"), fill="#06b6d4")
        
        busquedas_config = np.array([
            [240, 160, '🛒 Buscar Producto', 'Ver precios en todos los mercados', '#10b981'],
            [240, 230, '🏪 Consultar Mercado', 'Ver todos los productos de un mercado', '#8b5cf6'],
            [240, 300, '💰 Filtrar por Precio', 'Buscar ofertas en un rango de precio', '#f59e0b'],
            [240, 370, '🏆 Rankings', 'Top productos y mejores mercados', '#ec4899']
        ], dtype=object)
        
        comandos_busqueda = [self.buscar_producto, self.consultar_mercado, 
                            self.filtrar_por_precio, self.ver_rankings]
        
        for i, (x, y, titulo, desc, color) in enumerate(busquedas_config):
            self.crear_boton_consulta(int(x), int(y), titulo, desc, color, comandos_busqueda[i])
        
        self.canvas.create_rectangle(470, 95, 850, 480, fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(660, 115, text="📊 REPORTES", font=("Arial", 13, "bold"), fill="#06b6d4")
        
        reportes_config = np.array([
            [660, 160, '📄 Reporte General', 'Todos los productos con precios', '#3b82f6'],
            [660, 230, '📈 Comparar Mercados', 'Comparativa de precios entre mercados', '#06b6d4'],
            [660, 300, '📅 Historial de Cambios', 'Ver cambios de precio en el tiempo', '#8b5cf6'],
            [660, 370, '💾 Exportar Datos', 'Guardar reportes en CSV/Excel', '#10b981']
        ], dtype=object)
        
        comandos_reporte = [self.reporte_general, self.comparar_mercados,
                           self.historial_cambios, self.exportar_datos]
        
        for i, (x, y, titulo, desc, color) in enumerate(reportes_config):
            self.crear_boton_consulta(int(x), int(y), titulo, desc, color, comandos_reporte[i])
        
        self.canvas.create_rectangle(50, 500, 850, 540, fill="#1e293b", outline="#334155", width=1)
        
        self.mostrar_estadisticas_rapidas()
        
        self.btn_volver = tk.Button(self.frame_principal, text="← Volver al Menú",
            font=("Arial", 11, "bold"), bg="#475569", fg="white",
            activebackground="#334155", relief=tk.FLAT, cursor="hand2",
            padx=20, pady=8, command=self.volver)
        self.btn_volver.place(x=380, y=560)
    
    def crear_boton_consulta(self, x, y, titulo, descripcion, color, comando):
        tag = f"btn_{x}_{y}"
        
        rect_id = self.canvas.create_rectangle(x-160, y-25, x+160, y+25,
            fill="#0f172a", outline=color, width=2, tags=tag)
        
        self.canvas.create_text(x, y-8, text=titulo, font=("Arial", 11, "bold"),
            fill="#e2e8f0", tags=tag)
        
        self.canvas.create_text(x, y+10, text=descripcion, font=("Arial", 8),
            fill="#64748b", tags=tag)
        
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: comando())
        self.canvas.tag_bind(tag, "<Enter>", 
            lambda e: self.canvas.itemconfig(rect_id, fill="#1e3a5f", width=3))
        self.canvas.tag_bind(tag, "<Leave>", 
            lambda e: self.canvas.itemconfig(rect_id, fill="#0f172a", width=2))
        self.canvas.tag_bind(tag, "<Enter>", 
            lambda e: self.canvas.config(cursor="hand2"), add="+")
        self.canvas.tag_bind(tag, "<Leave>", 
            lambda e: self.canvas.config(cursor=""), add="+")
    
    def mostrar_estadisticas_rapidas(self):
        queries = {
            'productos': "SELECT COUNT(*) FROM producto WHERE activo = TRUE;",
            'mercados': "SELECT COUNT(*) FROM mercado WHERE activo = TRUE;",
            'ofertas': "SELECT COUNT(*) FROM oferta;",
            'precio': "SELECT AVG(precio) FROM oferta;"
        }
        
        stats = {}
        for key, query in queries.items():
            resultado = execute_query(query, fetch=True)
            stats[key] = resultado[0][0] if resultado and resultado[0][0] else 0
        
        stats_text = (f"📊 Sistema: {int(stats['productos'])} productos | "
                     f"{int(stats['mercados'])} mercados | "
                     f"{int(stats['ofertas'])} ofertas registradas | "
                     f"Precio promedio: {stats['precio']:.2f} Bs")
        
        self.canvas.create_text(450, 520, text=stats_text, font=("Arial", 10), fill="#94a3b8")
    
    def buscar_producto(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Buscar Producto")
        ventana.geometry("800x500")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="🛒 BUSCAR PRODUCTO", font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        frame_busqueda = tk.Frame(ventana, bg="#1e293b")
        frame_busqueda.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_busqueda, text="Nombre del producto:", font=("Arial", 10),
            bg="#1e293b", fg="#e2e8f0").pack(side=tk.LEFT, padx=10)
        
        entry_buscar = tk.Entry(frame_busqueda, font=("Arial", 10),
            bg="#0f172a", fg="white", width=30)
        entry_buscar.pack(side=tk.LEFT, padx=5)
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["Producto", "Mercado", "Precio", "Stock"]
        anchos = np.array([250, 250, 100, 80])
        
        tree = ttk.Treeview(frame_resultados, columns=columnas, show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        anchors = ["w", "w", "e", "center"]
        for col, ancho, anchor in zip(columnas, anchos, anchors):
            tree.heading(col, text=col if col != "Precio" else "Precio (Bs)")
            tree.column(col, width=int(ancho), anchor=anchor)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana, text="", font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def ejecutar_busqueda():
            termino = entry_buscar.get().strip()
            if not termino:
                messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
                return
            
            tree.delete(*tree.get_children())
            
            query = """
            SELECT p.nombre_producto, p.unidad_medida, m.nombre_mercado, m.ciudad,
                   o.precio, o.stock
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE LOWER(p.nombre_producto) LIKE LOWER(%s)
            ORDER BY o.precio ASC;
            """
            
            resultados = execute_query(query, (f"%{termino}%",), fetch=True)
            
            if resultados:
                df = pd.DataFrame(resultados, 
                    columns=['producto', 'unidad', 'mercado', 'ciudad', 'precio', 'stock'])
                
                df['producto_display'] = df['producto'] + ' (' + df['unidad'] + ')'
                df['mercado_display'] = df.apply(
                    lambda x: f"{x['mercado']} - {x['ciudad']}" if pd.notna(x['ciudad']) else x['mercado'],
                    axis=1
                )
                df['precio_display'] = df['precio'].apply(lambda x: f"{x:.2f}")
                df['stock_display'] = df['stock'].fillna("N/A")
                
                for _, row in df.iterrows():
                    tree.insert("", tk.END, values=(
                        row['producto_display'], row['mercado_display'],
                        row['precio_display'], row['stock_display']
                    ))
                
                precios = df['precio'].values
                stats = (f"Se encontraron {len(df)} ofertas | "
                        f"Precio mínimo: {np.min(precios):.2f} Bs | "
                        f"Precio máximo: {np.max(precios):.2f} Bs | "
                        f"Promedio: {np.mean(precios):.2f} Bs")
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(text=f"No se encontraron resultados para '{termino}'", fg="#f59e0b")
        
        btn_buscar = tk.Button(frame_busqueda, text="🔍 Buscar",
            font=("Arial", 10, "bold"), bg="#10b981", fg="white",
            command=ejecutar_busqueda, padx=15, pady=5)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        entry_buscar.bind("<Return>", lambda e: ejecutar_busqueda())
        
        tk.Button(ventana, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def consultar_mercado(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Consultar Mercado")
        ventana.geometry("800x550")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="🏪 CONSULTAR MERCADO", font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_seleccion, text="Seleccione un mercado:", font=("Arial", 10),
            bg="#1e293b", fg="#e2e8f0").pack(side=tk.LEFT, padx=10)
        
        query_mercados = """
        SELECT id_mercado, nombre_mercado, ciudad 
        FROM mercado WHERE activo = TRUE ORDER BY nombre_mercado;
        """
        mercados = execute_query(query_mercados, fetch=True)
        
        if not mercados:
            tk.Label(ventana, text="⚠️ No hay mercados registrados",
                font=("Arial", 11), bg="#0a0f1e", fg="#f59e0b").pack(pady=20)
            tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                     bg="#475569", fg="white", padx=20, pady=5).pack()
            return
        
        df_mercados = pd.DataFrame(mercados, columns=['id', 'nombre', 'ciudad'])
        df_mercados['display'] = df_mercados.apply(
            lambda x: f"{x['nombre']} - {x['ciudad']}" if pd.notna(x['ciudad']) else x['nombre'],
            axis=1
        )
        
        combo_mercado = ttk.Combobox(frame_seleccion,
            values=df_mercados['display'].tolist(), state="readonly",
            font=("Arial", 10), width=40)
        combo_mercado.pack(side=tk.LEFT, padx=5)
        combo_mercado.current(0)
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["Producto", "Categoría", "Precio", "Stock", "Última Actualización"]
        anchos = np.array([200, 120, 100, 80, 150])
        
        tree = ttk.Treeview(frame_resultados, columns=columnas, show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        anchors = ["w", "w", "e", "center", "center"]
        for col, ancho, anchor in zip(columnas, anchos, anchors):
            tree.heading(col, text=col if col != "Precio" else "Precio (Bs)")
            tree.column(col, width=int(ancho), anchor=anchor)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana, text="", font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def consultar():
            seleccion = combo_mercado.get()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un mercado")
                return
            
            match = df_mercados[df_mercados['display'] == seleccion]
            id_mercado = int(match.iloc[0]['id'])
            tree.delete(*tree.get_children())
            
            query = """
            SELECT p.nombre_producto, p.unidad_medida, p.categoria,
                   o.precio, o.stock, o.fecha_actualizacion
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            WHERE o.id_mercado = %s
            ORDER BY p.nombre_producto;
            """
            
            resultados = execute_query(query, (id_mercado,), fetch=True)
            
            if resultados:
                df = pd.DataFrame(resultados,
                    columns=['producto', 'unidad', 'categoria', 'precio', 'stock', 'fecha'])
                
                df['producto_display'] = df['producto'] + ' (' + df['unidad'] + ')'
                df['categoria_display'] = df['categoria'].fillna("Sin categoría")
                df['precio_display'] = df['precio'].apply(lambda x: f"{x:.2f}")
                df['stock_display'] = df['stock'].fillna("N/A")
                df['fecha_display'] = df['fecha'].apply(
                    lambda x: x.strftime("%d/%m/%Y %H:%M") if pd.notna(x) else "N/A"
                )
                
                for _, row in df.iterrows():
                    tree.insert("", tk.END, values=(
                        row['producto_display'], row['categoria_display'],
                        row['precio_display'], row['stock_display'], row['fecha_display']
                    ))
                
                precio_prom = np.mean(df['precio'].values)
                stats = f"Total: {len(df)} productos | Precio promedio: {precio_prom:.2f} Bs"
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(text="Este mercado no tiene productos registrados", fg="#f59e0b")
        
        btn_consultar = tk.Button(frame_seleccion, text="🔍 Consultar",
            font=("Arial", 10, "bold"), bg="#8b5cf6", fg="white",
            command=consultar, padx=15, pady=5)
        btn_consultar.pack(side=tk.LEFT, padx=5)
        
        consultar()
        
        tk.Button(ventana, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    def filtrar_por_precio(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Filtrar por Precio")
        ventana.geometry("800x550")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="💰 FILTRAR POR RANGO DE PRECIO",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        frame_filtros = tk.Frame(ventana, bg="#1e293b")
        frame_filtros.pack(fill=tk.X, padx=20, pady=10)
        
        labels_config = np.array([
            ["Precio mínimo (Bs):", 0, 0],
            ["Precio máximo (Bs):", 0, 2]
        ], dtype=object)
        
        for texto, row, col in labels_config:
            tk.Label(frame_filtros, text=texto, font=("Arial", 10),
                bg="#1e293b", fg="#e2e8f0").grid(row=int(row), column=int(col), 
                padx=10, pady=5, sticky="e")
        
        entry_min = tk.Entry(frame_filtros, font=("Arial", 10),
            bg="#0f172a", fg="white", width=15)
        entry_min.grid(row=0, column=1, padx=5, pady=5)
        entry_min.insert(0, "0")
        
        entry_max = tk.Entry(frame_filtros, font=("Arial", 10),
            bg="#0f172a", fg="white", width=15)
        entry_max.grid(row=0, column=3, padx=5, pady=5)
        entry_max.insert(0, "1000")
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["Producto", "Mercado", "Precio", "Stock"]
        anchos = np.array([250, 250, 120, 100])
        
        tree = ttk.Treeview(frame_resultados, columns=columnas, show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        anchors = ["w", "w", "e", "center"]
        for col, ancho, anchor in zip(columnas, anchos, anchors):
            tree.heading(col, text=col if col != "Precio" else "Precio (Bs)")
            tree.column(col, width=int(ancho), anchor=anchor)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana, text="", font=("Arial", 9),
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
            SELECT p.nombre_producto, p.unidad_medida, m.nombre_mercado, m.ciudad,
                   o.precio, o.stock
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE o.precio BETWEEN %s AND %s
            ORDER BY o.precio ASC;
            """
            
            resultados = execute_query(query, (precio_min, precio_max), fetch=True)
            
            if resultados:
                df = pd.DataFrame(resultados,
                    columns=['producto', 'unidad', 'mercado', 'ciudad', 'precio', 'stock'])
                
                df['producto_display'] = df['producto'] + ' (' + df['unidad'] + ')'
                df['mercado_display'] = df.apply(
                    lambda x: f"{x['mercado']} - {x['ciudad']}" if pd.notna(x['ciudad']) else x['mercado'],
                    axis=1
                )
                df['precio_display'] = df['precio'].apply(lambda x: f"{x:.2f}")
                df['stock_display'] = df['stock'].fillna("N/A")
                
                for _, row in df.iterrows():
                    tree.insert("", tk.END, values=(
                        row['producto_display'], row['mercado_display'],
                        row['precio_display'], row['stock_display']
                    ))
                
                stats = (f"Se encontraron {len(df)} ofertas entre "
                        f"{precio_min:.2f} Bs y {precio_max:.2f} Bs")
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(
                    text=f"No se encontraron ofertas en el rango especificado", fg="#f59e0b")
        
        btn_filtrar = tk.Button(frame_filtros, text="🔍 Filtrar",
            font=("Arial", 10, "bold"), bg="#f59e0b", fg="white",
            command=filtrar, padx=20, pady=5)
        btn_filtrar.grid(row=0, column=4, padx=10, pady=5)
        
        filtrar()
        
        tk.Button(ventana, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def ver_rankings(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Rankings de Productos")
        ventana.geometry("900x600")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="🏆 RANKINGS DE PRODUCTOS",
            font=("Arial", 16, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        frame_rankings = tk.Frame(ventana, bg="#0a0f1e")
        frame_rankings.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        rankings_config = [
            ("caros", "🔴 TOP 10 PRODUCTOS MÁS CAROS", "#dc2626", "DESC"),
            ("baratos", "🟢 TOP 10 PRODUCTOS MÁS BARATOS", "#10b981", "ASC")
        ]
        
        for idx, (key, titulo, color, orden) in enumerate(rankings_config):
            frame = tk.Frame(frame_rankings, bg="#1e293b")
            frame.grid(row=0, column=idx, padx=10, sticky="nsew")
            
            tk.Label(frame, text=titulo, font=("Arial", 12, "bold"),
                bg="#1e293b", fg=color).pack(pady=10)
            
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            columnas = ["Pos", "Producto", "Precio"]
            anchos = np.array([40, 250, 100])
            
            tree = ttk.Treeview(frame, columns=columnas, show="headings",
                height=15, yscrollcommand=scrollbar.set)
            scrollbar.config(command=tree.yview)
            
            anchors = ["center", "w", "e"]
            for col, ancho, anchor in zip(columnas, anchos, anchors):
                tree.heading(col, text="#" if col == "Pos" else col if col != "Precio" else "Precio (Bs)")
                tree.column(col, width=int(ancho), anchor=anchor)
            
            tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            query = f"""
            SELECT p.nombre_producto, p.unidad_medida, m.nombre_mercado, o.precio
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            ORDER BY o.precio {orden}
            LIMIT 10;
            """
            
            resultados = execute_query(query, fetch=True)
            
            if resultados:
                df = pd.DataFrame(resultados, columns=['producto', 'unidad', 'mercado', 'precio'])
                df['producto_display'] = (df['producto'] + ' (' + df['unidad'] + 
                                         ') - ' + df['mercado'])
                df['precio_display'] = df['precio'].apply(lambda x: f"{x:.2f}")
                
                for i, row in df.iterrows():
                    tree.insert("", tk.END, values=(i+1, row['producto_display'], row['precio_display']))
        
        frame_rankings.grid_columnconfigure(0, weight=1)
        frame_rankings.grid_columnconfigure(1, weight=1)
        frame_rankings.grid_rowconfigure(0, weight=1)
        
        tk.Button(ventana, text="Cerrar", font=("Arial", 11, "bold"),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=30, pady=8).pack(pady=15)
    
    def reporte_general(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Reporte General")
        ventana.geometry("1000x600")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="📄 REPORTE GENERAL DE PRODUCTOS",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        frame_tabla = tk.Frame(ventana, bg="#1e293b")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["Producto", "Categoría", "Mercado", "Ciudad", "Precio", "Stock", "Fecha"]
        anchos = np.array([180, 100, 150, 100, 90, 70, 140])
        
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        anchors = ["w", "w", "w", "w", "e", "center", "center"]
        for col, ancho, anchor in zip(columnas, anchos, anchors):
            tree.heading(col, text=col if col != "Precio" else "Precio (Bs)")
            tree.column(col, width=int(ancho), anchor=anchor)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana, text="Cargando datos...",
            font=("Arial", 9), bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        query = """
        SELECT p.nombre_producto, p.unidad_medida, p.categoria,
               m.nombre_mercado, m.ciudad, o.precio, o.stock, o.fecha_actualizacion
        FROM oferta o
        INNER JOIN producto p ON o.id_producto = p.id_producto
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        ORDER BY p.nombre_producto, m.nombre_mercado;
        """
        
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            df = pd.DataFrame(resultados,
                columns=['producto', 'unidad', 'categoria', 'mercado', 'ciudad', 
                        'precio', 'stock', 'fecha'])
            
            df['producto_display'] = df['producto'] + ' (' + df['unidad'] + ')'
            df['categoria_display'] = df['categoria'].fillna("Sin categoría")
            df['ciudad_display'] = df['ciudad'].fillna("N/A")
            df['precio_display'] = df['precio'].apply(lambda x: f"{x:.2f}")
            df['stock_display'] = df['stock'].fillna("N/A")
            df['fecha_display'] = df['fecha'].apply(
                lambda x: x.strftime("%d/%m/%Y %H:%M") if pd.notna(x) else "N/A"
            )
            
            for _, row in df.iterrows():
                tree.insert("", tk.END, values=(
                    row['producto_display'], row['categoria_display'], row['mercado'],
                    row['ciudad_display'], row['precio_display'], 
                    row['stock_display'], row['fecha_display']
                ))
            
            precios = df['precio'].values
            stats = (f"Total: {len(df)} registros | "
                    f"Promedio: {np.mean(precios):.2f} Bs | "
                    f"Mín: {np.min(precios):.2f} Bs | "
                    f"Máx: {np.max(precios):.2f} Bs")
            label_stats.config(text=stats, fg="#10b981")
        else:
            label_stats.config(text="No hay datos para mostrar", fg="#f59e0b")
        
        frame_botones = tk.Frame(ventana, bg="#0a0f1e")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="💾 Exportar a CSV",
            font=("Arial", 10, "bold"), bg="#10b981", fg="white",
            command=lambda: self.exportar_tabla_csv(resultados, "reporte_general"),
            padx=15, pady=6).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=6).pack(side=tk.LEFT, padx=5)
    def comparar_mercados(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Comparar Mercados")
        ventana.geometry("1000x650")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="📈 COMPARAR PRECIOS ENTRE MERCADOS",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        frame_seleccion = tk.Frame(ventana, bg="#1e293b")
        frame_seleccion.pack(fill=tk.X, padx=20, pady=10)
        
        query_mercados = """
        SELECT id_mercado, nombre_mercado, ciudad 
        FROM mercado WHERE activo = TRUE ORDER BY nombre_mercado;
        """
        mercados = execute_query(query_mercados, fetch=True)
        
        if not mercados or len(mercados) < 2:
            tk.Label(ventana, text="⚠️ Se necesitan al menos 2 mercados registrados para comparar",
                font=("Arial", 11), bg="#0a0f1e", fg="#f59e0b").pack(pady=20)
            tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                     bg="#475569", fg="white", padx=20, pady=5).pack()
            return
        
        df_mercados = pd.DataFrame(mercados, columns=['id', 'nombre', 'ciudad'])
        df_mercados['display'] = df_mercados.apply(
            lambda x: f"{x['nombre']} - {x['ciudad']}" if pd.notna(x['ciudad']) else x['nombre'],
            axis=1
        )
        
        labels_config = np.array([
            ["Mercado 1:", 0, 0],
            ["Mercado 2:", 0, 2]
        ], dtype=object)
        
        for texto, row, col in labels_config:
            tk.Label(frame_seleccion, text=texto, font=("Arial", 10, "bold"),
                bg="#1e293b", fg="#e2e8f0").grid(row=int(row), column=int(col), 
                padx=10, pady=5, sticky="e")
        
        combo_mercado1 = ttk.Combobox(frame_seleccion,
            values=df_mercados['display'].tolist(), state="readonly",
            font=("Arial", 10), width=35)
        combo_mercado1.grid(row=0, column=1, padx=5, pady=5)
        combo_mercado1.current(0)
        
        combo_mercado2 = ttk.Combobox(frame_seleccion,
            values=df_mercados['display'].tolist(), state="readonly",
            font=("Arial", 10), width=35)
        combo_mercado2.grid(row=0, column=3, padx=5, pady=5)
        if len(df_mercados) > 1:
            combo_mercado2.current(1)
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["Producto", "Mercado1", "Mercado2", "Diferencia"]
        anchos = np.array([300, 150, 150, 200])
        
        tree = ttk.Treeview(frame_resultados, columns=columnas, show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        anchors = ["w", "e", "e", "center"]
        for col, ancho, anchor in zip(columnas, anchos, anchors):
            texto = col
            if col == "Mercado1":
                texto = "Mercado 1 (Bs)"
            elif col == "Mercado2":
                texto = "Mercado 2 (Bs)"
            tree.heading(col, text=texto)
            tree.column(col, width=int(ancho), anchor=anchor)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana, text="", font=("Arial", 9),
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
            
            match1 = df_mercados[df_mercados['display'] == sel1]
            match2 = df_mercados[df_mercados['display'] == sel2]
            id_mercado1 = int(match1.iloc[0]['id'])
            id_mercado2 = int(match2.iloc[0]['id'])
            
            tree.delete(*tree.get_children())
            
            query = """
            SELECT p.nombre_producto, p.unidad_medida,
                   o1.precio as precio_m1, o2.precio as precio_m2
            FROM producto p
            LEFT JOIN oferta o1 ON p.id_producto = o1.id_producto AND o1.id_mercado = %s
            LEFT JOIN oferta o2 ON p.id_producto = o2.id_producto AND o2.id_mercado = %s
            WHERE o1.precio IS NOT NULL AND o2.precio IS NOT NULL
            ORDER BY p.nombre_producto;
            """
            
            resultados = execute_query(query, (id_mercado1, id_mercado2), fetch=True)
            
            if resultados:
                df = pd.DataFrame(resultados, columns=['producto', 'unidad', 'precio_m1', 'precio_m2'])
                df['producto_display'] = df['producto'] + ' (' + df['unidad'] + ')'
                df['precio_m1'] = pd.to_numeric(df['precio_m1'])
                df['precio_m2'] = pd.to_numeric(df['precio_m2'])
                df['diferencia'] = df['precio_m2'] - df['precio_m1']
                
                mercado1_mas_barato = 0
                mercado2_mas_barato = 0
                
                for _, row in df.iterrows():
                    precio_m1 = row['precio_m1']
                    precio_m2 = row['precio_m2']
                    diferencia = row['diferencia']
                    
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
                        row['producto_display'], f"{precio_m1:.2f}",
                        f"{precio_m2:.2f}", dif_texto
                    ), tags=(tag,))
                
                tree.tag_configure("mas_barato_m1", foreground="#10b981")
                tree.tag_configure("mas_barato_m2", foreground="#3b82f6")
                tree.tag_configure("igual", foreground="#94a3b8")
                
                promedio_dif = np.mean(np.abs(df['diferencia'].values))
                stats = (f"Productos comparados: {len(df)} | "
                        f"M1 más barato: {mercado1_mas_barato} | "
                        f"M2 más barato: {mercado2_mas_barato} | "
                        f"Diferencia promedio: {promedio_dif:.2f} Bs")
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(
                    text="No hay productos en común entre ambos mercados", fg="#f59e0b")
        
        btn_comparar = tk.Button(frame_seleccion, text="🔍 Comparar",
            font=("Arial", 10, "bold"), bg="#06b6d4", fg="white",
            command=comparar, padx=20, pady=5)
        btn_comparar.grid(row=0, column=4, padx=10, pady=5)
        
        comparar()
        
        tk.Button(ventana, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def historial_cambios(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Historial de Cambios")
        ventana.geometry("1000x600")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        
        tk.Label(ventana, text="📅 HISTORIAL DE CAMBIOS DE PRECIO",
            font=("Arial", 14, "bold"), bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        frame_filtros = tk.Frame(ventana, bg="#1e293b")
        frame_filtros.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_filtros, text="Filtrar por producto (opcional):",
            font=("Arial", 10), bg="#1e293b", fg="#e2e8f0").pack(side=tk.LEFT, padx=10)
        
        query_productos = """
        SELECT DISTINCT p.id_producto, p.nombre_producto, p.unidad_medida
        FROM producto p
        INNER JOIN historial_p h ON p.id_producto = h.id_producto
        ORDER BY p.nombre_producto;
        """
        productos = execute_query(query_productos, fetch=True)
        
        opciones = ["Todos los productos"]
        productos_dict = {"Todos los productos": None}
        
        if productos:
            df_productos = pd.DataFrame(productos, columns=['id', 'nombre', 'unidad'])
            df_productos['display'] = df_productos['nombre'] + ' (' + df_productos['unidad'] + ')'
            opciones.extend(df_productos['display'].tolist())
            for _, row in df_productos.iterrows():
                productos_dict[row['display']] = int(row['id'])
        
        combo_producto = ttk.Combobox(frame_filtros, values=opciones,
            state="readonly", font=("Arial", 10), width=40)
        combo_producto.pack(side=tk.LEFT, padx=5)
        combo_producto.current(0)
        
        frame_resultados = tk.Frame(ventana, bg="#1e293b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["Fecha", "Producto", "Cambio", "Fuente"]
        anchos = np.array([150, 200, 450, 120])
        
        tree = ttk.Treeview(frame_resultados, columns=columnas, show="headings",
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        anchors = ["center", "w", "w", "center"]
        for col, ancho, anchor in zip(columnas, anchos, anchors):
            tree.heading(col, text=col if col != "Cambio" else "Descripción del Cambio")
            tree.column(col, width=int(ancho), anchor=anchor)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        label_stats = tk.Label(ventana, text="", font=("Arial", 9),
            bg="#0a0f1e", fg="#94a3b8")
        label_stats.pack(pady=5)
        
        def cargar_historial():
            seleccion = combo_producto.get()
            id_producto = productos_dict[seleccion]
            
            tree.delete(*tree.get_children())
            
            if id_producto is None:
                query = """
                SELECT h.fecha_registro, p.nombre_producto, p.unidad_medida,
                       h.observaciones, h.fuente
                FROM historial_p h
                INNER JOIN producto p ON h.id_producto = p.id_producto
                ORDER BY h.fecha_registro DESC
                LIMIT 200;
                """
                resultados = execute_query(query, fetch=True)
            else:
                query = """
                SELECT h.fecha_registro, p.nombre_producto, p.unidad_medida,
                       h.observaciones, h.fuente
                FROM historial_p h
                INNER JOIN producto p ON h.id_producto = p.id_producto
                WHERE h.id_producto = %s
                ORDER BY h.fecha_registro DESC;
                """
                resultados = execute_query(query, (id_producto,), fetch=True)
            
            if resultados:
                df = pd.DataFrame(resultados,
                    columns=['fecha', 'producto', 'unidad', 'observacion', 'fuente'])
                
                df['producto_display'] = df['producto'] + ' (' + df['unidad'] + ')'
                df['fecha_display'] = df['fecha'].apply(
                    lambda x: x.strftime("%d/%m/%Y %H:%M:%S") if pd.notna(x) else "N/A"
                )
                df['observacion_display'] = df['observacion'].fillna("Sin descripción")
                df['fuente_display'] = df['fuente'].fillna("N/A")
                
                for _, row in df.iterrows():
                    tree.insert("", tk.END, values=(
                        row['fecha_display'], row['producto_display'],
                        row['observacion_display'], row['fuente_display']
                    ))
                
                stats = f"Se encontraron {len(df)} cambios registrados"
                label_stats.config(text=stats, fg="#10b981")
            else:
                label_stats.config(text="No hay cambios registrados", fg="#f59e0b")
        
        btn_cargar = tk.Button(frame_filtros, text="🔍 Buscar",
            font=("Arial", 10, "bold"), bg="#8b5cf6", fg="white",
            command=cargar_historial, padx=15, pady=5)
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        cargar_historial()
        
        tk.Button(ventana, text="Cerrar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=5).pack(pady=10)
    
    def exportar_datos(self):
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Exportar Datos")
        ventana.geometry("400x300")
        ventana.configure(bg="#0a0f1e")
        
        tk.Label(ventana, text="💾 EXPORTAR DATOS", font=("Arial", 14, "bold"),
            bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        tk.Label(ventana, text="Seleccione qué datos desea exportar:",
            font=("Arial", 10), bg="#0a0f1e", fg="#94a3b8").pack(pady=5)
        
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
            rb = tk.Radiobutton(frame_opciones, text=texto, variable=var_opcion,
                value=valor, font=("Arial", 10), bg="#0a0f1e", fg="#e2e8f0",
                selectcolor="#1e293b", activebackground="#0a0f1e",
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
            
            queries = {
                'ofertas': ("""
                    SELECT p.nombre_producto, p.unidad_medida, m.nombre_mercado, m.ciudad,
                           o.precio, o.stock, o.fecha_actualizacion
                    FROM oferta o
                    INNER JOIN producto p ON o.id_producto = p.id_producto
                    INNER JOIN mercado m ON o.id_mercado = m.id_mercado
                    ORDER BY p.nombre_producto;
                    """, ["Producto", "Unidad", "Mercado", "Ciudad", "Precio", "Stock", "Fecha"]),
                'productos': ("""
                    SELECT nombre_producto, categoria, unidad_medida, descripcion
                    FROM producto WHERE activo = TRUE ORDER BY nombre_producto;
                    """, ["Producto", "Categoría", "Unidad", "Descripción"]),
                'mercados': ("""
                    SELECT nombre_mercado, ciudad, departamento, direccion
                    FROM mercado WHERE activo = TRUE ORDER BY nombre_mercado;
                    """, ["Mercado", "Ciudad", "Departamento", "Dirección"]),
                'historial': ("""
                    SELECT p.nombre_producto, h.fecha_registro, h.stock, h.fuente, h.observaciones
                    FROM historial_p h
                    INNER JOIN producto p ON h.id_producto = p.id_producto
                    ORDER BY h.fecha_registro DESC
                    LIMIT 1000;
                    """, ["Producto", "Fecha", "Stock", "Fuente", "Observaciones"])
            }
            
            query, headers = queries[opcion]
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
        
        tk.Button(ventana, text="💾 Exportar a CSV", font=("Arial", 11, "bold"),
            bg="#10b981", fg="white", command=exportar_csv,
            padx=30, pady=8).pack(pady=15)
        
        tk.Button(ventana, text="Cancelar", font=("Arial", 10),
            bg="#475569", fg="white", command=ventana.destroy,
            padx=20, pady=5).pack()
    
    def exportar_tabla_csv(self, datos, nombre_base):
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
            headers = ["Producto", "Unidad", "Categoría", "Mercado", "Ciudad", 
                      "Precio", "Stock", "Fecha"] if nombre_base == "reporte_general" else [f"Columna_{i+1}" for i in range(len(datos[0]))]
            
            with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(datos)
            
            messagebox.showinfo("Éxito", 
                f"✓ Archivo exportado correctamente\n\n"
                f"Registros: {len(datos)}\n"
                f"Ubicación: {archivo}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
    
    def volver(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()