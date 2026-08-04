-- =============================================
-- SISTEMA VETERINARIO - Script de Base de Datos
-- =============================================

-- ===================== TABLAS PRINCIPALES =====================

-- Tabla: cliente
CREATE TABLE IF NOT EXISTS cliente (
    cedula character varying NOT NULL,
    direccion character varying,
    telefono character varying,
    nombre character varying,
    correo character varying,
    CONSTRAINT cliente_pkey PRIMARY KEY (cedula)
);

-- Tabla: mascota
CREATE SEQUENCE IF NOT EXISTS mascota_idmascota_seq;
CREATE TABLE IF NOT EXISTS mascota (
    idmascota integer NOT NULL DEFAULT nextval('mascota_idmascota_seq'),
    sexo character varying NOT NULL,
    edad integer,
    especie character varying,
    raza character varying,
    cedula character varying,
    nombre character varying,
    CONSTRAINT mascota_pkey PRIMARY KEY (idmascota),
    CONSTRAINT mascota_cedula_fkey FOREIGN KEY (cedula) REFERENCES cliente(cedula)
);

-- Tabla: producto_servicio
CREATE TABLE IF NOT EXISTS producto_servicio (
    codigo_producto_servicio character varying NOT NULL,
    descripcion character varying,
    tipo_iva numeric,
    precio numeric,
    tipo character varying NOT NULL,
    CONSTRAINT producto_servicio_pkey PRIMARY KEY (codigo_producto_servicio)
);

-- Tabla: proveedor
CREATE TABLE IF NOT EXISTS proveedor (
    id_proveedor integer NOT NULL,
    nombre character varying,
    contacto character varying,
    CONSTRAINT proveedor_pkey PRIMARY KEY (id_proveedor)
);

