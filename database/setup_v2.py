from connection import DatabaseConnection, execute_query

def create_tables_v2():
    """Crea la estructura completa con zona horaria de Bolivia"""
    print("\n" + "="*70)
    print("CREANDO ESTRUCTURA DE BASE DE DATOS - VERSIÓN COMPLETA")
    print("="*70)

    # ========== TABLA: USUARIO ==========
    create_usuario = """
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario SERIAL PRIMARY KEY,
        nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
        nombre VARCHAR(100) NOT NULL,
        app VARCHAR(50),
        apm VARCHAR(50),
        rol_en_mercado VARCHAR(50),
        fecha_registro TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        password_hash VARCHAR(255),
        activo BOOLEAN DEFAULT TRUE
    );
    """

    # ========== TABLA: CATEGORIAS ========== 
    create_categorias = """
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria SERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL UNIQUE,
        descripcion TEXT,
        fecha_registro TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        activo BOOLEAN DEFAULT TRUE
    );
    """

    # ========== TABLA: PRODUCTO ==========
    create_producto = """
    CREATE TABLE IF NOT EXISTS producto (
        id_producto SERIAL PRIMARY KEY,
        nombre_producto VARCHAR(100) NOT NULL,
        categoria VARCHAR(50) REFERENCES categorias(nombre),
        unidad_medida VARCHAR(20) NOT NULL,
        descripcion TEXT,
        fecha_registro TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        activo BOOLEAN DEFAULT TRUE,
        UNIQUE(nombre_producto, unidad_medida)
    );
    """

    # ========== TABLA: MERCADO ==========
    create_mercado = """
    CREATE TABLE IF NOT EXISTS mercado (
        id_mercado SERIAL PRIMARY KEY,
        nombre_mercado VARCHAR(100) NOT NULL UNIQUE,
        direccion TEXT,
        barrio VARCHAR(100),
        avenida VARCHAR(100),
        ciudad VARCHAR(50),
        departamento VARCHAR(50),
        fecha_registro TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        activo BOOLEAN DEFAULT TRUE
    );
    """

    # ========== TABLA: HISTORIAL_P ==========
    create_historial = """
    CREATE TABLE IF NOT EXISTS historial_p (
        id_historial SERIAL PRIMARY KEY,
        id_producto INTEGER NOT NULL REFERENCES producto(id_producto),
        fecha_registro TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        stock INTEGER,
        fuente VARCHAR(100),
        observaciones TEXT
    );
    """

    # ========== TABLA: CONSULTA_PRECIO ==========
    create_consulta_precio = """
    CREATE TABLE IF NOT EXISTS consulta_precio (
        id_consulta SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuario(id_usuario),
        id_producto INTEGER REFERENCES producto(id_producto),
        fecha_consulta TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        precio_visto DECIMAL(10, 2)
    );
    """

    # ========== TABLA: FACTOR_INFLUYENTE ==========
    create_factor = """
    CREATE TABLE IF NOT EXISTS factor_influyente (
        id_factor SERIAL PRIMARY KEY,
        tipo_factor VARCHAR(50) NOT NULL,
        descripcion_f TEXT,
        f_i DECIMAL(5, 2),
        f_f DECIMAL(5, 2),
        fecha_registro TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz')
    );
    """

    # ========== TABLA: CONSIDERA ==========
    create_considera = """
    CREATE TABLE IF NOT EXISTS considera (
        id_consulta INTEGER REFERENCES consulta_precio(id_consulta),
        id_factor INTEGER REFERENCES factor_influyente(id_factor),
        impacto DECIMAL(5, 2),
        PRIMARY KEY (id_consulta, id_factor)
    );
    """

    # ========== TABLA: AFECTA ==========
    create_afecta = """
    CREATE TABLE IF NOT EXISTS afecta (
        id_prediccion INTEGER,
        id_factor INTEGER REFERENCES factor_influyente(id_factor),
        peso DECIMAL(5, 2),
        PRIMARY KEY (id_prediccion, id_factor)
    );
    """

    # ========== TABLA: OFERTA ==========
    create_oferta = """
    CREATE TABLE IF NOT EXISTS oferta (
        id_oferta SERIAL PRIMARY KEY,
        id_producto INTEGER REFERENCES producto(id_producto),
        id_mercado INTEGER REFERENCES mercado(id_mercado),
        precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
        stock INTEGER,
        fecha_actualizacion TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        UNIQUE(id_producto, id_mercado)
    );
    """

    # ========== TABLA: TRANSACCION ==========
    create_transaccion = """
    CREATE TABLE IF NOT EXISTS transaccion (
        id_transaccion SERIAL PRIMARY KEY,
        id_mercado INTEGER REFERENCES mercado(id_mercado),
        fecha_venta TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        total DECIMAL(10, 2),
        cantidad INTEGER,
        observaciones TEXT
    );
    """

    # ========== TABLA: PREDICCION ==========
    create_prediccion = """
    CREATE TABLE IF NOT EXISTS prediccion (
        id_prediccion SERIAL PRIMARY KEY,
        precio_estimado DECIMAL(10, 2),
        nivel_confianza DECIMAL(5, 2),
        tendencia VARCHAR(20),
        fecha_prediccion TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        fecha_objetivo DATE,
        modelo_usado VARCHAR(50)
    );
    """

    # ========== TABLA: ALERTA ==========
    create_alerta = """
    CREATE TABLE IF NOT EXISTS alerta (
        id_alerta SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuario(id_usuario),
        mensaje TEXT NOT NULL,
        tipo_alerta VARCHAR(50),
        fecha_creacion TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/La_Paz'),
        leida BOOLEAN DEFAULT FALSE
    );
    """

    # ========== TABLA: GENERA ==========
    create_genera = """
    CREATE TABLE IF NOT EXISTS genera (
        id_alerta INTEGER REFERENCES alerta(id_alerta),
        id_prediccion INTEGER REFERENCES prediccion(id_prediccion),
        PRIMARY KEY (id_alerta, id_prediccion)
    );
    """

    # ========== FK AFECTA ==========
    alter_afecta = """
    ALTER TABLE afecta
    DROP CONSTRAINT IF EXISTS afecta_id_prediccion_fkey;
    
    ALTER TABLE afecta
    ADD CONSTRAINT afecta_id_prediccion_fkey
    FOREIGN KEY (id_prediccion) REFERENCES prediccion(id_prediccion);
    """

    # ========== ÍNDICES ==========
    create_indices = """
    CREATE INDEX IF NOT EXISTS idx_historial_producto ON historial_p(id_producto);
    CREATE INDEX IF NOT EXISTS idx_historial_fecha ON historial_p(fecha_registro);
    CREATE INDEX IF NOT EXISTS idx_consulta_usuario ON consulta_precio(id_usuario);
    CREATE INDEX IF NOT EXISTS idx_consulta_producto ON consulta_precio(id_producto);
    CREATE INDEX IF NOT EXISTS idx_oferta_producto ON oferta(id_producto);
    CREATE INDEX IF NOT EXISTS idx_oferta_mercado ON oferta(id_mercado);
    CREATE INDEX IF NOT EXISTS idx_transaccion_mercado ON transaccion(id_mercado);
    CREATE INDEX IF NOT EXISTS idx_transaccion_fecha ON transaccion(fecha_venta);
    CREATE INDEX IF NOT EXISTS idx_prediccion_fecha ON prediccion(fecha_prediccion);
    CREATE INDEX IF NOT EXISTS idx_alerta_usuario ON alerta(id_usuario);
    CREATE INDEX IF NOT EXISTS idx_categorias_activo ON categorias(activo);
    """

    # Lista de tablas a crear en orden
    tablas = [
        ("Usuario", create_usuario),
        ("Categorías", create_categorias),
        ("Producto", create_producto),
        ("Mercado", create_mercado),
        ("Historial de Precios", create_historial),
        ("Consulta de Precio", create_consulta_precio),
        ("Factor Influyente", create_factor),
        ("Considera (Factor-Consulta)", create_considera),
        ("Oferta", create_oferta),
        ("Transacción", create_transaccion),
        ("Predicción", create_prediccion),
        ("Afecta (Factor-Predicción)", create_afecta),
        ("Alerta", create_alerta),
        ("Genera (Alerta-Predicción)", create_genera),
        ("Restricción Afecta", alter_afecta),
        ("Índices", create_indices)
    ]

    for nombre, sql in tablas:
        print(f"\n→ Creando: {nombre}...", end=" ")
        if execute_query(sql):
            print("✓ OK")
        else:
            print("✗ ERROR")
            return False

    # ========== DATOS INICIALES ==========
    print("\n→ Insertando datos iniciales...", end=" ")
    
    # Categorías con activo=TRUE
    categorias_iniciales = [
        ('Frutas', 'Productos frutales'),
        ('Verduras', 'Hortalizas y verduras'),
        ('Tubérculos', 'Papa, yuca, etc.'),
        ('Cereales', 'Arroz, maíz, quinua, etc.'),
        ('Carnes', 'Carnes rojas y blancas'),
        ('Lácteos', 'Leche, queso, yogurt'),
        ('Otros', 'Productos varios')
    ]
    
    insert_categoria = """
    INSERT INTO categorias (nombre, descripcion, activo)
    VALUES (%s, %s, TRUE)
    ON CONFLICT (nombre) DO NOTHING;
    """
    
    for nombre, desc in categorias_iniciales:
        execute_query(insert_categoria, (nombre, desc))

    # Usuario administrador
    insert_admin = """
    INSERT INTO usuario (nombre_usuario, nombre, rol_en_mercado)
    VALUES ('admin', 'Administrador del Sistema', 'Analista')
    ON CONFLICT (nombre_usuario) DO NOTHING;
    """
    execute_query(insert_admin)
    
    print("✓ OK")

    print("\n" + "="*70)
    print("✓ BASE DE DATOS CONFIGURADA CORRECTAMENTE")
    print("="*70 + "\n")

    print("📊 RESUMEN DE TABLAS CREADAS:")
    print(" 1. usuario - Sistema de usuarios")
    print(" 2. categorias - Categorías de productos ✓ (con columna activo)")
    print(" 3. producto - Catálogo de productos")
    print(" 4. mercado - Mercados de Bolivia")
    print(" 5. historial_p - Historial de precios")
    print(" 6. consulta_precio - Consultas de usuarios")
    print(" 7. factor_influyente - Factores que afectan precios")
    print(" 8. considera - Relación factor-consulta")
    print(" 9. oferta - Productos disponibles en mercados")
    print(" 10. transaccion - Registro de ventas")
    print(" 11. prediccion - Predicciones de precios")
    print(" 12. afecta - Relación factor-predicción")
    print(" 13. alerta - Sistema de notificaciones")
    print(" 14. genera - Relación alerta-predicción")
    print("\n✓ Todas las fechas configuradas con zona horaria America/La_Paz")
    
    return True


