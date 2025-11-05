import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query
from datetime import datetime

class GestionPrecios:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        # Variables para almacenar datos
        self.productos_dict = {}  # {id_producto: "Nombre (unidad)"}
        self.mercados_dict = {}   # {id_mercado: "Nombre"}
        
        self.canvas.delete("all")
        self.cargar_productos()
        self.cargar_mercados()
        self.crear_interfaz()
        self.cargar_ofertas()
    
    def cargar_productos(self):
        """Carga productos activos desde la BD"""
        query = """
        SELECT id_producto, nombre_producto, unidad_medida 
        FROM producto 
        WHERE activo = TRUE
        ORDER BY nombre_producto;
        """
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            for fila in resultados:
                id_prod = fila[0]
                nombre = f"{fila[1]} ({fila[2]})"
                self.productos_dict[id_prod] = nombre
        
        print(f"✓ Cargados {len(self.productos_dict)} productos")
    
    def cargar_mercados(self):
        """Carga mercados activos desde la BD"""
        query = """
        SELECT id_mercado, nombre_mercado, ciudad
        FROM mercado
        WHERE activo = TRUE
        ORDER BY nombre_mercado;
        """
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            for fila in resultados:
                id_merc = fila[0]
                nombre = f"{fila[1]}"
                if fila[2]:  # Si tiene ciudad
                    nombre += f" - {fila[2]}"
                self.mercados_dict[id_merc] = nombre
        
        print(f"✓ Cargados {len(self.mercados_dict)} mercados")
    
    def crear_interfaz(self):
        """Crea la interfaz de gestión de precios"""
        
        # Header
        self.canvas.create_text(450, 30, 
                               text="💰 GESTIÓN DE PRECIOS", 
                               font=("Arial", 20, "bold"), 
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, 
                               text="Registro de ofertas de productos en mercados", 
                               font=("Arial", 11), 
                               fill="#94a3b8")
        
        # Línea divisoria
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        # === SECCIÓN FORMULARIO ===
        self.canvas.create_rectangle(50, 90, 850, 300, 
                                     fill="#1e293b", outline="#3b82f6", width=2)
        
        self.canvas.create_text(450, 105, 
                               text="REGISTRAR / ACTUALIZAR OFERTA", 
                               font=("Arial", 12, "bold"), 
                               fill="#3b82f6")
        
        # Verificar si hay productos y mercados
        if not self.productos_dict:
            self.canvas.create_text(450, 180, 
                                   text="⚠️  No hay productos registrados", 
                                   font=("Arial", 12, "bold"), 
                                   fill="#f59e0b")
            self.canvas.create_text(450, 210, 
                                   text="Por favor, registre productos primero en el módulo de Gestión", 
                                   font=("Arial", 10), 
                                   fill="#94a3b8")
            self.crear_boton_volver()
            return
        
        if not self.mercados_dict:
            self.canvas.create_text(450, 180, 
                                   text="⚠️  No hay mercados registrados", 
                                   font=("Arial", 12, "bold"), 
                                   fill="#f59e0b")
            self.canvas.create_text(450, 210, 
                                   text="Por favor, registre mercados primero en el módulo de Gestión", 
                                   font=("Arial", 10), 
                                   fill="#94a3b8")
            self.crear_boton_volver()
            return
        
        y_base = 140
        spacing = 40
        
        # --- Producto ---
        self.canvas.create_text(120, y_base, 
                               text="Producto:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        
        # Combobox para productos
        self.combo_producto = ttk.Combobox(
            self.frame_principal,
            values=list(self.productos_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=35
        )
        self.combo_producto.place(x=220, y=y_base-10)
        
        # --- Mercado ---
        self.canvas.create_text(120, y_base + spacing, 
                               text="Mercado:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        
        self.combo_mercado = ttk.Combobox(
            self.frame_principal,
            values=list(self.mercados_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=35
        )
        self.combo_mercado.place(x=220, y=y_base + spacing - 10)
        
        # --- Precio ---
        self.canvas.create_text(120, y_base + spacing*2, 
                               text="Precio (Bs):", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        
        self.entry_precio = tk.Entry(
            self.frame_principal, 
            font=("Arial", 10), 
            bg="#0f172a", fg="white",
            insertbackground="white",
            width=15
        )
        self.entry_precio.place(x=220, y=y_base + spacing*2 - 10)
        
        self.canvas.create_text(360, y_base + spacing*2, 
                               text="(ejemplo: 5.50)", 
                               font=("Arial", 9, "italic"), 
                               fill="#64748b", anchor="w")
        
        # --- Stock ---
        self.canvas.create_text(500, y_base + spacing*2, 
                               text="Stock:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        
        self.entry_stock = tk.Entry(
            self.frame_principal, 
            font=("Arial", 10), 
            bg="#0f172a", fg="white",
            insertbackground="white",
            width=15
        )
        self.entry_stock.place(x=570, y=y_base + spacing*2 - 10)
        
        self.canvas.create_text(720, y_base + spacing*2, 
                               text="(unidades disponibles)", 
                               font=("Arial", 9, "italic"), 
                               fill="#64748b", anchor="w")
        
        # --- Información adicional ---
        info_y = y_base + spacing*3 + 10
        self.canvas.create_rectangle(130, info_y, 770, info_y + 45,
                                     fill="#0f172a", outline="#475569", width=1)
        
        self.canvas.create_text(450, info_y + 12,
                               text="ℹ️  Información:",
                               font=("Arial", 9, "bold"),
                               fill="#3b82f6")
        
        self.canvas.create_text(450, info_y + 30,
                               text="• Si la oferta ya existe (mismo producto y mercado), se ACTUALIZARÁ el precio y stock",
                               font=("Arial", 8),
                               fill="#94a3b8")
        
        # --- Botones de acción del formulario ---
        btn_y = 250
        btn_spacing = 130  # Espaciado entre botones
        
        self.btn_guardar = tk.Button(
            self.frame_principal,
            text="💾 Guardar",
            font=("Arial", 10, "bold"),
            bg="#10b981", fg="white",
            activebackground="#059669",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6,
            command=self.guardar_oferta
        )
        self.btn_guardar.place(x=50, y=btn_y)
        
        self.btn_limpiar = tk.Button(
            self.frame_principal,
            text="🔄 Limpiar",
            font=("Arial", 10, "bold"),
            bg="#6366f1", fg="white",
            activebackground="#4f46e5",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6,
            command=self.limpiar_formulario
        )
        self.btn_limpiar.place(x=170, y=btn_y)
        
        self.btn_eliminar = tk.Button(
            self.frame_principal,
            text="🗑️ Eliminar",
            font=("Arial", 10, "bold"),
            bg="#dc2626", fg="white",
            activebackground="#991b1b",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6,
            command=self.eliminar_oferta
        )
        self.btn_eliminar.place(x=630, y=btn_y)
        
        # Botón "Ver Todas" (restaurar filtros)
        self.btn_ver_todas = tk.Button(
            self.frame_principal,
            text="⟲ Ver Todas",
            font=("Arial", 10, "bold"),
            bg="#475569", fg="white",
            activebackground="#334155",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=6,
            command=self.cargar_ofertas
        )
        self.btn_ver_todas.place(x=750, y=btn_y)
        
        # === SECCIÓN TABLA ===
        self.canvas.create_rectangle(50, 315, 850, 530, 
                                     fill="#1e293b", outline="#3b82f6", width=2)
        
        # Fila de título y controles
        self.canvas.create_text(130, 330, 
                               text="OFERTAS REGISTRADAS", 
                               font=("Arial", 12, "bold"), 
                               fill="#3b82f6", anchor="w")
        
        # --- FILTROS (bien espaciados horizontalmente) ---
        filtros_y = 323
        filtros_x_start = 440
        filtros_spacing = 110
        
        self.canvas.create_text(filtros_x_start - 30, 330, 
                               text="Filtrar:", 
                               font=("Arial", 9, "bold"), 
                               fill="#94a3b8")
        
        self.btn_filtro_producto = tk.Button(
            self.frame_principal,
            text="📦 Producto",
            font=("Arial", 9, "bold"),
            bg="#06b6d4", fg="white",
            activebackground="#0891b2",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=4,
            command=self.filtrar_por_producto
        )
        self.btn_filtro_producto.place(x=filtros_x_start, y=filtros_y)
        
        self.btn_filtro_mercado = tk.Button(
            self.frame_principal,
            text="🏪 Mercado",
            font=("Arial", 9, "bold"),
            bg="#06b6d4", fg="white",
            activebackground="#0891b2",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=4,
            command=self.filtrar_por_mercado
        )
        self.btn_filtro_mercado.place(x=filtros_x_start + filtros_spacing, y=filtros_y)
        
        # Botón Ver Historial
        self.btn_historial = tk.Button(
            self.frame_principal,
            text="📜 Historial",
            font=("Arial", 9, "bold"),
            bg="#8b5cf6", fg="white",
            activebackground="#7c3aed",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=4,
            command=self.ver_historial
        )
        self.btn_historial.place(x=filtros_x_start + filtros_spacing*2, y=filtros_y)
        
        # Frame para Treeview
        self.frame_tabla = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_tabla.place(x=70, y=350, width=760, height=160)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.frame_tabla,
            columns=("ID", "Producto", "Mercado", "Precio", "Stock", "Fecha"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=7
        )
        
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Mercado", text="Mercado")
        self.tree.heading("Precio", text="Precio (Bs)")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Fecha", text="Última Actualización")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Producto", width=200, anchor="w")
        self.tree.column("Mercado", width=180, anchor="w")
        self.tree.column("Precio", width=80, anchor="e")
        self.tree.column("Stock", width=70, anchor="center")
        self.tree.column("Fecha", width=150, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_oferta)
        
        # === PANEL DE ESTADÍSTICAS ===
        stats_y = 518
        self.canvas.create_text(450, stats_y, 
                               text="Estadísticas: Seleccione una oferta para ver detalles", 
                               font=("Arial", 9, "italic"), 
                               fill="#64748b",
                               tags="stats_text")
        
        # Estilo del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#0f172a",
                       foreground="white",
                       fieldbackground="#0f172a",
                       borderwidth=0)
        style.map("Treeview",
                 background=[("selected", "#3b82f6")])
        style.configure("Treeview.Heading",
                       background="#1e293b",
                       foreground="white",
                       borderwidth=1)
        
        # Crear botón volver
        self.crear_boton_volver()
    
    def crear_boton_volver(self):
        """Crea el botón de volver"""
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
        self.btn_volver.place(x=380, y=550)
    
    def cargar_ofertas(self):
        """Carga las ofertas existentes"""
        if not hasattr(self, 'tree'):
            return
        
        self.tree.delete(*self.tree.get_children())
        
        query = """
        SELECT 
            o.id_oferta,
            p.nombre_producto,
            p.unidad_medida,
            m.nombre_mercado,
            o.precio,
            o.stock,
            o.fecha_actualizacion
        FROM oferta o
        INNER JOIN producto p ON o.id_producto = p.id_producto
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        ORDER BY o.fecha_actualizacion DESC;
        """
        
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            for fila in resultados:
                id_oferta = fila[0]
                producto = f"{fila[1]} ({fila[2]})"
                mercado = fila[3]
                precio = f"{fila[4]:.2f}"
                stock = fila[5] if fila[5] is not None else "N/A"
                fecha = fila[6].strftime("%d/%m/%Y %H:%M") if fila[6] else ""
                
                self.tree.insert("", tk.END, values=(
                    id_oferta, producto, mercado, precio, stock, fecha
                ))
        
        # Restablecer texto de estadísticas
        if hasattr(self, 'canvas'):
            self.canvas.itemconfig("stats_text", 
                text="Estadísticas: Seleccione una oferta para ver detalles",
                fill="#64748b")
    
    def guardar_oferta(self):
        """Guarda o actualiza una oferta"""
        # Validar selecciones
        if not self.combo_producto.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        if not self.combo_mercado.get():
            messagebox.showwarning("Advertencia", "Seleccione un mercado")
            return
        
        # Validar precio
        precio_str = self.entry_precio.get().strip()
        if not precio_str:
            messagebox.showwarning("Advertencia", "Ingrese el precio")
            return
        
        try:
            precio = float(precio_str)
            if precio <= 0:
                messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingrese un precio válido (ejemplo: 5.50)")
            return
        
        # Validar stock (opcional)
        stock = None
        stock_str = self.entry_stock.get().strip()
        if stock_str:
            try:
                stock = int(stock_str)
                if stock < 0:
                    messagebox.showwarning("Advertencia", "El stock no puede ser negativo")
                    return
            except ValueError:
                messagebox.showwarning("Advertencia", "Ingrese un stock válido (número entero)")
                return
        
        # Obtener IDs
        id_producto = self.get_id_from_combo(self.combo_producto, self.productos_dict)
        id_mercado = self.get_id_from_combo(self.combo_mercado, self.mercados_dict)
        
        # Verificar si ya existe la oferta
        check_query = """
        SELECT id_oferta, precio FROM oferta 
        WHERE id_producto = %s AND id_mercado = %s;
        """
        resultado = execute_query(check_query, (id_producto, id_mercado), fetch=True)
        
        if resultado:
            # Ya existe, actualizar
            id_oferta = resultado[0][0]
            precio_anterior = resultado[0][1]
            
            # PASO 2: Guardar en historial antes de actualizar
            if precio != precio_anterior:  # Solo si el precio cambió
                historial_query = """
                INSERT INTO historial_p (id_producto, stock, fuente, observaciones)
                VALUES (%s, %s, %s, %s);
                """
                observacion = f"Precio actualizado de {precio_anterior:.2f} a {precio:.2f} Bs en {self.combo_mercado.get()}"
                execute_query(historial_query, (id_producto, stock, "Manual - Sistema", observacion))
                print(f"✓ Historial guardado: {observacion}")
            
            update_query = """
            UPDATE oferta 
            SET precio = %s, stock = %s, fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_oferta = %s;
            """
            
            if execute_query(update_query, (precio, stock, id_oferta)):
                messagebox.showinfo("Éxito", 
                    f"Oferta actualizada correctamente\n"
                    f"Precio anterior: {precio_anterior:.2f} Bs\n"
                    f"Precio nuevo: {precio:.2f} Bs\n\n"
                    f"✓ Cambio registrado en historial")
                self.limpiar_formulario()
                self.cargar_ofertas()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la oferta")
        else:
            # No existe, insertar nuevo
            insert_query = """
            INSERT INTO oferta (id_producto, id_mercado, precio, stock)
            VALUES (%s, %s, %s, %s);
            """
            
            if execute_query(insert_query, (id_producto, id_mercado, precio, stock)):
                messagebox.showinfo("Éxito", "Oferta registrada correctamente")
                self.limpiar_formulario()
                self.cargar_ofertas()
            else:
                messagebox.showerror("Error", "No se pudo registrar la oferta")
    
    def get_id_from_combo(self, combo, diccionario):
        """Obtiene el ID a partir del valor seleccionado en el combobox"""
        valor_seleccionado = combo.get()
        for id_item, nombre in diccionario.items():
            if nombre == valor_seleccionado:
                return id_item
        return None
    
    def seleccionar_oferta(self, event):
        """Llena el formulario con la oferta seleccionada y muestra estadísticas"""
        seleccion = self.tree.selection()
        if not seleccion:
            self.canvas.itemconfig("stats_text", 
                text="Estadísticas: Seleccione una oferta para ver detalles",
                fill="#64748b")
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        # valores = (ID, Producto, Mercado, Precio, Stock, Fecha)
        producto_str = valores[1]
        mercado_str = valores[2]
        precio = str(valores[3])
        stock = str(valores[4]) if valores[4] != "N/A" else ""
        
        # Buscar y seleccionar en combobox
        self.combo_producto.set(producto_str)
        self.combo_mercado.set(mercado_str)
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, precio)
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, stock)
        
        # Mostrar estadísticas de comparación
        id_producto = self.get_id_from_combo(self.combo_producto, self.productos_dict)
        
        # Obtener estadísticas del producto en todos los mercados
        query_stats = """
        SELECT 
            MIN(precio) as precio_min,
            MAX(precio) as precio_max,
            AVG(precio) as precio_prom,
            COUNT(*) as num_mercados
        FROM oferta
        WHERE id_producto = %s;
        """
        
        stats = execute_query(query_stats, (id_producto,), fetch=True)
        
        if stats and stats[0][0] is not None:
            precio_min = stats[0][0]
            precio_max = stats[0][1]
            precio_prom = stats[0][2]
            num_mercados = stats[0][3]
            precio_actual = float(precio)
            
            # Determinar si es buen precio
            if precio_actual <= precio_min:
                indicador = "🟢 PRECIO MÁS BAJO"
                color = "#10b981"
            elif precio_actual >= precio_max:
                indicador = "🔴 PRECIO MÁS ALTO"
                color = "#dc2626"
            elif precio_actual <= precio_prom:
                indicador = "🟡 PRECIO BAJO"
                color = "#f59e0b"
            else:
                indicador = "🟠 PRECIO ALTO"
                color = "#f97316"
            
            stats_text = (f"{indicador}  |  "
                        f"Este producto: Mín: {precio_min:.2f} Bs  "
                        f"Máx: {precio_max:.2f} Bs  "
                        f"Prom: {precio_prom:.2f} Bs  "
                        f"({num_mercados} mercado{'s' if num_mercados > 1 else ''})")
            
            self.canvas.itemconfig("stats_text", text=stats_text, fill=color)
        else:
            self.canvas.itemconfig("stats_text", 
                text="📊 Este es el único registro de este producto",
                fill="#64748b")
    
    def eliminar_oferta(self):
        """Elimina la oferta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una oferta para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        id_oferta = item['values'][0]
        producto = item['values'][1]
        mercado = item['values'][2]
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar esta oferta?\n\n"
            f"Producto: {producto}\n"
            f"Mercado: {mercado}"
        )
        
        if respuesta:
            query = "DELETE FROM oferta WHERE id_oferta = %s;"
            
            if execute_query(query, (id_oferta,)):
                # Verificar si la tabla quedó vacía
                check_query = "SELECT COUNT(*) FROM oferta;"
                resultado = execute_query(check_query, fetch=True)
                
                if resultado and resultado[0][0] == 0:
                    # Si está vacía, reiniciar la secuencia
                    reset_query = "ALTER SEQUENCE oferta_id_oferta_seq RESTART WITH 1;"
                    execute_query(reset_query)
                    messagebox.showinfo("Éxito", 
                        "Oferta eliminada correctamente\n\n"
                        "✓ Secuencia de IDs reiniciada (tabla vacía)")
                else:
                    messagebox.showinfo("Éxito", "Oferta eliminada correctamente")
                
                self.limpiar_formulario()
                self.cargar_ofertas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la oferta")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.combo_producto.set("")
        self.combo_mercado.set("")
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        
        # Deseleccionar en el tree
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        # Restablecer estadísticas
        self.canvas.itemconfig("stats_text", 
            text="Estadísticas: Seleccione una oferta para ver detalles",
            fill="#64748b")
    
    def filtrar_por_producto(self):
        """Filtra ofertas por producto específico"""
        if not self.productos_dict:
            return
        
        # Crear ventana de selección
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Filtrar por Producto")
        ventana.geometry("450x200")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        ventana.grab_set()
        
        tk.Label(ventana,
                text="Seleccione el producto:",
                font=("Arial", 11, "bold"),
                bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        combo = ttk.Combobox(
            ventana,
            values=list(self.productos_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=35
        )
        combo.pack(pady=10)
        
        def aplicar_filtro():
            if not combo.get():
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            id_producto = self.get_id_from_combo(combo, self.productos_dict)
            self.tree.delete(*self.tree.get_children())
            
            query = """
            SELECT 
                o.id_oferta,
                p.nombre_producto,
                p.unidad_medida,
                m.nombre_mercado,
                o.precio,
                o.stock,
                o.fecha_actualizacion
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE o.id_producto = %s
            ORDER BY o.precio ASC;
            """
            
            resultados = execute_query(query, (id_producto,), fetch=True)
            
            if resultados:
                for fila in resultados:
                    producto = f"{fila[1]} ({fila[2]})"
                    mercado = fila[3]
                    precio = f"{fila[4]:.2f}"
                    stock = fila[5] if fila[5] is not None else "N/A"
                    fecha = fila[6].strftime("%d/%m/%Y %H:%M") if fila[6] else ""
                    
                    self.tree.insert("", tk.END, values=(
                        fila[0], producto, mercado, precio, stock, fecha
                    ))
                
                # Calcular estadísticas
                precios = [float(fila[4]) for fila in resultados]
                precio_min = min(precios)
                precio_max = max(precios)
                precio_prom = sum(precios) / len(precios)
                
                stats_text = (f"📊 {combo.get()}: "
                            f"Mín: {precio_min:.2f} Bs  |  "
                            f"Máx: {precio_max:.2f} Bs  |  "
                            f"Promedio: {precio_prom:.2f} Bs  |  "
                            f"Mercados: {len(resultados)}")
                
                self.canvas.itemconfig("stats_text", text=stats_text, fill="#10b981")
                
                messagebox.showinfo("Filtro aplicado", 
                    f"Se encontraron {len(resultados)} ofertas de {combo.get()}")
            else:
                messagebox.showinfo("Sin resultados", 
                    f"No hay ofertas registradas para {combo.get()}")
            
            ventana.destroy()
        
        tk.Button(ventana,
                 text="✓ Aplicar Filtro",
                 font=("Arial", 10, "bold"),
                 bg="#10b981", fg="white",
                 command=aplicar_filtro,
                 padx=20, pady=8).pack(pady=10)
        
        tk.Button(ventana,
                 text="✕ Cancelar",
                 font=("Arial", 9),
                 bg="#475569", fg="white",
                 command=ventana.destroy,
                 padx=15, pady=5).pack()
    
    def filtrar_por_mercado(self):
        """Filtra ofertas por mercado específico"""
        if not self.mercados_dict:
            return
        
        # Crear ventana de selección
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Filtrar por Mercado")
        ventana.geometry("450x200")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        ventana.grab_set()
        
        tk.Label(ventana,
                text="Seleccione el mercado:",
                font=("Arial", 11, "bold"),
                bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        combo = ttk.Combobox(
            ventana,
            values=list(self.mercados_dict.values()),
            state="readonly",
            font=("Arial", 10),
            width=35
        )
        combo.pack(pady=10)
        
        def aplicar_filtro():
            if not combo.get():
                messagebox.showwarning("Advertencia", "Seleccione un mercado")
                return
            
            id_mercado = self.get_id_from_combo(combo, self.mercados_dict)
            self.tree.delete(*self.tree.get_children())
            
            query = """
            SELECT 
                o.id_oferta,
                p.nombre_producto,
                p.unidad_medida,
                m.nombre_mercado,
                o.precio,
                o.stock,
                o.fecha_actualizacion
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE o.id_mercado = %s
            ORDER BY p.nombre_producto ASC;
            """
            
            resultados = execute_query(query, (id_mercado,), fetch=True)
            
            if resultados:
                for fila in resultados:
                    producto = f"{fila[1]} ({fila[2]})"
                    mercado = fila[3]
                    precio = f"{fila[4]:.2f}"
                    stock = fila[5] if fila[5] is not None else "N/A"
                    fecha = fila[6].strftime("%d/%m/%Y %H:%M") if fila[6] else ""
                    
                    self.tree.insert("", tk.END, values=(
                        fila[0], producto, mercado, precio, stock, fecha
                    ))
                
                # Calcular estadísticas
                precios = [float(fila[4]) for fila in resultados]
                precio_prom = sum(precios) / len(precios)
                
                stats_text = (f"🏪 {combo.get()}: "
                            f"{len(resultados)} productos  |  "
                            f"Precio promedio: {precio_prom:.2f} Bs")
                
                self.canvas.itemconfig("stats_text", text=stats_text, fill="#06b6d4")
                
                messagebox.showinfo("Filtro aplicado", 
                    f"Se encontraron {len(resultados)} productos en {combo.get()}")
            else:
                messagebox.showinfo("Sin resultados", 
                    f"No hay ofertas registradas en {combo.get()}")
            
            ventana.destroy()
        
        tk.Button(ventana,
                 text="✓ Aplicar Filtro",
                 font=("Arial", 10, "bold"),
                 bg="#10b981", fg="white",
                 command=aplicar_filtro,
                 padx=20, pady=8).pack(pady=10)
        
        tk.Button(ventana,
                 text="✕ Cancelar",
                 font=("Arial", 9),
                 bg="#475569", fg="white",
                 command=ventana.destroy,
                 padx=15, pady=5).pack()
    
    def ver_historial(self):
        """Muestra el historial de cambios de precios"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Información", 
                "Seleccione una oferta para ver su historial de cambios")
            return
        
        item = self.tree.item(seleccion[0])
        id_oferta = item['values'][0]
        producto = item['values'][1]
        
        # Obtener id_producto
        query_id = """
        SELECT id_producto FROM oferta WHERE id_oferta = %s;
        """
        result = execute_query(query_id, (id_oferta,), fetch=True)
        if not result:
            return
        
        id_producto = result[0][0]
        
        # Obtener historial
        query_historial = """
        SELECT fecha_registro, stock, fuente, observaciones
        FROM historial_p
        WHERE id_producto = %s
        ORDER BY fecha_registro DESC
        LIMIT 10;
        """
        
        historial = execute_query(query_historial, (id_producto,), fetch=True)
        
        if not historial:
            messagebox.showinfo("Historial", 
                f"No hay historial de cambios para:\n{producto}")
            return
        
        # Crear ventana de historial
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title(f"Historial - {producto}")
        ventana.geometry("700x400")
        ventana.configure(bg="#0a0f1e")
        
        # Título
        tk.Label(ventana, 
                text=f"📜 Historial de Cambios",
                font=("Arial", 14, "bold"),
                bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana, 
                text=producto,
                font=("Arial", 11),
                bg="#0a0f1e", fg="#94a3b8").pack()
        
        # Frame para tabla
        frame = tk.Frame(ventana, bg="#1e293b")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        tree_hist = ttk.Treeview(frame,
                                columns=("Fecha", "Stock", "Fuente", "Observaciones"),
                                show="headings",
                                yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree_hist.yview)
        
        tree_hist.heading("Fecha", text="Fecha/Hora")
        tree_hist.heading("Stock", text="Stock")
        tree_hist.heading("Fuente", text="Fuente")
        tree_hist.heading("Observaciones", text="Observaciones")
        
        tree_hist.column("Fecha", width=150)
        tree_hist.column("Stock", width=80)
        tree_hist.column("Fuente", width=120)
        tree_hist.column("Observaciones", width=300)
        
        tree_hist.pack(fill=tk.BOTH, expand=True)
        
        # Llenar datos
        for fila in historial:
            fecha = fila[0].strftime("%d/%m/%Y %H:%M:%S") if fila[0] else ""
            stock = fila[1] if fila[1] is not None else "N/A"
            fuente = fila[2] or "N/A"
            obs = fila[3] or ""
            
            tree_hist.insert("", tk.END, values=(fecha, stock, fuente, obs))
        
        # Botón cerrar
        tk.Button(ventana,
                 text="Cerrar",
                 font=("Arial", 10, "bold"),
                 bg="#475569", fg="white",
                 command=ventana.destroy,
                 padx=20, pady=5).pack(pady=10)
    
    def resetear_secuencia(self):
        """Reinicia la secuencia de IDs de la tabla oferta"""
        # Verificar cuántas ofertas hay
        check_query = "SELECT COUNT(*) FROM oferta;"
        resultado = execute_query(check_query, fetch=True)
        
        if not resultado:
            return
        
        cantidad = resultado[0][0]
        
        if cantidad > 0:
            respuesta = messagebox.askyesno(
                "Advertencia",
                f"⚠️  Hay {cantidad} oferta(s) registrada(s)\n\n"
                "Si resetea los IDs ahora, podría causar conflictos.\n"
                "Es recomendable solo resetear cuando la tabla está VACÍA.\n\n"
                "¿Desea continuar de todos modos?"
            )
            if not respuesta:
                return
        
        # Obtener el ID máximo actual
        max_query = "SELECT COALESCE(MAX(id_oferta), 0) FROM oferta;"
        max_result = execute_query(max_query, fetch=True)
        max_id = max_result[0][0] if max_result else 0
        
        # Reiniciar la secuencia al siguiente ID disponible
        nuevo_inicio = max_id + 1 if cantidad > 0 else 1
        
        reset_query = f"ALTER SEQUENCE oferta_id_oferta_seq RESTART WITH {nuevo_inicio};"
        
        if execute_query(reset_query):
            if cantidad == 0:
                messagebox.showinfo(
                    "Éxito",
                    f"✓ Secuencia reiniciada\n\n"
                    f"Los próximos IDs comenzarán desde: {nuevo_inicio}"
                )
            else:
                messagebox.showinfo(
                    "Éxito",
                    f"✓ Secuencia ajustada\n\n"
                    f"Próximo ID disponible: {nuevo_inicio}\n"
                    f"(Basado en el ID máximo actual: {max_id})"
                )
            self.cargar_ofertas()
        else:
            messagebox.showerror("Error", "No se pudo resetear la secuencia")
    
    def volver(self):
        """Vuelve al menú principal"""
        self.limpiar_formulario()
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()