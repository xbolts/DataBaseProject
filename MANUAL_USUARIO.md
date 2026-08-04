# MANUAL DE USUARIO - SISTEMA VETERINARIO

## 1. DESCRIPCIÓN GENERAL

El Sistema Veterinario es una aplicación de línea de comandos (CLI) diseñada para la gestión integral de una clínica veterinaria. Permite registrar clientes, mascotas, productos/servicios, citas, consultas clínicas, facturas y más. Conecta con una base de datos en la nube (Supabase) para almacenar toda la información de forma segura.

### Características principales
- Registro completo de clientes y mascotas
- Gestión de productos (medicinas, accesorios) y servicios
- Programación y seguimiento de citas
- Historial clínico con diagnósticos y recetas
- Sistema de facturación con detalles
- Atención estética (baños, cortes)
- Reportes gerenciales (ventas, stock, agenda)
- CRUD completo para todas las tablas

---

## 2. REQUISITOS PREVIOS

### Software necesario
- Python 3.10 o superior
- Conexión a internet
- Archivo `.env` con credenciales de Supabase

### Instalación
1. Instalar Python desde https://www.python.org/downloads/
2. Marcar "Add Python to PATH" durante la instalación
3. Copiar los archivos del proyecto en una carpeta
4. Abrir terminal en esa carpeta
5. Ejecutar: `pip install -r requirements.txt`
6. Crear archivo `.env` con las credenciales (ver `.env.example`)

---

## 3. ESTRUCTURA DEL MENÚ PRINCIPAL

Al ejecutar `python main.py`, aparece el siguiente menú:

```
--- SISTEMA VETERINARIO ---
  1. Módulo de Reportes Gerenciales
  2. Módulo de Registro de Datos
  3. Editar / Eliminar Registros
  4. Salir
```

---

## 4. MÓDULO DE REPORTES GERENCIALES (Opción 1)

### 4.1 Reporte de Ventas y Facturación del Día
- Muestra todas las facturas emitidas el día actual
- Si no hay facturas del día, muestra las de la última fecha disponible
- Indica: N° comprobante, cédula cliente, estado de pago, forma de pago y total

### 4.2 Agenda del Día (Baños Programados)
- Lista todas las atenciones estéticas registradas
- Muestra: ID de atención, nombre de mascota, hora inicio, hora fin y observaciones

### 4.3 Reporte de Necesidad de Insumos (Alerta de Stock)
- Alerta cuando medicinas o accesorios tienen stock <= 5 unidades
- Si no hay alertas, muestra los 5 insumos con menor stock

### 4.4 Historial Clínico Completo
- Busca por nombre de mascota o cédula del dueño
- Muestra información del paciente y propietario
- Lista todas las consultas con diagnóstico, tratamiento y receta asociada

---

## 5. MÓDULO DE REGISTRO DE DATOS (Opción 2)

### 5.1 Registrar Cliente
**Campos:**
- Cédula (obligatorio, único)
- Nombre completo (obligatorio)
- Dirección (opcional)
- Teléfono (opcional)
- Correo electrónico (opcional)

**Pasos:**
1. Seleccionar opción 1
2. Ingresar los datos solicitados
3. El sistema verifica que no exista otra persona con la misma cédula
4. Confirma el registro

### 5.2 Registrar Mascota
**Campos:**
- Nombre (obligatorio)
- Sexo: M o F (obligatorio)
- Edad en años (obligatorio)
- Especie: Perro, Gato, etc. (obligatorio)
- Raza (obligatorio)
- Cédula del dueño (obligatorio, debe existir)

**Pasos:**
1. Seleccionar opción 2
2. Ingresar datos de la mascota
3. Seleccionar el dueño de la lista de clientes
4. El sistema asigna un ID automáticamente

### 5.3 Registrar Producto / Servicio
**Campos:**
- Código (formato: SERV-001, MED-001, ACC-001)
- Descripción (obligatorio)
- Tipo: Servicio, Medicina o Accesorio (obligatorio)
- Precio (obligatorio)
- Tipo IVA % (obligatorio)

**Detalles adicionales según tipo:**
- **Medicina:** Stock, fecha de caducidad, presentación
- **Accesorio:** Stock, categoría, marca
- **Servicio:** Duración estimada (minutos), requiere cita (s/n)

