import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query

class GestionMercados:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        self.canvas.delete("all")
        self.crear_interfaz()
        self.cargar_mercados()
    
    def crear_interfaz(self):
        """Crea la interfaz de gestión de mercados"""
        
        # Header
        self.canvas.create_text(450, 30, 
                               text="🏪 GESTIÓN DE MERCADOS", 
                               font=("Arial", 20, "bold"), 
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, 
                               text="Administración de mercados de Bolivia", 
                               font=("Arial", 11), 
                               fill="#94a3b8")
        
        # Línea divisoria
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        # === SECCIÓN FORMULARIO ===
        self.canvas.create_rectangle(50, 90, 850, 280, 
                                     fill="#1e293b", outline="#3b82f6", width=2)
        
        self.canvas.create_text(450, 105, 
                               text="REGISTRAR / EDITAR MERCADO", 
                               font=("Arial", 12, "bold"), 
                               fill="#3b82f6")
        
        # Labels y Entries - Columna 1
        y_base = 135
        spacing = 40
        
        # Nombre del Mercado
        self.canvas.create_text(120, y_base, 
                               text="Nombre:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.entry_nombre = tk.Entry(self.frame_principal, 
                                     font=("Arial", 10), 
                                     bg="#0f172a", fg="white",
                                     insertbackground="white",
                                     width=30)
        self.entry_nombre.place(x=200, y=y_base-10)
        
        # Ciudad
        self.canvas.create_text(120, y_base + spacing, 
                               text="Ciudad:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.entry_ciudad = tk.Entry(self.frame_principal, 
                                      font=("Arial", 10), 
                                      bg="#0f172a", fg="white",
                                      insertbackground="white",
                                      width=30)
        self.entry_ciudad.place(x=200, y=y_base + spacing - 10)
        
        # Departamento
        self.canvas.create_text(120, y_base + spacing*2, 
                               text="Departamento:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.entry_departamento = tk.Entry(self.frame_principal, 
                                           font=("Arial", 10), 
                                           bg="#0f172a", fg="white",
                                           insertbackground="white",
                                           width=30)
        self.entry_departamento.place(x=200, y=y_base + spacing*2 - 10)
        
        # Columna 2
        col2_x = 480
        
        # Barrio
        self.canvas.create_text(col2_x, y_base, 
                               text="Barrio:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.entry_barrio = tk.Entry(self.frame_principal, 
                                     font=("Arial", 10), 
                                     bg="#0f172a", fg="white",
                                     insertbackground="white",
                                     width=30)
        self.entry_barrio.place(x=560, y=y_base-10)
        
        # Avenida
        self.canvas.create_text(col2_x, y_base + spacing, 
                               text="Avenida:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.entry_avenida = tk.Entry(self.frame_principal, 
                                      font=("Arial", 10), 
                                      bg="#0f172a", fg="white",
                                      insertbackground="white",
                                      width=30)
        self.entry_avenida.place(x=560, y=y_base + spacing - 10)
        
        # Dirección completa
        self.canvas.create_text(120, y_base + spacing*3, 
                               text="Dirección:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.entry_direccion = tk.Entry(self.frame_principal, 
                                        font=("Arial", 10), 
                                        bg="#0f172a", fg="white",
                                        insertbackground="white",
                                        width=75)
        self.entry_direccion.place(x=200, y=y_base + spacing*3 - 10)
        
        # Botones de acción
        btn_y = 273
        
        self.btn_agregar = tk.Button(self.frame_principal,
                                     text="✚ Agregar",
                                     font=("Arial", 10, "bold"),
                                     bg="#10b981", fg="white",
                                     activebackground="#059669",
                                     relief=tk.FLAT, cursor="hand2",
                                     padx=15, pady=5,
                                     command=self.agregar_mercado)
        self.btn_agregar.place(x=50, y=btn_y)
        
        self.btn_editar = tk.Button(self.frame_principal,
                                    text="✎ Editar",
                                    font=("Arial", 10, "bold"),
                                    bg="#f59e0b", fg="white",
                                    activebackground="#d97706",
                                    relief=tk.FLAT, cursor="hand2",
                                    padx=15, pady=5,
                                    command=self.editar_mercado)
        self.btn_editar.place(x=170, y=btn_y)
        
        self.btn_eliminar = tk.Button(self.frame_principal,
                                      text="🗑 Eliminar",
                                      font=("Arial", 10, "bold"),
                                      bg="#dc2626", fg="white",
                                      activebackground="#991b1b",
                                      relief=tk.FLAT, cursor="hand2",
                                      padx=15, pady=5,
                                      command=self.eliminar_mercado)
        self.btn_eliminar.place(x=630, y=btn_y)
        
        self.btn_limpiar = tk.Button(self.frame_principal,
                                     text="⟲ Limpiar",
                                     font=("Arial", 10, "bold"),
                                     bg="#6366f1", fg="white",
                                     activebackground="#4f46e5",
                                     relief=tk.FLAT, cursor="hand2",
                                     padx=15, pady=5,
                                     command=self.limpiar_formulario)
        self.btn_limpiar.place(x=750, y=btn_y)
        
        # === SECCIÓN TABLA ===
        self.canvas.create_rectangle(50, 295, 850, 530, 
                                     fill="#1e293b", outline="#3b82f6", width=2)
        
        self.canvas.create_text(450, 310, 
                               text="LISTA DE MERCADOS REGISTRADOS", 
                               font=("Arial", 12, "bold"), 
                               fill="#3b82f6")
        
        # Frame para Treeview
        self.frame_tabla = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_tabla.place(x=70, y=330, width=760, height=180)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(self.frame_tabla,
                                columns=("ID", "Nombre", "Ciudad", "Departamento", 
                                        "Barrio", "Avenida", "Estado"),
                                show="headings",
                                yscrollcommand=scrollbar.set,
                                height=8)
        
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del Mercado")
        self.tree.heading("Ciudad", text="Ciudad")
        self.tree.heading("Departamento", text="Departamento")
        self.tree.heading("Barrio", text="Barrio")
        self.tree.heading("Avenida", text="Avenida")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=180, anchor="w")
        self.tree.column("Ciudad", width=100, anchor="w")
        self.tree.column("Departamento", width=100, anchor="w")
        self.tree.column("Barrio", width=100, anchor="w")
        self.tree.column("Avenida", width=100, anchor="w")
        self.tree.column("Estado", width=80, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_mercado)
        
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
        
        # Botón Volver
        self.btn_volver = tk.Button(self.frame_principal,
                                    text="← Volver al Menú",
                                    font=("Arial", 11, "bold"),
                                    bg="#475569", fg="white",
                                    activebackground="#334155",
                                    relief=tk.FLAT, cursor="hand2",
                                    padx=20, pady=8,
                                    command=self.volver)
        self.btn_volver.place(x=380, y=550)
    
    def cargar_mercados(self):
        """Carga mercados desde la base de datos"""
        self.tree.delete(*self.tree.get_children())
        
        query = """
        SELECT id_mercado, nombre_mercado, ciudad, departamento, 
               barrio, avenida, activo
        FROM mercado
        ORDER BY nombre_mercado;
        """
        
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            for fila in resultados:
                estado = "Activo" if fila[6] else "Inactivo"
                self.tree.insert("", tk.END, values=(
                    fila[0], fila[1], fila[2], fila[3], 
                    fila[4], fila[5], estado
                ))
    
    def agregar_mercado(self):
        """Agrega un nuevo mercado"""
        nombre = self.entry_nombre.get().strip()
        ciudad = self.entry_ciudad.get().strip()
        departamento = self.entry_departamento.get().strip()
        barrio = self.entry_barrio.get().strip()
        avenida = self.entry_avenida.get().strip()
        direccion = self.entry_direccion.get().strip()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre del mercado es obligatorio")
            return
        
        query = """
        INSERT INTO mercado (nombre_mercado, ciudad, departamento, 
                            barrio, avenida, direccion)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        
        if execute_query(query, (nombre, ciudad, departamento, barrio, avenida, direccion)):
            messagebox.showinfo("Éxito", f"Mercado '{nombre}' agregado correctamente")
            self.limpiar_formulario()
            self.cargar_mercados()
        else:
            messagebox.showerror("Error", "No se pudo agregar el mercado")
    
    def seleccionar_mercado(self, event):
        """Llena el formulario con el mercado seleccionado"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']
            
            self.limpiar_formulario()
            self.entry_nombre.insert(0, valores[1])
            self.entry_ciudad.insert(0, valores[2])
            self.entry_departamento.insert(0, valores[3])
            self.entry_barrio.insert(0, valores[4])
            self.entry_avenida.insert(0, valores[5])
            
            # Cargar dirección completa de la BD
            query = "SELECT direccion FROM mercado WHERE id_mercado = %s;"
            resultado = execute_query(query, (valores[0],), fetch=True)
            if resultado and resultado[0][0]:
                self.entry_direccion.insert(0, resultado[0][0])
    
    def editar_mercado(self):
        """Edita el mercado seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un mercado para editar")
            return
        
        item = self.tree.item(seleccion[0])
        id_mercado = item['values'][0]
        
        nombre = self.entry_nombre.get().strip()
        ciudad = self.entry_ciudad.get().strip()
        departamento = self.entry_departamento.get().strip()
        barrio = self.entry_barrio.get().strip()
        avenida = self.entry_avenida.get().strip()
        direccion = self.entry_direccion.get().strip()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre del mercado es obligatorio")
            return
        
        query = """
        UPDATE mercado 
        SET nombre_mercado=%s, ciudad=%s, departamento=%s, 
            barrio=%s, avenida=%s, direccion=%s
        WHERE id_mercado=%s;
        """
        
        if execute_query(query, (nombre, ciudad, departamento, barrio, 
                                avenida, direccion, id_mercado)):
            messagebox.showinfo("Éxito", "Mercado actualizado correctamente")
            self.limpiar_formulario()
            self.cargar_mercados()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el mercado")
    
    def eliminar_mercado(self):
        """Elimina (desactiva) el mercado seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un mercado para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        id_mercado = item['values'][0]
        nombre = item['values'][1]
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de desactivar el mercado '{nombre}'?\n\n"
            "Nota: El mercado se marcará como inactivo pero no se eliminará permanentemente."
        )
        
        if respuesta:
            query = "UPDATE mercado SET activo = FALSE WHERE id_mercado = %s;"
            
            if execute_query(query, (id_mercado,)):
                messagebox.showinfo("Éxito", "Mercado desactivado correctamente")
                self.limpiar_formulario()
                self.cargar_mercados()
            else:
                messagebox.showerror("Error", "No se pudo desactivar el mercado")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_ciudad.delete(0, tk.END)
        self.entry_departamento.delete(0, tk.END)
        self.entry_barrio.delete(0, tk.END)
        self.entry_avenida.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        
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