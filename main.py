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
        
        # Variables para mantener las referencias de las imágenes
        self.logo_izquierdo = None
        self.logo_derecho = None
        
        self.inicializar_base_datos()
        # Centrar la ventana en la pantalla
        self.centrar_ventana()
        
        # Crear la interfaz inicial
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
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg="#0a0f1e")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para efectos visuales
        self.canvas = tk.Canvas(self.frame_principal, width=900, height=600, 
                               bg="#0a0f1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Cargar logos
        self.logo_izquierdo = self.cargar_logo("logo_izquierdo.png", 100, 100)
        self.logo_derecho = self.cargar_logo("logo_derecho.png", 100, 100)
        
        # Insertar logo izquierdo con efecto de brillo
        if self.logo_izquierdo:
            self.canvas.create_oval(10, 0, 110, 100, fill="#1e293b", outline="")
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        else:
            self.canvas.create_oval(10, 0, 110, 100, fill="#1e293b", outline="#3b82f6", width=2)
            self.canvas.create_text(60, 50, text="LOGO\nUAB", font=("Arial", 12, "bold"), fill="#64748b")
        
        # Insertar logo derecho con efecto de brillo
        if self.logo_derecho:
            self.canvas.create_oval(790, 0, 890, 100, fill="#1e293b", outline="")
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
        else:
            self.canvas.create_oval(790, 0, 890, 100, fill="#1e293b", outline="#3b82f6", width=2)
            self.canvas.create_text(840, 50, text="LOGO\nSIS", font=("Arial", 12, "bold"), fill="#64748b")
        
        # Elementos decorativos de fondo mejorados
        self.crear_elementos_decorativos()
        
        # Header con mejor espaciado
        self.canvas.create_text(450, 105, 
                               text="UNIVERSIDAD AUTÓNOMA DEL BENI", 
                               font=("Arial", 15, "bold"), 
                               fill="#64748b")
        
        self.canvas.create_text(450, 130, 
                               text='"JOSÉ BALLIVIÁN"', 
                               font=("Arial", 13), 
                               fill="#94a3b8")
        
        # Línea decorativa sutil
        self.canvas.create_line(250, 150, 650, 150, fill="#334155", width=1)
        
        # Título principal con gradiente visual simulado
        self.canvas.create_text(450, 190, 
                               text="Sistema de Análisis y", 
                               font=("Arial", 30, "bold"), 
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 230, 
                               text="Predicción de Precios del Mercado", 
                               font=("Arial", 30, "bold"), 
                               fill="#3b82f6")
        
        # Subtítulo mejorado
        self.canvas.create_text(450, 275, 
                               text="Herramienta integral para el análisis de datos históricos", 
                               font=("Arial", 13), 
                               fill="#94a3b8")
        
        self.canvas.create_text(450, 297, 
                               text="y proyección inteligente de precios en el mercado boliviano", 
                               font=("Arial", 13), 
                               fill="#94a3b8")
        
        # Iconos informativos con tarjetas mejoradas
        info_y = 360
        # Tarjeta 1
        self.canvas.create_rectangle(120, info_y-30, 280, info_y+35, 
                                     fill="#1e293b", outline="#10b981", width=2)
        self.canvas.create_text(200, info_y-10, 
                               text="📈", 
                               font=("Arial", 24), 
                               fill="#10b981")
        self.canvas.create_text(200, info_y+15, 
                               text="Análisis Estadístico", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0")
        
        # Tarjeta 2
        self.canvas.create_rectangle(370, info_y-30, 530, info_y+35, 
                                     fill="#1e293b", outline="#8b5cf6", width=2)
        self.canvas.create_text(450, info_y-10, 
                               text="🗄️", 
                               font=("Arial", 24), 
                               fill="#8b5cf6")
        self.canvas.create_text(450, info_y+15, 
                               text="Base de Datos PostgreSQL", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0")
        
        # Tarjeta 3
        self.canvas.create_rectangle(620, info_y-30, 780, info_y+35, 
                                     fill="#1e293b", outline="#f59e0b", width=2)
        self.canvas.create_text(700, info_y-10, 
                               text="🔮", 
                               font=("Arial", 24), 
                               fill="#f59e0b")
        self.canvas.create_text(700, info_y+15, 
                               text="Predicción Inteligente", 
                               font=("Arial", 10, "bold"), 
                               fill="#e2e8f0")
        
        # Botón de inicio mejorado
        self.btn_inicio = tk.Button(
            self.frame_principal,
            text="🚀  INICIAR SISTEMA",
            font=("Arial", 15, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=50,
            pady=18,
            borderwidth=0,
            command=self.iniciar_sistema
        )
        self.btn_inicio.place(x=450, y=450, anchor="center")
        
        # Efecto hover para el botón
        self.btn_inicio.bind("<Enter>", self.hover_enter)
        self.btn_inicio.bind("<Leave>", self.hover_leave)
        
        # Sección de equipo rediseñada
        self.canvas.create_text(450, 500, 
                               text="EQUIPO DE DESARROLLO", 
                               font=("Arial", 10, "bold"), 
                               fill="#64748b")
        
        # Fondo elegante para nombres
        self.canvas.create_rectangle(50, 518, 850, 575, 
                                     fill="#1a1f2e", outline="#334155", width=1)
        
        # Grid de nombres más organizado (3 columnas)
        col1_x, col2_x, col3_x = 180, 450, 720
        row1_y, row2_y = 535, 560
        
        nombres = [
            "Jhon Ever García Quispe",
            "Uriel David Ribera Choque",
            "Aldo Andrés Arandia Vásquez",
            "José Raul Melgar Guagama",
            "Yaimara Jissel Gil Inchu"
        ]
        
        self.canvas.create_text(col1_x, row1_y, text=f"• {nombres[0]}", 
                               font=("Arial", 9), fill="#e2e8f0", anchor="center")
        self.canvas.create_text(col2_x, row1_y, text=f"• {nombres[1]}", 
                               font=("Arial", 9), fill="#e2e8f0", anchor="center")
        self.canvas.create_text(col3_x, row1_y, text=f"• {nombres[2]}", 
                               font=("Arial", 9), fill="#e2e8f0", anchor="center")
        self.canvas.create_text(col1_x, row2_y, text=f"• {nombres[3]}", 
                               font=("Arial", 9), fill="#e2e8f0", anchor="center")
        self.canvas.create_text(col2_x, row2_y, text=f"• {nombres[4]}", 
                               font=("Arial", 9), fill="#e2e8f0", anchor="center")
        
        # Copyright
        self.canvas.create_text(450, 590, 
                               text="© 2025 - Ingeniería de Sistemas UAB | v1.0 Beta", 
                               font=("Arial", 8), 
                               fill="#475569")
    
    def crear_elementos_decorativos(self):
        # Círculos decorativos más sutiles
        self.canvas.create_oval(-30, 120, 180, 330, 
                               outline="#1e3a8a", width=1, dash=(8, 4))
        self.canvas.create_oval(720, 420, 930, 630, 
                               outline="#1e3a8a", width=1, dash=(8, 4))
        
        # Líneas decorativas más elegantes
        self.canvas.create_line(100, 165, 800, 165, 
                               fill="#1e40af", width=1, dash=(10, 5))
        self.canvas.create_line(100, 318, 800, 318, 
                               fill="#1e40af", width=1, dash=(10, 5))
        
        # Puntos decorativos pequeños
        for x in range(150, 750, 100):
            self.canvas.create_oval(x-2, 163, x+2, 167, fill="#3b82f6", outline="")
            self.canvas.create_oval(x-2, 316, x+2, 320, fill="#3b82f6", outline="")
    
    def hover_enter(self, event):
        self.btn_inicio.config(bg="#2563eb", padx=55, pady=20)
    
    def hover_leave(self, event):
        self.btn_inicio.config(bg="#3b82f6", padx=50, pady=18)
    
    def iniciar_sistema(self):
        self.btn_inicio.place_forget()
        self.mostrar_pantalla_carga()
    
    def mostrar_pantalla_carga(self):
        self.canvas.delete("all")
        
        # Recrear logos
        if self.logo_izquierdo:
            self.canvas.create_oval(10, 0, 110, 100, fill="#1e293b", outline="")
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_oval(790, 0, 890, 100, fill="#1e293b", outline="")
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
        
        # Título de carga
        self.canvas.create_text(450, 200, 
                               text="Inicializando Sistema", 
                               font=("Arial", 26, "bold"), 
                               fill="#e2e8f0",
                               tags="carga_texto")
        
        # Subtítulo
        self.canvas.create_text(450, 235, 
                               text="Preparando módulos y conexiones", 
                               font=("Arial", 12), 
                               fill="#94a3b8")
        
        # Barra de progreso mejorada (fondo)
        self.canvas.create_rectangle(200, 280, 700, 315, 
                                     fill="#1e293b", outline="#334155", width=2,
                                     tags="barra_fondo")
        
        # Barra de progreso (progreso) con gradiente simulado
        self.barra_progreso = self.canvas.create_rectangle(200, 280, 200, 315, 
                                                           fill="#3b82f6", outline="",
                                                           tags="barra_progreso")
        
        # Texto de porcentaje
        self.texto_porcentaje = self.canvas.create_text(450, 350, 
                                                         text="0%", 
                                                         font=("Arial", 16, "bold"), 
                                                         fill="#e2e8f0",
                                                         tags="porcentaje")
        
        # Texto de estado con ícono
        self.texto_estado = self.canvas.create_text(450, 390, 
                                                     text="⚙️ Conectando a base de datos...", 
                                                     font=("Arial", 11), 
                                                     fill="#94a3b8",
                                                     tags="estado")
        
        # Indicador de carga (puntos animados)
        self.puntos_carga = self.canvas.create_text(450, 430, 
                                                     text="●", 
                                                     font=("Arial", 18), 
                                                     fill="#3b82f6",
                                                     tags="puntos")
        
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
        self.animar_carga()
    
    def animar_carga(self):
        if self.progreso <= 100:
            nuevo_ancho = 200 + (500 * self.progreso / 100)
            self.canvas.coords(self.barra_progreso, 200, 280, nuevo_ancho, 315)
            
            self.canvas.itemconfig(self.texto_porcentaje, text=f"{self.progreso}%")
            
            if self.progreso % 17 == 0 and self.estado_actual < len(self.estados_carga):
                self.canvas.itemconfig(self.texto_estado, text=self.estados_carga[self.estado_actual])
                self.estado_actual += 1
            
            puntos = ["●", "●●", "●●●"][int(self.progreso / 7) % 3]
            self.canvas.itemconfig(self.puntos_carga, text=puntos)
            
            self.progreso += 2
            self.root.after(50, self.animar_carga)
        else:
            self.root.after(500, self.mostrar_menu_principal)
    
    def mostrar_menu_principal(self):
        self.canvas.delete("all")
        
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        # Recrear logos
        if self.logo_izquierdo:
            self.canvas.create_oval(10, 0, 110, 100, fill="#1e293b", outline="")
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_oval(790, 0, 890, 100, fill="#1e293b", outline="")
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
        
        # Crear tarjetas mejoradas (2x2)
        self.crear_tarjeta_modulo(270, 240, "📊", "Gestión de Datos", 
                                 "Productos, Precios y Mercados", "#10b981", self.modulo_gestion)
        
        self.crear_tarjeta_modulo(630, 240, "📈", "Análisis Estadístico", 
                                 "Tendencias y Volatilidad", "#8b5cf6", self.modulo_analisis)
        
        self.crear_tarjeta_modulo(270, 400, "🔮", "Predicciones", 
                                 "Proyección de Precios", "#f59e0b", self.modulo_prediccion)
        
        self.crear_tarjeta_modulo(630, 400, "🔍", "Consultas y Reportes", 
                                 "Búsqueda y Exportación", "#06b6d4", self.modulo_consultas)
        
        # Botones footer mejorados
        self.crear_boton_footer(370, 520, "⚙️ Configuración", "#475569", self.modulo_config)
        self.crear_boton_footer(530, 520, "🚪 Salir", "#dc2626", self.salir_sistema)
        
        # Footer
        self.canvas.create_text(450, 565, 
                               text="Sistema Integrado de Análisis de Mercados", 
                               font=("Arial", 9), 
                               fill="#64748b")
        self.canvas.create_text(450, 585, 
                               text="v1.0 Beta - © 2025 Ingeniería de Sistemas UAB", 
                               font=("Arial", 8), 
                               fill="#475569")
    
    def crear_tarjeta_modulo(self, x, y, icono, titulo, descripcion, color, comando):
        
        # Sombra de tarjeta
        self.canvas.create_rectangle(x-128, y-38, x+132, y+102, 
                                     fill="#0a0f1e", outline="",
                                     tags=f"tarjeta_{x}_{y}")
        
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
        
        #  EVENTOS DEL CANVAS (no más botones invisibles)
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
        """Efecto hover al entrar"""
        self.canvas.itemconfig(tarjeta_id, fill="#334155", width=3)
    
    def hover_tarjeta_leave(self, tarjeta_id):
        """Efecto hover al salir"""
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
            self.canvas.create_oval(10, 0, 110, 100, fill="#1e293b", outline="")
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_oval(790, 0, 890, 100, fill="#1e293b", outline="")
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
        
        # Tarjetas de opciones (también corregidas)
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
        """Abre el módulo de gestión de productos"""
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        GestionProductos(
            self.canvas, 
            self.frame_principal, 
            self.mostrar_submenu_gestion
        )

    def abrir_gestion_mercados(self):
        """Abre el módulo de gestión de mercados"""
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        GestionMercados(
            self.canvas, 
            self.frame_principal, 
            self.mostrar_submenu_gestion
        )
    
    def abrir_gestion_precios(self):
        """Abre el módulo de gestión de precios"""
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        GestionPrecios(
            self.canvas, 
            self.frame_principal, 
            self.mostrar_submenu_gestion
        )
    
    def abrir_gestion_categorias(self):
        """Abre el módulo de gestión de categorías"""
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
    
    def modulo_config(self):
        self.mostrar_mensaje_desarrollo("Configuración", "#475569")
    
    def salir_sistema(self):
        self.root.quit()
    
    def mostrar_mensaje_desarrollo(self, modulo, color):
        # Crear rectángulo de fondo
        rect = self.canvas.create_rectangle(250, 130, 650, 180, 
                                           fill="#1e293b", outline=color, width=2,
                                           tags="temp_msg")
        # Texto
        msg = self.canvas.create_text(450, 155, 
                                      text=f"✨ Módulo '{modulo}' en desarrollo", 
                                      font=("Arial", 13, "bold"), 
                                      fill=color,
                                      tags="temp_msg")
        self.root.after(2500, lambda: self.canvas.delete("temp_msg"))


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaMercado(root)
    root.mainloop()
    DatabaseConnection.close_all_connections()