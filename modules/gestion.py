import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from database.connection import DatabaseConnection, execute_query


class GestionProductos:
    def __init__(self, parent_canvas, parent_frame, volver_callback):
        self.canvas = parent_canvas
        self.frame = parent_frame
        self.volver_callback = volver_callback
        
        # Variables del formulario
        self.producto_seleccionado = None
        self.modo_edicion = False
        self.df_productos = None  # DataFrame para almacenar productos
        
        # Limpiar canvas
        self.canvas.delete("all")
        
        # Crear interfaz
        self.crear_interfaz()
        self.cargar_productos()
        
    
    def crear_interfaz(self):
        """Crea la interfaz completa del módulo"""
        
        # Header
        self.canvas.create_text(450, 30, 
                               text="📊 Gestión de Productos", 
                               font=("Arial", 20, "bold"), 
                               fill="#10b981")
        
        self.canvas.create_text(450, 55, 
                               text="Administra el catálogo de productos del mercado", 
                               font=("Arial", 10), 
                               fill="#94a3b8")
        
        # Línea divisoria
        self.canvas.create_line(50, 75, 850, 75, fill="#334155", width=2)
        
        # Frame para formulario (izquierda)
        self.crear_formulario()
        
        # Frame para tabla (derecha)
        self.crear_tabla()
        
        # Botón volver
        btn_volver = tk.Button(
            self.frame,
            text="← Volver al Menú",
            font=("Arial", 10, "bold"),
            bg="#475569",
            fg="white",
            activebackground="#1e293b",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.volver_menu
        )
        btn_volver.place(x=50, y=560)
    
    def crear_formulario(self):
        """Crea el formulario de entrada de datos"""
        
        # Fondo del formulario
        self.canvas.create_rectangle(50, 100, 350, 540, 
                                     fill="#1e293b", outline="#10b981", width=2)
        
        self.canvas.create_text(200, 120, 
                               text="FORMULARIO DE PRODUCTO", 
                               font=("Arial", 11, "bold"), 
                               fill="#e2e8f0")
        
        # Labels y campos
        y_start = 160
        y_gap = 70
        
        # Nombre del producto
        self.canvas.create_text(80, y_start, 
                               text="Nombre:", 
                               font=("Arial", 9, "bold"), 
                               fill="#94a3b8", anchor="w")
        self.entry_nombre = tk.Entry(self.frame, font=("Arial", 10), 
                                     bg="#0a0f1e", fg="#e2e8f0",
                                     insertbackground="#10b981",
                                     relief=tk.FLAT, width=25)
        self.entry_nombre.place(x=80, y=y_start + 10)
        
        # Categoría
        y_start += y_gap
        self.canvas.create_text(80, y_start, 
                               text="Categoría:", 
                               font=("Arial", 9, "bold"), 
                               fill="#94a3b8", anchor="w")
        
        self.combo_categoria = ttk.Combobox(
            self.frame, 
            font=("Arial", 10),
            width=23,
            state="readonly"
        )
        self.combo_categoria.place(x=80, y=y_start + 10)
        self.cargar_categorias()
        
        # Unidad de medida
        y_start += y_gap
        self.canvas.create_text(80, y_start, 
                               text="Unidad:", 
                               font=("Arial", 9, "bold"), 
                               fill="#94a3b8", anchor="w")
        
        self.combo_unidad = ttk.Combobox(
            self.frame,
            font=("Arial", 10),
            values=["kg", "lb", "unidad", "docena", "arroba", "quintal", "litro"],
            width=23,
            state="readonly"
        )
        self.combo_unidad.place(x=80, y=y_start + 10)
        self.combo_unidad.current(0)
        
        # Descripción
        y_start += y_gap
        self.canvas.create_text(80, y_start, 
                               text="Descripción:", 
                               font=("Arial", 9, "bold"), 
                               fill="#94a3b8", anchor="w")
        
        self.text_descripcion = tk.Text(
            self.frame,
            font=("Arial", 9),
            bg="#0a0f1e",
            fg="#e2e8f0",
            insertbackground="#10b981",
            relief=tk.FLAT,
            width=28,
            height=3,
            wrap=tk.WORD
        )
        self.text_descripcion.place(x=80, y=y_start + 10)
        
        # Botones de acción
        y_botones = 480
        
        self.btn_agregar = tk.Button(
            self.frame,
            text="✓ Agregar",
            font=("Arial", 10, "bold"),
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            relief=tk.FLAT,
            cursor="hand2",
            width=10,
            command=self.agregar_producto
        )
        self.btn_agregar.place(x=70, y=y_botones)
        
        self.btn_limpiar = tk.Button(
            self.frame,
            text="⟲ Limpiar",
            font=("Arial", 10, "bold"),
            bg="#6366f1",
            fg="white",
            activebackground="#4f46e5",
            relief=tk.FLAT,
            cursor="hand2",
            width=10,
            command=self.limpiar_formulario
        )
        self.btn_limpiar.place(x=190, y=y_botones)
    
    def crear_tabla(self):
        """Crea la tabla para mostrar productos usando pandas para configuración"""
        
        # Fondo de la tabla
        self.canvas.create_rectangle(370, 100, 850, 540, 
                                     fill="#1e293b", outline="#10b981", width=2)
        
        self.canvas.create_text(610, 120, 
                               text="LISTA DE PRODUCTOS", 
                               font=("Arial", 11, "bold"), 
                               fill="#e2e8f0")
        
        # Frame para contener el Treeview y scrollbar
        frame_tabla = tk.Frame(self.frame, bg="#1e293b")
        frame_tabla.place(x=385, y=145, width=450, height=340)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configuración de columnas con numpy array para dimensiones
        columnas = ["ID", "Nombre", "Categoría", "Unidad"]
        anchos = np.array([40, 180, 120, 80])
        
        # Treeview (tabla)
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=14,
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas usando numpy para iterar
        for i, col in enumerate(columnas):
            self.tree.heading(col, text=col)
            anchor = "center" if i in [0, 3] else "w"
            self.tree.column(col, width=int(anchos[i]), anchor=anchor)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#0a0f1e",
                       foreground="#e2e8f0",
                       fieldbackground="#0a0f1e",
                       borderwidth=0)
        style.map('Treeview', background=[('selected', '#10b981')])
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Botones de acción para la tabla
        y_btn = 500
        
        self.btn_editar = tk.Button(
            self.frame,
            text="✎ Editar",
            font=("Arial", 9, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            relief=tk.FLAT,
            cursor="hand2",
            width=12,
            command=self.editar_producto
        )
        self.btn_editar.place(x=450, y=y_btn)
        
        self.btn_eliminar = tk.Button(
            self.frame,
            text="✗ Eliminar",
            font=("Arial", 9, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#991b1b",
            relief=tk.FLAT,
            cursor="hand2",
            width=12,
            command=self.eliminar_producto
        )
        self.btn_eliminar.place(x=590, y=y_btn)
        
        self.btn_refrescar = tk.Button(
            self.frame,
            text="↻ Refrescar",
            font=("Arial", 9, "bold"),
            bg="#6366f1",
            fg="white",
            activebackground="#4f46e5",
            relief=tk.FLAT,
            cursor="hand2",
            width=12,
            command=self.cargar_productos
        )
        self.btn_refrescar.place(x=730, y=y_btn)
    
    def cargar_categorias(self):
        """Carga las categorías usando pandas"""
        query = "SELECT nombre FROM categorias ORDER BY nombre"
        categorias = execute_query(query, fetch=True)
        
        if categorias:
            # Usar pandas para procesar rápidamente
            df_cat = pd.DataFrame(categorias, columns=['nombre'])
            nombres_categorias = df_cat['nombre'].tolist()
            
            self.combo_categoria['values'] = nombres_categorias
            if nombres_categorias:
                self.combo_categoria.current(0)
    
    def cargar_productos(self):
        """Carga productos usando pandas para mejor manejo de datos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Consultar productos
        query = """
        SELECT id_producto, nombre_producto, categoria, unidad_medida
        FROM producto
        WHERE activo = TRUE
        ORDER BY nombre_producto
        """
        
        productos = execute_query(query, fetch=True)
        
        if productos:
            # Usar pandas DataFrame para procesar datos
            self.df_productos = pd.DataFrame(productos, 
                                            columns=['id', 'nombre', 'categoria', 'unidad'])
            
            # Insertar en la tabla de forma eficiente
            for row in self.df_productos.itertuples(index=False):
                self.tree.insert("", tk.END, values=row)
    
    def agregar_producto(self):
        """Agrega o actualiza un producto con validación optimizada"""
        # Obtener y validar datos usando dict comprehension
        datos = {
            'nombre': self.entry_nombre.get().strip(),
            'categoria': self.combo_categoria.get(),
            'unidad': self.combo_unidad.get(),
            'descripcion': self.text_descripcion.get("1.0", tk.END).strip()
        }
        
        # Validación compacta
        if not datos['nombre']:
            messagebox.showwarning("Validación", "El nombre es obligatorio")
            return
        
        if not datos['categoria']:
            messagebox.showwarning("Validación", "Seleccione una categoría")
            return
        
        try:
            if self.modo_edicion and self.producto_seleccionado:
                # Actualizar producto existente
                query = """
                UPDATE producto 
                SET nombre_producto = %s, categoria = %s, unidad_medida = %s, descripcion = %s
                WHERE id_producto = %s
                """
                params = (datos['nombre'], datos['categoria'], datos['unidad'], 
                         datos['descripcion'], self.producto_seleccionado)
                
                if execute_query(query, params):
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                    self.limpiar_formulario()
                    self.cargar_productos()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el producto")
            else:
                # Insertar nuevo producto
                query = """
                INSERT INTO producto (nombre_producto, categoria, unidad_medida, descripcion)
                VALUES (%s, %s, %s, %s)
                """
                params = (datos['nombre'], datos['categoria'], datos['unidad'], datos['descripcion'])
                
                if execute_query(query, params):
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                    self.limpiar_formulario()
                    self.cargar_productos()
                else:
                    messagebox.showerror("Error", "No se pudo agregar el producto.\nPuede que ya exista.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar: {str(e)}")
    
    def editar_producto(self):
        """Prepara el formulario para editar usando pandas para búsqueda rápida"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        # Usar pandas para búsqueda rápida si el DataFrame existe
        if self.df_productos is not None:
            producto = self.df_productos[self.df_productos['id'] == valores[0]].iloc[0]
            
            # Cargar datos en el formulario
            self.producto_seleccionado = int(producto['id'])
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, producto['nombre'])
            
            # Seleccionar categoría
            if pd.notna(producto['categoria']):
                self.combo_categoria.set(producto['categoria'])
            
            # Seleccionar unidad
            self.combo_unidad.set(producto['unidad'])
        
        # Cargar descripción
        query = "SELECT descripcion FROM producto WHERE id_producto = %s"
        result = execute_query(query, (self.producto_seleccionado,), fetch=True)
        if result and result[0][0]:
            self.text_descripcion.delete("1.0", tk.END)
            self.text_descripcion.insert("1.0", result[0][0])
        
        # Cambiar modo
        self.modo_edicion = True
        self.btn_agregar.config(text="✓ Actualizar", bg="#f59e0b")
    
    def eliminar_producto(self):
        """Elimina (desactiva) un producto"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        id_producto = item['values'][0]
        nombre = item['values'][1]
        
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el producto '{nombre}'?"
        )
        
        if respuesta:
            query = "UPDATE producto SET activo = FALSE WHERE id_producto = %s"
            if execute_query(query, (id_producto,)):
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.cargar_productos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        if self.combo_categoria['values']:
            self.combo_categoria.current(0)
        self.combo_unidad.current(0)
        self.text_descripcion.delete("1.0", tk.END)
        self.producto_seleccionado = None
        self.modo_edicion = False
        self.btn_agregar.config(text="✓ Agregar", bg="#10b981")
    
    def on_select(self, event):
        """Evento cuando se selecciona un item de la tabla"""
        pass
    
    def volver_menu(self):
        """Vuelve al menú principal"""
        # Limpiar widgets
        for widget in self.frame.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        # Llamar al callback
        self.volver_callback()