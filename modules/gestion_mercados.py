import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from database.connection import execute_query


class GestionMercados:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        # Variables
        self.df_mercados = None  # DataFrame para almacenar mercados
        self.mercado_seleccionado = None  # ← AGREGADO: Variable para guardar ID
        
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
        
        # Configuración de campos usando numpy para posiciones
        y_base = 135
        spacing = 40
        
        # Diccionario de configuración de campos
        campos_config = {
            'nombre': ('Nombre:', 120, y_base, 30),
            'ciudad': ('Ciudad:', 120, y_base + spacing, 30),
            'departamento': ('Departamento:', 120, y_base + spacing*2, 30),
            'barrio': ('Barrio:', 480, y_base, 30),
            'avenida': ('Avenida:', 480, y_base + spacing, 30)
        }
        
        # Crear campos dinámicamente
        self.entries = {}
        for key, (label, x, y, width) in campos_config.items():
            self.canvas.create_text(x, y, 
                                   text=label, 
                                   font=("Arial", 10, "bold"), 
                                   fill="#e2e8f0", anchor="w")
            
            entry = tk.Entry(self.frame_principal, 
                           font=("Arial", 10), 
                           bg="#0f172a", fg="white",
                           insertbackground="white",
                           width=width)
            entry.place(x=x + 80 if x == 120 else x + 80, y=y-10)
            self.entries[key] = entry
        
        # Dirección completa (campo especial más largo)
        self.canvas.create_text(120, y_base + spacing*3, 
                               text="Dirección:", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0", anchor="w")
        self.entries['direccion'] = tk.Entry(
            self.frame_principal, 
            font=("Arial", 10), 
            bg="#0f172a", fg="white",
            insertbackground="white",
            width=75
        )
        self.entries['direccion'].place(x=200, y=y_base + spacing*3 - 10)
        
        # Botones de acción del formulario
        btn_config = [
            ('agregar', "✚ Agregar", "#10b981", "#059669", 50, self.agregar_mercado),
            ('editar', "✎ Editar", "#f59e0b", "#d97706", 170, self.editar_mercado),
            ('eliminar', "🗑 Eliminar", "#dc2626", "#991b1b", 630, self.eliminar_mercado),
            ('limpiar', "⟲ Limpiar", "#6366f1", "#4f46e5", 750, self.limpiar_formulario)
        ]
        
        btn_y = 273
        self.buttons = {}
        for attr, text, bg, active_bg, x, cmd in btn_config:
            btn = tk.Button(self.frame_principal,
                          text=text,
                          font=("Arial", 10, "bold"),
                          bg=bg, fg="white",
                          activebackground=active_bg,
                          relief=tk.FLAT, cursor="hand2",
                          padx=15, pady=5,
                          command=cmd)
            btn.place(x=x, y=btn_y)
            self.buttons[attr] = btn
        
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
        
        # Configuración de columnas con numpy
        columnas = ["ID", "Nombre", "Ciudad", "Departamento", "Barrio", "Avenida", "Estado"]
        anchos = np.array([40, 180, 100, 100, 100, 100, 80])
        
        # Treeview
        self.tree = ttk.Treeview(self.frame_tabla,
                                columns=columnas,
                                show="headings",
                                yscrollcommand=scrollbar.set,
                                style="Mercados.Treeview",  # ← Estilo específico
                                height=8)
        
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas con numpy
        for i, col in enumerate(columnas):
            self.tree.heading(col, text=col)
            anchor = "center" if i in [0, 6] else "w"
            self.tree.column(col, width=int(anchos[i]), anchor=anchor)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_mercado)
        
        # Configurar tag para fila seleccionada con color más visible
        self.tree.tag_configure('selected', background='#3b82f6', foreground='white')
        
        # Estilo del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo específico para esta tabla
        style.configure("Mercados.Treeview",
                       background="#0f172a",
                       foreground="white",
                       fieldbackground="#0f172a",
                       borderwidth=0,
                       rowheight=25)
        style.map("Mercados.Treeview",
                 background=[("selected", "#3b82f6")],
                 foreground=[("selected", "white")])
        style.configure("Mercados.Treeview.Heading",
                       background="#1e293b",
                       foreground="white",
                       borderwidth=1,
                       relief="flat")
        
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
        """Carga mercados usando pandas"""
        self.tree.delete(*self.tree.get_children())
        
        query = """
        SELECT id_mercado, nombre_mercado, ciudad, departamento, 
               barrio, avenida, activo
        FROM mercado
        ORDER BY nombre_mercado;
        """
        
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            # Usar pandas DataFrame
            columnas = ['id', 'nombre', 'ciudad', 'depto', 'barrio', 'avenida', 'activo']
            self.df_mercados = pd.DataFrame(resultados, columns=columnas)
            
            # Mapear valores booleanos a texto
            self.df_mercados['estado_texto'] = self.df_mercados['activo'].map({True: 'Activo', False: 'Inactivo'})
            
            # Insertar en tabla
            for row in self.df_mercados.itertuples(index=False):
                self.tree.insert("", tk.END, values=(
                    row.id, row.nombre, row.ciudad, row.depto,
                    row.barrio, row.avenida, row.estado_texto
                ))
    
    def obtener_datos_formulario(self):
        """Obtiene datos del formulario como diccionario"""
        return {key: entry.get().strip() for key, entry in self.entries.items()}
    
    def agregar_mercado(self):
        """Agrega un nuevo mercado"""
        datos = self.obtener_datos_formulario()
        
        if not datos['nombre']:
            messagebox.showwarning("Advertencia", "El nombre del mercado es obligatorio")
            return
        
        query = """
        INSERT INTO mercado (nombre_mercado, ciudad, departamento, 
                            barrio, avenida, direccion)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        
        params = (datos['nombre'], datos['ciudad'], datos['departamento'],
                 datos['barrio'], datos['avenida'], datos['direccion'])
        
        if execute_query(query, params):
            messagebox.showinfo("Éxito", f"Mercado '{datos['nombre']}' agregado correctamente")
            self.limpiar_formulario()
            self.cargar_mercados()
        else:
            messagebox.showerror("Error", "No se pudo agregar el mercado")
    
    def seleccionar_mercado(self, event):
        """Llena el formulario con el mercado seleccionado usando pandas"""
        seleccion = self.tree.selection()
        if seleccion:
            # Quitar tags de filas anteriores
            for item in self.tree.get_children():
                self.tree.item(item, tags=())
            
            item = self.tree.item(seleccion[0])
            valores = item['values']
            
            # ← CORREGIDO: Guardar ID del mercado seleccionado
            self.mercado_seleccionado = valores[0]
            print(f"✓ Mercado seleccionado: ID {self.mercado_seleccionado}")
            
            # Aplicar tag de selección visual
            self.tree.item(seleccion[0], tags=('selected',))
            
            # Buscar en DataFrame si existe
            if self.df_mercados is not None:
                mercado = self.df_mercados[self.df_mercados['id'] == valores[0]].iloc[0]
                
                # Mapear campos
                campos_map = {
                    'nombre': 'nombre',
                    'ciudad': 'ciudad',
                    'departamento': 'depto',
                    'barrio': 'barrio',
                    'avenida': 'avenida'
                }
                
                # Llenar formulario
                self.limpiar_formulario()
                for key, col in campos_map.items():
                    valor = mercado[col]
                    if pd.notna(valor):
                        self.entries[key].insert(0, str(valor))
                
                # Cargar dirección completa
                query = "SELECT direccion FROM mercado WHERE id_mercado = %s;"
                resultado = execute_query(query, (valores[0],), fetch=True)
                if resultado and resultado[0][0]:
                    self.entries['direccion'].insert(0, resultado[0][0])
    
    def editar_mercado(self):
        """Edita el mercado seleccionado"""
        # ← CORREGIDO: Validar que haya un mercado seleccionado
        if self.mercado_seleccionado is None:
            messagebox.showwarning("Advertencia", 
                "Seleccione un mercado de la tabla haciendo clic sobre él")
            return
        
        datos = self.obtener_datos_formulario()
        
        if not datos['nombre']:
            messagebox.showwarning("Advertencia", "El nombre del mercado es obligatorio")
            return
        
        query = """
        UPDATE mercado 
        SET nombre_mercado=%s, ciudad=%s, departamento=%s, 
            barrio=%s, avenida=%s, direccion=%s
        WHERE id_mercado=%s;
        """
        
        params = (datos['nombre'], datos['ciudad'], datos['departamento'],
                 datos['barrio'], datos['avenida'], datos['direccion'], 
                 self.mercado_seleccionado)  # ← Usar variable guardada
        
        if execute_query(query, params):
            messagebox.showinfo("Éxito", "Mercado actualizado correctamente")
            self.limpiar_formulario()
            self.cargar_mercados()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el mercado")
    
    def eliminar_mercado(self):
        """Elimina (desactiva) el mercado seleccionado"""
        # ← CORREGIDO: Validar que haya un mercado seleccionado
        if self.mercado_seleccionado is None:
            messagebox.showwarning("Advertencia", 
                "Seleccione un mercado de la tabla haciendo clic sobre él")
            return
        
        # Obtener nombre del mercado para el mensaje de confirmación
        if self.df_mercados is not None:
            mercado = self.df_mercados[self.df_mercados['id'] == self.mercado_seleccionado]
            if len(mercado) > 0:
                nombre = mercado.iloc[0]['nombre']
            else:
                nombre = "este mercado"
        else:
            nombre = "este mercado"
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de desactivar el mercado '{nombre}'?\n\n"
            "Nota: El mercado se marcará como inactivo pero no se eliminará permanentemente."
        )
        
        if respuesta:
            query = "UPDATE mercado SET activo = FALSE WHERE id_mercado = %s;"
            
            if execute_query(query, (self.mercado_seleccionado,)):
                messagebox.showinfo("Éxito", "Mercado desactivado correctamente")
                self.limpiar_formulario()
                self.cargar_mercados()
            else:
                messagebox.showerror("Error", "No se pudo desactivar el mercado")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        # ← AGREGADO: Limpiar la variable de selección
        self.mercado_seleccionado = None
        
        # Quitar tags visuales de todas las filas
        for item in self.tree.get_children():
            self.tree.item(item, tags=())
        
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