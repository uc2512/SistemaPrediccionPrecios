import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query

class GestionCategorias:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        # Variables
        self.categoria_seleccionada = None
        self.modo_edicion = False
        
        self.canvas.delete("all")
        self.crear_interfaz()
        self.cargar_categorias()
    
    def crear_interfaz(self):
        """Crea la interfaz de gestión de categorías"""
        # Header
        self.canvas.create_text(450, 30,
                               text="📋 GESTIÓN DE CATEGORÍAS",
                               font=("Arial", 20, "bold"),
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 55,
                               text="Clasificación de productos del mercado",
                               font=("Arial", 11),
                               fill="#94a3b8")
        
        # Línea divisoria
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        # === SECCIÓN FORMULARIO ===
        self.canvas.create_rectangle(50, 90, 420, 380,
                                     fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(235, 105,
                               text="FORMULARIO DE CATEGORÍA",
                               font=("Arial", 12, "bold"),
                               fill="#06b6d4")
        
        y_base = 145
        spacing = 70
        
        # Nombre de la categoría
        self.canvas.create_text(90, y_base,
                               text="Nombre:",
                               font=("Arial", 10, "bold"),
                               fill="#e2e8f0", anchor="w")
        
        self.entry_nombre = tk.Entry(
            self.frame_principal,
            font=("Arial", 11),
            bg="#0f172a", fg="white",
            insertbackground="white",
            width=30
        )
        self.entry_nombre.place(x=90, y=y_base + 15)
        
        # Descripción
        self.canvas.create_text(90, y_base + spacing,
                               text="Descripción:",
                               font=("Arial", 10, "bold"),
                               fill="#e2e8f0", anchor="w")
        
        self.text_descripcion = tk.Text(
            self.frame_principal,
            font=("Arial", 10),
            bg="#0f172a", fg="white",
            insertbackground="white",
            width=33,
            height=5,
            wrap=tk.WORD
        )
        self.text_descripcion.place(x=90, y=y_base + spacing + 15)
        
        # Botones de acción
        btn_y = 340
        
        self.btn_agregar = tk.Button(
            self.frame_principal,
            text="✚ Agregar",
            font=("Arial", 10, "bold"),
            bg="#10b981", fg="white",
            activebackground="#059669",
            relief=tk.FLAT, cursor="hand2",
            padx=18, pady=6,
            command=self.agregar_categoria
        )
        self.btn_agregar.place(x=100, y=btn_y)
        
        self.btn_limpiar = tk.Button(
            self.frame_principal,
            text="🔄 Limpiar",
            font=("Arial", 10, "bold"),
            bg="#6366f1", fg="white",
            activebackground="#4f46e5",
            relief=tk.FLAT, cursor="hand2",
            padx=18, pady=6,
            command=self.limpiar_formulario
        )
        self.btn_limpiar.place(x=230, y=btn_y)
        
        # === SECCIÓN TABLA ===
        self.canvas.create_rectangle(440, 90, 850, 380,
                                     fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(645, 105,
                               text="CATEGORÍAS REGISTRADAS",
                               font=("Arial", 12, "bold"),
                               fill="#06b6d4")
        
        # Frame para Treeview
        self.frame_tabla = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_tabla.place(x=460, y=130, width=370, height=190)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.frame_tabla,
            columns=("ID", "Nombre", "Productos"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Categoría")
        self.tree.heading("Productos", text="Productos")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=220, anchor="w")
        self.tree.column("Productos", width=80, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_categoria)
        
        # Estilo del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#0f172a",
                       foreground="white",
                       fieldbackground="#0f172a",
                       borderwidth=0)
        style.map("Treeview", background=[("selected", "#06b6d4")])
        style.configure("Treeview.Heading",
                       background="#1e293b",
                       foreground="white",
                       borderwidth=1)
        
        # Botones de acción de tabla
        btn_tabla_y = 340
        
        self.btn_editar = tk.Button(
            self.frame_principal,
            text="✎ Editar",
            font=("Arial", 9, "bold"),
            bg="#f59e0b", fg="white",
            activebackground="#d97706",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=5,
            command=self.editar_categoria
        )
        self.btn_editar.place(x=510, y=btn_tabla_y)
        
        self.btn_eliminar = tk.Button(
            self.frame_principal,
            text="🗑 Eliminar",
            font=("Arial", 9, "bold"),
            bg="#dc2626", fg="white",
            activebackground="#991b1b",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=5,
            command=self.eliminar_categoria
        )
        self.btn_eliminar.place(x=620, y=btn_tabla_y)
        
        self.btn_refrescar = tk.Button(
            self.frame_principal,
            text="↻ Refrescar",
            font=("Arial", 9, "bold"),
            bg="#8b5cf6", fg="white",
            activebackground="#7c3aed",
            relief=tk.FLAT, cursor="hand2",
            padx=15, pady=5,
            command=self.cargar_categorias
        )
        self.btn_refrescar.place(x=730, y=btn_tabla_y)
        
        # === PANEL DE ESTADÍSTICAS ===
        self.canvas.create_rectangle(50, 400, 850, 550,
                                     fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(450, 415,
                               text="📊 DISTRIBUCIÓN DE PRODUCTOS POR CATEGORÍA",
                               font=("Arial", 11, "bold"),
                               fill="#06b6d4")
        
        # Área de estadísticas (se actualizará dinámicamente)
        self.stats_frame = tk.Frame(self.frame_principal, bg="#1e293b")
        self.stats_frame.place(x=70, y=427, width=760, height=104)
        
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
        
        self.btn_volver.place(x=380, y=559)
    
    def cargar_categorias(self):
        """Carga las categorías desde la base de datos"""
        print("🔄 Cargando categorías...")  # Debug
    
        # Limpiar tabla FORZANDO la actualización
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        # FORZAR actualización del widget
        self.tree.update_idletasks()
    
        # Consulta simplificada
        query = """
        SELECT 
            id_categoria,
            nombre,
            COALESCE(
                (SELECT COUNT(*) 
                FROM producto 
                WHERE categoria = categorias.nombre AND activo = TRUE), 
                0
            ) as num_productos
        FROM categorias
        WHERE activo = TRUE
        ORDER BY nombre;
        """
    
        try:
            resultados = execute_query(query, fetch=True)
            print(f"✓ Resultados obtenidos: {len(resultados) if resultados else 0}")
        
            if resultados:
                for fila in resultados:
                    print(f"  - Insertando: ID={fila[0]}, Nombre={fila[1]}, Productos={fila[2]}")
                    # Insertar y FORZAR visualización
                    item_id = self.tree.insert("", tk.END, values=(
                        fila[0],  # ID
                        fila[1],  # Nombre
                        fila[2]   # Cantidad de productos
                    ))
                    print(f"    ✓ Item insertado con ID: {item_id}")
            
                # FORZAR renderizado
                self.tree.update()
                print(f"✓ Total de items en el Treeview: {len(self.tree.get_children())}")
            else:
                print("⚠️ No se encontraron categorías activas")
    
        except Exception as e:
            print(f"❌ Error al cargar categorías: {e}")
            import traceback
            traceback.print_exc()  # Muestra el error completo
            messagebox.showerror("Error", f"No se pudieron cargar las categorías:\n{str(e)}")
    
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        """Actualiza el panel de estadísticas - Versión optimizada con 5 barras visibles"""
        # Limpiar frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
    
        # Obtener estadísticas
        query = """
        SELECT 
            c.nombre,
            COUNT(p.id_producto) as num_productos
        FROM categorias c
        LEFT JOIN producto p ON c.nombre = p.categoria AND p.activo = TRUE
        WHERE c.activo = TRUE
        GROUP BY c.nombre
        ORDER BY num_productos DESC
        LIMIT 5;
        """
    
        stats = execute_query(query, fetch=True)
    
        print(f"📊 Estadísticas obtenidas: {stats}")  # Debug
    
        if not stats or all(s[1] == 0 for s in stats):
            tk.Label(
                self.stats_frame,
                text="📦 No hay productos asignados a categorías",
                font=("Arial", 11),
                bg="#1e293b", fg="#94a3b8"
            ).pack(pady=20)
            return
    
        # Título MÁS COMPACTO (sin padding superior)
        tk.Label(
            self.stats_frame,
            text="Top 5 Categorías:",
            font=("Arial", 9, "bold"),
            bg="#1e293b", fg="#e2e8f0"
        ).pack(anchor="w", padx=10, pady=(0, 3))  # ← Cambió de (0,5) a (0,3)
    
        # Frame directo para las barras
        frame_barras = tk.Frame(self.stats_frame, bg="#1e293b")
        frame_barras.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)
    
        max_productos = max([s[1] for s in stats]) if stats else 1
        colores = ["#10b981", "#06b6d4", "#8b5cf6", "#f59e0b", "#ec4899"]
    
        # Filtrar solo las que tienen productos
        stats_con_productos = [(n, c) for n, c in stats if c > 0]
    
        if not stats_con_productos:
            tk.Label(
                frame_barras,
                text="📦 No hay productos asignados a categorías",
                font=("Arial", 10),
                bg="#1e293b", fg="#94a3b8"
            ).pack(pady=15)
            return
    
        num_barras = len(stats_con_productos)
        print(f"  📊 Creando {num_barras} barras")
    
        # Altura fija por barra (reducida para que quepan 5)
        altura_por_barra = 12  # ← Reducido de 13 a 12
    
        for idx, (nombre, cantidad) in enumerate(stats_con_productos):
            print(f"  Creando barra {idx+1}/{num_barras}: {nombre} = {cantidad} productos")
        
            # Frame para cada barra con altura fija
            fila = tk.Frame(frame_barras, bg="#1e293b", height=altura_por_barra)
            fila.pack(fill=tk.X, pady=1.5)  # ← Reducido de 2 a 1.5px
            fila.pack_propagate(False)
        
            # Nombre de categoría (ancho fijo)
            nombre_display = nombre[:12] + "..." if len(nombre) > 12 else nombre
        
            lbl_nombre = tk.Label(
                fila,
                text=f"{nombre_display}:",
                font=("Arial", 8),
                bg="#1e293b", fg="#e2e8f0",
                width=13,
                anchor="w"
            )
            lbl_nombre.pack(side=tk.LEFT)
        
            # Canvas para la barra
            ancho_max_barra = 620
            ancho_barra = int((cantidad / max_productos) * ancho_max_barra)
            ancho_barra = max(ancho_barra, 15)  # Mínimo visible
        
            color = colores[idx % len(colores)]
        
            canvas_barra = tk.Canvas(
                fila,
                width=ancho_max_barra,
                height=9,  # ← Reducido de 10 a 9px
                bg="#0f172a",
                highlightthickness=0
            )
            canvas_barra.pack(side=tk.LEFT, padx=3)
        
            # Dibujar barra
            canvas_barra.create_rectangle(
                0, 0, ancho_barra, 9,
                fill=color, outline=""
            )
        
            # Cantidad con color
            lbl_cantidad = tk.Label(
                fila,
                text=f"{cantidad}",
                font=("Arial", 9, "bold"),
                bg="#1e293b", fg=color,
                width=2,
                anchor="e"
            )
            lbl_cantidad.pack(side=tk.LEFT, padx=3)
    
        print(f"✓ Total de barras creadas: {num_barras}")
    
    def agregar_categoria(self):
        """Agrega o actualiza una categoría"""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()

        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre de la categoría es obligatorio")
            return

        print(f"📝 Intentando {'actualizar' if self.modo_edicion else 'agregar'}: '{nombre}'")

        try:
            if self.modo_edicion and self.categoria_seleccionada:
                # Actualizar categoría existente
                query = """
                UPDATE categorias
                SET nombre = %s, descripcion = %s
                WHERE id_categoria = %s
                RETURNING id_categoria;
                """
        
                resultado = execute_query(query, (nombre, descripcion, self.categoria_seleccionada), fetch=True)
        
                if resultado:
                    print(f"✓ Categoría actualizada: ID {resultado[0][0]}")
                    messagebox.showinfo("Éxito", "Categoría actualizada correctamente")
                    self.limpiar_formulario()
                
                    # ESPERAR un momento antes de recargar
                    self.frame_principal.after(100, self.cargar_categorias)
                else:
                    print("❌ No se pudo actualizar")
                    messagebox.showerror("Error", "No se pudo actualizar la categoría")
    
            else:
                # Insertar nueva categoría
                query = """
                INSERT INTO categorias (nombre, descripcion, activo)
                VALUES (%s, %s, TRUE)
                RETURNING id_categoria;
                """
        
                resultado = execute_query(query, (nombre, descripcion), fetch=True)
        
                if resultado:
                    nuevo_id = resultado[0][0]
                    print(f"✓ Categoría agregada: ID {nuevo_id}")
                
                    # Mostrar mensaje
                    messagebox.showinfo("Éxito", 
                        f"✓ Categoría '{nombre}' agregada correctamente\n"
                        f"ID asignado: {nuevo_id}")
                
                    self.limpiar_formulario()
                
                    # ESPERAR un momento antes de recargar
                    print("⏳ Esperando 100ms antes de recargar...")
                    self.frame_principal.after(100, self.cargar_categorias)
                else:
                    print("❌ No se pudo agregar")
                    messagebox.showerror("Error", 
                        "No se pudo agregar la categoría.\n"
                        "Puede que ya exista una con ese nombre.")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")
    
    def seleccionar_categoria(self, event):
        """Llena el formulario con la categoría seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        # Cargar datos en el formulario
        self.categoria_seleccionada = valores[0]
        
        # Obtener descripción completa
        query = "SELECT nombre, descripcion FROM categorias WHERE id_categoria = %s;"
        resultado = execute_query(query, (self.categoria_seleccionada,), fetch=True)
        
        if resultado:
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, resultado[0][0])
            
            self.text_descripcion.delete("1.0", tk.END)
            if resultado[0][1]:
                self.text_descripcion.insert("1.0", resultado[0][1])
    
    def editar_categoria(self):
        """Prepara el formulario para editar"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una categoría de la tabla")
            return
        
        # Ya se cargaron los datos con seleccionar_categoria
        self.modo_edicion = True
        self.btn_agregar.config(text="✓ Actualizar", bg="#f59e0b")
    
    def eliminar_categoria(self):
        """Elimina (desactiva) una categoría si no tiene productos"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una categoría de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        id_categoria = item['values'][0]
        nombre = item['values'][1]
        num_productos = item['values'][2]
        
        # Verificar si tiene productos asociados
        if num_productos > 0:
            messagebox.showwarning(
                "No se puede eliminar",
                f"La categoría '{nombre}' tiene {num_productos} producto(s) asociado(s).\n\n"
                "Debe reasignar o eliminar esos productos primero."
            )
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar la categoría '{nombre}'?"
        )
        
        if respuesta:
            query = "UPDATE categorias SET activo = FALSE WHERE id_categoria = %s;"
            
            if execute_query(query, (id_categoria,)):
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
                self.limpiar_formulario()
                self.cargar_categorias()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.text_descripcion.delete("1.0", tk.END)
        
        self.categoria_seleccionada = None
        self.modo_edicion = False
        self.btn_agregar.config(text="✚ Agregar", bg="#10b981")
        
        # Deseleccionar en el tree
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def volver(self):
        """Vuelve al menú principal"""
        self.limpiar_formulario()
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()