import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import time
from database.connection import DatabaseConnection  
from modules.gestion import GestionProductos
from modules.gestion_mercados import GestionMercados
from modules.gestion_precios import GestionPrecios
from tkinter import messagebox
from modules.analisis_estadistico import AnalisisEstadistico
from modules.gestion_consultas import GestionConsultas
from modules.gestion_predicciones import GestionPredicciones

class SistemaMercado:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Análisis y Predicción de Precios del Mercado")
        self.root.geometry("900x600")
        self.root.configure(bg="#0a0f1e")
        self.root.resizable(False, False)
        
        
        self.logo_izquierdo = None
        self.logo_derecho = None
        
        self.inicializar_base_datos()
        
        self.centrar_ventana()
        
       
        self.crear_interfaz_inicial()
    
    def inicializar_base_datos(self):
        if not DatabaseConnection.test_connection():
            messagebox.showerror(
                "Error de Conexión",
                "No se pudo conectar a la base de datos PostgreSQL.\n\n"
                "Verifique:\n"
                "1. PostgreSQL está corriendo\n"
                "2. La base de datos 'mercado_db' existe\n"
                "3. Usuario y contraseña en connection.py son correctos"
            )
            self.root.quit()
    
    def centrar_ventana(self):
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def cargar_logo(self, ruta_imagen, ancho=80, alto=80):
        """Carga y redimensiona una imagen"""
        try:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(imagen)
        except Exception as e:
            print(f"Error al cargar imagen {ruta_imagen}: {e}")
            return None
    
    def crear_interfaz_inicial(self):
       
        self.frame_principal = tk.Frame(self.root, bg="#0a0f1e")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)
        
        
        self.canvas = tk.Canvas(self.frame_principal, width=900, height=600, 
                               bg="#0a0f1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
       
        self.logo_izquierdo = self.cargar_logo("logo_izquierdo.png", 100, 100)
        self.logo_derecho = self.cargar_logo("logo_derecho.png", 100, 100)
        
       
        if self.logo_izquierdo:
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        
        if self.logo_derecho:
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
        
        self.canvas.create_text(450, 100, 
                               text="UNIVERSIDAD AUTÓNOMA DEL BENI", 
                               font=("Arial", 13), 
                               fill="#64748b")
        
        self.canvas.create_text(450, 120, 
                               text='"José Ballivián"', 
                               font=("Arial", 11), 
                               fill="#94a3b8")
        
        self.canvas.create_text(450, 185, 
                               text="Sistema de Análisis y", 
                               font=("Arial", 28), 
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 220, 
                               text="Predicción de Precios del Mercado", 
                               font=("Arial", 28, "bold"), 
                               fill="#e2e8f0")
        
        info_y = 350
        
        self.canvas.create_rectangle(145, info_y-25, 275, info_y+30, 
                                     fill="#0f1419", outline="#10b981", width=1,
                                     tags="card1")
        self.canvas.create_text(210, info_y-8, 
                               text="📈", 
                               font=("Arial", 20))
        self.canvas.create_text(210, info_y+13, 
                               text="Análisis Estadístico", 
                               font=("Arial", 9, "bold"), 
                               fill="#e2e8f0")
        
        
        self.canvas.create_rectangle(320, info_y-25, 580, info_y+30, 
                                     fill="#0f1419", outline="#8b5cf6", width=1,
                                     tags="card2")
        self.canvas.create_text(450, info_y-8, 
                               text="🗄️", 
                               font=("Arial", 20))
        self.canvas.create_text(450, info_y+13, 
                               text="Base de Datos PostgreSQL", 
                               font=("Arial", 9, "bold"), 
                               fill="#e2e8f0")
        
       
        self.canvas.create_rectangle(625, info_y-25, 755, info_y+30, 
                                     fill="#0f1419", outline="#f59e0b", width=1,
                                     tags="card3")
        self.canvas.create_text(690, info_y-8, 
                               text="🔮", 
                               font=("Arial", 20))
        self.canvas.create_text(690, info_y+13, 
                               text="Predicción Inteligente", 
                               font=("Arial", 9, "bold"), 
                               fill="#e2e8f0")
        
        
        self.canvas.tag_bind("card1", "<Enter>", lambda e: self.hover_card(145, info_y-25, 275, info_y+30, "#10b981"))
        self.canvas.tag_bind("card1", "<Leave>", lambda e: self.leave_card(145, info_y-25, 275, info_y+30, "#10b981"))
        
        self.canvas.tag_bind("card2", "<Enter>", lambda e: self.hover_card(320, info_y-25, 580, info_y+30, "#8b5cf6"))
        self.canvas.tag_bind("card2", "<Leave>", lambda e: self.leave_card(320, info_y-25, 580, info_y+30, "#8b5cf6"))
        
        self.canvas.tag_bind("card3", "<Enter>", lambda e: self.hover_card(625, info_y-25, 755, info_y+30, "#f59e0b"))
        self.canvas.tag_bind("card3", "<Leave>", lambda e: self.leave_card(625, info_y-25, 755, info_y+30, "#f59e0b"))
        
       
        self.btn_inicio = tk.Button(
            self.frame_principal,
            text="Iniciar Sistema",
            font=("Arial", 14, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=45,
            pady=15,
            borderwidth=0,
            command=self.iniciar_sistema
        )
        self.btn_inicio.place(x=450, y=430, anchor="center")
        
        
        self.btn_inicio.bind("<Enter>", self.hover_enter)
        self.btn_inicio.bind("<Leave>", self.hover_leave)
        
        self.canvas.create_text(450, 490, 
                               text="INTEGRANTES", 
                               font=("Arial", 9, "bold"), 
                               fill="white")
        
        nombres_linea1 = "Jhon Ever García Quispe  •  Uriel David Ribera Choque  •  Aldo Andrés Arandia Vásquez"
        nombres_linea2 = "José Raul Melgar Guagama  •  Yaimara Jissel Gil Inchu"
        
        self.canvas.create_text(450, 515, text=nombres_linea1, 
                               font=("Arial", 8), fill="white", anchor="center")
        self.canvas.create_text(450, 535, text=nombres_linea2, 
                               font=("Arial", 8), fill="white", anchor="center")
        
        self.animar_entrada()
    
    def hover_card(self, x1, y1, x2, y2, color):
        """Efecto hover suave en las tarjetas"""
        items = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in items:
            if self.canvas.type(item) == "rectangle":
                self.canvas.itemconfig(item, fill="#1e293b", width=2)
    
    def leave_card(self, x1, y1, x2, y2, color):
        """Revertir efecto hover"""
        items = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in items:
            if self.canvas.type(item) == "rectangle":
                self.canvas.itemconfig(item, fill="#0f1419", width=1)
    
    def animar_entrada(self):
        """Animación sutil de aparición"""
        pass  
    
    def hover_enter(self, event):
        self.btn_inicio.config(bg="#2563eb", padx=50, pady=17)
    
    def hover_leave(self, event):
        self.btn_inicio.config(bg="#3b82f6", padx=45, pady=15)
    
    def iniciar_sistema(self):
        self.btn_inicio.place_forget()
        self.mostrar_pantalla_carga()
    
    def mostrar_pantalla_carga(self):
        self.canvas.delete("all")
    
       
        if self.logo_izquierdo:
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
    
        self.particulas = []
        import random
        for i in range(15): 
            x = random.randint(100, 800)
            y = random.randint(150, 550)
            size = random.randint(2, 5)
            particula = self.canvas.create_oval(
                x, y, x+size, y+size,
                fill="#10b981", outline="",
                tags="particula"
            )
            self.particulas.append({
                'id': particula,
                'x': x,
                'y': y,
                'velocidad': random.uniform(0.3, 0.8),
                'direccion': random.choice([-1, 1])
            })
    
        self.canvas.create_text(450, 200, 
                            text="Inicializando Sistema", 
                            font=("Arial", 26, "bold"), 
                            fill="#e2e8f0",
                            tags="carga_texto")
    
        self.canvas.create_text(450, 235, 
                            text="Preparando módulos y conexiones", 
                            font=("Arial", 12), 
                            fill="#94a3b8")
    
        self.canvas.create_rectangle(202, 282, 702, 317, 
                                    fill="#0a0f1e", outline="",
                                    tags="barra_sombra")
    
        self.canvas.create_rectangle(200, 280, 700, 315, 
                                    fill="#1e293b", outline="#334155", width=2,
                                    tags="barra_fondo")
    
        self.canvas.create_rectangle(202, 282, 698, 290, 
                                    fill="#2d3748", outline="",
                                    tags="barra_brillo_interno")
    
        self.barra_progreso = self.canvas.create_rectangle(200, 280, 200, 315, 
                                                        fill="#10b981", outline="",
                                                        tags="barra_progreso")
    
        self.barra_brillo = self.canvas.create_rectangle(200, 280, 200, 290,
                                                        fill="#34d399", outline="",
                                                        tags="barra_brillo")
    
        self.barra_borde = self.canvas.create_rectangle(200, 280, 200, 315,
                                                        outline="#059669", width=2,
                                                        tags="barra_borde")
    
        self.texto_porcentaje = self.canvas.create_text(450, 350, 
                                                        text="0%", 
                                                        font=("Arial", 16, "bold"), 
                                                        fill="#10b981",  # Verde
                                                        tags="porcentaje")
    
        self.texto_estado = self.canvas.create_text(450, 390, 
                                                    text="⚙️ Conectando a base de datos...", 
                                                    font=("Arial", 11), 
                                                    fill="#94a3b8",
                                                    tags="estado")
    
        self.puntos_carga = self.canvas.create_text(450, 430, 
                                                    text="●", 
                                                    font=("Arial", 18), 
                                                    fill="#10b981",  # Verde
                                                    tags="puntos")
    
        self.anillo_pulso = self.canvas.create_oval(440, 420, 460, 440,
                                                    outline="#10b981", width=2,
                                                    tags="anillo_pulso")
    
        self.canvas.create_line(150, 300, 190, 300, fill="#10b981", width=2, tags="linea_izq")
        self.canvas.create_line(710, 300, 750, 300, fill="#10b981", width=2, tags="linea_der")
    
        self.progreso = 0
        self.estados_carga = [
            "⚙️ Conectando a base de datos...",
            "📊 Cargando módulos estadísticos...",
            "🔮 Inicializando algoritmos de predicción...",
            "🗂️ Cargando estructuras de datos...",
            "🎨 Preparando interfaz gráfica...",
            "✅ Finalizando configuración..."
        ]
        self.estado_actual = 0
        self.pulso_dir = 1  
        self.pulso_scale = 1.0
    
        self.animar_carga()
        self.animar_particulas()
        self.animar_pulso()

    def animar_carga(self):
        if self.progreso <= 100:
            nuevo_ancho = 200 + (500 * self.progreso / 100)
        
            
            self.canvas.coords(self.barra_progreso, 200, 280, nuevo_ancho, 315)
        
            brillo_ancho = max(200, nuevo_ancho - 10)
            self.canvas.coords(self.barra_brillo, 200, 280, brillo_ancho, 290)
        
            self.canvas.coords(self.barra_borde, 200, 280, nuevo_ancho, 315)
        
            self.canvas.itemconfig(self.texto_porcentaje, text=f"{self.progreso}%")
        
            if self.progreso < 33:
                self.canvas.itemconfig(self.texto_porcentaje, fill="#10b981")  # Verde
            elif self.progreso < 66:
                self.canvas.itemconfig(self.texto_porcentaje, fill="#34d399")  # Verde claro
            else:
                self.canvas.itemconfig(self.texto_porcentaje, fill="#059669")  # Verde oscuro
        
            if self.progreso % 17 == 0 and self.estado_actual < len(self.estados_carga):
                self.canvas.itemconfig(self.texto_estado, text=self.estados_carga[self.estado_actual])
                self.estado_actual += 1
        
            
            puntos = ["●", "●●", "●●●"][int(self.progreso / 7) % 3]
            self.canvas.itemconfig(self.puntos_carga, text=puntos)
        
           
            if self.progreso % 10 == 0:
                
                self.canvas.coords("linea_izq", 150, 300, 190 - (self.progreso % 20), 300)
                
                self.canvas.coords("linea_der", 710 + (self.progreso % 20), 300, 750, 300)
        
            self.progreso += 2
            self.root.after(50, self.animar_carga)
        else:
            
            self.canvas.itemconfig(self.barra_progreso, fill="#059669")
            self.canvas.itemconfig(self.texto_porcentaje, text="100%", fill="#059669")
            self.root.after(500, self.mostrar_menu_principal)
    def animar_particulas(self):
        """Anima las partículas de fondo sutilmente"""
        if self.progreso <= 100:
            import random
            for p in self.particulas:
                
                p['y'] += p['velocidad'] * p['direccion']
                
                
                if p['y'] < 150:
                    p['y'] = 550
                    p['x'] = random.randint(100, 800)
                elif p['y'] > 550:
                    p['y'] = 150
                    p['x'] = random.randint(100, 800)
                
                
                coords = self.canvas.coords(p['id'])
                if coords:
                    size = coords[2] - coords[0]
                    self.canvas.coords(p['id'], p['x'], p['y'], p['x']+size, p['y']+size)
                
               
                if random.random() > 0.95:
                    colores = ["#10b981", "#34d399", "#059669", "#064e3b"]
                    self.canvas.itemconfig(p['id'], fill=random.choice(colores))
            
            self.root.after(50, self.animar_particulas)

    def animar_pulso(self):
        """Anima el anillo pulsante alrededor de los puntos"""
        if self.progreso <= 100:
            # Escalar el anillo
            self.pulso_scale += 0.05 * self.pulso_dir
            
            if self.pulso_scale >= 1.3:
                self.pulso_dir = -1
            elif self.pulso_scale <= 1.0:
                self.pulso_dir = 1
            
            # Calcular nuevo tamaño
            base_size = 20
            nuevo_size = base_size * self.pulso_scale
            offset = nuevo_size / 2
            
            self.canvas.coords(self.anillo_pulso,
                            450 - offset, 430 - offset,
                            450 + offset, 430 + offset)
            
            # Cambiar opacidad (simulado con width)
            nuevo_width = max(1, int(3 - (self.pulso_scale - 1) * 3))
            self.canvas.itemconfig(self.anillo_pulso, width=nuevo_width)
            
            self.root.after(50, self.animar_pulso)
    def mostrar_menu_principal(self):
        self.canvas.delete("all")
        
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        # Recrear logos
        if self.logo_izquierdo:
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
        
        # Header
        self.canvas.create_text(450, 40, 
                               text="Sistema de Análisis y Predicción de Precios", 
                               font=("Arial", 17, "bold"), 
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 65, 
                               text="Mercado Boliviano", 
                               font=("Arial", 12), 
                               fill="#94a3b8")
        
        # Línea divisoria elegante
        self.canvas.create_line(80, 90, 820, 90, fill="#334155", width=2)
        
        # Título del menú
        self.canvas.create_text(450, 125, 
                               text="MENÚ PRINCIPAL", 
                               font=("Arial", 22, "bold"), 
                               fill="#3b82f6")
        
        # Crear tarjetas mejoradas (2x2) - más arriba
        self.crear_tarjeta_modulo(270, 220, "📊", "Gestión de Datos", 
                                 "Productos, Precios y Mercados", "#10b981", self.modulo_gestion)
        
        self.crear_tarjeta_modulo(630, 220, "📈", "Análisis Estadístico", 
                                 "Tendencias y Volatilidad", "#8b5cf6", self.modulo_analisis)
        
        self.crear_tarjeta_modulo(270, 360, "🔮", "Predicciones", 
                                 "Proyección de Precios", "#f59e0b", self.modulo_prediccion)
        
        self.crear_tarjeta_modulo(630, 360, "🔍", "Consultas y Reportes", 
                                 "Búsqueda y Exportación", "#06b6d4", self.modulo_consultas)
        
        # Botón Salir centrado
        self.crear_boton_footer(450, 490, "🚪 Salir", "#dc2626", self.salir_sistema)
        
       
    
    def crear_tarjeta_modulo(self, x, y, icono, titulo, descripcion, color, comando):
        
        # Fondo de tarjeta (guardamos ID para hover)
        tarjeta_id = self.canvas.create_rectangle(x-130, y-40, x+130, y+100, 
                                                  fill="#1e293b", outline=color, width=2,
                                                  tags=f"tarjeta_{x}_{y}")
        
        # Icono con fondo circular
        self.canvas.create_oval(x-25, y-25, x+25, y+25, 
                               fill="#0a0f1e", outline=color, width=2,
                               tags=f"tarjeta_{x}_{y}")
        self.canvas.create_text(x, y, 
                               text=icono, 
                               font=("Arial", 32), 
                               fill=color,
                               tags=f"tarjeta_{x}_{y}")
        
        # Título
        self.canvas.create_text(x, y+50, 
                               text=titulo, 
                               font=("Arial", 12, "bold"), 
                               fill="#e2e8f0",
                               tags=f"tarjeta_{x}_{y}")
        
        # Descripción
        self.canvas.create_text(x, y+73, 
                               text=descripcion, 
                               font=("Arial", 9), 
                               fill="#94a3b8",
                               tags=f"tarjeta_{x}_{y}")
        
        # EVENTOS DEL CANVAS (no más botones invisibles)
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Button-1>", lambda e: comando())
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Enter>", 
            lambda e: self.hover_tarjeta_enter(tarjeta_id, color))
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Leave>", 
            lambda e: self.hover_tarjeta_leave(tarjeta_id))
        
        # Cambiar cursor
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Enter>", 
            lambda e: self.canvas.config(cursor="hand2"), add="+")
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Leave>", 
            lambda e: self.canvas.config(cursor=""), add="+")
    
    def hover_tarjeta_enter(self, tarjeta_id, color):
        self.canvas.itemconfig(tarjeta_id, fill="#334155", width=3)
    
    def hover_tarjeta_leave(self, tarjeta_id):
        self.canvas.itemconfig(tarjeta_id, fill="#1e293b", width=2)
    
    def crear_boton_footer(self, x, y, texto, color, comando):
        btn = tk.Button(self.frame_principal,
                       text=texto,
                       font=("Arial", 10, "bold"),
                       bg=color,
                       fg="white",
                       activebackground=color,
                       relief=tk.FLAT,
                       cursor="hand2",
                       borderwidth=0,
                       padx=25,
                       pady=10,
                       command=comando)
        btn.place(x=x, y=y, anchor="center")
        
        def on_enter(e):
            btn.config(bg="#1e293b" if "Configuración" in texto else "#991b1b")
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def modulo_gestion(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        # Mostrar menú de opciones de gestión
        self.mostrar_submenu_gestion()

    def mostrar_submenu_gestion(self):
        self.canvas.delete("all")
        
        # Recrear logos
        if self.logo_izquierdo:
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
        
        # Título
        self.canvas.create_text(450, 100, 
                               text="📊 GESTIÓN DE DATOS", 
                               font=("Arial", 22, "bold"), 
                               fill="#10b981")
        
        self.canvas.create_text(450, 130, 
                               text="Seleccione qué desea gestionar", 
                               font=("Arial", 12), 
                               fill="#94a3b8")
        
        # Tarjetas de opciones
        self.crear_tarjeta_modulo(270, 250, "🛒", "Productos", 
                                 "Catálogo de productos", "#10b981", 
                                 self.abrir_gestion_productos)
        
        self.crear_tarjeta_modulo(630, 250, "🏪", "Mercados", 
                                 "Mercados de Bolivia", "#8b5cf6", 
                                 self.abrir_gestion_mercados)
        
        self.crear_tarjeta_modulo(270, 410, "💰", "Precios", 
                                 "Ofertas y precios", "#f59e0b", 
                                 self.abrir_gestion_precios)
        
        self.crear_tarjeta_modulo(630, 410, "📋", "Categorías", 
                                 "Categorías de productos", "#06b6d4", 
                                 self.abrir_gestion_categorias)
        
        # Botón volver
        self.btn_volver = tk.Button(self.frame_principal,
                                   text="← Volver al Menú Principal",
                                   font=("Arial", 11, "bold"),
                                   bg="#475569", fg="white",
                                   activebackground="#334155",
                                   relief=tk.FLAT, cursor="hand2",
                                   padx=20, pady=8,
                                   command=self.mostrar_menu_principal)
        self.btn_volver.place(x=350, y=530)

    def abrir_gestion_productos(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        GestionProductos(
            self.canvas, 
            self.frame_principal, 
            self.mostrar_submenu_gestion
        )

    def abrir_gestion_mercados(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        GestionMercados(
            self.canvas, 
            self.frame_principal, 
            self.mostrar_submenu_gestion
        )
    
    def abrir_gestion_precios(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        GestionPrecios(
            self.canvas, 
            self.frame_principal, 
            self.mostrar_submenu_gestion
        )
    
    def abrir_gestion_categorias(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        from modules.gestion_categorias import GestionCategorias
        GestionCategorias(
            self.canvas, 
            self.frame_principal, 
            self.mostrar_submenu_gestion
        )
    
    def modulo_analisis(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        AnalisisEstadistico(
            self.canvas,
            self.frame_principal,
            self.mostrar_menu_principal
        )
    
    def modulo_prediccion(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
    
        
        GestionPredicciones(
            self.canvas,
            self.frame_principal,
            self.mostrar_menu_principal
    )
    
    def modulo_consultas(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        GestionConsultas(
            self.canvas,
            self.frame_principal,
            self.mostrar_menu_principal
        )
    
    def salir_sistema(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaMercado(root)
    root.mainloop()
    DatabaseConnection.close_all_connections()