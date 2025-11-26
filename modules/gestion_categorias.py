import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query
import pandas as pd
import numpy as np

class GestionCategorias:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        self.categoria_seleccionada = None
        self.modo_edicion = False
        self.df_categorias = None
        
        self.canvas.delete("all")
        self.crear_interfaz()
        self.cargar_categorias()
    
    def crear_interfaz(self):
        self.canvas.create_text(450, 30, text="📋 GESTIÓN DE CATEGORÍAS",
                               font=("Arial", 20, "bold"), fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, text="Clasificación de productos del mercado",
                               font=("Arial", 11), fill="#94a3b8")
        
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        self.canvas.create_rectangle(50, 90, 420, 380, fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(235, 105, text="FORMULARIO DE CATEGORÍA",
                               font=("Arial", 12, "bold"), fill="#06b6d4")
        
        campos_config = {
            'nombre': (90, 145, "Nombre:", 30),
            'descripcion': (90, 215, "Descripción:", (33, 5))
        }
        
        self.canvas.create_text(campos_config['nombre'][0], campos_config['nombre'][1],
                               text=campos_config['nombre'][2], font=("Arial", 10, "bold"),
                               fill="#e2e8f0", anchor="w")
        
        self.entry_nombre = tk.Entry(self.frame_principal, font=("Arial", 11),
                                     bg="#0f172a", fg="white", insertbackground="white",
                                     width=campos_config['nombre'][3])
        self.entry_nombre.place(x=90, y=160)
        
        self.canvas.create_text(campos_config['descripcion'][0], campos_config['descripcion'][1],
                               text=campos_config['descripcion'][2], font=("Arial", 10, "bold"),
                               fill="#e2e8f0", anchor="w")
        
        self.text_descripcion = tk.Text(self.frame_principal, font=("Arial", 10),
                                        bg="#0f172a", fg="white", insertbackground="white",
                                        width=campos_config['descripcion'][3][0],
                                        height=campos_config['descripcion'][3][1],
                                        wrap=tk.WORD)
        self.text_descripcion.place(x=90, y=230)
        
        btn_config = np.array([
            ['agregar', '✚ Agregar', '#10b981', '#059669', 100, 340],
            ['limpiar', '🔄 Limpiar', '#6366f1', '#4f46e5', 230, 340]
        ], dtype=object)
        
        self.buttons = {}
        for key, text, bg, active_bg, x, y in btn_config:
            cmd = self.agregar_categoria if key == 'agregar' else self.limpiar_formulario
            btn = tk.Button(self.frame_principal, text=text, font=("Arial", 10, "bold"),
                          bg=bg, fg="white", activebackground=active_bg,
                          relief=tk.FLAT, cursor="hand2", padx=18, pady=6, command=cmd)
            btn.place(x=int(x), y=int(y))
            self.buttons[key] = btn
        
        self.canvas.create_rectangle(440, 90, 850, 380, fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(645, 105, text="CATEGORÍAS REGISTRADAS",
                               font=("Arial", 12, "bold"), fill="#06b6d4")
        
        self.frame_tabla = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_tabla.place(x=460, y=130, width=370, height=190)
        
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["ID", "Nombre", "Productos"]
        anchos = np.array([40, 220, 80])
        
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings",
                                yscrollcommand=scrollbar.set, height=8)
        scrollbar.config(command=self.tree.yview)
        
        anchors = ["center", "w", "center"]
        for i, (col, ancho, anchor) in enumerate(zip(columnas, anchos, anchors)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=int(ancho), anchor=anchor)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_categoria)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0f172a", foreground="white",
                       fieldbackground="#0f172a", borderwidth=0)
        style.map("Treeview", background=[("selected", "#06b6d4")])
        style.configure("Treeview.Heading", background="#1e293b",
                       foreground="white", borderwidth=1)
        
        btn_tabla_config = np.array([
            ['editar', '✎ Editar', '#f59e0b', '#d97706', 510, 340],
            ['eliminar', '🗑 Eliminar', '#dc2626', '#991b1b', 620, 340],
            ['refrescar', '↻ Refrescar', '#8b5cf6', '#7c3aed', 730, 340]
        ], dtype=object)
        
        for key, text, bg, active_bg, x, y in btn_tabla_config:
            if key == 'editar':
                cmd = self.editar_categoria
            elif key == 'eliminar':
                cmd = self.eliminar_categoria
            else:
                cmd = self.cargar_categorias
            
            btn = tk.Button(self.frame_principal, text=text, font=("Arial", 9, "bold"),
                          bg=bg, fg="white", activebackground=active_bg,
                          relief=tk.FLAT, cursor="hand2", padx=15, pady=5, command=cmd)
            btn.place(x=int(x), y=int(y))
            self.buttons[key] = btn
        
        self.canvas.create_rectangle(50, 400, 850, 550, fill="#1e293b", outline="#06b6d4", width=2)
        
        self.canvas.create_text(450, 415, text="📊 DISTRIBUCIÓN DE PRODUCTOS POR CATEGORÍA",
                               font=("Arial", 11, "bold"), fill="#06b6d4")
        
        self.stats_frame = tk.Frame(self.frame_principal, bg="#1e293b")
        self.stats_frame.place(x=70, y=427, width=760, height=104)
        
        self.btn_volver = tk.Button(self.frame_principal, text="← Volver al Menú",
                                    font=("Arial", 11, "bold"), bg="#475569", fg="white",
                                    activebackground="#334155", relief=tk.FLAT, cursor="hand2",
                                    padx=20, pady=8, command=self.volver)
        self.btn_volver.place(x=380, y=559)
    
    def cargar_categorias(self):
        print("🔄 Cargando categorías...")
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree.update_idletasks()
        
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
                self.df_categorias = pd.DataFrame(resultados, 
                                                 columns=['id', 'nombre', 'num_productos'])
                
                for _, row in self.df_categorias.iterrows():
                    item_id = self.tree.insert("", tk.END, values=(
                        int(row['id']),
                        row['nombre'],
                        int(row['num_productos'])
                    ))
                    print(f"  - Insertado: ID={row['id']}, Nombre={row['nombre']}, Productos={row['num_productos']}")
            
                self.tree.update()
                print(f"✓ Total de items en el Treeview: {len(self.tree.get_children())}")
            else:
                print("⚠️ No se encontraron categorías activas")
                self.df_categorias = None
    
        except Exception as e:
            print(f"❌ Error al cargar categorías: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudieron cargar las categorías:\n{str(e)}")
        
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
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
        
        print(f"📊 Estadísticas obtenidas: {stats}")
        
        if not stats or all(s[1] == 0 for s in stats):
            tk.Label(self.stats_frame, text="📦 No hay productos asignados a categorías",
                    font=("Arial", 11), bg="#1e293b", fg="#94a3b8").pack(pady=20)
            return
        
        tk.Label(self.stats_frame, text="Top 5 Categorías:",
                font=("Arial", 9, "bold"), bg="#1e293b", fg="#e2e8f0").pack(anchor="w", padx=10, pady=(0, 3))
        
        frame_barras = tk.Frame(self.stats_frame, bg="#1e293b")
        frame_barras.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)
        
        df_stats = pd.DataFrame(stats, columns=['nombre', 'cantidad'])
        df_stats = df_stats[df_stats['cantidad'] > 0]
        
        if len(df_stats) == 0:
            tk.Label(frame_barras, text="📦 No hay productos asignados a categorías",
                    font=("Arial", 10), bg="#1e293b", fg="#94a3b8").pack(pady=15)
            return
        
        max_productos = df_stats['cantidad'].max()
        colores = np.array(["#10b981", "#06b6d4", "#8b5cf6", "#f59e0b", "#ec4899"])
        
        print(f"  📊 Creando {len(df_stats)} barras")
        
        altura_por_barra = 12
        
        for idx, row in df_stats.iterrows():
            nombre = row['nombre']
            cantidad = int(row['cantidad'])
            
            print(f"  Creando barra {idx+1}/{len(df_stats)}: {nombre} = {cantidad} productos")
            
            fila = tk.Frame(frame_barras, bg="#1e293b", height=altura_por_barra)
            fila.pack(fill=tk.X, pady=1.5)
            fila.pack_propagate(False)
            
            nombre_display = nombre[:12] + "..." if len(nombre) > 12 else nombre
            
            lbl_nombre = tk.Label(fila, text=f"{nombre_display}:", font=("Arial", 8),
                                 bg="#1e293b", fg="#e2e8f0", width=13, anchor="w")
            lbl_nombre.pack(side=tk.LEFT)
            
            ancho_max_barra = 620
            ancho_barra = int((cantidad / max_productos) * ancho_max_barra)
            ancho_barra = max(ancho_barra, 15)
            
            color = colores[idx % len(colores)]
            
            canvas_barra = tk.Canvas(fila, width=ancho_max_barra, height=9,
                                    bg="#0f172a", highlightthickness=0)
            canvas_barra.pack(side=tk.LEFT, padx=3)
            
            canvas_barra.create_rectangle(0, 0, ancho_barra, 9, fill=color, outline="")
            
            lbl_cantidad = tk.Label(fila, text=f"{cantidad}", font=("Arial", 9, "bold"),
                                   bg="#1e293b", fg=color, width=2, anchor="e")
            lbl_cantidad.pack(side=tk.LEFT, padx=3)
        
        print(f"✓ Total de barras creadas: {len(df_stats)}")
    
    def agregar_categoria(self):
        nombre = self.entry_nombre.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()

        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre de la categoría es obligatorio")
            return

        print(f"📝 Intentando {'actualizar' if self.modo_edicion else 'agregar'}: '{nombre}'")

        try:
            if self.modo_edicion and self.categoria_seleccionada:
                query = """
                UPDATE categorias
                SET nombre = %s, descripcion = %s
                WHERE id_categoria = %s
                RETURNING id_categoria;
                """
        
                resultado = execute_query(query, (nombre, descripcion, 
                                                 int(self.categoria_seleccionada)), fetch=True)
        
                if resultado:
                    print(f"✓ Categoría actualizada: ID {resultado[0][0]}")
                    messagebox.showinfo("Éxito", "Categoría actualizada correctamente")
                    self.limpiar_formulario()
                    self.frame_principal.after(100, self.cargar_categorias)
                else:
                    print("❌ No se pudo actualizar")
                    messagebox.showerror("Error", "No se pudo actualizar la categoría")
    
            else:
                query = """
                INSERT INTO categorias (nombre, descripcion, activo)
                VALUES (%s, %s, TRUE)
                RETURNING id_categoria;
                """
        
                resultado = execute_query(query, (nombre, descripcion), fetch=True)
        
                if resultado:
                    nuevo_id = resultado[0][0]
                    print(f"✓ Categoría agregada: ID {nuevo_id}")
                
                    messagebox.showinfo("Éxito", 
                        f"✓ Categoría '{nombre}' agregada correctamente\n"
                        f"ID asignado: {nuevo_id}")
                
                    self.limpiar_formulario()
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
        seleccion = self.tree.selection()
        if not seleccion:
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        self.categoria_seleccionada = int(valores[0])
        
        query = "SELECT nombre, descripcion FROM categorias WHERE id_categoria = %s;"
        resultado = execute_query(query, (self.categoria_seleccionada,), fetch=True)
        
        if resultado:
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, resultado[0][0])
            
            self.text_descripcion.delete("1.0", tk.END)
            if resultado[0][1]:
                self.text_descripcion.insert("1.0", resultado[0][1])
    
    def editar_categoria(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una categoría de la tabla")
            return
        
        self.modo_edicion = True
        self.buttons['agregar'].config(text="✓ Actualizar", bg="#f59e0b")
    
    def eliminar_categoria(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una categoría de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        valores_array = np.array(item['values'])
        id_categoria = int(valores_array[0])
        nombre = valores_array[1]
        num_productos = int(valores_array[2])
        
        if num_productos > 0:
            messagebox.showwarning("No se puede eliminar",
                f"La categoría '{nombre}' tiene {num_productos} producto(s) asociado(s).\n\n"
                "Debe reasignar o eliminar esos productos primero.")
            return
        
        respuesta = messagebox.askyesno("Confirmar",
            f"¿Está seguro de eliminar la categoría '{nombre}'?")
        
        if respuesta:
            query = "UPDATE categorias SET activo = FALSE WHERE id_categoria = %s;"
            
            if execute_query(query, (id_categoria,)):
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
                self.limpiar_formulario()
                self.cargar_categorias()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría")
    
    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.text_descripcion.delete("1.0", tk.END)
        
        self.categoria_seleccionada = None
        self.modo_edicion = False
        self.buttons['agregar'].config(text="✚ Agregar", bg="#10b981")
        
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def volver(self):
        self.limpiar_formulario()
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()