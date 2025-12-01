import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import execute_query
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class GestionPrecios:
    def __init__(self, canvas, frame_principal, volver_menu):
        self.canvas = canvas
        self.frame_principal = frame_principal
        self.volver_menu = volver_menu
        
        self.df_productos = None
        self.df_mercados = None
        self.df_ofertas = None
        
        self.canvas.delete("all")
        self.cargar_datos_base()
        self.crear_interfaz()
        self.cargar_ofertas()
        
    
    def cargar_datos_base(self):
        query_productos = """
        SELECT id_producto, nombre_producto, unidad_medida 
        FROM producto WHERE activo = TRUE ORDER BY nombre_producto;
        """
        productos = execute_query(query_productos, fetch=True)
        
        if productos:
            self.df_productos = pd.DataFrame(productos, columns=['id', 'nombre', 'unidad'])
            self.df_productos['display'] = self.df_productos.apply(
                lambda x: f"{x['nombre']} ({x['unidad']})", axis=1
            )
        
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
        
        print(f"✓ Cargados {len(self.df_productos) if self.df_productos is not None else 0} productos")
        print(f"✓ Cargados {len(self.df_mercados) if self.df_mercados is not None else 0} mercados")
    
    def crear_interfaz(self):
        self.canvas.create_text(450, 30, text="💰 GESTIÓN DE PRECIOS", 
                               font=("Arial", 20, "bold"), fill="#e2e8f0")
        
        self.canvas.create_text(450, 55, text="Registro de ofertas de productos en mercados", 
                               font=("Arial", 11), fill="#94a3b8")
        
        self.canvas.create_line(80, 75, 820, 75, fill="#334155", width=2)
        
        self.canvas.create_rectangle(50, 90, 850, 300, fill="#1e293b", outline="#3b82f6", width=2)
        
        self.canvas.create_text(450, 105, text="REGISTRAR / ACTUALIZAR OFERTA", 
                               font=("Arial", 12, "bold"), fill="#3b82f6")
        
        if self.df_productos is None or len(self.df_productos) == 0:
            self.canvas.create_text(450, 180, text="⚠️  No hay productos registrados", 
                                   font=("Arial", 12, "bold"), fill="#f59e0b")
            self.canvas.create_text(450, 210, 
                                   text="Por favor, registre productos primero en el módulo de Gestión", 
                                   font=("Arial", 10), fill="#94a3b8")
            self.crear_boton_volver()
            return
        
        if self.df_mercados is None or len(self.df_mercados) == 0:
            self.canvas.create_text(450, 180, text="⚠️  No hay mercados registrados", 
                                   font=("Arial", 12, "bold"), fill="#f59e0b")
            self.canvas.create_text(450, 210, 
                                   text="Por favor, registre mercados primero en el módulo de Gestión", 
                                   font=("Arial", 10), fill="#94a3b8")
            self.crear_boton_volver()
            return
        
        config_campos = {
            'producto': (120, 140, "Producto:", 35),
            'mercado': (120, 180, "Mercado:", 35),
            'precio': (120, 220, "Precio (Bs):", 15),
            'stock': (500, 220, "Stock:", 15)
        }
        
        for key, (x, y, label, width) in config_campos.items():
            self.canvas.create_text(x, y, text=label, font=("Arial", 10, "bold"), 
                                   fill="#e2e8f0", anchor="w")
        
        self.combo_producto = ttk.Combobox(self.frame_principal,
            values=self.df_productos['display'].tolist(),
            state="readonly", font=("Arial", 10), width=35)
        self.combo_producto.place(x=220, y=130)
        
        self.combo_mercado = ttk.Combobox(self.frame_principal,
            values=self.df_mercados['display'].tolist(),
            state="readonly", font=("Arial", 10), width=35)
        self.combo_mercado.place(x=220, y=170)
        
        self.entry_precio = tk.Entry(self.frame_principal, font=("Arial", 10), 
                                     bg="#0f172a", fg="white", insertbackground="white", width=15)
        self.entry_precio.place(x=220, y=210)
        
        self.canvas.create_text(360, 220, text="(ejemplo: 5.50)", 
                               font=("Arial", 9, "italic"), fill="#64748b", anchor="w")
        
        self.entry_stock = tk.Entry(self.frame_principal, font=("Arial", 10), 
                                    bg="#0f172a", fg="white", insertbackground="white", width=15)
        self.entry_stock.place(x=570, y=210)
        
        self.canvas.create_text(720, 220, text="(unidades disponibles)", 
                               font=("Arial", 9, "italic"), fill="#64748b", anchor="w")
        
        info_y = 260
        self.canvas.create_rectangle(130, info_y, 770, info_y + 45,
                                     fill="#0f172a", outline="#475569", width=1)
        
        self.canvas.create_text(450, info_y + 12, text="ℹ️  Información:",
                               font=("Arial", 9, "bold"), fill="#3b82f6")
        
        self.canvas.create_text(450, info_y + 30,
                               text="• Si la oferta ya existe (mismo producto y mercado), se ACTUALIZARÁ el precio y stock",
                               font=("Arial", 8), fill="#94a3b8")
        
        btn_config = [
            ('guardar', "💾 Guardar", "#10b981", "#059669", 50, 250, self.guardar_oferta),
            ('limpiar', "🔄 Limpiar", "#6366f1", "#4f46e5", 170, 250, self.limpiar_formulario),
            ('eliminar', "🗑️ Eliminar", "#dc2626", "#991b1b", 630, 250, self.eliminar_oferta),
            ('ver_todas', "⟲ Ver Todas", "#475569", "#334155", 750, 250, self.cargar_ofertas)
        ]
        
        self.buttons = {}
        for key, text, bg, active_bg, x, y, cmd in btn_config:
            btn = tk.Button(self.frame_principal, text=text, font=("Arial", 10, "bold"),
                          bg=bg, fg="white", activebackground=active_bg,
                          relief=tk.FLAT, cursor="hand2", padx=15, pady=6, command=cmd)
            btn.place(x=x, y=y)
            self.buttons[key] = btn
        
        self.canvas.create_rectangle(50, 315, 850, 530, fill="#1e293b", outline="#3b82f6", width=2)
        
        self.canvas.create_text(130, 330, text="OFERTAS REGISTRADAS", 
                               font=("Arial", 12, "bold"), fill="#3b82f6", anchor="w")
        
        filtros_config = [
            ('filtro_producto', "📦 Producto", "#06b6d4", "#0891b2", 440, 323, self.filtrar_por_producto),
            ('filtro_mercado', "🏪 Mercado", "#06b6d4", "#0891b2", 550, 323, self.filtrar_por_mercado),
            ('historial', "📜 Historial", "#8b5cf6", "#7c3aed", 660, 323, self.ver_historial)
        ]
        
        self.canvas.create_text(410, 330, text="Filtrar:", font=("Arial", 9, "bold"), fill="#94a3b8")
        
        for key, text, bg, active_bg, x, y, cmd in filtros_config:
            btn = tk.Button(self.frame_principal, text=text, font=("Arial", 9, "bold"),
                          bg=bg, fg="white", activebackground=active_bg,
                          relief=tk.FLAT, cursor="hand2", padx=12, pady=4, command=cmd)
            btn.place(x=x, y=y)
            self.buttons[key] = btn
        
        self.frame_tabla = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_tabla.place(x=70, y=350, width=760, height=160)
        
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ["ID", "Producto", "Mercado", "Precio", "Stock", "Fecha"]
        anchos = np.array([40, 200, 180, 80, 70, 150])
        
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings",
                                yscrollcommand=scrollbar.set, height=7)
        
        scrollbar.config(command=self.tree.yview)
        
        for i, col in enumerate(columnas):
            self.tree.heading(col, text=col)
            anchor = "center" if i in [0, 4] else "e" if i == 3 else "w"
            self.tree.column(col, width=int(anchos[i]), anchor=anchor)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_oferta)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0f172a", foreground="white",
                       fieldbackground="#0f172a", borderwidth=0)
        style.map("Treeview", background=[("selected", "#3b82f6")])
        style.configure("Treeview.Heading", background="#1e293b",
                       foreground="white", borderwidth=1)
        
        self.canvas.create_text(450, 518, 
                               text="Estadísticas: Seleccione una oferta para ver detalles", 
                               font=("Arial", 9, "italic"), fill="#64748b", tags="stats_text")
        
        self.crear_boton_volver()
    
    def crear_boton_volver(self):
        self.btn_volver = tk.Button(self.frame_principal, text="← Volver al Menú",
                                    font=("Arial", 11, "bold"), bg="#475569", fg="white",
                                    activebackground="#334155", relief=tk.FLAT, cursor="hand2",
                                    padx=20, pady=8, command=self.volver)
        self.btn_volver.place(x=380, y=550)
    
    def cargar_ofertas(self):
        if not hasattr(self, 'tree'):
            return
        
        self.tree.delete(*self.tree.get_children())
        
        query = """
        SELECT o.id_oferta, p.nombre_producto, p.unidad_medida, m.nombre_mercado,
               o.precio, o.stock, o.fecha_actualizacion
        FROM oferta o
        INNER JOIN producto p ON o.id_producto = p.id_producto
        INNER JOIN mercado m ON o.id_mercado = m.id_mercado
        ORDER BY o.fecha_actualizacion DESC;
        """
        
        resultados = execute_query(query, fetch=True)
        
        if resultados:
            df_ofertas = pd.DataFrame(resultados, 
                                     columns=['id', 'producto', 'unidad', 'mercado', 
                                             'precio', 'stock', 'fecha'])
            
            df_ofertas['producto_display'] = df_ofertas['producto'] + ' (' + df_ofertas['unidad'] + ')'
            df_ofertas['precio_display'] = df_ofertas['precio'].apply(lambda x: f"{x:.2f}")
            df_ofertas['stock_display'] = df_ofertas['stock'].fillna("N/A")
            df_ofertas['fecha_display'] = df_ofertas['fecha'].apply(
                lambda x: x.strftime("%d/%m/%Y %H:%M") if pd.notna(x) else ""
            )
            
            for _, row in df_ofertas.iterrows():
                self.tree.insert("", tk.END, values=(
                    row['id'], row['producto_display'], row['mercado'],
                    row['precio_display'], row['stock_display'], row['fecha_display']
                ))
            
            self.df_ofertas = df_ofertas
        
        if hasattr(self, 'canvas'):
            self.canvas.itemconfig("stats_text", 
                text="Estadísticas: Seleccione una oferta para ver detalles", fill="#64748b")
    
    def guardar_oferta(self):
        if not self.combo_producto.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        if not self.combo_mercado.get():
            messagebox.showwarning("Advertencia", "Seleccione un mercado")
            return
        
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
        
        id_producto = self.get_id_from_display(self.combo_producto.get(), self.df_productos)
        id_mercado = self.get_id_from_display(self.combo_mercado.get(), self.df_mercados)
        
        check_query = "SELECT id_oferta, precio FROM oferta WHERE id_producto = %s AND id_mercado = %s;"
        resultado = execute_query(check_query, (id_producto, id_mercado), fetch=True)
        
        if resultado:
            id_oferta = resultado[0][0]
            precio_anterior = resultado[0][1]
            
            if precio != precio_anterior:
                historial_query = """
                INSERT INTO historial_p (id_producto, stock, fuente, observaciones)
                VALUES (%s, %s, %s, %s);
                """
                observacion = f"Precio actualizado de {precio_anterior:.2f} a {precio:.2f} Bs en {self.combo_mercado.get()}"
                execute_query(historial_query, (id_producto, stock, "Manual - Sistema", observacion))
            
            update_query = """
            UPDATE oferta SET precio = %s, stock = %s, fecha_actualizacion = CURRENT_TIMESTAMP
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
            insert_query = "INSERT INTO oferta (id_producto, id_mercado, precio, stock) VALUES (%s, %s, %s, %s);"
            
            if execute_query(insert_query, (id_producto, id_mercado, precio, stock)):
                messagebox.showinfo("Éxito", "Oferta registrada correctamente")
                self.limpiar_formulario()
                self.cargar_ofertas()
            else:
                messagebox.showerror("Error", "No se pudo registrar la oferta")
    
    def get_id_from_display(self, display_value, df):
        if df is None:
            return None
        match = df[df['display'] == display_value]
        return int(match.iloc[0]['id']) if len(match) > 0 else None
    def seleccionar_oferta(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            self.canvas.itemconfig("stats_text", 
                text="Estadísticas: Seleccione una oferta para ver detalles", fill="#64748b")
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        producto_str = valores[1]
        mercado_str = valores[2]
        precio = str(valores[3])
        stock = str(valores[4]) if valores[4] != "N/A" else ""
        
        self.combo_producto.set(producto_str)
        self.combo_mercado.set(mercado_str)
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, precio)
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, stock)
        
        id_producto = self.get_id_from_display(self.combo_producto.get(), self.df_productos)
        
        query_stats = """
        SELECT MIN(precio) as precio_min, MAX(precio) as precio_max,
               AVG(precio) as precio_prom, COUNT(*) as num_mercados
        FROM oferta WHERE id_producto = %s;
        """
        
        stats = execute_query(query_stats, (id_producto,), fetch=True)
        
        if stats and stats[0][0] is not None:
            df_stats = pd.DataFrame([stats[0]], columns=['min', 'max', 'prom', 'num'])
            precio_min = df_stats.iloc[0]['min']
            precio_max = df_stats.iloc[0]['max']
            precio_prom = df_stats.iloc[0]['prom']
            num_mercados = df_stats.iloc[0]['num']
            precio_actual = float(precio)
            
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
                text="📊 Este es el único registro de este producto", fill="#64748b")
    
    def eliminar_oferta(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una oferta para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        id_oferta = item['values'][0]
        producto = item['values'][1]
        mercado = item['values'][2]
        
        respuesta = messagebox.askyesno("Confirmar",
            f"¿Está seguro de eliminar esta oferta?\n\n"
            f"Producto: {producto}\n"
            f"Mercado: {mercado}")
        
        if respuesta:
            query = "DELETE FROM oferta WHERE id_oferta = %s;"
            
            if execute_query(query, (id_oferta,)):
                check_query = "SELECT COUNT(*) FROM oferta;"
                resultado = execute_query(check_query, fetch=True)
                
                if resultado and resultado[0][0] == 0:
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
        self.combo_producto.set("")
        self.combo_mercado.set("")
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        self.canvas.itemconfig("stats_text", 
            text="Estadísticas: Seleccione una oferta para ver detalles", fill="#64748b")
    
    def filtrar_por_producto(self):
        if self.df_productos is None or len(self.df_productos) == 0:
            return
        
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Filtrar por Producto")
        ventana.geometry("450x200")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        ventana.grab_set()
        
        tk.Label(ventana, text="Seleccione el producto:", font=("Arial", 11, "bold"),
                bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        combo = ttk.Combobox(ventana, values=self.df_productos['display'].tolist(),
                            state="readonly", font=("Arial", 10), width=35)
        combo.pack(pady=10)
        
        def aplicar_filtro():
            if not combo.get():
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            id_producto = self.get_id_from_display(combo.get(), self.df_productos)
            self.tree.delete(*self.tree.get_children())
            
            query = """
            SELECT o.id_oferta, p.nombre_producto, p.unidad_medida, m.nombre_mercado,
                   o.precio, o.stock, o.fecha_actualizacion
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE o.id_producto = %s ORDER BY o.precio ASC;
            """
            
            resultados = execute_query(query, (id_producto,), fetch=True)
            
            if resultados:
                df_filtrado = pd.DataFrame(resultados, 
                                          columns=['id', 'producto', 'unidad', 'mercado', 
                                                  'precio', 'stock', 'fecha'])
                
                df_filtrado['producto_display'] = df_filtrado['producto'] + ' (' + df_filtrado['unidad'] + ')'
                df_filtrado['precio_display'] = df_filtrado['precio'].apply(lambda x: f"{x:.2f}")
                df_filtrado['stock_display'] = df_filtrado['stock'].fillna("N/A")
                df_filtrado['fecha_display'] = df_filtrado['fecha'].apply(
                    lambda x: x.strftime("%d/%m/%Y %H:%M") if pd.notna(x) else ""
                )
                
                for _, row in df_filtrado.iterrows():
                    self.tree.insert("", tk.END, values=(
                        row['id'], row['producto_display'], row['mercado'],
                        row['precio_display'], row['stock_display'], row['fecha_display']
                    ))
                
                precios = df_filtrado['precio'].values
                precio_min = np.min(precios)
                precio_max = np.max(precios)
                precio_prom = np.mean(precios)
                
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
        
        tk.Button(ventana, text="✓ Aplicar Filtro", font=("Arial", 10, "bold"),
                 bg="#10b981", fg="white", command=aplicar_filtro,
                 padx=20, pady=8).pack(pady=10)
        
        tk.Button(ventana, text="✕ Cancelar", font=("Arial", 9),
                 bg="#475569", fg="white", command=ventana.destroy,
                 padx=15, pady=5).pack()
    
    def filtrar_por_mercado(self):
        if self.df_mercados is None or len(self.df_mercados) == 0:
            return
        
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title("Filtrar por Mercado")
        ventana.geometry("450x200")
        ventana.configure(bg="#0a0f1e")
        ventana.transient(self.frame_principal)
        ventana.grab_set()
        
        tk.Label(ventana, text="Seleccione el mercado:", font=("Arial", 11, "bold"),
                bg="#0a0f1e", fg="#e2e8f0").pack(pady=15)
        
        combo = ttk.Combobox(ventana, values=self.df_mercados['display'].tolist(),
                            state="readonly", font=("Arial", 10), width=35)
        combo.pack(pady=10)
        
        def aplicar_filtro():
            if not combo.get():
                messagebox.showwarning("Advertencia", "Seleccione un mercado")
                return
            
            id_mercado = self.get_id_from_display(combo.get(), self.df_mercados)
            self.tree.delete(*self.tree.get_children())
            
            query = """
            SELECT o.id_oferta, p.nombre_producto, p.unidad_medida, m.nombre_mercado,
                   o.precio, o.stock, o.fecha_actualizacion
            FROM oferta o
            INNER JOIN producto p ON o.id_producto = p.id_producto
            INNER JOIN mercado m ON o.id_mercado = m.id_mercado
            WHERE o.id_mercado = %s ORDER BY p.nombre_producto ASC;
            """
            
            resultados = execute_query(query, (id_mercado,), fetch=True)
            
            if resultados:
                df_filtrado = pd.DataFrame(resultados, 
                                          columns=['id', 'producto', 'unidad', 'mercado', 
                                                  'precio', 'stock', 'fecha'])
                
                df_filtrado['producto_display'] = df_filtrado['producto'] + ' (' + df_filtrado['unidad'] + ')'
                df_filtrado['precio_display'] = df_filtrado['precio'].apply(lambda x: f"{x:.2f}")
                df_filtrado['stock_display'] = df_filtrado['stock'].fillna("N/A")
                df_filtrado['fecha_display'] = df_filtrado['fecha'].apply(
                    lambda x: x.strftime("%d/%m/%Y %H:%M") if pd.notna(x) else ""
                )
                
                for _, row in df_filtrado.iterrows():
                    self.tree.insert("", tk.END, values=(
                        row['id'], row['producto_display'], row['mercado'],
                        row['precio_display'], row['stock_display'], row['fecha_display']
                    ))
                
                precio_prom = np.mean(df_filtrado['precio'].values)
                
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
        
        tk.Button(ventana, text="✓ Aplicar Filtro", font=("Arial", 10, "bold"),
                 bg="#10b981", fg="white", command=aplicar_filtro,
                 padx=20, pady=8).pack(pady=10)
        
        tk.Button(ventana, text="✕ Cancelar", font=("Arial", 9),
                 bg="#475569", fg="white", command=ventana.destroy,
                 padx=15, pady=5).pack()
    
    def ver_historial(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Información", 
                "Seleccione una oferta para ver su historial de cambios")
            return
        
        item = self.tree.item(seleccion[0])
        id_oferta = item['values'][0]
        producto = item['values'][1]
        
        query_id = "SELECT id_producto FROM oferta WHERE id_oferta = %s;"
        result = execute_query(query_id, (id_oferta,), fetch=True)
        if not result:
            return
        
        id_producto = result[0][0]
        
        query_historial = """
        SELECT fecha_registro, stock, fuente, observaciones
        FROM historial_p WHERE id_producto = %s
        ORDER BY fecha_registro DESC LIMIT 10;
        """
        
        historial = execute_query(query_historial, (id_producto,), fetch=True)
        
        if not historial:
            messagebox.showinfo("Historial", 
                f"No hay historial de cambios para:\n{producto}")
            return
        
        ventana = tk.Toplevel(self.frame_principal)
        ventana.title(f"Historial - {producto}")
        ventana.geometry("700x400")
        ventana.configure(bg="#0a0f1e")
        
        tk.Label(ventana, text=f"📜 Historial de Cambios", font=("Arial", 14, "bold"),
                bg="#0a0f1e", fg="#e2e8f0").pack(pady=10)
        
        tk.Label(ventana, text=producto, font=("Arial", 11),
                bg="#0a0f1e", fg="#94a3b8").pack()
        
        frame = tk.Frame(ventana, bg="#1e293b")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_hist = ttk.Treeview(frame,
                                columns=("Fecha", "Stock", "Fuente", "Observaciones"),
                                show="headings", yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree_hist.yview)
        
        columnas_config = [
            ("Fecha", 150, "Fecha/Hora"),
            ("Stock", 80, "Stock"),
            ("Fuente", 120, "Fuente"),
            ("Observaciones", 300, "Observaciones")
        ]
        
        for col, width, text in columnas_config:
            tree_hist.heading(col, text=text)
            tree_hist.column(col, width=width)
        
        tree_hist.pack(fill=tk.BOTH, expand=True)
        
        df_hist = pd.DataFrame(historial, columns=['fecha', 'stock', 'fuente', 'obs'])
        df_hist['fecha_display'] = df_hist['fecha'].apply(
            lambda x: x.strftime("%d/%m/%Y %H:%M:%S") if pd.notna(x) else ""
        )
        df_hist['stock_display'] = df_hist['stock'].fillna("N/A")
        df_hist['fuente_display'] = df_hist['fuente'].fillna("N/A")
        df_hist['obs_display'] = df_hist['obs'].fillna("")
        
        for _, row in df_hist.iterrows():
            tree_hist.insert("", tk.END, values=(
                row['fecha_display'], row['stock_display'],
                row['fuente_display'], row['obs_display']
            ))
        
        tk.Button(ventana, text="Cerrar", font=("Arial", 10, "bold"),
                 bg="#475569", fg="white", command=ventana.destroy,
                 padx=20, pady=5).pack(pady=10)
    
    def volver(self):
        self.limpiar_formulario()
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.volver_menu()