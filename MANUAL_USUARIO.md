# Manual de Usuario - Sistema Veterinario

## Instalacion

```bash
pip install -r requirements.txt
```

Crear archivo `.env` con las credenciales de Supabase (ver `.env.example`).

Ejecutar:
```bash
python main.py
```

---

## Menu Principal

```
1. Reportes Gerenciales
2. Registros (Crear)
3. Editar / Eliminar
4. Salir
```

**En cualquier campo de entrada** puede escribir `cancelar` para volver al menu anterior.

---

## 1. Reportes

| Opcion | Descripcion |
|--------|-------------|
| 1 | Ventas del dia |
| 2 | Agenda de banos |
| 3 | Alerta de stock bajo |
| 4 | Historial clinico (buscar por nombre o cedula) |

---

## 2. Registros (Crear datos)

### Tablas Principales
| Opcion | Tabla | Campos obligatorios |
|--------|-------|---------------------|
| 1 | Cliente | Cedula, Nombre |
| 2 | Mascota | Nombre, Sexo (M/H), Fecha nacimiento, Especie, Raza, Cedula dueño |
| 3 | Producto/Servicio | Codigo (MED-/ACC-/SER-), Descripcion, Precio, IVA |
| 4 | Cita | Mascota, Servicio, Estado, Hora |
| 5 | Consulta | Mascota, Diagnostico, Tratamiento |
| 6 | Factura | Cliente, Estado pago, Forma pago, Productos |
| 7 | Proveedor | ID, Nombre, Contacto |

### Tablas de Relacion
| Opcion | Tabla | Que hace |
|--------|-------|----------|
| 1 | Detalle Factura | Agregar producto a factura existente |
| 2 | Receta | Crear receta para una consulta |
| 3 | Atencion Estetica | Registrar bano/corte |
| 4 | Medicina | Agregar stock a medicina existente |
| 5 | Accesorio | Agregar stock a accesorio existente |
| 6 | Servicio | Configurar duracion y si requiere cita |
| 7 | Reserva | Reservar servicio para una cita |

### Tablas Administrativas
| Opcion | Tabla | Que hace |
|--------|-------|----------|
| 1 | Compra Insumo | Registrar compra a proveedor |
| 2 | Examen Lab | Registrar examen con resultados |
| 3 | Consulta Producto | Asociar producto a una consulta |

---

## 3. Editar / Eliminar

### Como funciona
1. Selecciona la categoria (Principal, Relacion, Administrativa)
2. Selecciona la tabla
3. Elige: **Editar** o **Eliminar**
4. Selecciona el registro por ID
5. **Editar:** Ingresa nuevos valores (deja en blanco para mantener)
6. **Eliminar:** Confirma con `s`

### Cancelar operacion
En cualquier momento escriba `cancelar`, `c` o `salir`.

---

## Codigos de Producto

| Prefijo | Tipo | Ejemplo |
|---------|------|---------|
| MED- | Medicina | MED-001 |
| ACC- | Accesorio | ACC-001 |
| SER- | Servicio | SER-001 |

---

## Errores Comunes

| Error | Solucion |
|-------|----------|
| "Error al conectar" | Verificar internet y archivo `.env` |
| "Ya existe un registro" | Usar otro identificador |
| "No existe..." | Crear el registro primero |
| "Ingrese un numero valido" | Solo numeros en campos numericos |
