-- ==========================
-- Usuarios registrados
-- ==========================
CREATE TABLE usuarios (
    id_usuario       INT AUTO_INCREMENT PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    email            VARCHAR(150) UNIQUE NOT NULL,
    password_hash    VARCHAR(255) NOT NULL,
    telefono         VARCHAR(20),
    fecha_nacimiento DATE,
    fecha_registro   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acepta_marketing BOOLEAN DEFAULT FALSE,
    rol              ENUM('cliente','vendedor') DEFAULT 'cliente'
);

-- ==========================
-- Dirección de envío
-- ==========================
CREATE TABLE direcciones (
    id_direccion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario   INT NOT NULL,
    calle        VARCHAR(150) NOT NULL,
    numero       VARCHAR(20),
    ciudad       VARCHAR(100) NOT NULL,
    region       VARCHAR(100),
    pais         VARCHAR(100) DEFAULT 'Chile',
    codigo_postal VARCHAR(20),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- ==========================
-- Productos
-- ==========================
CREATE TABLE productos (
    id_producto    INT AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(150) NOT NULL,
    descripcion    TEXT,
    precio         DECIMAL(10,2) NOT NULL,
    stock          INT NOT NULL DEFAULT 0,
    categoria      VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo         BOOLEAN DEFAULT TRUE
);

-- ==========================
-- Pedidos
-- ==========================
CREATE TABLE pedidos (
    id_pedido        INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario       INT NOT NULL,
    id_direccion     INT NOT NULL,
    fecha_pedido     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado           ENUM('pendiente','pagado','enviado','entregado','cancelado') DEFAULT 'pendiente',
    total            DECIMAL(10,2) NOT NULL,
    proveedor_pago   ENUM('paypal','webpay','mercadopago') DEFAULT 'paypal',
    referencia_pago  VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_direccion) REFERENCES direcciones(id_direccion)
);

-- ==========================
-- Detalles del pedido
-- ==========================
CREATE TABLE detalle_pedidos (
    id_detalle     INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido      INT NOT NULL,
    id_producto    INT NOT NULL,
    cantidad       INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);