### 5.4 Registrar Cita
**Campos:**
- ID de mascota (seleccionar de la lista)
- Código del servicio (seleccionar de la lista)
- Estado: Programada, En progreso, Finalizada, Cancelada

**Pasos:**
1. Seleccionar opción 4
2. Ver lista de mascotas disponibles y seleccionar ID
3. Ver lista de servicios disponibles y seleccionar código
4. Indicar estado de la cita

### 5.5 Registrar Consulta Clínica
**Campos:**
- ID de mascota (seleccionar de la lista)
- Diagnóstico (obligatorio)
- Tratamiento clínico (obligatorio)

**Pasos:**
1. Seleccionar opción 5
2. Seleccionar mascota de la lista
3. Ingresar diagnóstico y tratamiento
4. El sistema asigna un ID automáticamente

### 5.6 Registrar Factura
**Campos:**
- Cédula del cliente (seleccionar de la lista)
- Estado de pago: Pagado, Pendiente, Anulado
- Forma de pago: Efectivo, Tarjeta, Transferencia, Ninguna
- Productos/servicios (agregar varios con cantidad)

**Pasos:**
1. Seleccionar opción 6
2. Seleccionar cliente
3. Indicar estado y forma de pago
4. Agregar productos escribiendo el código (escribir "fin" para terminar)
5. Para cada producto indicar cantidad
6. Ver resumen y confirmar

---

## 6. EDITAR / ELIMINAR REGISTROS (Opción 3)

### 6.1 Tablas Principales (Opciones 1-10)

#### Editar (Opciones 1-5)
1. **Editar Cliente:** Modificar nombre, dirección, teléfono o correo
2. **Editar Mascota:** Modificar nombre, sexo, edad, especie o raza
3. **Editar Producto:** Modificar descripción, precio o IVA
4. **Editar Cita:** Modificar estado de la cita
5. **Editar Consulta:** Modificar diagnóstico o tratamiento

**Funcionamiento general:**
- Se muestra el registro actual con sus datos
- Se pide ingresar nuevos valores (dejar en blanco para mantener)
- Solo se actualizan los campos con nuevos valores

#### Eliminar (Opciones 6-10)
1. **Eliminar Cliente** (Opción 6)
2. **Eliminar Mascota** (Opción 7)
3. **Eliminar Producto** (Opción 8)
4. **Eliminar Cita** (Opción 9)
5. **Eliminar Consulta** (Opción 10)

**Funcionamiento general:**
- Se muestra el registro a eliminar
- Se pide confirmación (s/n)
- Solo se elimina si el usuario confirma

### 6.2 Tablas de Relación (Opciones 11-28)

#### Detalle de Factura (Opciones 11-13)
- **Agregar (11):** Agregar producto/servicio a una factura existente
- **Editar (12):** Modificar cantidad o precio unitario de un detalle
- **Eliminar (13):** Quitar un producto de una factura

#### Receta (Opciones 14-16)
- **Agregar (14):** Crear receta para una consulta clínica (solo si no tiene)
- **Editar (15):** Modificar indicaciones en casa
- **Eliminar (16):** Eliminar una receta

#### Atención Estética (Opciones 17-19)
- **Agregar (17):** Registrar baño o corte para una mascota
- **Editar (18):** Modificar horas u observaciones
- **Eliminar (19):** Eliminar una atención estética

#### Detalle de Medicina (Opciones 20-22)
- **Agregar (20):** Registrar stock, caducidad y presentación
- **Editar (21):** Modificar stock, caducidad o presentación
- **Eliminar (22):** Eliminar detalles de una medicina

#### Detalle de Accesorio (Opciones 23-25)
- **Agregar (23):** Registrar stock, categoría y marca
- **Editar (24):** Modificar stock, categoría o marca
- **Eliminar (25):** Eliminar detalles de un accesorio

#### Detalle de Servicio (Opciones 26-28)
- **Agregar (26):** Registrar duración y si requiere cita
- **Editar (27):** Modificar duración o requisito de cita
- **Eliminar (28):** Eliminar detalles de un servicio

