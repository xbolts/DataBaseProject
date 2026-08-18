-- =============================================
-- SISTEMA VETERINARIO - Script MySQL
-- =============================================

-- ===================== TABLAS PRINCIPALES =====================

CREATE TABLE IF NOT EXISTS cliente (
    cedula_cliente VARCHAR(20) NOT NULL,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    nombre VARCHAR(100),
    correo VARCHAR(100),
    PRIMARY KEY (cedula_cliente)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS mascota (
    idmascota INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50),
    sexo CHAR(1) NOT NULL,
    fecha_nacimiento DATE,
    especie VARCHAR(50),
    raza VARCHAR(50),
    cedula_cliente VARCHAR(20),
    PRIMARY KEY (idmascota),
    FOREIGN KEY (cedula_cliente) REFERENCES cliente(cedula_cliente)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS producto_servicio (
    codigo_producto_servicio VARCHAR(20) NOT NULL,
    descripcion VARCHAR(100),
    porcentaje_iva DECIMAL(5,2),
    precio DECIMAL(10,2),
    PRIMARY KEY (codigo_producto_servicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS proveedor (
    id_proveedor INT NOT NULL,
    nombre VARCHAR(100),
    contacto VARCHAR(50),
    PRIMARY KEY (id_proveedor)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS cita (
    idcita INT NOT NULL AUTO_INCREMENT,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hora TIME DEFAULT '09:00:00',
    estado VARCHAR(20) NOT NULL,
    idmascota INT NOT NULL,
    PRIMARY KEY (idcita),
    FOREIGN KEY (idmascota) REFERENCES mascota(idmascota)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS consulta (
    id_consulta INT NOT NULL,
    fecha DATE,
    tratamiento_clinico TEXT,
    diagnostico TEXT,
    idmascota INT NOT NULL,
    PRIMARY KEY (id_consulta),
    FOREIGN KEY (idmascota) REFERENCES mascota(idmascota)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factura (
    num_comprobante VARCHAR(20) NOT NULL,
    cedula_cliente VARCHAR(20) NOT NULL,
    clave_acceso VARCHAR(30),
    fecha_emision DATE ,
    estado_pago VARCHAR(20),
    forma_pago VARCHAR(30),
    PRIMARY KEY (num_comprobante),
    FOREIGN KEY (cedula_cliente) REFERENCES cliente(cedula_cliente)
) ENGINE=InnoDB;

-- ===================== TABLAS DE RELACION =====================

CREATE TABLE IF NOT EXISTS medicina (
    codigo_producto_servicio VARCHAR(20) NOT NULL,
    stock_disponible INT,
    fecha_caducidad DATE,
    presentacion VARCHAR(50),
    PRIMARY KEY (codigo_producto_servicio),
    FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS accesorio (
    codigo_producto_servicio VARCHAR(20) NOT NULL,
    stock_disponible INT,
    categoria VARCHAR(50),
    marca VARCHAR(50),
    PRIMARY KEY (codigo_producto_servicio),
    FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS servicio (
    codigo_producto_servicio VARCHAR(20) NOT NULL,
    duracion_estimada INT,
    requiere_cita TINYINT(1),
    PRIMARY KEY (codigo_producto_servicio),
    FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS receta (
    id_receta INT NOT NULL,
    indicaciones_casa TEXT,
    id_consulta INT NOT NULL,
    PRIMARY KEY (id_receta),
    FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS factura_detalle (
    num_comprobante VARCHAR(20) NOT NULL,
    codigo_producto_servicio VARCHAR(20) NOT NULL,
    cantidad INT,
    subtotal DECIMAL(10,2),
    precio_unitario DECIMAL(10,2),
    PRIMARY KEY (num_comprobante, codigo_producto_servicio),
    FOREIGN KEY (num_comprobante) REFERENCES factura(num_comprobante),
    FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS atencion_estetica (
    id_atencion_estetica INT NOT NULL,
    hora_inicio TIME,
    hora_fin TIME,
    observaciones TEXT,
    idmascota INT NOT NULL,
    PRIMARY KEY (id_atencion_estetica),
    FOREIGN KEY (idmascota) REFERENCES mascota(idmascota)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS compra_insumo (
    id_compra INT NOT NULL,
    fecha_ingreso DATE ,
    cantidad_recibida INT,
    id_proveedor INT,
    codigo_producto_servicio VARCHAR(20),
    PRIMARY KEY (id_compra),
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor),
    FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS examen_lab (
    id_examen INT NOT NULL,
    resultados TEXT,
    tipo_muestra VARCHAR(50),
    fecha_muestra DATE ,
    id_consulta INT NOT NULL,
    id_proveedor INT NOT NULL,
    PRIMARY KEY (id_examen),
    FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta),
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reserva (
    idcita INT NOT NULL,
    codigo_producto_servicio VARCHAR(20) NOT NULL,
    PRIMARY KEY (idcita, codigo_producto_servicio),
    FOREIGN KEY (idcita) REFERENCES cita(idcita),
    FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS consulta_producto (
    id_consulta INT NOT NULL,
    codigo_producto_servicio VARCHAR(20) NOT NULL,
    cantidad_gastada DECIMAL(10,2),
    PRIMARY KEY (id_consulta, codigo_producto_servicio),
    FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta),
    FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
) ENGINE=InnoDB;

-- ===================== DATOS DE PRUEBA =====================

INSERT INTO cliente (cedula_cliente, direccion, telefono, nombre, correo) VALUES
('1724567890', 'Av. Amazonas N24', '0991234567', 'Juan Perez', 'juan.perez@email.com'),
('1724567891', 'Calle Larga 456', '0997654321', 'Maria Lopez', 'maria.lopez@email.com'),
('1724567892', 'Av. De la Prensa', '0983334444', 'Carlos Mendoza', 'carlos.m@email.com'),
('1724567893', 'Cumbaya, Los Olivos', '0975556666', 'Ana Gomez', 'ana.gomez@email.com'),
('1724567894', 'Villaflora, Sur', '0961112222', 'Luis Andrade', 'luis.a@email.com'),
('1724567895', 'Av. 10 de Agosto', '0958889999', 'Diana Flores', 'diana.f@email.com'),
('1724567896', 'La Mariscal', '0944445555', 'Jorge Martinez', 'jorge.m@email.com'),
('1724567897', 'San Rafael', '0932223333', 'Elena Castro', 'elena.c@email.com'),
('1724567898', 'Carcelen', '0929990000', 'Pedro Solis', 'pedro.s@email.com'),
('1724567899', 'El Condado', '0917778888', 'Lucia Pena', 'lucia.p@email.com'),
('2345311234', 'Guasmo Central 1212', '0965472112', 'Gregory Jesus Puglla Puglla', 'fish@gmail.com'),
('0930101190', 'Chongon', '0129281932', 'Jean', 'benites@gmail.com');

INSERT INTO mascota (nombre, sexo, fecha_nacimiento, especie, raza, cedula_cliente) VALUES
('Max', 'M', '2023-06-15', 'Perro', 'Golden Retriever', '1724567890'),
('Nala', 'H', '2024-07-20', 'Gato', 'Siamés', '1724567891'),
('Humbert', 'M', '2021-03-10', 'Perro', 'Pastor Aleman', '1724567892'),
('Kitty', 'H', '2025-05-01', 'Gato', 'Persa', '1724567893'),
('Zeus', 'M', '2019-01-25', 'Perro', 'Chihuahua', '1724567894'),
('Belle', 'H', '2022-09-12', 'Perro', 'Poodle', '1724567895'),
('Luna', 'M', '2024-08-05', 'Gato', 'Bengala', '1724567896'),
('Lucero', 'H', '2020-04-18', 'Perro', 'Labrador', '1724567897'),
('Beto', 'M', '2025-06-22', 'Hamster', 'Sirio', '1724567898'),
('Triny', 'H', '2023-11-30', 'Loro', 'Amazonas', '1724567899'),
('Meta', 'M', '2024-09-14', 'Conejo', 'Silvestre', '2345311234'),
('Oso', 'M', '2016-02-08', 'Perro', 'Sin Raza', '0930101190');

INSERT INTO producto_servicio (codigo_producto_servicio, descripcion, porcentaje_iva, precio) VALUES
('SER-001', 'Consulta Medica General', 0.0, 25.0),
('SER-002', 'Corte de Pelo y Bano', 12.0, 18.5),
('SER-003', 'Profilaxis Dental', 12.0, 45.0),
('MED-001', 'Amoxicilina 250mg', 0.0, 12.3),
('MED-002', 'Antiparasitario Bravecto', 0.0, 35.0),
('MED-003', 'Vitamina Canina Jarabe', 0.0, 8.5),
('ACC-001', 'Collar de Cuero Ajustable', 12.0, 10.0),
('ACC-002', 'Plato de Acero Inoxidable', 12.0, 6.5),
('ACC-003', 'Cama Acolchada Mediana', 12.0, 28.0),
('ACC-004', 'Juguete Raton de Goma', 12.0, 3.2);

INSERT INTO medicina (codigo_producto_servicio, stock_disponible, fecha_caducidad, presentacion) VALUES
('MED-001', 3, '2027-12-01', 'Pastilla'),
('MED-002', 15, '2028-06-15', 'Pastilla'),
('MED-003', 5, '2027-03-20', 'Jarabe');

INSERT INTO accesorio (codigo_producto_servicio, stock_disponible, categoria, marca) VALUES
('ACC-001', 5, 'Paseo', 'DoggyStyle'),
('ACC-002', 30, 'Alimentacion', 'PetBowl'),
('ACC-003', 4, 'Descanso', 'CozyPets'),
('ACC-004', 50, 'Juguetes', 'CatFun');

INSERT INTO servicio (codigo_producto_servicio, duracion_estimada, requiere_cita) VALUES
('SER-001', 30, 1),
('SER-002', 60, 1),
('SER-003', 45, 1);

INSERT INTO proveedor (id_proveedor, nombre, contacto) VALUES
(1, 'Drogueria Veterinaria Alfa', '099000111'),
(2, 'PetFood Mayoristas', '099000222'),
(3, 'Distribuidora Accesorios Caninos', '099000333'),
(4, 'Laboratorios VetSalud', '099000444'),
(5, 'Importadora Bichos', '099000555'),
(6, 'Farmacos del Norte', '099000666'),
(7, 'Equipos Medicos Zoetis', '099000777'),
(8, 'Distribuidora Central de Balanceados', '099000888'),
(9, 'Insumos Clinicos del Austro', '099000999'),
(10, 'Mundo Mascota Proveedores', '099000101');

INSERT INTO consulta (id_consulta, fecha, diagnostico, tratamiento_clinico, idmascota) VALUES
(1, '2026-07-10', 'Infeccion respiratoria leve', 'Administrar Amoxicilina cada 12 horas', 1),
(2, '2026-07-11', 'Otitis externa por hongos', 'Limpieza de oidos externa y gotas', 2),
(3, '2026-07-12', 'Gastroenteritis viral', 'Reposo absoluto e hidratacion', 3),
(4, '2026-07-12', 'Sarro dental severo', 'Profilaxis bajo anestesia general', 4),
(5, '2026-07-13', 'Dermatitis por pulgas', 'Aplicar pipeta antiparasitaria', 5),
(6, '2026-07-14', 'Traumatismo leve en pata posterior', 'Inyeccion antiinflamatoria intramuscular', 6),
(7, '2026-07-15', 'Alergia alimentaria', 'Cambio de dieta a comida hipoalergenica', 7),
(8, '2026-07-16', 'Asma felina', 'Nebulizaciones dos veces al dia', 8),
(9, '2026-07-17', 'Herida superficial por pelea', 'Limpieza de herida y vendaje', 9),
(10, '2026-07-18', 'Desnutricion leve', 'Suplemento vitaminico diario', 10);

INSERT INTO receta (id_receta, indicaciones_casa, id_consulta) VALUES
(1, 'Dar 1 pastilla de amoxicilina en la comida por 7 dias', 1),
(2, 'Colocar 3 gotas en cada oido tras la limpieza por 5 dias', 2),
(3, 'Dar suero oral 20ml cada 2 horas y dieta blanda', 3),
(4, 'No dar alimentos solidos hasta 6 horas post-operatorio', 4),
(5, 'Evitar banos por 48 horas post-aplicacion de pipeta', 5),
(6, 'Dar analgesico jarabe 2ml cada 24 horas por 3 dias', 6),
(7, 'Exclusividad estricta de croquetas hipoalergenicas', 7),
(8, 'Mantener al felino en ambientes libres de polvo y humo', 8),
(9, 'Limpiar con antisepctico y cambiar vendaje interdiario', 9),
(10, 'Dar 1ml de vitaminas por las mananas durante un mes', 10);

INSERT INTO cita (fecha, hora, estado, idmascota) VALUES
('2026-07-19 21:03:47', '09:00:00', 'ATENDIDA', 1),
('2026-07-19 21:03:47', '10:15:00', 'ATENDIDA', 2),
('2026-07-19 21:03:47', '11:00:00', 'PROGRAMADA', 3),
('2026-07-19 21:03:47', '14:00:00', 'ATENDIDA', 4),
('2026-07-19 21:03:47', '15:30:00', 'CANCELADA', 5),
('2026-07-19 21:03:47', '08:30:00', 'PROGRAMADA', 6),
('2026-07-19 21:03:47', '10:00:00', 'ATENDIDA', 7),
('2026-07-19 21:03:47', '12:30:00', 'PROGRAMADA', 8),
('2026-07-19 21:03:47', '14:30:00', 'ATENDIDA', 9),
('2026-07-19 21:03:47', '16:00:00', 'CANCELADA', 10),
('2026-07-30 21:57:12', '09:00:00', 'PROGRAMADA', 12);

INSERT INTO factura (num_comprobante, cedula_cliente, clave_acceso, fecha_emision, estado_pago, forma_pago) VALUES
('001-001-000000001', '1724567890', '190720260117245678901', '2026-07-10', 'PAGADA', 'EFECTIVO'),
('001-001-000000002', '1724567891', '190720260117245678911', '2026-07-11', 'PAGADA', 'TARJETA_CREDITO'),
('001-001-000000003', '1724567892', '190720260117245678921', '2026-07-12', 'PENDIENTE', 'TRANSFERENCIA'),
('001-001-000000004', '1724567893', '190720260117245678931', '2026-07-12', 'PAGADA', 'EFECTIVO'),
('001-001-000000005', '1724567894', '190720260117245678941', '2026-07-13', 'ANULADA', 'EFECTIVO'),
('001-001-000000006', '1724567895', '190720260117245678951', '2026-07-14', 'PAGADA', 'TARJETA_DEBITO'),
('001-001-000000007', '1724567896', '190720260117245678961', '2026-07-15', 'PAGADA', 'TRANSFERENCIA'),
('001-001-000000008', '1724567897', '190720260117245678971', '2026-07-16', 'PENDIENTE', 'EFECTIVO'),
('001-001-000000009', '1724567898', '190720260117245678981', '2026-07-17', 'PAGADA', 'TARJETA_CREDITO'),
('001-001-000000010', '1724567899', '190720260117245678991', '2026-07-18', 'PAGADA', 'EFECTIVO'),
('001-001-000000011', '1724567890', '190720260117245678901', '2026-07-19', 'PAGADA', 'EFECTIVO'),
('001-001-000000012', '1724567893', '190720260117245678931', '2026-07-19', 'PENDIENTE', 'TARJETA_CREDITO');

INSERT INTO factura_detalle (num_comprobante, codigo_producto_servicio, cantidad, precio_unitario, subtotal) VALUES
('001-001-000000001', 'SER-001', 1, 25.0, 25.0),
('001-001-000000001', 'MED-001', 2, 12.3, 24.6),
('001-001-000000002', 'SER-002', 1, 18.5, 18.5),
('001-001-000000003', 'SER-001', 1, 25.0, 25.0),
('001-001-000000004', 'SER-003', 1, 45.0, 45.0),
('001-001-000000006', 'SER-002', 1, 18.5, 18.5),
('001-001-000000007', 'SER-001', 1, 25.0, 25.0),
('001-001-000000007', 'ACC-003', 1, 28.0, 28.0),
('001-001-000000009', 'SER-001', 1, 25.0, 25.0),
('001-001-000000010', 'SER-002', 1, 18.5, 18.5),
('001-001-000000011', 'SER-001', 1, 25.0, 25.0),
('001-001-000000011', 'MED-003', 3, 8.5, 25.5),
('001-001-000000012', 'SER-002', 1, 18.5, 18.5),
('001-001-000000012', 'ACC-004', 2, 3.2, 6.4);

INSERT INTO atencion_estetica (id_atencion_estetica, hora_inicio, hora_fin, observaciones, idmascota) VALUES
(1, '09:00:00', '10:00:00', 'Corte estilo cachorro, se porto excelente', 1),
(2, '10:15:00', '11:30:00', 'Solo bano y cepillado profundo para retirar pelo muerto', 2),
(3, '11:00:00', '12:00:00', 'Corte higienico, un poco nervioso al inicio', 4),
(4, '14:00:00', '15:15:00', 'Bano medicado antipulgas, requiere cuidado con los ojos', 6),
(5, '15:30:00', '16:15:00', 'Corte de unas y limpieza de drenajes lagrimales', 10),
(6, '08:30:00', '09:45:00', 'Corte estandar de raza, requiere desenredado', 3),
(7, '10:00:00', '11:00:00', 'Bano cosmético aromatico', 5),
(8, '12:30:00', '13:45:00', 'Corte bajo por nudos excesivos en el lomo', 7),
(9, '14:30:00', '15:30:00', 'Primer bano del cachorro, se uso agua tibia y paciencia', 8),
(10, '16:00:00', '17:00:00', 'Limpieza general y perfume hipoalergenico', 9);

INSERT INTO compra_insumo (id_compra, fecha_ingreso, cantidad_recibida, id_proveedor, codigo_producto_servicio) VALUES
(1, '2026-05-01', 50, 1, 'MED-001'),
(2, '2026-05-10', 30, 4, 'MED-002'),
(3, '2026-05-15', 20, 1, 'MED-003'),
(4, '2026-06-01', 100, 3, 'ACC-001'),
(5, '2026-06-05', 40, 5, 'ACC-002'),
(6, '2026-06-12', 15, 3, 'ACC-003'),
(7, '2026-06-20', 200, 10, 'ACC-004'),
(8, '2026-07-01', 40, 6, 'MED-001'),
(9, '2026-07-05', 25, 4, 'MED-002'),
(10, '2026-07-10', 35, 3, 'ACC-001');

INSERT INTO examen_lab (id_examen, resultados, tipo_muestra, fecha_muestra, id_consulta, id_proveedor) VALUES
(1, 'Hemoglobina normal, leucocitos elevados', 'Sangre', '2026-07-10', 1, 4),
(2, 'Presencia de Malassezia spp', 'Hisopado otico', '2026-07-11', 2, 4),
(3, 'Parvovirus resultado Negativo', 'Heces', '2026-07-12', 3, 9),
(4, 'Creatinina y Urea estables para anestesia', 'Sangre', '2026-07-12', 4, 4),
(5, 'Presencia de acaros del genero Otodectes', 'Raspado de piel', '2026-07-13', 5, 9),
(6, 'Placa radiografica no muestra fracturas', 'Rayos X', '2026-07-14', 6, 7),
(7, 'Enzimas hepaticas ligeramente alteradas', 'Sangre', '2026-07-15', 7, 4),
(8, 'Celulas inflamatorias ausentes', 'Lavado bronquial', '2026-07-16', 8, 7),
(9, 'Cultivo bacteriano negativo', 'Secrecion de herida', '2026-07-17', 9, 4),
(10, 'Anemia normocitica normocromica', 'Sangre', '2026-07-18', 10, 4);

INSERT INTO reserva (idcita, codigo_producto_servicio) VALUES
(1, 'SER-001'),
(2, 'SER-002'),
(3, 'SER-001'),
(4, 'SER-003'),
(5, 'SER-001'),
(6, 'SER-002'),
(7, 'SER-001'),
(8, 'SER-003'),
(9, 'SER-001'),
(10, 'SER-002');

INSERT INTO consulta_producto (id_consulta, codigo_producto_servicio, cantidad_gastada) VALUES
(1, 'MED-001', 1.0),
(2, 'MED-003', 1.0),
(3, 'MED-001', 2.0),
(4, 'SER-003', 1.0),
(5, 'MED-002', 1.0),
(6, 'MED-001', 1.0),
(7, 'ACC-002', 1.0),
(8, 'MED-003', 1.0),
(9, 'MED-001', 1.0),
(10, 'MED-003', 2.0);

-- ===================== TRIGGERS =====================

DELIMITER //

-- Trigger 1: Restar stock al consumir un producto
CREATE TRIGGER trg_restar_stock_consulta
AFTER INSERT ON consulta_producto
FOR EACH ROW
BEGIN
    DECLARE stock_actual INT;
    
    SELECT stock_disponible INTO stock_actual 
    FROM medicina 
    WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
    
    IF stock_actual IS NOT NULL THEN
        IF stock_actual < NEW.cantidad_gastada THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Stock insuficiente';
        END IF;
        UPDATE medicina
        SET stock_disponible = stock_disponible - NEW.cantidad_gastada
        WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
    ELSE
        SELECT stock_disponible INTO stock_actual 
        FROM accesorio 
        WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
        
        IF stock_actual IS NOT NULL THEN
            IF stock_actual < NEW.cantidad_gastada THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Stock insuficiente';
            END IF;
            UPDATE accesorio
            SET stock_disponible = stock_disponible - NEW.cantidad_gastada
            WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
        END IF;
    END IF;
END //

-- Trigger 2: Sumar stock al ingresar una compra
CREATE TRIGGER trg_sumar_stock_compra
AFTER INSERT ON compra_insumo
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM medicina WHERE codigo_producto_servicio = NEW.codigo_producto_servicio) THEN
        UPDATE medicina
        SET stock_disponible = stock_disponible + NEW.cantidad_recibida
        WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
    ELSEIF EXISTS (SELECT 1 FROM accesorio WHERE codigo_producto_servicio = NEW.codigo_producto_servicio) THEN
        UPDATE accesorio
        SET stock_disponible = stock_disponible + NEW.cantidad_recibida
        WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
    END IF;
END //

DELIMITER ;

-- ===================== VISTAS =====================

-- Vista 1: Agenda de atenciones esteticas
CREATE OR REPLACE VIEW vw_agenda_atenciones AS
SELECT 
    ae.id_atencion_estetica,
    ae.hora_inicio,
    ae.hora_fin,
    ae.observaciones,
    m.idmascota,
    m.nombre AS nombre_mascota,
    m.especie,
    m.raza,
    c.cedula_cliente,
    c.nombre AS nombre_dueno,
    c.telefono
FROM atencion_estetica ae
JOIN mascota m ON ae.idmascota = m.idmascota
JOIN cliente c ON m.cedula_cliente = c.cedula_cliente;

-- Vista 2: Historial clinico completo
CREATE OR REPLACE VIEW vw_historial_clinico AS
SELECT 
    con.id_consulta,
    con.fecha,
    con.diagnostico,
    con.tratamiento_clinico,
    r.indicaciones_casa,
    m.idmascota,
    m.nombre AS nombre_mascota,
    m.especie,
    m.raza,
    m.sexo,
    m.fecha_nacimiento,
    c.cedula_cliente,
    c.nombre AS nombre_dueno,
    c.telefono,
    c.direccion,
    c.correo
FROM consulta con
JOIN mascota m ON con.idmascota = m.idmascota
JOIN cliente c ON m.cedula_cliente = c.cedula_cliente
LEFT JOIN receta r ON con.id_consulta = r.id_consulta;

-- Vista 3: Facturacion detallada
CREATE OR REPLACE VIEW vw_facturacion_detallada AS
SELECT 
    f.num_comprobante,
    f.fecha_emision,
    f.estado_pago,
    f.forma_pago,
    c.cedula_cliente,
    c.nombre AS nombre_cliente,
    c.telefono,
    fd.codigo_producto_servicio,
    ps.descripcion AS nombre_producto,
    fd.cantidad,
    fd.precio_unitario,
    fd.subtotal
FROM factura f
JOIN cliente c ON f.cedula_cliente = c.cedula_cliente
JOIN factura_detalle fd ON f.num_comprobante = fd.num_comprobante
JOIN producto_servicio ps ON fd.codigo_producto_servicio = ps.codigo_producto_servicio;

-- Vista 4: Inventario con alertas de stock
CREATE OR REPLACE VIEW vw_inventario_alertas AS
SELECT 
    ps.codigo_producto_servicio,
    ps.descripcion,
    ps.precio,
    ps.porcentaje_iva,
    COALESCE(m.stock_disponible, a.stock_disponible) AS stock_disponible,
    m.fecha_caducidad,
    m.presentacion,
    a.categoria,
    a.marca,
    CASE 
        WHEN m.codigo_producto_servicio IS NOT NULL THEN 'MEDICINA'
        WHEN a.codigo_producto_servicio IS NOT NULL THEN 'ACCESORIO'
        ELSE 'SERVICIO'
    END AS tipo_producto,
    CASE 
        WHEN COALESCE(m.stock_disponible, a.stock_disponible, 0) <= 5 THEN 'CRITICO'
        WHEN COALESCE(m.stock_disponible, a.stock_disponible, 0) <= 10 THEN 'BAJO'
        ELSE 'OK'
    END AS estado_stock
FROM producto_servicio ps
LEFT JOIN medicina m ON ps.codigo_producto_servicio = m.codigo_producto_servicio
LEFT JOIN accesorio a ON ps.codigo_producto_servicio = a.codigo_producto_servicio;

-- ===================== STORED PROCEDURES =====================

DELIMITER //

-- SP 1: Insertar cliente
CREATE PROCEDURE sp_cliente_insertar(
    IN p_cedula VARCHAR(20),
    IN p_nombre VARCHAR(100),
    IN p_direccion VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_correo VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    IF p_cedula IS NULL OR TRIM(p_cedula) = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cedula no puede estar vacia';
    END IF;
    
    IF p_nombre IS NULL OR TRIM(p_nombre) = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El nombre no puede estar vacio';
    END IF;
    
    IF EXISTS (SELECT 1 FROM cliente WHERE cedula_cliente = p_cedula) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe un cliente con esa cedula';
    END IF;
    
    INSERT INTO cliente (cedula_cliente, nombre, direccion, telefono, correo)
    VALUES (p_cedula, p_nombre, p_direccion, p_telefono, p_correo);
    
    COMMIT;
END //

-- SP 2: Actualizar cliente
CREATE PROCEDURE sp_cliente_actualizar(
    IN p_cedula VARCHAR(20),
    IN p_nombre VARCHAR(100),
    IN p_direccion VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_correo VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    IF NOT EXISTS (SELECT 1 FROM cliente WHERE cedula_cliente = p_cedula) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe un cliente con esa cedula';
    END IF;
    
    UPDATE cliente SET
        nombre = COALESCE(p_nombre, nombre),
        direccion = COALESCE(p_direccion, direccion),
        telefono = COALESCE(p_telefono, telefono),
        correo = COALESCE(p_correo, correo)
    WHERE cedula_cliente = p_cedula;
    
    COMMIT;
END //

-- SP 3: Eliminar cliente
CREATE PROCEDURE sp_cliente_eliminar(
    IN p_cedula VARCHAR(20)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    IF NOT EXISTS (SELECT 1 FROM cliente WHERE cedula_cliente = p_cedula) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe un cliente con esa cedula';
    END IF;
    
    IF EXISTS (SELECT 1 FROM factura WHERE cedula_cliente = p_cedula) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: el cliente tiene facturas asociadas';
    END IF;
    
    DELETE FROM cliente WHERE cedula_cliente = p_cedula;
    
    COMMIT;
END //

-- SP 4: Insertar mascota
CREATE PROCEDURE sp_mascota_insertar(
    IN p_nombre VARCHAR(50),
    IN p_sexo CHAR(1),
    IN p_fecha_nacimiento DATE,
    IN p_especie VARCHAR(50),
    IN p_raza VARCHAR(50),
    IN p_cedula_cliente VARCHAR(20)
)
BEGIN
    DECLARE v_nuevo_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    IF p_nombre IS NULL OR TRIM(p_nombre) = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El nombre no puede estar vacio';
    END IF;
    
    IF UPPER(p_sexo) NOT IN ('M', 'H') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El sexo debe ser M o H';
    END IF;
    
    IF p_fecha_nacimiento IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La fecha de nacimiento es obligatoria';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM cliente WHERE cedula_cliente = p_cedula_cliente) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe un cliente con esa cedula';
    END IF;
    
    SELECT COALESCE(MAX(idmascota), 0) + 1 INTO v_nuevo_id FROM mascota;
    
    INSERT INTO mascota (idmascota, nombre, sexo, fecha_nacimiento, especie, raza, cedula_cliente)
    VALUES (v_nuevo_id, p_nombre, UPPER(p_sexo), p_fecha_nacimiento, p_especie, p_raza, p_cedula_cliente);
    
    COMMIT;
END //

-- SP 5: Actualizar mascota
CREATE PROCEDURE sp_mascota_actualizar(
    IN p_id INT,
    IN p_nombre VARCHAR(50),
    IN p_sexo CHAR(1),
    IN p_especie VARCHAR(50),
    IN p_raza VARCHAR(50)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    IF NOT EXISTS (SELECT 1 FROM mascota WHERE idmascota = p_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe una mascota con ese ID';
    END IF;
    
    IF p_sexo IS NOT NULL AND UPPER(p_sexo) NOT IN ('M', 'H') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El sexo debe ser M o H';
    END IF;
    
    UPDATE mascota SET
        nombre = COALESCE(p_nombre, nombre),
        sexo = COALESCE(UPPER(p_sexo), sexo),
        especie = COALESCE(p_especie, especie),
        raza = COALESCE(p_raza, raza)
    WHERE idmascota = p_id;
    
    COMMIT;
END //

-- SP 6: Eliminar mascota
CREATE PROCEDURE sp_mascota_eliminar(
    IN p_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    IF NOT EXISTS (SELECT 1 FROM mascota WHERE idmascota = p_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe una mascota con ese ID';
    END IF;
    
    IF EXISTS (SELECT 1 FROM consulta WHERE idmascota = p_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: la mascota tiene consultas asociadas';
    END IF;
    
    DELETE FROM mascota WHERE idmascota = p_id;
    
    COMMIT;
END //

DELIMITER ;

-- ===================== INDICES =====================

CREATE INDEX idx_factura_fecha_emision ON factura(fecha_emision);
CREATE INDEX idx_consulta_mascota_fecha ON consulta(idmascota, fecha);
CREATE INDEX idx_cita_fecha ON cita(fecha);
CREATE INDEX idx_medicina_stock ON medicina(stock_disponible);
CREATE INDEX idx_accesorio_stock ON accesorio(stock_disponible);

-- ===================== USUARIOS Y PERMISOS =====================

-- Crear usuarios
CREATE USER IF NOT EXISTS 'app_veterinaria'@'%' IDENTIFIED BY 'vet_app_2026';
CREATE USER IF NOT EXISTS 'auditor_sri'@'%' IDENTIFIED BY 'auditoria_2026';
CREATE USER IF NOT EXISTS 'asistente_citas'@'%' IDENTIFIED BY 'citas_2026';
CREATE USER IF NOT EXISTS 'gestor_inventario'@'%' IDENTIFIED BY 'bodega_2026';
CREATE USER IF NOT EXISTS 'veterinario_jefe'@'%' IDENTIFIED BY 'vet_admin_2026';

-- Permisos a tablas
GRANT SELECT, INSERT, UPDATE ON cliente TO 'app_veterinaria'@'%';
GRANT SELECT ON factura TO 'auditor_sri'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON cita TO 'asistente_citas'@'%';
GRANT SELECT, INSERT, UPDATE ON mascota TO 'asistente_citas'@'%';
GRANT SELECT, INSERT, UPDATE ON medicina TO 'gestor_inventario'@'%';
GRANT SELECT, INSERT ON compra_insumo TO 'gestor_inventario'@'%';
GRANT SELECT, INSERT, UPDATE ON consulta TO 'veterinario_jefe'@'%';

-- Permisos a vistas
GRANT SELECT ON vw_facturacion_detallada TO 'auditor_sri'@'%';
GRANT SELECT ON vw_historial_clinico TO 'veterinario_jefe'@'%';
GRANT SELECT ON vw_agenda_atenciones TO 'asistente_citas'@'%';
GRANT SELECT ON vw_inventario_alertas TO 'gestor_inventario'@'%';

-- Permisos a stored procedures
GRANT EXECUTE ON PROCEDURE sp_cliente_insertar TO 'app_veterinaria'@'%';
GRANT EXECUTE ON PROCEDURE sp_cliente_actualizar TO 'app_veterinaria'@'%';
GRANT EXECUTE ON PROCEDURE sp_cliente_eliminar TO 'app_veterinaria'@'%';
GRANT EXECUTE ON PROCEDURE sp_mascota_insertar TO 'app_veterinaria'@'%';
GRANT EXECUTE ON PROCEDURE sp_mascota_actualizar TO 'app_veterinaria'@'%';
GRANT EXECUTE ON PROCEDURE sp_mascota_eliminar TO 'app_veterinaria'@'%';

FLUSH PRIVILEGES;