def migrar_datos_antiguos():
    """Migra datos de la estructura antigua a la nueva (si existen)"""
    print("\n🔄 MIGRANDO DATOS EXISTENTES...")
    
    check_query = """
    SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_name = 'productos' AND table_schema = 'public';
    """
    result = execute_query(check_query, fetch=True)
    
    if result and result[0][0] > 0:
        print("→ Detectada tabla 'productos' antigua")
        print("→ Migrando a tabla 'producto'...")
        
        migrate_productos = """
        INSERT INTO producto (nombre_producto, categoria, unidad_medida, descripcion, activo)
        SELECT p.nombre, c.nombre, p.unidad_medida, p.descripcion, p.activo
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        ON CONFLICT (nombre_producto, unidad_medida) DO NOTHING;
        """
        
        if execute_query(migrate_productos):
            print("✓ Productos migrados correctamente")
        else:
            print("✗ Error al migrar productos")
    
    print("✓ Migración completada\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SISTEMA DE ANÁLISIS Y PREDICCIÓN DE PRECIOS DEL MERCADO")
    print("Configurador de Base de Datos - VERSIÓN COMPLETA")
    print("="*70)

    # Probar conexión
    if not DatabaseConnection.test_connection():
        print("\n✗ No se pudo conectar a PostgreSQL")
        exit(1)

    print("\n⚠️ OPCIONES DE INSTALACIÓN:")
    print(" 1. Crear estructura nueva (recomendado si es primera vez)")
    print(" 2. Actualizar estructura existente (mantiene datos)")
    print(" 3. RESET COMPLETO (⚠️ BORRA TODO y recrea con zona horaria correcta)")
    
    opcion = input("\nSeleccione opción (1-3): ").strip()

    if opcion == "1":
        create_tables_v2()
    elif opcion == "2":
        create_tables_v2()
        migrar_datos_antiguos()
    elif opcion == "3":
        confirmar = input("⚠️ ¿SEGURO? Esto borrará TODOS los datos (si/no): ").strip().lower()
        if confirmar == "si":
            drop_query = """
            DROP TABLE IF EXISTS genera CASCADE;
            DROP TABLE IF EXISTS alerta CASCADE;
            DROP TABLE IF EXISTS afecta CASCADE;
            DROP TABLE IF EXISTS prediccion CASCADE;
            DROP TABLE IF EXISTS transaccion CASCADE;
            DROP TABLE IF EXISTS oferta CASCADE;
            DROP TABLE IF EXISTS considera CASCADE;
            DROP TABLE IF EXISTS factor_influyente CASCADE;
            DROP TABLE IF EXISTS consulta_precio CASCADE;
            DROP TABLE IF EXISTS historial_p CASCADE;
            DROP TABLE IF EXISTS producto CASCADE;
            DROP TABLE IF EXISTS mercado CASCADE;
            DROP TABLE IF EXISTS categorias CASCADE;
            DROP TABLE IF EXISTS usuario CASCADE;
            """
            if execute_query(drop_query):
                print("✓ Tablas eliminadas")
                create_tables_v2()
            else:
                print("✗ Error al eliminar tablas")
        else:
            print("Operación cancelada")
    else:
        print("Opción inválida")

    print("\n✓ Configuración completada")
    print("\nPróximos pasos:")
    print(" 1. Ejecutar main.py")
    print(" 2. Agregar productos/precios y verificar las fechas\n")