-- Tabla: cita
CREATE SEQUENCE IF NOT EXISTS cita_idcita_seq;
CREATE TABLE IF NOT EXISTS cita (
    idcita integer NOT NULL DEFAULT nextval('cita_idcita_seq'),
    fecha timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado character varying NOT NULL,
    idmascota integer NOT NULL,
    codigo_producto_servicio character varying NOT NULL,
    CONSTRAINT cita_pkey PRIMARY KEY (idcita),
    CONSTRAINT fk_mascota_cita FOREIGN KEY (idmascota) REFERENCES mascota(idmascota),
    CONSTRAINT fk_cita_producto_servicio FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- Tabla: consulta
CREATE TABLE IF NOT EXISTS consulta (
    id_consulta integer NOT NULL,
    fecha date DEFAULT CURRENT_DATE,
    tratamiento_clinico text,
    diagnostico text,
    idmascota integer NOT NULL,
    CONSTRAINT consulta_pkey PRIMARY KEY (id_consulta),
    CONSTRAINT fk_consulta_mascota FOREIGN KEY (idmascota) REFERENCES mascota(idmascota)
);

-- Tabla: factura
CREATE TABLE IF NOT EXISTS factura (
    num_comprobante integer NOT NULL,
    cedula character varying NOT NULL,
    clave_acceso character varying,
    fecha_emision date DEFAULT CURRENT_DATE,
    estado_pago character varying,
    forma_pago character varying,
    CONSTRAINT factura_pkey PRIMARY KEY (num_comprobante),
    CONSTRAINT fk_factura_cliente FOREIGN KEY (cedula) REFERENCES cliente(cedula)
);

-- ===================== TABLAS DE RELACIÓN =====================

-- Tabla: medicina_detalles
CREATE TABLE IF NOT EXISTS medicina_detalles (
    codigo_producto_servicio character varying NOT NULL,
    stock_disponible integer,
    fecha_caducidad date,
    presentacion character varying,
    CONSTRAINT medicina_detalles_pkey PRIMARY KEY (codigo_producto_servicio),
    CONSTRAINT medicina_detalles_codigo_fkey FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- Tabla: accesorio_detalles
CREATE TABLE IF NOT EXISTS accesorio_detalles (
    codigo_producto_servicio character varying NOT NULL,
    stock_disponible integer,
    categoria character varying,
    marca character varying,
    CONSTRAINT accesorio_detalles_pkey PRIMARY KEY (codigo_producto_servicio),
    CONSTRAINT accesorio_detalles_codigo_fkey FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- Tabla: servicio_detalles
CREATE TABLE IF NOT EXISTS servicio_detalles (
    codigo_producto_servicio character varying NOT NULL,
    duracion_estimada integer,
    requiere_cita boolean,
    CONSTRAINT servicio_detalles_pkey PRIMARY KEY (codigo_producto_servicio),
    CONSTRAINT servicio_detalles_codigo_fkey FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- Tabla: receta
CREATE TABLE IF NOT EXISTS receta (
    id_receta integer NOT NULL,
    indicaciones_en_casa text,
    id_consulta integer NOT NULL,
    CONSTRAINT receta_pkey PRIMARY KEY (id_receta),
    CONSTRAINT fk_receta_consulta FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta)
);

-- Tabla: factura_detalle
CREATE TABLE IF NOT EXISTS factura_detalle (
    num_comprobante integer NOT NULL,
    codigo_producto_servicio character varying NOT NULL,
    cantidad integer,
    subtotal numeric,
    precio_unitario numeric,
    CONSTRAINT factura_detalle_pkey PRIMARY KEY (num_comprobante, codigo_producto_servicio),
    CONSTRAINT fk_detalle_factura FOREIGN KEY (num_comprobante) REFERENCES factura(num_comprobante),
    CONSTRAINT fk_detalle_producto FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- Tabla: atencion_estetica
CREATE TABLE IF NOT EXISTS atencion_estetica (
    id_peluqueria integer NOT NULL,
    hora_inicio time without time zone DEFAULT CURRENT_TIME,
    hora_fin time without time zone DEFAULT CURRENT_TIME,
    observaciones text,
    idmascota integer NOT NULL,
    CONSTRAINT atencion_estetica_pkey PRIMARY KEY (id_peluqueria),
    CONSTRAINT fk_atencion_estetica_mascota FOREIGN KEY (idmascota) REFERENCES mascota(idmascota)
);

-- Tabla: compra_insumo
CREATE TABLE IF NOT EXISTS compra_insumo (
    id_compra integer NOT NULL,
    fecha_ingreso date DEFAULT CURRENT_DATE,
    cantidad_recibida integer,
    id_proveedor integer,
    codigo_producto_servicio character varying,
    CONSTRAINT compra_insumo_pkey PRIMARY KEY (id_compra),
    CONSTRAINT fk_proveedor_compra FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor),
    CONSTRAINT fk_compra_producto FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- Tabla: examen_lab
CREATE TABLE IF NOT EXISTS examen_lab (
    id_examen integer NOT NULL,
    resultados text,
    tipo_muestra character varying,
    fecha_muestra date DEFAULT CURRENT_DATE,
    id_consulta integer NOT NULL,
    id_proveedor integer NOT NULL,
    CONSTRAINT examen_lab_pkey PRIMARY KEY (id_examen),
    CONSTRAINT fk_examen_lab_consulta FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta),
    CONSTRAINT fk_examen_lab_proveedor FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
);

-- Tabla: reserva
CREATE TABLE IF NOT EXISTS reserva (
    idcita integer NOT NULL,
    codigo_producto_servicio character varying NOT NULL,
    CONSTRAINT reserva_pkey PRIMARY KEY (idcita, codigo_producto_servicio),
    CONSTRAINT fk_reserva_cita FOREIGN KEY (idcita) REFERENCES cita(idcita),
    CONSTRAINT fk_reserva_producto FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- Tabla: consulta_producto
CREATE TABLE IF NOT EXISTS consulta_producto (
    id_consulta integer NOT NULL,
    codigo_producto_servicio character varying NOT NULL,
    cantidad_gastada numeric,
    CONSTRAINT consulta_producto_pkey PRIMARY KEY (id_consulta, codigo_producto_servicio),
    CONSTRAINT fk_consulta_producto_consulta FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta),
    CONSTRAINT fk_consulta_producto_producto FOREIGN KEY (codigo_producto_servicio) REFERENCES producto_servicio(codigo_producto_servicio)
);

-- ===================== DATOS DE PRUEBA =====================

-- CLIENTES (12 registros)
INSERT INTO cliente (cedula, direccion, telefono, nombre, correo) VALUES
('1724567890', 'Av. Amazonas N24', '0991234567', 'Juan Pérez', 'juan.perez@email.com'),
('1724567891', 'Calle Larga 456', '0997654321', 'María López', 'maria.lopez@email.com'),
('1724567892', 'Av. De la Prensa', '0983334444', 'Carlos Mendoza', 'carlos.m@email.com'),
('1724567893', 'Cumbayá, Los Olivos', '0975556666', 'Ana Gómez', 'ana.gomez@email.com'),
('1724567894', 'Villaflora, Sur', '0961112222', 'Luis Andrade', 'luis.a@email.com'),
('1724567895', 'Av. 10 de Agosto', '0958889999', 'Diana Flores', 'diana.f@email.com'),
('1724567896', 'La Mariscal', '0944445555', 'Jorge Martínez', 'jorge.m@email.com'),
('1724567897', 'San Rafael', '0932223333', 'Elena Castro', 'elena.c@email.com'),
('1724567898', 'Carcelén', '0929990000', 'Pedro Solís', 'pedro.s@email.com'),
('1724567899', 'El Condado', '0917778888', 'Lucía Peña', 'lucia.p@email.com'),
('2345311234', 'Guasmo Central 1212', '0965472112', 'Gregory Jesús Puglla Puglla', 'fish@gmail.com'),
('0930101190', 'Chongón', '0129281932', 'Jean', 'benites@gmail.com');

-- MASCOTAS (12 registros)
INSERT INTO mascota (idmascota, nombre, sexo, edad, especie, raza, cedula) VALUES
(1, 'Max', 'M', 3, 'Perro', 'Golden Retriever', '1724567890'),
(2, 'Nala', 'F', 2, 'Gato', 'Siamés', '1724567891'),
(3, 'Humbert', 'M', 5, 'Perro', 'Pastor Alemán', '1724567892'),
(4, 'Kitty', 'F', 1, 'Gato', 'Persa', '1724567893'),
(5, 'Zeus', 'M', 7, 'Perro', 'Chihuahua', '1724567894'),
(6, 'Belle', 'F', 4, 'Perro', 'Poodle', '1724567895'),
(7, 'Luna', 'M', 2, 'Gato', 'Bengala', '1724567896'),
(8, 'Lucero', 'F', 6, 'Perro', 'Labrador', '1724567897'),
(9, 'Beto', 'M', 1, 'Hámster', 'Sirio', '1724567898'),
(10, 'Triny', 'F', 3, 'Loro', 'Amazonas', '1724567899'),
(11, 'Meta', 'M', 2, 'Conejo', 'Silvestre', '2345311234'),
(12, 'Oso', 'M', 10, 'Perro', 'Sin Raza', '0930101190');

-- PRODUCTOS Y SERVICIOS (10 registros)
INSERT INTO producto_servicio (codigo_producto_servicio, descripcion, tipo_iva, precio, tipo) VALUES
('SERV-001', 'Consulta Médica General', 0.0, 25.0, 'Servicio'),
('SERV-002', 'Corte de Pelo y Baño', 12.0, 18.5, 'Servicio'),
('SERV-003', 'Profilaxis Dental', 12.0, 45.0, 'Servicio'),
('MED-001', 'Amoxicilina 250mg', 0.0, 12.3, 'Medicina'),
('MED-002', 'Antiparasitario Bravecto', 0.0, 35.0, 'Medicina'),
('MED-003', 'Vitamina Canina Jarabe', 0.0, 8.5, 'Medicina'),
('ACC-001', 'Collar de Cuero Ajustable', 12.0, 10.0, 'Accesorio'),
('ACC-002', 'Plato de Acero Inoxidable', 12.0, 6.5, 'Accesorio'),
('ACC-003', 'Cama Acolchada Mediana', 12.0, 28.0, 'Accesorio'),
('ACC-004', 'Juguete Ratón de Goma', 12.0, 3.2, 'Accesorio');

-- DETALLES DE MEDICINAS (3 registros)
INSERT INTO medicina_detalles (codigo_producto_servicio, stock_disponible, fecha_caducidad, presentacion) VALUES
('MED-001', 3, '2027-12-01', 'Pastilla'),
('MED-002', 15, '2028-06-15', 'Pastilla'),
('MED-003', 5, '2027-03-20', 'Jarabe');

-- DETALLES DE ACCESORIOS (4 registros)
INSERT INTO accesorio_detalles (codigo_producto_servicio, stock_disponible, categoria, marca) VALUES
('ACC-001', 5, 'Paseo', 'DoggyStyle'),
('ACC-002', 30, 'Alimentación', 'PetBowl'),
('ACC-003', 4, 'Descanso', 'CozyPets'),
('ACC-004', 50, 'Juguetes', 'CatFun');

-- DETALLES DE SERVICIOS (3 registros)
INSERT INTO servicio_detalles (codigo_producto_servicio, duracion_estimada, requiere_cita) VALUES
('SERV-001', 30, true),
('SERV-002', 60, true),
('SERV-003', 45, true);

-- PROVEEDORES (10 registros)
INSERT INTO proveedor (id_proveedor, nombre, contacto) VALUES
(1, 'Droguería Veterinaria Alfa', '099000111'),
(2, 'PetFood Mayoristas', '099000222'),
(3, 'Distribuidora Accesorios Caninos', '099000333'),
(4, 'Laboratorios VetSalud', '099000444'),
(5, 'Importadora Bichos', '099000555'),
(6, 'Fármacos del Norte', '099000666'),
(7, 'Equipos Médicos Zoetis', '099000777'),
(8, 'Distribuidora Central de Balanceados', '099000888'),
(9, 'Insumos Clínicos del Austro', '099000999'),
(10, 'Mundo Mascota Proveedores', '099000101');

-- CONSULTAS (10 registros)
INSERT INTO consulta (id_consulta, fecha, diagnostico, tratamiento_clinico, idmascota) VALUES
(1, '2026-07-10', 'Infección respiratoria leve', 'Administrar Amoxicilina cada 12 horas', 1),
(2, '2026-07-11', 'Otitis externa por hongos', 'Limpieza de oídos externa y gotas', 2),
(3, '2026-07-12', 'Gastroenteritis viral', 'Reposo absoluto e hidratación', 3),
(4, '2026-07-12', 'Sarro dental severo', 'Profilaxis bajo anestesia general', 4),
(5, '2026-07-13', 'Dermatitis por pulgas', 'Aplicar pipeta antiparasitaria', 5),
(6, '2026-07-14', 'Traumatismo leve en pata posterior', 'Inyección antiinflamatoria intramuscular', 6),
(7, '2026-07-15', 'Alergia alimentaria', 'Cambio de dieta a comida hipoalergénica', 7),
(8, '2026-07-16', 'Asma felina', 'Nebulizaciones dos veces al día', 8),
(9, '2026-07-17', 'Herida superficial por pelea', 'Limpieza de herida y vendaje', 9),
(10, '2026-07-18', 'Desnutrición leve', 'Suplemento vitamínico diario', 10);

-- RECETAS (10 registros)
INSERT INTO receta (id_receta, indicaciones_en_casa, id_consulta) VALUES
(1, 'Dar 1 pastilla de amoxicilina en la comida por 7 días', 1),
(2, 'Colocar 3 gotas en cada oído tras la limpieza por 5 días', 2),
(3, 'Dar suero oral 20ml cada 2 horas y dieta blanda', 3),
(4, 'No dar alimentos sólidos hasta 6 horas post-operatorio', 4),
(5, 'Evitar baños por 48 horas post-aplicación de pipeta', 5),
(6, 'Dar analgésico jarabe 2ml cada 24 horas por 3 días', 6),
(7, 'Exclusividad estricta de croquetas hipoalergénicas', 7),
(8, 'Mantener al felino en ambientes libres de polvo y humo', 8),
(9, 'Limpiar con antiséptico y cambiar vendaje interdiario', 9),
(10, 'Dar 1ml de vitaminas por las mañanas durante un mes', 10);

-- CITAS (11 registros)
INSERT INTO cita (idcita, fecha, estado, idmascota, codigo_producto_servicio) VALUES
(1, '2026-07-19 21:03:47', 'Finalizada', 1, 'SERV-001'),
(2, '2026-07-19 21:03:47', 'Finalizada', 2, 'SERV-002'),
(3, '2026-07-19 21:03:47', 'Programada', 3, 'SERV-001'),
(4, '2026-07-19 21:03:47', 'En progreso', 4, 'SERV-003'),
(5, '2026-07-19 21:03:47', 'Cancelada', 5, 'SERV-001'),
(6, '2026-07-19 21:03:47', 'Programada', 6, 'SERV-002'),
(7, '2026-07-19 21:03:47', 'Finalizada', 7, 'SERV-001'),
(8, '2026-07-19 21:03:47', 'Programada', 8, 'SERV-003'),
(9, '2026-07-19 21:03:47', 'Finalizada', 9, 'SERV-001'),
(10, '2026-07-19 21:03:47', 'Cancelada', 10, 'SERV-002'),
(11, '2026-07-30 21:57:12', 'Programada', 12, 'SERV-001');

-- FACTURAS (12 registros)
INSERT INTO factura (num_comprobante, cedula, clave_acceso, fecha_emision, estado_pago, forma_pago) VALUES
(1001, '1724567890', '190720260117245678901', '2026-07-10', 'Pagado', 'Efectivo'),
(1002, '1724567891', '190720260117245678911', '2026-07-11', 'Pagado', 'Tarjeta'),
(1003, '1724567892', '190720260117245678921', '2026-07-12', 'Pendiente', 'Transferencia'),
(1004, '1724567893', '190720260117245678931', '2026-07-12', 'Pagado', 'Efectivo'),
(1005, '1724567894', '190720260117245678941', '2026-07-13', 'Anulado', 'Ninguna'),
(1006, '1724567895', '190720260117245678951', '2026-07-14', 'Pagado', 'Tarjeta'),
(1007, '1724567896', '190720260117245678961', '2026-07-15', 'Pagado', 'Transferencia'),
(1008, '1724567897', '190720260117245678971', '2026-07-16', 'Pendiente', 'Efectivo'),
(1009, '1724567898', '190720260117245678981', '2026-07-17', 'Pagado', 'Tarjeta'),
(1010, '1724567899', '190720260117245678991', '2026-07-18', 'Pagado', 'Efectivo'),
(1011, '1724567890', '190720260117245678901', '2026-07-19', 'Pagado', 'Efectivo'),
(1012, '1724567893', '190720260117245678931', '2026-07-19', 'Pendiente', 'Tarjeta');

-- DETALLES DE FACTURAS (14 registros)
INSERT INTO factura_detalle (num_comprobante, codigo_producto_servicio, cantidad, precio_unitario, subtotal) VALUES
(1001, 'SERV-001', 1, 25.0, 25.0),
(1001, 'MED-001', 2, 12.3, 24.6),
(1002, 'SERV-002', 1, 18.5, 18.5),
(1003, 'SERV-001', 1, 25.0, 25.0),
(1004, 'SERV-003', 1, 45.0, 45.0),
(1006, 'SERV-002', 1, 18.5, 18.5),
(1007, 'SERV-001', 1, 25.0, 25.0),
(1007, 'ACC-003', 1, 28.0, 28.0),
(1009, 'SERV-001', 1, 25.0, 25.0),
(1010, 'SERV-002', 1, 18.5, 18.5),
(1011, 'SERV-001', 1, 25.0, 25.0),
(1011, 'MED-003', 3, 8.5, 25.5),
(1012, 'SERV-002', 1, 18.5, 18.5),
(1012, 'ACC-004', 2, 3.2, 6.4);

-- ATENCIONES ESTÉTICAS (10 registros)
INSERT INTO atencion_estetica (id_peluqueria, hora_inicio, hora_fin, observaciones, idmascota) VALUES
(1, '09:00:00', '10:00:00', 'Corte estilo cachorro, se portó excelente', 1),
(2, '10:15:00', '11:30:00', 'Solo baño y cepillado profundo para retirar pelo muerto', 2),
(3, '11:00:00', '12:00:00', 'Corte higiénico, un poco nervioso al inicio', 4),
(4, '14:00:00', '15:15:00', 'Baño medicado antipulgas, requiere cuidado con los ojos', 6),
(5, '15:30:00', '16:15:00', 'Corte de uñas y limpieza de drenajes lagrimales', 10),
(6, '08:30:00', '09:45:00', 'Corte estándar de raza, requiere desenredado', 3),
(7, '10:00:00', '11:00:00', 'Baño cosmético aromático', 5),
(8, '12:30:00', '13:45:00', 'Corte bajo por nudos excesivos en el lomo', 7),
(9, '14:30:00', '15:30:00', 'Primer baño del cachorro, se usó agua tibia y paciencia', 8),
(10, '16:00:00', '17:00:00', 'Limpieza general y perfume hipoalergénico', 9);

-- COMPRAS DE INSUMOS (10 registros)
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

-- EXÁMENES DE LABORATORIO (10 registros)
INSERT INTO examen_lab (id_examen, resultados, tipo_muestra, fecha_muestra, id_consulta, id_proveedor) VALUES
(1, 'Hemoglobina normal, leucocitos elevados', 'Sangre', '2026-07-10', 1, 4),
(2, 'Presencia de Malassezia spp', 'Hisopado ótico', '2026-07-11', 2, 4),
(3, 'Parvovirus resultado Negativo', 'Heces', '2026-07-12', 3, 9),
(4, 'Creatinina y Urea estables para anestesia', 'Sangre', '2026-07-12', 4, 4),
(5, 'Presencia de ácaros del género Otodectes', 'Raspado de piel', '2026-07-13', 5, 9),
(6, 'Placa radiográfica no muestra fracturas', 'Rayos X', '2026-07-14', 6, 7),
(7, 'Enzimas hepáticas ligeramente alteradas', 'Sangre', '2026-07-15', 7, 4),
(8, 'Células inflamatorias ausentes', 'Lavado bronquial', '2026-07-16', 8, 7),
(9, 'Cultivo bacteriano negativo', 'Secreción de herida', '2026-07-17', 9, 4),
(10, 'Anemia normocítica normocrómica', 'Sangre', '2026-07-18', 10, 4);

-- RESERVAS (10 registros)
INSERT INTO reserva (idcita, codigo_producto_servicio) VALUES
(1, 'SERV-001'),
(2, 'SERV-002'),
(3, 'SERV-001'),
(4, 'SERV-003'),
(5, 'SERV-001'),
(6, 'SERV-002'),
(7, 'SERV-001'),
(8, 'SERV-003'),
(9, 'SERV-001'),
(10, 'SERV-002');

-- CONSULTA-PRODUCTO (10 registros)
INSERT INTO consulta_producto (id_consulta, codigo_producto_servicio, cantidad_gastada) VALUES
(1, 'MED-001', 1.0),
(2, 'MED-003', 1.0),
(3, 'MED-001', 2.0),
(4, 'SERV-003', 1.0),
(5, 'MED-002', 1.0),
(6, 'MED-001', 1.0),
(7, 'ACC-002', 1.0),
(8, 'MED-003', 1.0),
(9, 'MED-001', 1.0),
(10, 'MED-003', 2.0);

-- ===================== SECUENCIAS =====================
SELECT setval('mascota_idmascota_seq', 12);
SELECT setval('cita_idcita_seq', 11);
