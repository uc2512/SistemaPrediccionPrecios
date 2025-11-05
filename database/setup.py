from database.connection import DatabaseConnection, execute_query

def create_tables():
    """Crea las tablas necesarias para el sistema"""
    
    # SQL para crear tabla de mercados
    create_mercados = """
    CREATE TABLE IF NOT EXISTS mercados (
        id_mercado SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        ciudad VARCHAR(50) NOT NULL,
        departamento VARCHAR(50) NOT NULL,
        direccion TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        activo BOOLEAN DEFAULT TRUE
    );
    """
    
    # SQL para crear tabla de categorías
    create_categorias = """
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria SERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL UNIQUE,
        descripcion TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # SQL para crear tabla de productos
    create_productos = """
    CREATE TABLE IF NOT EXISTS productos (
        id_producto SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        id_categoria INTEGER REFERENCES categorias(id_categoria),
        unidad_medida VARCHAR(20) NOT NULL,
        descripcion TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        activo BOOLEAN DEFAULT TRUE,
        UNIQUE(nombre, unidad_medida)
    );
    """
    
    # SQL para crear tabla de precios
    create_precios = """
    CREATE TABLE IF NOT EXISTS precios (
        id_precio SERIAL PRIMARY KEY,
        id_producto INTEGER NOT NULL REFERENCES productos(id_producto),
        id_mercado INTEGER NOT NULL REFERENCES mercados(id_mercado),
        fecha DATE NOT NULL,
        precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario >= 0),
        observaciones TEXT,
        fuente VARCHAR(100),
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(id_producto, id_mercado, fecha)
    );
    """
    
    # Crear índices para mejorar rendimiento
    create_indices = """
    CREATE INDEX IF NOT EXISTS idx_precios_fecha ON precios(fecha);
    CREATE INDEX IF NOT EXISTS idx_precios_producto ON precios(id_producto);
    CREATE INDEX IF NOT EXISTS idx_precios_mercado ON precios(id_mercado);
    CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(id_categoria);
    """
    
    print("\n" + "="*60)
    print("CREANDO ESTRUCTURA DE BASE DE DATOS")
    print("="*60)
    
    # Ejecutar creación de tablas
    tablas = [
        ("Mercados", create_mercados),
        ("Categorías", create_categorias),
        ("Productos", create_productos),
        ("Precios", create_precios),
        ("Índices", create_indices)
    ]
    
    for nombre, sql in tablas:
        print(f"\n→ Creando tabla: {nombre}...", end=" ")
        if execute_query(sql):
            print("✓ OK")
        else:
            print("✗ ERROR")
            return False
    
    # Insertar datos iniciales (categorías básicas)
    print("\n→ Insertando categorías iniciales...", end=" ")
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
    INSERT INTO categorias (nombre, descripcion) 
    VALUES (%s, %s)
    ON CONFLICT (nombre) DO NOTHING;
    """
    
    success = True
    for nombre, desc in categorias_iniciales:
        if not execute_query(insert_categoria, (nombre, desc)):
            success = False
            break
    
    if success:
        print("✓ OK")
    else:
        print("✗ ERROR")
        return False
    
    print("\n" + "="*60)
    print("✓ BASE DE DATOS CONFIGURADA CORRECTAMENTE")
    print("="*60 + "\n")
    
    return True


def drop_tables():
    """Elimina todas las tablas (usar con precaución)"""
    print("\n⚠️  ADVERTENCIA: Esto eliminará todas las tablas y datos")
    
    drop_sql = """
    DROP TABLE IF EXISTS precios CASCADE;
    DROP TABLE IF EXISTS productos CASCADE;
    DROP TABLE IF EXISTS categorias CASCADE;
    DROP TABLE IF EXISTS mercados CASCADE;
    """
    
    if execute_query(drop_sql):
        print("✓ Tablas eliminadas correctamente")
        return True
    else:
        print("✗ Error al eliminar tablas")
        return False


def reset_database():
    """Reinicia la base de datos (elimina y recrea)"""
    print("\n🔄 REINICIANDO BASE DE DATOS...")
    drop_tables()
    create_tables()


if __name__ == "__main__":
    # Script de inicialización
    print("\n" + "="*60)
    print("SISTEMA DE ANÁLISIS Y PREDICCIÓN DE PRECIOS DEL MERCADO")
    print("Configurador de Base de Datos PostgreSQL")
    print("="*60)
    
    # Probar conexión
    if not DatabaseConnection.test_connection():
        print("\n✗ No se pudo conectar a PostgreSQL")
        print("\nVerifica:")
        print("  1. PostgreSQL está instalado y corriendo")
        print("  2. Existe la base de datos 'mercado_db'")
        print("  3. Usuario y contraseña son correctos en connection.py")
        exit(1)
    
    # Crear tablas
    create_tables()
    
    print("\n✓ Sistema listo para usar")
    print("\nPróximos pasos:")
    print("  1. Ejecutar main.py para iniciar la interfaz")
    print("  2. Usar el módulo de Gestión de Datos\n")