#### Proveedor (Opciones 29-31)
- **Registrar (29):** Crear nuevo proveedor con ID, nombre y contacto
- **Editar (30):** Modificar nombre o contacto del proveedor
- **Eliminar (31):** Eliminar un proveedor

#### Compra de Insumo (Opciones 32-34)
- **Registrar (32):** Registrar compra de producto a proveedor
- **Editar (33):** Modificar cantidad recibida
- **Eliminar (34):** Eliminar un registro de compra

#### Examen de Laboratorio (Opciones 35-37)
- **Registrar (35):** Crear examen con tipo de muestra y resultados
- **Editar (36):** Modificar resultados o tipo de muestra
- **Eliminar (37):** Eliminar un examen

#### Reserva (Opciones 38-39)
- **Agregar (38):** Reservar servicio para una cita
- **Eliminar (39):** Eliminar una reserva

#### Producto en Consulta (Opciones 40-42)
- **Agregar (40):** Registrar producto utilizado en una consulta
- **Editar (41):** Modificar cantidad gastada
- **Eliminar (42):** Eliminar registro de producto

---

## 7. TABLAS DEL SISTEMA

### Tablas Principales
| Tabla | Descripción | Campos principales |
|-------|-------------|-------------------|
| cliente | Datos de los clientes | cédula, nombre, dirección, teléfono, correo |
| mascota | Mascotas registradas | ID, nombre, sexo, edad, especie, raza, cédula dueño |
| producto_servicio | Productos y servicios | código, descripción, precio, IVA, tipo |
| cita | Citas veterinarias | ID, fecha, estado, mascota, servicio |
| consulta | Consultas clínicas | ID, fecha, diagnóstico, tratamiento, mascota |
| factura | Facturas emitidas | N° comprobante, cédula, fecha, estado, forma pago |
| proveedor | Proveedores | ID, nombre, contacto |

### Tablas de Relación
| Tabla | Descripción | Relaciona |
|-------|-------------|-----------|
| factura_detalle | Detalles de factura | factura ↔ producto_servicio |
| receta | Recetas médicas | consulta |
| atencion_estetica | Servicios de estética | mascota |
| medicina_detalles | Detalles de medicinas | producto_servicio |
| accesorio_detalles | Detalles de accesorios | producto_servicio |
| servicio_detalles | Detalles de servicios | producto_servicio |
| compra_insumo | Compras a proveedores | proveedor ↔ producto_servicio |
| examen_lab | Exámenes de laboratorio | consulta ↔ proveedor |
| reserva | Reservas de servicios | cita ↔ producto_servicio |
| consulta_producto | Productos en consultas | consulta ↔ producto_servicio |

---

## 8. CONSEJOS DE USO

1. **Guardar regularmente:** El sistema guarda automáticamente cada registro
2. **Verificar existencia:** Antes de crear citas o facturas, verifique que existan los registros relacionados
3. **Confirmar eliminaciones:** Siempre se pide confirmación antes de eliminar
4. **Campos obligatorios:** Los marcados con (obligatorio) no pueden quedar vacíos
5. **Códigos de producto:** Use el formato establecido (SERV-001, MED-001, ACC-001)
6. **Navegación:** Use "fin" para terminar de agregar productos en una factura
7. **Voltar:** La opción "Volver" regresa al menú anterior

---

## 9. SOLUCIÓN DE PROBLEMAS

| Problema | Solución |
|----------|----------|
| "Error: Variables SUPABASE_URL y SUPABASE_KEY no configuradas" | Verificar que el archivo `.env` existe y tiene las credenciales correctas |
| "Error al conectar con Supabase" | Verificar conexión a internet |
| "Ya existe un registro con..." | Usar otro identificador (cédula, código, etc.) |
| "No existe..." | Verificar que el registro esté creado en la base de datos |
| "Ingrese un número válido" | Ingresar solo números en los campos numéricos |

---

## 10. INFORMACIÓN TÉCNICA

- **Lenguaje:** Python 3.12
- **Base de datos:** Supabase (PostgreSQL en la nube)
- **Cliente Supabase:** supabase-py v2.31.0
- **Variables de entorno:** python-dotenv
- **Arquitectura:** CLI (interfaz de línea de comandos)
