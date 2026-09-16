
use kiosko;

CREATE TABLE users(
	id int unsigned auto_increment primary key,
    nombre varchar(100)not null,
    email varchar(100) not null unique,
    password varchar(255) not null,
    rol enum('admin', 'vendedor') not null default 'vendedor',
    activo tinyint not null default 1,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp
);

CREATE TABLE proveedores(
	id int unsigned auto_increment primary key,
    nombre varchar(100) not null,
    telefono varchar(30) not null,
    email varchar(100),
    direccion varchar(100),
    activo tinyint not null default 1,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp
);

CREATE TABLE productos(
	id int unsigned auto_increment primary key,
    codigo varchar(50) unique,
    nombre varchar(100) not null,
    precio_costo decimal(10, 2) not null default 0.00,
    precio_venta decimal(10, 2) not null default 0.00,
    cantidad int not null default 0,
    stock_minimo int not null default 0,
    proveedor_id int unsigned,
    activo tinyint not null default 1,
    fecha_carga DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL,
    INDEX idx_productos_nombre (nombre)
);

CREATE TABLE movimientos_stock(
	id int unsigned auto_increment primary key,
    producto_id int unsigned not null,
    tipo enum('entrada', 'salida', 'ajuste') not null,
    cantidad int not null,
    cantidad_anterior int not null,
    cantidad_nueva int not null,
    motivo varchar(100),
    usuario_id int unsigned,
    referencia_id int unsigned,
    fecha datetime not null default current_timestamp,
    
    foreign key (producto_id) references productos(id),
    foreign key (usuario_id) references users(id),
    index idx_mov_fecha (fecha)
);

CREATE TABLE ventas(
	id int unsigned auto_increment primary key,
    fecha datetime not null default current_timestamp,
    usuario_id int unsigned,
    total decimal(10, 2) not null default 0.00,
    metodo_pago enum('efectivo', 'transferencia', 'tarjeta') default 'efectivo',
    anulado tinyint not null default 0,
    created_at datetime not null default current_timestamp,
    
    foreign key (usuario_id) references users(id),
    index idx_ventas_fecha (fecha)
);

CREATE TABLE ventas_detalles(
	id int unsigned auto_increment primary key,
    venta_id int unsigned not null,
    producto_id int unsigned not null,
    cantidad int not null,
    precio_unitario decimal(10, 2) not null,
    subtotal decimal(10, 2) not null,
    
    foreign key (venta_id) references ventas(id) on delete cascade,
    foreign key (producto_id) references productos(id)
);

show tables;

SELECT id, nombre, proveedor_id
FROM productos
WHERE proveedor_id IS NULL;

ALTER TABLE productos
  DROP FOREIGN KEY productos_ibfk_1;

ALTER TABLE productos
  MODIFY proveedor_id INT UNSIGNED NOT NULL;

ALTER TABLE productos
  ADD CONSTRAINT productos_ibfk_1
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
    ON DELETE RESTRICT;
    
SHOW CREATE TABLE productos;