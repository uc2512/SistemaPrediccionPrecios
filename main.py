import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import time
from tkinter import messagebox
from database.connection import DatabaseConnection  
from modules.gestion import GestionProductos
from modules.gestion_categorias import GestionCategorias
from modules.gestion_mercados import GestionMercados
from modules.gestion_precios import GestionPrecios
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
                                     fill="#0f1419", outline="#10b981", width=1)
        self.canvas.create_text(210, info_y-8, 
                               text="📈", 
                               font=("Arial", 20))
        self.canvas.create_text(210, info_y+13, 
                               text="Análisis Estadístico", 
                               font=("Arial", 9, "bold"), 
                               fill="#e2e8f0")
        
        
        self.canvas.create_rectangle(320, info_y-25, 580, info_y+30, 
                                     fill="#0f1419", outline="#8b5cf6", width=1)
        self.canvas.create_text(450, info_y-8, 
                               text="🗄️", 
                               font=("Arial", 20))
        self.canvas.create_text(450, info_y+13, 
                               text="Base de Datos PostgreSQL", 
                               font=("Arial", 9, "bold"), 
                               fill="#e2e8f0")
        
       
        self.canvas.create_rectangle(625, info_y-25, 755, info_y+30, 
                                     fill="#0f1419", outline="#f59e0b", width=1)
        self.canvas.create_text(690, info_y-8, 
                               text="🔮", 
                               font=("Arial", 20))
        self.canvas.create_text(690, info_y+13, 
                               text="Predicción Inteligente", 
                               font=("Arial", 9, "bold"), 
                               fill="#e2e8f0")
        
       
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
    
    def iniciar_sistema(self):
        self.btn_inicio.place_forget()
        self.mostrar_menu_principal()
    
    def mostrar_menu_principal(self):
        self.canvas.delete("all")
        
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        if self.logo_izquierdo:
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
        
        self.canvas.create_text(450, 40, 
                               text="Sistema de Análisis y Predicción de Precios", 
                               font=("Arial", 17, "bold"), 
                               fill="#e2e8f0")
        
        self.canvas.create_text(450, 65, 
                               text="Mercado Boliviano", 
                               font=("Arial", 12), 
                               fill="#94a3b8")
        
        
        self.canvas.create_line(80, 90, 820, 90, fill="#334155", width=2)
        
        
        self.canvas.create_text(450, 125, 
                               text="MENÚ PRINCIPAL", 
                               font=("Arial", 22, "bold"), 
                               fill="#3b82f6")
        
        self.crear_tarjeta_modulo(270, 220, "📊", "Gestión de Datos", 
                                 "Productos, Precios y Mercados", "#10b981", self.modulo_gestion)
        
        self.crear_tarjeta_modulo(630, 220, "📈", "Análisis Estadístico", 
                                 "Tendencias y Volatilidad", "#8b5cf6", self.modulo_analisis)
        
        self.crear_tarjeta_modulo(270, 360, "🔮", "Predicciones", 
                                 "Proyección de Precios", "#f59e0b", self.modulo_prediccion)
        
        self.crear_tarjeta_modulo(630, 360, "🔍", "Consultas y Reportes", 
                                 "Búsqueda y Exportación", "#06b6d4", self.modulo_consultas)
        
       
        self.crear_boton_footer(450, 490, "Salir", "#dc2626", self.salir_sistema)
    
    def crear_tarjeta_modulo(self, x, y, icono, titulo, descripcion, color, comando):
        
        tarjeta_id = self.canvas.create_rectangle(x-130, y-40, x+130, y+100, 
                                                  fill="#1e293b", outline=color, width=2,
                                                  tags=f"tarjeta_{x}_{y}")
        
        self.canvas.create_oval(x-25, y-25, x+25, y+25, 
                               fill="#0a0f1e", outline=color, width=2,
                               tags=f"tarjeta_{x}_{y}")
        self.canvas.create_text(x, y, 
                               text=icono, 
                               font=("Arial", 32), 
                               fill=color,
                               tags=f"tarjeta_{x}_{y}")
        
        self.canvas.create_text(x, y+50, 
                               text=titulo, 
                               font=("Arial", 12, "bold"), 
                               fill="#e2e8f0",
                               tags=f"tarjeta_{x}_{y}")
        
        self.canvas.create_text(x, y+73, 
                               text=descripcion, 
                               font=("Arial", 9), 
                               fill="#94a3b8",
                               tags=f"tarjeta_{x}_{y}")
        
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Button-1>", lambda e: comando())
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Enter>", 
            lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(f"tarjeta_{x}_{y}", "<Leave>", 
            lambda e: self.canvas.config(cursor=""))
    
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
    
    def modulo_gestion(self):
        for widget in self.frame_principal.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        self.mostrar_submenu_gestion()

    def mostrar_submenu_gestion(self):
        self.canvas.delete("all")
        
        if self.logo_izquierdo:
            self.canvas.create_image(60, 50, image=self.logo_izquierdo, anchor="center")
        if self.logo_derecho:
            self.canvas.create_image(840, 50, image=self.logo_derecho, anchor="center")
        
        self.canvas.create_text(450, 100, 
                               text="GESTIÓN DE DATOS", 
                               font=("Arial", 22, "bold"), 
                               fill="#10b981")
        
        self.canvas.create_text(450, 130, 
                               text="Seleccione qué desea gestionar", 
                               font=("Arial", 12), 
                               fill="#94a3b8")
        
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