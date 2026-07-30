import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import date

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

if not URL or not KEY:
    print("Error: Variables SUPABASE_URL y SUPABASE_KEY no configuradas.")
    print("Crea un archivo .env con tus credenciales. Ver .env.example")
    exit(1)

supabase: Client = create_client(URL, KEY)


def separador():
    print("-" * 56)


def titulo(texto):
    separador()
    print(f"  {texto}")
    separador()


def _input_no_vacio(msg):
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        print("  Este campo es obligatorio. Intente de nuevo.")


def _input_numero(msg, tipo=int):
    while True:
        valor = input(msg).strip()
        try:
            return tipo(valor)
        except (ValueError, TypeError):
            print(f"  Ingrese un número válido ({tipo.__name__}).")


def _seleccionar_registro(tabla, campos_mostrar, msg="Seleccione el ID: "):
    try:
        resp = supabase.table(tabla).select("*").execute()
        registros = resp.data
    except Exception as e:
        print(f"  Error al cargar {tabla}: {e}")
        return None

    if not registros:
        print(f"  No hay registros en {tabla}.")
        return None

    print()
    for r in registros:
        partes = [str(r.get(c, "")) for c in campos_mostrar]
        print(f"  ID: {r.get(campos_mostrar[0], '')}  |  {'  |  '.join(partes)}")

    return _input_numero(f"\n  {msg}")


# ===================== FUNCIONES DE INSERCIÓN =====================


def registrar_cliente():
    titulo("REGISTRAR CLIENTE")
    cedula = _input_no_vacio("  Cédula: ")
    nombre = _input_no_vacio("  Nombre completo: ")
    direccion = input("  Dirección: ").strip()
    telefono = input("  Teléfono: ").strip()
    correo = input("  Correo electrónico: ").strip()

    # Verificar si ya existe
    try:
        existe = supabase.table("cliente").select("*").eq("cedula", cedula).execute()
        if existe.data:
            print(f"\n  Error: Ya existe un cliente con cédula {cedula}.")
            return
    except Exception:
        pass

    cliente = {
        "cedula": cedula,
        "nombre": nombre,
        "direccion": direccion or None,
        "telefono": telefono or None,
        "correo": correo or None,
    }

    try:
        supabase.table("cliente").insert(cliente).execute()
        print(f"\n  Cliente '{nombre}' registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar cliente: {e}")


def registrar_mascota():
    titulo("REGISTRAR MASCOTA")

    nombre = _input_no_vacio("  Nombre de la mascota: ")

    sexo = ""
    while sexo not in ("M", "F"):
        sexo = input("  Sexo (M/F): ").strip().upper()
        if sexo not in ("M", "F"):
            print("  Ingrese 'M' o 'F'.")

    edad = _input_numero("  Edad (años): ")
    especie = _input_no_vacio("  Especie (Perro, Gato, etc.): ")
    raza = _input_no_vacio("  Raza: ")

    # Seleccionar dueño (cliente)
    print("\n  --- Clientes disponibles ---")
    try:
        resp_cli = supabase.table("cliente").select("*").execute()
        for c in resp_cli.data:
            print(f"  {c['cedula']}  |  {c.get('nombre', 'N/A')}")
    except Exception:
        pass

    cedula = _input_no_vacio("  Cédula del dueño: ")

    # Verificar que el cliente existe
    try:
        existe = supabase.table("cliente").select("*").eq("cedula", cedula).execute()
        if not existe.data:
            print(f"\n  Error: No existe un cliente con cédula {cedula}.")
            return
    except Exception:
        pass

    # Obtener el siguiente ID disponible
    try:
        resp = supabase.table("mascota").select("idmascota").order("idmascota", desc=True).execute()
        max_id = resp.data[0]["idmascota"] if resp.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    mascota = {
        "idmascota": nuevo_id,
        "nombre": nombre,
        "sexo": sexo,
        "edad": edad,
        "especie": especie,
        "raza": raza,
        "cedula": cedula,
    }

    try:
        supabase.table("mascota").insert(mascota).execute()
        print(f"\n  Mascota '{nombre}' ({especie} - {raza}) registrada con ID {nuevo_id} (Dueño: {cedula}).")
    except Exception as e:
        print(f"\n  Error al registrar mascota: {e}")


def registrar_producto():
    titulo("REGISTRAR PRODUCTO / SERVICIO")

    codigo = _input_no_vacio("  Código (ej: SERV-004, MED-004, ACC-005): ")
    descripcion = _input_no_vacio("  Descripción: ")

    tipo = ""
    while tipo not in ("Servicio", "Medicina", "Accesorio"):
        tipo = input("  Tipo (Servicio/Medicina/Accesorio): ").strip().capitalize()
        if tipo not in ("Servicio", "Medicina", "Accesorio"):
            print("  Opciones válidas: Servicio, Medicina, Accesorio.")

    precio = _input_numero("  Precio: ", float)
    tipo_iva = _input_numero("  Tipo IVA (%): ", float)

    # Verificar si ya existe
    try:
        existe = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", codigo).execute()
        if existe.data:
            print(f"\n  Error: Ya existe un producto con código {codigo}.")
            return
    except Exception:
        pass

    producto = {
        "codigo_producto_servicio": codigo,
        "descripcion": descripcion,
        "precio": precio,
        "tipo_iva": tipo_iva,
        "tipo": tipo,
    }

    try:
        supabase.table("producto_servicio").insert(producto).execute()
        print(f"\n  Producto '{descripcion}' registrado exitosamente.")

        # Registrar detalles según el tipo
        if tipo == "Medicina":
            stock = _input_numero("  Stock disponible: ")
            cad = input("  Fecha de caducidad (YYYY-MM-DD): ").strip()
            pres = input("  Presentación: ").strip()
            supabase.table("medicina_detalles").insert({
                "codigo_producto_servicio": codigo,
                "stock_disponible": stock,
                "fecha_caducidad": cad or None,
                "presentacion": pres or None,
            }).execute()
            print("  Detalles de medicina registrados.")

        elif tipo == "Accesorio":
            stock = _input_numero("  Stock disponible: ")
            cat = input("  Categoría: ").strip()
            mar = input("  Marca: ").strip()
            supabase.table("accesorio_detalles").insert({
                "codigo_producto_servicio": codigo,
                "stock_disponible": stock,
                "categoria": cat or None,
                "marca": mar or None,
            }).execute()
            print("  Detalles de accesorio registrados.")

        elif tipo == "Servicio":
            duracion = _input_numero("  Duración estimada (minutos): ")
            requiere = input("  ¿Requiere cita? (s/n): ").strip().lower() == "s"
            supabase.table("servicio_detalles").insert({
                "codigo_producto_servicio": codigo,
                "duracion_estimada": duracion,
                "requiere_cita": requiere,
            }).execute()
            print("  Detalles de servicio registrados.")

    except Exception as e:
        print(f"\n  Error al registrar producto: {e}")


def registrar_cita():
    titulo("REGISTRAR CITA")

    # Seleccionar mascota
    print("\n  --- Mascotas disponibles ---")
    id_mascota = _seleccionar_registro("mascota", ["idmascota", "especie", "raza"], "ID de la mascota: ")
    if id_mascota is None:
        return

    # Seleccionar servicio
    print("\n  --- Servicios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").eq("tipo", "Servicio").execute()
        servicios = resp.data
    except Exception as e:
        print(f"  Error al cargar servicios: {e}")
        return

    if not servicios:
        print("  No hay servicios registrados.")
        return

    for s in servicios:
        print(f"  {s['codigo_producto_servicio']}  |  {s['descripcion']}  |  ${s.get('precio', 0)}")

    cod_servicio = _input_no_vacio("  Código del servicio: ")

    # Verificar que el servicio existe
    if not any(s["codigo_producto_servicio"] == cod_servicio for s in servicios):
        print(f"\n  Error: El servicio {cod_servicio} no existe.")
        return

    # Estado
    estado = ""
    while estado not in ("Programada", "En progreso", "Finalizada", "Cancelada"):
        estado = input("  Estado (Programada/En progreso/Finalizada/Cancelada): ").strip().capitalize()
        if estado not in ("Programada", "En progreso", "Finalizada", "Cancelada"):
            print("  Opciones válidas: Programada, En progreso, Finalizada, Cancelada.")

    # Obtener siguiente ID
    try:
        resp = supabase.table("cita").select("idcita").order("idcita", desc=True).execute()
        max_id = resp.data[0]["idcita"] if resp.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    cita = {
        "idcita": nuevo_id,
        "idmascota": id_mascota,
        "codigo_producto_servicio": cod_servicio,
        "estado": estado,
    }

    try:
        supabase.table("cita").insert(cita).execute()
        print(f"\n  Cita {nuevo_id} registrada exitosamente (Mascota {id_mascota} - {cod_servicio}).")
    except Exception as e:
        print(f"\n  Error al registrar cita: {e}")


def registrar_consulta():
    titulo("REGISTRAR CONSULTA CLÍNICA")

    # Seleccionar mascota
    print("\n  --- Mascotas disponibles ---")
    id_mascota = _seleccionar_registro("mascota", ["idmascota", "especie", "raza"], "ID de la mascota: ")
    if id_mascota is None:
        return

    diagnostico = _input_no_vacio("  Diagnóstico: ")
    tratamiento = _input_no_vacio("  Tratamiento clínico: ")

    # Obtener siguiente ID
    try:
        resp = supabase.table("consulta").select("id_consulta").order("id_consulta", desc=True).execute()
        max_id = resp.data[0]["id_consulta"] if resp.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    consulta = {
        "id_consulta": nuevo_id,
        "diagnostico": diagnostico,
        "tratamiento_clinico": tratamiento,
        "idmascota": id_mascota,
    }

    try:
        supabase.table("consulta").insert(consulta).execute()
        print(f"\n  Consulta {nuevo_id} registrada exitosamente (Mascota {id_mascota}).")
    except Exception as e:
        print(f"\n  Error al registrar consulta: {e}")


def registrar_factura():
    titulo("REGISTRAR FACTURA")

    # Seleccionar cliente
    print("\n  --- Clientes disponibles ---")
    resp_cli = supabase.table("cliente").select("*").execute()
    if not resp_cli.data:
        print("  No hay clientes registrados. Registre uno primero.")
        return

    for c in resp_cli.data:
        print(f"  {c['cedula']}  |  {c.get('nombre', 'N/A')}")

    cedula = _input_no_vacio("  Cédula del cliente: ")

    if not any(cl["cedula"] == cedula for cl in resp_cli.data):
        print(f"\n  Error: No existe un cliente con cédula {cedula}.")
        return

    # Estado y forma de pago
    estado_pago = ""
    while estado_pago not in ("Pagado", "Pendiente", "Anulado"):
        estado_pago = input("  Estado de pago (Pagado/Pendiente/Anulado): ").strip().capitalize()
        if estado_pago not in ("Pagado", "Pendiente", "Anulado"):
            print("  Opciones válidas: Pagado, Pendiente, Anulado.")

    forma_pago = ""
    while forma_pago not in ("Efectivo", "Tarjeta", "Transferencia", "Ninguna"):
        forma_pago = input("  Forma de pago (Efectivo/Tarjeta/Transferencia/Ninguna): ").strip().capitalize()
        if forma_pago not in ("Efectivo", "Tarjeta", "Transferencia", "Ninguna"):
            print("  Opciones válidas: Efectivo, Tarjeta, Transferencia, Ninguna.")

    # Obtener siguiente ID de comprobante
    try:
        resp = supabase.table("factura").select("num_comprobante").order("num_comprobante", desc=True).execute()
        max_id = resp.data[0]["num_comprobante"] if resp.data else 0
        nuevo_num = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener número de comprobante: {e}")
        return

    # Agregar detalles de productos
    detalles = []
    print("\n  --- Agregar productos/servicios a la factura ---")
    print("  (Escriba 'fin' en el código del producto para terminar)\n")

    while True:
        cod = input("  Código del producto/servicio (o 'fin'): ").strip()
        if cod.lower() == "fin":
            break

        # Verificar que existe
        try:
            resp_prod = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", cod).execute()
            if not resp_prod.data:
                print(f"  Error: No existe producto con código {cod}.")
                continue
        except Exception:
            print(f"  Error al verificar producto {cod}.")
            continue

        prod = resp_prod.data[0]
        print(f"    -> {prod['descripcion']} (${prod.get('precio', 0)})")

        cantidad = _input_numero("    Cantidad: ")

        precio_unitario = float(prod.get("precio", 0))
        subtotal = round(precio_unitario * cantidad, 2)

        detalles.append({
            "codigo_producto_servicio": cod,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal,
        })
        print(f"    Agregado: {cantidad} x ${precio_unitario} = ${subtotal}")

    if not detalles:
        print("\n  No se agregaron productos. Factura cancelada.")
        return

    # Mostrar resumen
    total = sum(d["subtotal"] for d in detalles)
    print(f"\n  --- RESUMEN FACTURA {nuevo_num} ---")
    print(f"  Cliente: {cedula}")
    print(f"  Productos: {len(detalles)}")
    print(f"  Total: ${total:,.2f}")

    confirmar = input("\n  ¿Confirmar factura? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Factura cancelada.")
        return

    # Insertar factura
    factura = {
        "num_comprobante": nuevo_num,
        "cedula": cedula,
        "estado_pago": estado_pago,
        "forma_pago": forma_pago,
    }

    try:
        supabase.table("factura").insert(factura).execute()

        # Insertar detalles
        for d in detalles:
            d["num_comprobante"] = nuevo_num
            supabase.table("factura_detalle").insert(d).execute()

        print(f"\n  Factura {nuevo_num} registrada exitosamente. Total: ${total:,.2f}")
    except Exception as e:
        print(f"\n  Error al registrar factura: {e}")


# ===================== FUNCIONES DE EDICIÓN =====================


def editar_cliente():
    titulo("EDITAR CLIENTE")

    cedula = _input_no_vacio("  Cédula del cliente a editar: ")

    try:
        resp = supabase.table("cliente").select("*").eq("cedula", cedula).execute()
        if not resp.data:
            print(f"\n  No existe un cliente con cédula {cedula}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cliente: {e}")
        return

    cliente = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Nombre: {cliente.get('nombre', '')}")
    print(f"  Dirección: {cliente.get('direccion', '')}")
    print(f"  Teléfono: {cliente.get('telefono', '')}")
    print(f"  Correo: {cliente.get('correo', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    nombre = input(f"  Nombre [{cliente.get('nombre', '')}]: ").strip()
    direccion = input(f"  Dirección [{cliente.get('direccion', '')}]: ").strip()
    telefono = input(f"  Teléfono [{cliente.get('telefono', '')}]: ").strip()
    correo = input(f"  Correo [{cliente.get('correo', '')}]: ").strip()

    datos = {}
    if nombre:
        datos["nombre"] = nombre
    if direccion:
        datos["direccion"] = direccion
    if telefono:
        datos["telefono"] = telefono
    if correo:
        datos["correo"] = correo

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("cliente").update(datos).eq("cedula", cedula).execute()
        print(f"\n  Cliente {cedula} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar cliente: {e}")


def editar_mascota():
    titulo("EDITAR MASCOTA")

    print("\n  --- Mascotas disponibles ---")
    id_mascota = _seleccionar_registro("mascota", ["idmascota", "nombre", "especie"], "ID de la mascota: ")
    if id_mascota is None:
        return

    try:
        resp = supabase.table("mascota").select("*").eq("idmascota", id_mascota).execute()
        if not resp.data:
            print(f"\n  No existe una mascota con ID {id_mascota}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar mascota: {e}")
        return

    mascota = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Nombre: {mascota.get('nombre', '')}")
    print(f"  Sexo: {mascota.get('sexo', '')}")
    print(f"  Edad: {mascota.get('edad', '')}")
    print(f"  Especie: {mascota.get('especie', '')}")
    print(f"  Raza: {mascota.get('raza', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    nombre = input(f"  Nombre [{mascota.get('nombre', '')}]: ").strip()
    sexo = input(f"  Sexo [{mascota.get('sexo', '')}]: ").strip().upper()
    edad = input(f"  Edad [{mascota.get('edad', '')}]: ").strip()
    especie = input(f"  Especie [{mascota.get('especie', '')}]: ").strip()
    raza = input(f"  Raza [{mascota.get('raza', '')}]: ").strip()

    datos = {}
    if nombre:
        datos["nombre"] = nombre
    if sexo and sexo in ("M", "F"):
        datos["sexo"] = sexo
    if edad:
        try:
            datos["edad"] = int(edad)
        except ValueError:
            print("  Edad inválida, se mantendrá la anterior.")
    if especie:
        datos["especie"] = especie
    if raza:
        datos["raza"] = raza

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("mascota").update(datos).eq("idmascota", id_mascota).execute()
        print(f"\n  Mascota {id_mascota} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar mascota: {e}")


def editar_producto():
    titulo("EDITAR PRODUCTO / SERVICIO")

    codigo = _input_no_vacio("  Código del producto a editar: ")

    try:
        resp = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", codigo).execute()
        if not resp.data:
            print(f"\n  No existe un producto con código {codigo}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar producto: {e}")
        return

    prod = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Descripción: {prod.get('descripcion', '')}")
    print(f"  Precio: ${prod.get('precio', 0)}")
    print(f"  Tipo IVA: {prod.get('tipo_iva', '')}%")
    print(f"  Tipo: {prod.get('tipo', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    descripcion = input(f"  Descripción [{prod.get('descripcion', '')}]: ").strip()
    precio = input(f"  Precio [{prod.get('precio', 0)}]: ").strip()
    tipo_iva = input(f"  Tipo IVA [{prod.get('tipo_iva', '')}]: ").strip()

    datos = {}
    if descripcion:
        datos["descripcion"] = descripcion
    if precio:
        try:
            datos["precio"] = float(precio)
        except ValueError:
            print("  Precio inválido, se mantendrá el anterior.")
    if tipo_iva:
        try:
            datos["tipo_iva"] = float(tipo_iva)
        except ValueError:
            print("  IVA inválido, se mantendrá el anterior.")

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("producto_servicio").update(datos).eq("codigo_producto_servicio", codigo).execute()
        print(f"\n  Producto {codigo} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar producto: {e}")


def editar_cita():
    titulo("EDITAR CITA")

    print("\n  --- Citas disponibles ---")
    try:
        resp = supabase.table("cita").select("*").execute()
        citas = resp.data
    except Exception as e:
        print(f"  Error al cargar citas: {e}")
        return

    if not citas:
        print("  No hay citas registradas.")
        return

    for c in citas:
        print(f"  ID: {c['idcita']}  |  Mascota: {c.get('idmascota', '')}  |  Servicio: {c.get('codigo_producto_servicio', '')}  |  Estado: {c.get('estado', '')}")

    id_cita = _input_numero("\n  ID de la cita a editar: ")

    try:
        resp = supabase.table("cita").select("*").eq("idcita", id_cita).execute()
        if not resp.data:
            print(f"\n  No existe una cita con ID {id_cita}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cita: {e}")
        return

    cita = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Mascota: {cita.get('idmascota', '')}")
    print(f"  Servicio: {cita.get('codigo_producto_servicio', '')}")
    print(f"  Estado: {cita.get('estado', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    print(f"  Estado actual: {cita.get('estado', '')}")
    print("  Opciones: Programada, En progreso, Finalizada, Cancelada")
    estado = input("  Nuevo estado: ").strip().capitalize()

    datos = {}
    if estado and estado in ("Programada", "En progreso", "Finalizada", "Cancelada"):
        datos["estado"] = estado
    elif estado:
        print("  Estado inválido, se mantendrá el anterior.")

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("cita").update(datos).eq("idcita", id_cita).execute()
        print(f"\n  Cita {id_cita} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar cita: {e}")


def editar_consulta():
    titulo("EDITAR CONSULTA CLÍNICA")

    print("\n  --- Consultas disponibles ---")
    try:
        resp = supabase.table("consulta").select("*").execute()
        consultas = resp.data
    except Exception as e:
        print(f"  Error al cargar consultas: {e}")
        return

    if not consultas:
        print("  No hay consultas registradas.")
        return

    for c in consultas:
        print(f"  ID: {c['id_consulta']}  |  Mascota: {c.get('idmascota', '')}  |  Diagnóstico: {c.get('diagnostico', '')[:30]}")

    id_consulta = _input_numero("\n  ID de la consulta a editar: ")

    try:
        resp = supabase.table("consulta").select("*").eq("id_consulta", id_consulta).execute()
        if not resp.data:
            print(f"\n  No existe una consulta con ID {id_consulta}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar consulta: {e}")
        return

    consulta = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Diagnóstico: {consulta.get('diagnostico', '')}")
    print(f"  Tratamiento: {consulta.get('tratamiento_clinico', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    diagnostico = input(f"  Diagnóstico [{consulta.get('diagnostico', '')}]: ").strip()
    tratamiento = input(f"  Tratamiento [{consulta.get('tratamiento_clinico', '')}]: ").strip()

    datos = {}
    if diagnostico:
        datos["diagnostico"] = diagnostico
    if tratamiento:
        datos["tratamiento_clinico"] = tratamiento

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("consulta").update(datos).eq("id_consulta", id_consulta).execute()
        print(f"\n  Consulta {id_consulta} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar consulta: {e}")


# ===================== FUNCIONES DE ELIMINACIÓN =====================


def eliminar_cliente():
    titulo("ELIMINAR CLIENTE")

    cedula = _input_no_vacio("  Cédula del cliente a eliminar: ")

    try:
        resp = supabase.table("cliente").select("*").eq("cedula", cedula).execute()
        if not resp.data:
            print(f"\n  No existe un cliente con cédula {cedula}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cliente: {e}")
        return

    cliente = resp.data[0]
    print(f"\n  Cliente a eliminar:")
    print(f"  Cédula: {cliente.get('cedula', '')}")
    print(f"  Nombre: {cliente.get('nombre', '')}")
    print(f"  Teléfono: {cliente.get('telefono', '')}")

    confirmar = input("\n  ¿Está seguro de eliminar este cliente? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("cliente").delete().eq("cedula", cedula).execute()
        print(f"\n  Cliente {cedula} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar cliente: {e}")


def eliminar_mascota():
    titulo("ELIMINAR MASCOTA")

    print("\n  --- Mascotas disponibles ---")
    id_mascota = _seleccionar_registro("mascota", ["idmascota", "nombre", "especie"], "ID de la mascota: ")
    if id_mascota is None:
        return

    try:
        resp = supabase.table("mascota").select("*").eq("idmascota", id_mascota).execute()
        if not resp.data:
            print(f"\n  No existe una mascota con ID {id_mascota}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar mascota: {e}")
        return

    mascota = resp.data[0]
    print(f"\n  Mascota a eliminar:")
    print(f"  ID: {mascota.get('idmascota', '')}")
    print(f"  Nombre: {mascota.get('nombre', '')}")
    print(f"  Especie: {mascota.get('especie', '')}")
    print(f"  Raza: {mascota.get('raza', '')}")

    confirmar = input("\n  ¿Está seguro de eliminar esta mascota? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("mascota").delete().eq("idmascota", id_mascota).execute()
        print(f"\n  Mascota {id_mascota} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar mascota: {e}")


def eliminar_producto():
    titulo("ELIMINAR PRODUCTO / SERVICIO")

    codigo = _input_no_vacio("  Código del producto a eliminar: ")

    try:
        resp = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", codigo).execute()
        if not resp.data:
            print(f"\n  No existe un producto con código {codigo}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar producto: {e}")
        return

    prod = resp.data[0]
    print(f"\n  Producto a eliminar:")
    print(f"  Código: {prod.get('codigo_producto_servicio', '')}")
    print(f"  Descripción: {prod.get('descripcion', '')}")
    print(f"  Tipo: {prod.get('tipo', '')}")
    print(f"  Precio: ${prod.get('precio', 0)}")

    confirmar = input("\n  ¿Está seguro de eliminar este producto? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("producto_servicio").delete().eq("codigo_producto_servicio", codigo).execute()
        print(f"\n  Producto {codigo} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar producto: {e}")


def eliminar_cita():
    titulo("ELIMINAR CITA")

    print("\n  --- Citas disponibles ---")
    try:
        resp = supabase.table("cita").select("*").execute()
        citas = resp.data
    except Exception as e:
        print(f"  Error al cargar citas: {e}")
        return

    if not citas:
        print("  No hay citas registradas.")
        return

    for c in citas:
        print(f"  ID: {c['idcita']}  |  Mascota: {c.get('idmascota', '')}  |  Servicio: {c.get('codigo_producto_servicio', '')}  |  Estado: {c.get('estado', '')}")

    id_cita = _input_numero("\n  ID de la cita a eliminar: ")

    try:
        resp = supabase.table("cita").select("*").eq("idcita", id_cita).execute()
        if not resp.data:
            print(f"\n  No existe una cita con ID {id_cita}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cita: {e}")
        return

    cita = resp.data[0]
    print(f"\n  Cita a eliminar:")
    print(f"  ID: {cita.get('idcita', '')}")
    print(f"  Mascota: {cita.get('idmascota', '')}")
    print(f"  Servicio: {cita.get('codigo_producto_servicio', '')}")
    print(f"  Estado: {cita.get('estado', '')}")

    confirmar = input("\n  ¿Está seguro de eliminar esta cita? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("cita").delete().eq("idcita", id_cita).execute()
        print(f"\n  Cita {id_cita} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar cita: {e}")


def eliminar_consulta():
    titulo("ELIMINAR CONSULTA CLÍNICA")

    print("\n  --- Consultas disponibles ---")
    try:
        resp = supabase.table("consulta").select("*").execute()
        consultas = resp.data
    except Exception as e:
        print(f"  Error al cargar consultas: {e}")
        return

    if not consultas:
        print("  No hay consultas registradas.")
        return

    for c in consultas:
        print(f"  ID: {c['id_consulta']}  |  Mascota: {c.get('idmascota', '')}  |  Diagnóstico: {c.get('diagnostico', '')[:30]}")

    id_consulta = _input_numero("\n  ID de la consulta a eliminar: ")

    try:
        resp = supabase.table("consulta").select("*").eq("id_consulta", id_consulta).execute()
        if not resp.data:
            print(f"\n  No existe una consulta con ID {id_consulta}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar consulta: {e}")
        return

    consulta = resp.data[0]
    print(f"\n  Consulta a eliminar:")
    print(f"  ID: {consulta.get('id_consulta', '')}")
    print(f"  Mascota: {consulta.get('idmascota', '')}")
    print(f"  Diagnóstico: {consulta.get('diagnostico', '')}")

    confirmar = input("\n  ¿Está seguro de eliminar esta consulta? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("consulta").delete().eq("id_consulta", id_consulta).execute()
        print(f"\n  Consulta {id_consulta} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar consulta: {e}")


# ===================== CRUD TABLAS DE RELACIÓN =====================


# ---------- FACTURA_DETALLE ----------


def agregar_detalle_factura():
    titulo("AGREGAR DETALLE A FACTURA")

    try:
        resp = supabase.table("factura").select("*").execute()
        if not resp.data:
            print("  No hay facturas registradas.")
            return
        print("\n  --- Facturas disponibles ---")
        for f in resp.data:
            print(f"  N° {f['num_comprobante']}  |  Cliente: {f.get('cedula', '')}  |  Estado: {f.get('estado_pago', '')}")
    except Exception as e:
        print(f"  Error al cargar facturas: {e}")
        return

    num_comp = _input_numero("  N° de comprobante: ")

    try:
        resp = supabase.table("factura").select("*").eq("num_comprobante", num_comp).execute()
        if not resp.data:
            print(f"\n  No existe factura con N° {num_comp}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar factura: {e}")
        return

    print("\n  --- Productos/Servicios disponibles ---")
    try:
        resp_prod = supabase.table("producto_servicio").select("*").execute()
        for p in resp_prod.data:
            print(f"  {p['codigo_producto_servicio']}  |  {p.get('descripcion', '')}  |  ${p.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar productos: {e}")
        return

    cod = _input_no_vacio("  Código del producto: ")

    try:
        resp_p = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp_p.data:
            print(f"\n  No existe producto con código {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al verificar producto: {e}")
        return

    prod = resp_p.data[0]
    print(f"  -> {prod['descripcion']} (${prod.get('precio', 0)})")

    cantidad = _input_numero("  Cantidad: ")
    precio_unitario = float(prod.get("precio", 0))
    subtotal = round(precio_unitario * cantidad, 2)

    detalle = {
        "num_comprobante": num_comp,
        "codigo_producto_servicio": cod,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "subtotal": subtotal,
    }

    try:
        supabase.table("factura_detalle").insert(detalle).execute()
        print(f"\n  Detalle agregado: {cantidad} x ${precio_unitario} = ${subtotal}")
    except Exception as e:
        print(f"\n  Error al agregar detalle: {e}")


def editar_detalle_factura():
    titulo("EDITAR DETALLE DE FACTURA")

    num_comp = _input_numero("  N° de comprobante: ")

    try:
        resp = supabase.table("factura_detalle").select("*").eq("num_comprobante", num_comp).execute()
        if not resp.data:
            print(f"\n  No hay detalles para la factura {num_comp}.")
            return
        print(f"\n  --- Detalles de factura {num_comp} ---")
        for d in resp.data:
            print(f"  Producto: {d.get('codigo_producto_servicio', '')}  |  Cant: {d.get('cantidad', 0)}  |  Subtotal: ${d.get('subtotal', 0)}")
    except Exception as e:
        print(f"\n  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del producto a editar: ")

    try:
        resp = supabase.table("factura_detalle").select("*").eq("num_comprobante", num_comp).eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para producto {cod} en factura {num_comp}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Cantidad: {det.get('cantidad', 0)}")
    print(f"  Precio unitario: ${det.get('precio_unitario', 0)}")

    cantidad = input(f"\n  Nueva cantidad [{det.get('cantidad', 0)}]: ").strip()
    precio = input(f"  Nuevo precio unitario [{det.get('precio_unitario', 0)}]: ").strip()

    datos = {}
    if cantidad:
        try:
            datos["cantidad"] = int(cantidad)
        except ValueError:
            print("  Cantidad inválida.")
    if precio:
        try:
            datos["precio_unitario"] = float(precio)
        except ValueError:
            print("  Precio inválido.")

    if "cantidad" in datos or "precio_unitario" in datos:
        cant = datos.get("cantidad", det.get("cantidad", 0))
        prec = datos.get("precio_unitario", det.get("precio_unitario", 0))
        datos["subtotal"] = round(cant * prec, 2)

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("factura_detalle").update(datos).eq("num_comprobante", num_comp).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar detalle: {e}")


def eliminar_detalle_factura():
    titulo("ELIMINAR DETALLE DE FACTURA")

    num_comp = _input_numero("  N° de comprobante: ")

    try:
        resp = supabase.table("factura_detalle").select("*").eq("num_comprobante", num_comp).execute()
        if not resp.data:
            print(f"\n  No hay detalles para la factura {num_comp}.")
            return
        print(f"\n  --- Detalles de factura {num_comp} ---")
        for d in resp.data:
            print(f"  Producto: {d.get('codigo_producto_servicio', '')}  |  Cant: {d.get('cantidad', 0)}  |  Subtotal: ${d.get('subtotal', 0)}")
    except Exception as e:
        print(f"\n  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del producto a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar detalle {cod} de factura {num_comp}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("factura_detalle").delete().eq("num_comprobante", num_comp).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")


# ---------- RECETA ----------


def agregar_receta():
    titulo("AGREGAR RECETA")

    print("\n  --- Consultas disponibles ---")
    try:
        resp = supabase.table("consulta").select("*").execute()
        if not resp.data:
            print("  No hay consultas registradas.")
            return
        for c in resp.data:
            print(f"  ID: {c['id_consulta']}  |  Mascota: {c.get('idmascota', '')}  |  Diagnóstico: {c.get('diagnostico', '')[:30]}")
    except Exception as e:
        print(f"  Error al cargar consultas: {e}")
        return

    id_consulta = _input_numero("  ID de la consulta: ")

    try:
        resp = supabase.table("consulta").select("*").eq("id_consulta", id_consulta).execute()
        if not resp.data:
            print(f"\n  No existe consulta con ID {id_consulta}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar consulta: {e}")
        return

    try:
        resp_rec = supabase.table("receta").select("*").eq("id_consulta", id_consulta).execute()
        if resp_rec.data:
            print(f"\n  Esta consulta ya tiene una receta (ID: {resp_rec.data[0].get('id_receta', '')}).")
            return
    except Exception:
        pass

    indicaciones = _input_no_vacio("  Indicaciones en casa: ")

    try:
        resp_max = supabase.table("receta").select("id_receta").order("id_receta", desc=True).execute()
        max_id = resp_max.data[0]["id_receta"] if resp_max.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    receta = {
        "id_receta": nuevo_id,
        "indicaciones_en_casa": indicaciones,
        "id_consulta": id_consulta,
    }

    try:
        supabase.table("receta").insert(receta).execute()
        print(f"\n  Receta {nuevo_id} registrada para consulta {id_consulta}.")
    except Exception as e:
        print(f"\n  Error al registrar receta: {e}")


def editar_receta():
    titulo("EDITAR RECETA")

    print("\n  --- Recetas disponibles ---")
    try:
        resp = supabase.table("receta").select("*").execute()
        if not resp.data:
            print("  No hay recetas registradas.")
            return
        for r in resp.data:
            print(f"  ID: {r['id_receta']}  |  Consulta: {r.get('id_consulta', '')}  |  Indicaciones: {r.get('indicaciones_en_casa', '')[:40]}")
    except Exception as e:
        print(f"  Error al cargar recetas: {e}")
        return

    id_receta = _input_numero("  ID de la receta a editar: ")

    try:
        resp = supabase.table("receta").select("*").eq("id_receta", id_receta).execute()
        if not resp.data:
            print(f"\n  No existe receta con ID {id_receta}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar receta: {e}")
        return

    receta = resp.data[0]
    print(f"\n  Indicaciones actuales: {receta.get('indicaciones_en_casa', '')}")

    nuevas_ind = input("\n  Nuevas indicaciones (deje en blanco para mantener): ").strip()

    if not nuevas_ind:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("receta").update({"indicaciones_en_casa": nuevas_ind}).eq("id_receta", id_receta).execute()
        print(f"\n  Receta {id_receta} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar receta: {e}")


def eliminar_receta():
    titulo("ELIMINAR RECETA")

    print("\n  --- Recetas disponibles ---")
    try:
        resp = supabase.table("receta").select("*").execute()
        if not resp.data:
            print("  No hay recetas registradas.")
            return
        for r in resp.data:
            print(f"  ID: {r['id_receta']}  |  Consulta: {r.get('id_consulta', '')}  |  Indicaciones: {r.get('indicaciones_en_casa', '')[:40]}")
    except Exception as e:
        print(f"  Error al cargar recetas: {e}")
        return

    id_receta = _input_numero("  ID de la receta a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar receta {id_receta}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("receta").delete().eq("id_receta", id_receta).execute()
        print(f"\n  Receta {id_receta} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar receta: {e}")


# ---------- ATENCIÓN ESTÉTICA ----------


def agregar_atencion_estetica():
    titulo("AGREGAR ATENCIÓN ESTÉTICA")

    print("\n  --- Mascotas disponibles ---")
    try:
        resp = supabase.table("mascota").select("*").execute()
        for m in resp.data:
            print(f"  ID: {m['idmascota']}  |  {m.get('nombre', '')}  |  {m.get('especie', '')}  |  {m.get('raza', '')}")
    except Exception as e:
        print(f"  Error al cargar mascotas: {e}")
        return

    id_mascota = _input_numero("  ID de la mascota: ")

    try:
        resp = supabase.table("mascota").select("*").eq("idmascota", id_mascota).execute()
        if not resp.data:
            print(f"\n  No existe mascota con ID {id_mascota}.")
            return
    except Exception as e:
        print(f"\n  Error al verificar mascota: {e}")
        return

    hora_inicio = _input_no_vacio("  Hora de inicio (HH:MM): ")
    hora_fin = _input_no_vacio("  Hora de fin (HH:MM): ")
    observaciones = input("  Observaciones: ").strip()

    try:
        resp_max = supabase.table("atencion_estetica").select("id_peluqueria").order("id_peluqueria", desc=True).execute()
        max_id = resp_max.data[0]["id_peluqueria"] if resp_max.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    atencion = {
        "id_peluqueria": nuevo_id,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "observaciones": observaciones or None,
        "idmascota": id_mascota,
    }

    try:
        supabase.table("atencion_estetica").insert(atencion).execute()
        print(f"\n  Atención estética {nuevo_id} registrada para mascota {id_mascota}.")
    except Exception as e:
        print(f"\n  Error al registrar atención: {e}")


def editar_atencion_estetica():
    titulo("EDITAR ATENCIÓN ESTÉTICA")

    try:
        resp = supabase.table("atencion_estetica").select("*").execute()
        if not resp.data:
            print("  No hay atenciones estéticas registradas.")
            return
        for a in resp.data:
            print(f"  ID: {a['id_peluqueria']}  |  Mascota: {a.get('idmascota', '')}  |  Inicio: {a.get('hora_inicio', '')}  |  Fin: {a.get('hora_fin', '')}")
    except Exception as e:
        print(f"  Error al cargar atenciones: {e}")
        return

    id_atencion = _input_numero("  ID de la atención a editar: ")

    try:
        resp = supabase.table("atencion_estetica").select("*").eq("id_peluqueria", id_atencion).execute()
        if not resp.data:
            print(f"\n  No existe atención con ID {id_atencion}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar atención: {e}")
        return

    atencion = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Hora inicio: {atencion.get('hora_inicio', '')}")
    print(f"  Hora fin: {atencion.get('hora_fin', '')}")
    print(f"  Observaciones: {atencion.get('observaciones', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    hora_inicio = input(f"  Hora inicio [{atencion.get('hora_inicio', '')}]: ").strip()
    hora_fin = input(f"  Hora fin [{atencion.get('hora_fin', '')}]: ").strip()
    observaciones = input(f"  Observaciones [{atencion.get('observaciones', '')}]: ").strip()

    datos = {}
    if hora_inicio:
        datos["hora_inicio"] = hora_inicio
    if hora_fin:
        datos["hora_fin"] = hora_fin
    if observaciones:
        datos["observaciones"] = observaciones

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("atencion_estetica").update(datos).eq("id_peluqueria", id_atencion).execute()
        print(f"\n  Atención {id_atencion} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar atención: {e}")


def eliminar_atencion_estetica():
    titulo("ELIMINAR ATENCIÓN ESTÉTICA")

    try:
        resp = supabase.table("atencion_estetica").select("*").execute()
        if not resp.data:
            print("  No hay atenciones estéticas registradas.")
            return
        for a in resp.data:
            print(f"  ID: {a['id_peluqueria']}  |  Mascota: {a.get('idmascota', '')}  |  Inicio: {a.get('hora_inicio', '')}")
    except Exception as e:
        print(f"  Error al cargar atenciones: {e}")
        return

    id_atencion = _input_numero("  ID de la atención a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar atención {id_atencion}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("atencion_estetica").delete().eq("id_peluqueria", id_atencion).execute()
        print(f"\n  Atención {id_atencion} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar atención: {e}")


# ---------- MEDICINA_DETALLES ----------


def agregar_medicina_detalle():
    titulo("AGREGAR DETALLE DE MEDICINA")

    print("\n  --- Medicinas disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").eq("tipo", "Medicina").execute()
        if not resp.data:
            print("  No hay medicinas registradas.")
            return
        for m in resp.data:
            print(f"  {m['codigo_producto_servicio']}  |  {m.get('descripcion', '')}  |  ${m.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar medicinas: {e}")
        return

    cod = _input_no_vacio("  Código de la medicina: ")

    try:
        resp = supabase.table("medicina_detalles").select("*").eq("codigo_producto_servicio", cod).execute()
        if resp.data:
            print(f"\n  Esta medicina ya tiene detalles registrados.")
            return
    except Exception:
        pass

    stock = _input_numero("  Stock disponible: ")
    caducidad = input("  Fecha de caducidad (YYYY-MM-DD): ").strip()
    presentacion = input("  Presentación: ").strip()

    detalle = {
        "codigo_producto_servicio": cod,
        "stock_disponible": stock,
        "fecha_caducidad": caducidad or None,
        "presentacion": presentacion or None,
    }

    try:
        supabase.table("medicina_detalles").insert(detalle).execute()
        print(f"\n  Detalle de medicina {cod} registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar detalle: {e}")


def editar_medicina_detalle():
    titulo("EDITAR DETALLE DE MEDICINA")

    try:
        resp = supabase.table("medicina_detalles").select("*").execute()
        if not resp.data:
            print("  No hay detalles de medicinas registrados.")
            return
        for m in resp.data:
            print(f"  Código: {m.get('codigo_producto_servicio', '')}  |  Stock: {m.get('stock_disponible', 0)}  |  Presentación: {m.get('presentacion', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código de la medicina a editar: ")

    try:
        resp = supabase.table("medicina_detalles").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para medicina {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Stock: {det.get('stock_disponible', 0)}")
    print(f"  Caducidad: {det.get('fecha_caducidad', '')}")
    print(f"  Presentación: {det.get('presentacion', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    stock = input(f"  Stock [{det.get('stock_disponible', 0)}]: ").strip()
    caducidad = input(f"  Caducidad [{det.get('fecha_caducidad', '')}]: ").strip()
    presentacion = input(f"  Presentación [{det.get('presentacion', '')}]: ").strip()

    datos = {}
    if stock:
        try:
            datos["stock_disponible"] = int(stock)
        except ValueError:
            print("  Stock inválido.")
    if caducidad:
        datos["fecha_caducidad"] = caducidad
    if presentacion:
        datos["presentacion"] = presentacion

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("medicina_detalles").update(datos).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Medicina {cod} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar medicina: {e}")


def eliminar_medicina_detalle():
    titulo("ELIMINAR DETALLE DE MEDICINA")

    try:
        resp = supabase.table("medicina_detalles").select("*").execute()
        if not resp.data:
            print("  No hay detalles de medicinas registrados.")
            return
        for m in resp.data:
            print(f"  Código: {m.get('codigo_producto_servicio', '')}  |  Stock: {m.get('stock_disponible', 0)}  |  Presentación: {m.get('presentacion', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código de la medicina a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar detalle de medicina {cod}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("medicina_detalles").delete().eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle de medicina {cod} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")


# ---------- ACCESORIO_DETALLES ----------


def agregar_accesorio_detalle():
    titulo("AGREGAR DETALLE DE ACCESORIO")

    print("\n  --- Accesorios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").eq("tipo", "Accesorio").execute()
        if not resp.data:
            print("  No hay accesorios registrados.")
            return
        for a in resp.data:
            print(f"  {a['codigo_producto_servicio']}  |  {a.get('descripcion', '')}  |  ${a.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar accesorios: {e}")
        return

    cod = _input_no_vacio("  Código del accesorio: ")

    try:
        resp = supabase.table("accesorio_detalles").select("*").eq("codigo_producto_servicio", cod).execute()
        if resp.data:
            print(f"\n  Este accesorio ya tiene detalles registrados.")
            return
    except Exception:
        pass

    stock = _input_numero("  Stock disponible: ")
    categoria = input("  Categoría: ").strip()
    marca = input("  Marca: ").strip()

    detalle = {
        "codigo_producto_servicio": cod,
        "stock_disponible": stock,
        "categoria": categoria or None,
        "marca": marca or None,
    }

    try:
        supabase.table("accesorio_detalles").insert(detalle).execute()
        print(f"\n  Detalle de accesorio {cod} registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar detalle: {e}")


def editar_accesorio_detalle():
    titulo("EDITAR DETALLE DE ACCESORIO")

    try:
        resp = supabase.table("accesorio_detalles").select("*").execute()
        if not resp.data:
            print("  No hay detalles de accesorios registrados.")
            return
        for a in resp.data:
            print(f"  Código: {a.get('codigo_producto_servicio', '')}  |  Stock: {a.get('stock_disponible', 0)}  |  Categoría: {a.get('categoria', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del accesorio a editar: ")

    try:
        resp = supabase.table("accesorio_detalles").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para accesorio {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Stock: {det.get('stock_disponible', 0)}")
    print(f"  Categoría: {det.get('categoria', '')}")
    print(f"  Marca: {det.get('marca', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    stock = input(f"  Stock [{det.get('stock_disponible', 0)}]: ").strip()
    categoria = input(f"  Categoría [{det.get('categoria', '')}]: ").strip()
    marca = input(f"  Marca [{det.get('marca', '')}]: ").strip()

    datos = {}
    if stock:
        try:
            datos["stock_disponible"] = int(stock)
        except ValueError:
            print("  Stock inválido.")
    if categoria:
        datos["categoria"] = categoria
    if marca:
        datos["marca"] = marca

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("accesorio_detalles").update(datos).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Accesorio {cod} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar accesorio: {e}")


def eliminar_accesorio_detalle():
    titulo("ELIMINAR DETALLE DE ACCESORIO")

    try:
        resp = supabase.table("accesorio_detalles").select("*").execute()
        if not resp.data:
            print("  No hay detalles de accesorios registrados.")
            return
        for a in resp.data:
            print(f"  Código: {a.get('codigo_producto_servicio', '')}  |  Stock: {a.get('stock_disponible', 0)}  |  Categoría: {a.get('categoria', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del accesorio a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar detalle de accesorio {cod}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("accesorio_detalles").delete().eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle de accesorio {cod} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")


# ---------- SERVICIO_DETALLES ----------


def agregar_servicio_detalle():
    titulo("AGREGAR DETALLE DE SERVICIO")

    print("\n  --- Servicios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").eq("tipo", "Servicio").execute()
        if not resp.data:
            print("  No hay servicios registrados.")
            return
        for s in resp.data:
            print(f"  {s['codigo_producto_servicio']}  |  {s.get('descripcion', '')}  |  ${s.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar servicios: {e}")
        return

    cod = _input_no_vacio("  Código del servicio: ")

    try:
        resp = supabase.table("servicio_detalles").select("*").eq("codigo_producto_servicio", cod).execute()
        if resp.data:
            print(f"\n  Este servicio ya tiene detalles registrados.")
            return
    except Exception:
        pass

    duracion = _input_numero("  Duración estimada (minutos): ")
    requiere = input("  ¿Requiere cita? (s/n): ").strip().lower() == "s"

    detalle = {
        "codigo_producto_servicio": cod,
        "duracion_estimada": duracion,
        "requiere_cita": requiere,
    }

    try:
        supabase.table("servicio_detalles").insert(detalle).execute()
        print(f"\n  Detalle de servicio {cod} registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar detalle: {e}")


def editar_servicio_detalle():
    titulo("EDITAR DETALLE DE SERVICIO")

    try:
        resp = supabase.table("servicio_detalles").select("*").execute()
        if not resp.data:
            print("  No hay detalles de servicios registrados.")
            return
        for s in resp.data:
            req = "Sí" if s.get("requiere_cita") else "No"
            print(f"  Código: {s.get('codigo_producto_servicio', '')}  |  Duración: {s.get('duracion_estimada', 0)} min  |  Requiere cita: {req}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del servicio a editar: ")

    try:
        resp = supabase.table("servicio_detalles").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para servicio {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    req_actual = "Sí" if det.get("requiere_cita") else "No"
    print(f"\n  Datos actuales:")
    print(f"  Duración: {det.get('duracion_estimada', 0)} minutos")
    print(f"  Requiere cita: {req_actual}")

    duracion = input(f"\n  Nueva duración [{det.get('duracion_estimada', 0)}]: ").strip()
    requiere = input(f"  Requiere cita (s/n) [{req_actual}]: ").strip().lower()

    datos = {}
    if duracion:
        try:
            datos["duracion_estimada"] = int(duracion)
        except ValueError:
            print("  Duración inválida.")
    if requiere in ("s", "n"):
        datos["requiere_cita"] = requiere == "s"

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("servicio_detalles").update(datos).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Servicio {cod} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar servicio: {e}")


def eliminar_servicio_detalle():
    titulo("ELIMINAR DETALLE DE SERVICIO")

    try:
        resp = supabase.table("servicio_detalles").select("*").execute()
        if not resp.data:
            print("  No hay detalles de servicios registrados.")
            return
        for s in resp.data:
            req = "Sí" if s.get("requiere_cita") else "No"
            print(f"  Código: {s.get('codigo_producto_servicio', '')}  |  Duración: {s.get('duracion_estimada', 0)} min  |  Requiere cita: {req}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del servicio a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar detalle de servicio {cod}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("servicio_detalles").delete().eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle de servicio {cod} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")


# ===================== MENÚ DE EDICIÓN / ELIMINACIÓN =====================


def menu_editar_eliminar():
    while True:
        print()
        separador()
        print("    --- EDITAR / ELIMINAR REGISTROS ---")
        separador()
        print("  --- Tablas Principales ---")
        print("  1. Editar Cliente")
        print("  2. Editar Mascota")
        print("  3. Editar Producto / Servicio")
        print("  4. Editar Cita")
        print("  5. Editar Consulta Clínica")
        print("  ---")
        print("  6. Eliminar Cliente")
        print("  7. Eliminar Mascota")
        print("  8. Eliminar Producto / Servicio")
        print("  9. Eliminar Cita")
        print("  10. Eliminar Consulta Clínica")
        print("  --- Tablas de Relación ---")
        print("  11. Agregar Detalle a Factura")
        print("  12. Editar Detalle de Factura")
        print("  13. Eliminar Detalle de Factura")
        print("  ---")
        print("  14. Agregar Receta")
        print("  15. Editar Receta")
        print("  16. Eliminar Receta")
        print("  ---")
        print("  17. Agregar Atención Estética")
        print("  18. Editar Atención Estética")
        print("  19. Eliminar Atención Estética")
        print("  ---")
        print("  20. Agregar Detalle de Medicina")
        print("  21. Editar Detalle de Medicina")
        print("  22. Eliminar Detalle de Medicina")
        print("  ---")
        print("  23. Agregar Detalle de Accesorio")
        print("  24. Editar Detalle de Accesorio")
        print("  25. Eliminar Detalle de Accesorio")
        print("  ---")
        print("  26. Agregar Detalle de Servicio")
        print("  27. Editar Detalle de Servicio")
        print("  28. Eliminar Detalle de Servicio")
        print("  ---")
        print("  29. Volver")
        separador()

        opcion = input("  Seleccione una opción (1-29): ").strip()

        if opcion == "1":
            print()
            editar_cliente()
        elif opcion == "2":
            print()
            editar_mascota()
        elif opcion == "3":
            print()
            editar_producto()
        elif opcion == "4":
            print()
            editar_cita()
        elif opcion == "5":
            print()
            editar_consulta()
        elif opcion == "6":
            print()
            eliminar_cliente()
        elif opcion == "7":
            print()
            eliminar_mascota()
        elif opcion == "8":
            print()
            eliminar_producto()
        elif opcion == "9":
            print()
            eliminar_cita()
        elif opcion == "10":
            print()
            eliminar_consulta()
        elif opcion == "11":
            print()
            agregar_detalle_factura()
        elif opcion == "12":
            print()
            editar_detalle_factura()
        elif opcion == "13":
            print()
            eliminar_detalle_factura()
        elif opcion == "14":
            print()
            agregar_receta()
        elif opcion == "15":
            print()
            editar_receta()
        elif opcion == "16":
            print()
            eliminar_receta()
        elif opcion == "17":
            print()
            agregar_atencion_estetica()
        elif opcion == "18":
            print()
            editar_atencion_estetica()
        elif opcion == "19":
            print()
            eliminar_atencion_estetica()
        elif opcion == "20":
            print()
            agregar_medicina_detalle()
        elif opcion == "21":
            print()
            editar_medicina_detalle()
        elif opcion == "22":
            print()
            eliminar_medicina_detalle()
        elif opcion == "23":
            print()
            agregar_accesorio_detalle()
        elif opcion == "24":
            print()
            editar_accesorio_detalle()
        elif opcion == "25":
            print()
            eliminar_accesorio_detalle()
        elif opcion == "26":
            print()
            agregar_servicio_detalle()
        elif opcion == "27":
            print()
            editar_servicio_detalle()
        elif opcion == "28":
            print()
            eliminar_servicio_detalle()
        elif opcion == "29":
            print("\n  Volviendo al menú anterior...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-29).")

        input("\n  Presione Enter para continuar...")


# ===================== MENÚ DE REGISTROS =====================


def menu_registros():
    while True:
        print()
        separador()
        print("    --- MÓDULO DE REGISTRO DE DATOS ---")
        separador()
        print("  1. Registrar Cliente")
        print("  2. Registrar Mascota")
        print("  3. Registrar Producto / Servicio")
        print("  4. Registrar Cita")
        print("  5. Registrar Consulta Clínica")
        print("  6. Registrar Factura")
        print("  7. Volver al Menú Principal")
        separador()

        opcion = input("  Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            print()
            registrar_cliente()
        elif opcion == "2":
            print()
            registrar_mascota()
        elif opcion == "3":
            print()
            registrar_producto()
        elif opcion == "4":
            print()
            registrar_cita()
        elif opcion == "5":
            print()
            registrar_consulta()
        elif opcion == "6":
            print()
            registrar_factura()
        elif opcion == "7":
            print("\n  Volviendo al menú principal...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-7).")

        input("\n  Presione Enter para continuar...")


# ===================== FUNCIONES DE REPORTES =====================


def _mostrar_facturas(facturas, etiqueta_fecha):
    print(f"\n  Fecha: {etiqueta_fecha}")
    print(f"\n  {'N° Comp.':<12} {'Cédula':<12} {'Estado Pago':<15} {'Forma Pago':<12}")
    print(f"  {'-'*10:<12} {'-'*10:<12} {'-'*13:<15} {'-'*10:<12}")

    total_general = 0.0

    for f in facturas:
        num = f["num_comprobante"]
        cedula = f["cedula"]
        estado = f.get("estado_pago", "N/A") or "N/A"
        forma = f.get("forma_pago", "N/A") or "N/A"

        try:
            det = supabase.table("factura_detalle").select("*").eq("num_comprobante", num).execute()
            detalles = det.data
        except Exception:
            detalles = []

        total_factura = 0.0
        for d in detalles:
            subtotal = d.get("subtotal") or 0
            total_factura += float(subtotal)

        total_general += total_factura
        print(f"  {str(num):<12} {cedula:<12} {estado:<15} {forma:<12}  Total: ${total_factura:,.2f}")

    separador()
    print(f"  TOTAL: ${total_general:,.2f}")
    separador()


def reporte_ventas_dia():
    titulo("REPORTE DE VENTAS Y FACTURACIÓN DEL DÍA")
    hoy = date.today().isoformat()

    try:
        resp = supabase.table("factura").select("*").eq("fecha_emision", hoy).execute()
    except Exception as e:
        print(f"\n  Error al consultar facturas: {e}")
        return

    facturas = resp.data

    if facturas:
        _mostrar_facturas(facturas, f"Hoy ({hoy})")
        return

    print(f"\n  No existen facturas registradas el día de hoy ({hoy}).")

    try:
        resp_all = supabase.table("factura").select("*").order("fecha_emision", desc=True).execute()
    except Exception as e:
        print(f"  Error al buscar última fecha: {e}")
        return

    todas = resp_all.data
    if not todas:
        print("  No existen facturas registradas en el sistema.")
        return

    ultima_fecha = todas[0].get("fecha_emision")
    facturas_ultima = [f for f in todas if f.get("fecha_emision") == ultima_fecha]

    print(f"  Mostrando facturas de la última fecha disponible:")
    _mostrar_facturas(facturas_ultima, ultima_fecha)


def reporte_banos_programados():
    titulo("AGENDA DEL DÍA (BAÑOS PROGRAMADOS)")

    try:
        resp = supabase.table("atencion_estetica").select("*").execute()
    except Exception as e:
        print(f"\n  Error al consultar atenciones estéticas: {e}")
        return

    registros = resp.data

    if not registros:
        print("\n  No existen baños programados registrados.")
        return

    # Cargar nombres de mascotas
    nombres_mascotas = {}
    try:
        resp_m = supabase.table("mascota").select("idmascota,nombre").execute()
        for m in resp_m.data:
            nombres_mascotas[m["idmascota"]] = m.get("nombre", "N/A") or "N/A"
    except Exception:
        pass

    print(f"\n  {'ID Atención':<10} {'Mascota':<18} {'Hora Inicio':<14} {'Hora Fin':<14} {'Observaciones'}")
    print(f"  {'-'*8:<10} {'-'*16:<18} {'-'*12:<14} {'-'*12:<14} {'-'*25}")

    for r in registros:
        id_atencion = r["id_peluqueria"]
        id_mascota = r["idmascota"]
        nombre_mascota = nombres_mascotas.get(id_mascota, f"ID {id_mascota}")
        h_inicio = r.get("hora_inicio", "N/A") or "N/A"
        h_fin = r.get("hora_fin", "N/A") or "N/A"
        obs = r.get("observaciones", "") or ""

        print(f"  {str(id_atencion):<10} {nombre_mascota:<18} {h_inicio:<14} {h_fin:<14} {obs}")

    separador()
    print(f"  Total de registros: {len(registros)}")
    separador()


def reporte_alerta_stock():
    titulo("REPORTE DE NECESIDAD DE INSUMOS (ALERTA DE STOCK)")

    medicinas = []
    accesorios = []

    try:
        resp_med = supabase.table("medicina_detalles").select("*").execute()
        medicinas = resp_med.data
    except Exception as e:
        print(f"\n  Error al consultar medicinas: {e}")

    try:
        resp_acc = supabase.table("accesorio_detalles").select("*").execute()
        accesorios = resp_acc.data
    except Exception as e:
        print(f"\n  Error al consultar accesorios: {e}")

    alertas_med = [m for m in medicinas if (m.get("stock_disponible") or 0) <= 5]
    alertas_acc = [a for a in accesorios if (a.get("stock_disponible") or 0) <= 5]

    if alertas_med:
        print("\n  --- MEDICINAS CON STOCK BAJO (<= 5) ---")
        print(f"  {'Código Producto':<20} {'Stock':<10} {'Presentación':<20} {'Fecha Caducidad'}")
        print(f"  {'-'*18:<20} {'-'*6:<10} {'-'*14:<20} {'-'*16}")

        for m in alertas_med:
            cod = m["codigo_producto_servicio"]
            stock = m.get("stock_disponible", 0) or 0
            pres = m.get("presentacion", "N/A") or "N/A"
            cad = m.get("fecha_caducidad", "N/A") or "N/A"
            print(f"  {cod:<20} {str(stock):<10} {pres:<20} {cad}")

    if alertas_acc:
        print("\n  --- ACCESORIOS CON STOCK BAJO (<= 5) ---")
        print(f"  {'Código Producto':<20} {'Stock':<10} {'Categoría':<20} {'Marca'}")
        print(f"  {'-'*18:<20} {'-'*6:<10} {'-'*12:<20} {'-'*15}")

        for a in alertas_acc:
            cod = a["codigo_producto_servicio"]
            stock = a.get("stock_disponible", 0) or 0
            cat = a.get("categoria", "N/A") or "N/A"
            mar = a.get("marca", "N/A") or "N/A"
            print(f"  {cod:<20} {str(stock):<10} {cat:<20} {mar}")

    total_alertas = len(alertas_med) + len(alertas_acc)

    if total_alertas == 0:
        print("\n  No existen insumos con stock bajo (<= 5 unidades).")
        print("\n  --- RESUMEN: 5 INSUMOS CON MENOR STOCK ---")
        todos = []
        for m in medicinas:
            todos.append({
                "codigo": m["codigo_producto_servicio"],
                "stock": m.get("stock_disponible", 0) or 0,
                "detalle": m.get("presentacion", ""),
                "tipo": "Medicina",
            })
        for a in accesorios:
            todos.append({
                "codigo": a["codigo_producto_servicio"],
                "stock": a.get("stock_disponible", 0) or 0,
                "detalle": a.get("categoria", ""),
                "tipo": "Accesorio",
            })

        todos_ordenados = sorted(todos, key=lambda x: x["stock"])[:5]

        print(f"\n  {'Código':<20} {'Stock':<10} {'Tipo':<12} {'Detalle'}")
        print(f"  {'-'*18:<20} {'-'*6:<10} {'-'*10:<12} {'-'*20}")
        for item in todos_ordenados:
            print(f"  {item['codigo']:<20} {str(item['stock']):<10} {item['tipo']:<12} {item['detalle']}")

    separador()
    print(f"  Total de alertas activas: {total_alertas}")
    separador()


def reporte_historial_clinico():
    titulo("HISTORIAL CLÍNICO COMPLETO")

    busqueda = input("  Ingrese el Nombre de la Mascota o Cédula del Dueño: ").strip()
    if not busqueda:
        print("  Debe ingresar un valor de búsqueda.")
        return

    print("\n  Recopilando historial médico...")

    mascota_encontrada = None
    cliente_encontrado = None
    es_cedula = busqueda.isdigit()

    if es_cedula:
        # Buscar cliente por cédula
        try:
            resp_cli = supabase.table("cliente").select("*").eq("cedula", busqueda).execute()
            if resp_cli.data:
                cliente_encontrado = resp_cli.data[0]
        except Exception:
            pass

        # Buscar mascota(s) por cédula del dueño (FK en tabla mascota)
        try:
            resp_m = supabase.table("mascota").select("*").eq("cedula", busqueda).execute()
            mascotas_dueño = resp_m.data
        except Exception:
            mascotas_dueño = []

        if len(mascotas_dueño) == 1:
            mascota_encontrada = mascotas_dueño[0]
        elif len(mascotas_dueño) > 1:
            print(f"\n  Cliente: {cliente_encontrado.get('nombre', 'N/A') if cliente_encontrado else busqueda}")
            print("  Mascotas registradas:")
            print(f"  {'ID':<8} {'Nombre':<15} {'Especie':<12} {'Raza':<20} {'Edad'}")
            print(f"  {'-'*6:<8} {'-'*13:<15} {'-'*10:<12} {'-'*18:<20} {'-'*4}")
            for m in mascotas_dueño:
                edad = m.get("edad", "N/A") or "N/A"
                nom = m.get("nombre", "N/A") or "N/A"
                print(f"  {str(m['idmascota']):<8} {nom:<15} {m.get('especie', 'N/A'):<12} {m.get('raza', 'N/A'):<20} {edad}")
            seleccion = input("\n  Ingrese el ID de la mascota: ").strip()
            try:
                mascota_encontrada = next(
                    (m for m in mascotas_dueño if m["idmascota"] == int(seleccion)), None
                )
            except (ValueError, StopIteration):
                pass
    else:
        # Buscar mascota por nombre (búsqueda parcial)
        try:
            resp_mascotas = supabase.table("mascota").select("*").execute()
            for m in resp_mascotas.data:
                nombre_m = (m.get("nombre") or "").lower()
                especie = (m.get("especie") or "").lower()
                raza = (m.get("raza") or "").lower()
                busq = busqueda.lower()
                if busq in nombre_m or busq in especie or busq in raza:
                    mascota_encontrada = m
                    break
        except Exception:
            pass

        # Si no se encontró, intentar como ID de mascota
        if mascota_encontrada is None:
            try:
                resp_m = supabase.table("mascota").select("*").eq("idmascota", int(busqueda)).execute()
                if resp_m.data:
                    mascota_encontrada = resp_m.data[0]
            except (ValueError, Exception):
                pass

        # Obtener cliente desde la FK de mascota
        if mascota_encontrada and mascota_encontrada.get("cedula"):
            try:
                resp_cli = supabase.table("cliente").select("*").eq("cedula", mascota_encontrada["cedula"]).execute()
                if resp_cli.data:
                    cliente_encontrado = resp_cli.data[0]
            except Exception:
                pass

    if mascota_encontrada is None:
        print(f"\n  No se encontraron resultados para '{busqueda}'.")
        return

    # Obtener consultas de la mascota
    try:
        resp_cons = supabase.table("consulta").select("*").eq("idmascota", mascota_encontrada["idmascota"]).order("fecha", desc=True).execute()
        consultas = resp_cons.data
    except Exception:
        consultas = []

    # Buscar recetas asociadas a cada consulta
    recetas = {}
    for cons in consultas:
        try:
            resp_rec = supabase.table("receta").select("*").eq("id_consulta", cons["id_consulta"]).execute()
            if resp_rec.data:
                recetas[cons["id_consulta"]] = resp_rec.data[0]
        except Exception:
            pass

    # Encabezado
    separador()
    print("  HISTORIAL CLÍNICO")
    separador()

    nombre_mascota = mascota_encontrada.get("nombre", "N/A") or "N/A"
    esp = mascota_encontrada.get("especie", "N/A") or "N/A"
    edad = mascota_encontrada.get("edad", "N/A") or "N/A"
    raza = mascota_encontrada.get("raza", "N/A") or "N/A"
    sexo = mascota_encontrada.get("sexo", "N/A") or "N/A"
    print(f"\n  PACIENTE: {nombre_mascota} ({raza} {esp})    EDAD: {edad} años    SEXO: {sexo}")
    print(f"  ID MASCOTA: {mascota_encontrada['idmascota']}")

    if cliente_encontrado:
        nombre = cliente_encontrado.get("nombre", "N/A") or "N/A"
        tel = cliente_encontrado.get("telefono", "N/A") or "N/A"
        dir_ = cliente_encontrado.get("direccion", "N/A") or "N/A"
        print(f"\n  PROPIETARIO: {nombre}    CONTACTO: {tel}")
        print(f"  CÉDULA: {cliente_encontrado['cedula']}    DIRECCIÓN: {dir_}")

    separador()

    if not consultas:
        print("\n  No existen consultas registradas para esta mascota.")
        separador()
        return

    # Tabla de consultas
    print(f"\n  {'FECHA':<14} | {'DIAGNÓSTICO':<35} | {'TRATAMIENTO Y RECETA'}")
    print(f"  {'-'*12:<14}-+-{'-'*33:<35}-+-{'-'*30}")

    for c in consultas:
        fecha = c.get("fecha", "N/A") or "N/A"
        diag = c.get("diagnostico", "N/A") or "N/A"
        trat = c.get("tratamiento_clinico", "N/A") or "N/A"

        rec = recetas.get(c["id_consulta"])
        receta_texto = ""
        if rec and rec.get("indicaciones_en_casa"):
            receta_texto = f"\n  {'':14} | {'':35} | Casa: {rec['indicaciones_en_casa']}"

        diag_corto = diag[:33] + "..." if len(diag) > 35 else diag
        trat_corto = trat[:30] + "..." if len(trat) > 33 else trat

        print(f"  {fecha:<14} | {diag_corto:<35} | {trat_corto}")
        if receta_texto:
            print(receta_texto)

    separador()
    print(f"  Total de consultas: {len(consultas)}")
    separador()


# ===================== MENÚ PRINCIPAL =====================


def menu_principal():
    while True:
        print()
        separador()
        print("    --- SISTEMA VETERINARIO ---")
        separador()
        print("  1. Módulo de Reportes Gerenciales")
        print("  2. Módulo de Registro de Datos")
        print("  3. Editar / Eliminar Registros")
        print("  4. Salir")
        separador()

        opcion = input("  Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            print()
            menu_reportes()
        elif opcion == "2":
            print()
            menu_registros()
        elif opcion == "3":
            print()
            menu_editar_eliminar()
        elif opcion == "4":
            print("\n  Saliendo del sistema...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-4).")

        input("\n  Presione Enter para continuar...")


def menu_reportes():
    while True:
        print()
        separador()
        print("    --- MÓDULO DE REPORTES GERENCIALES ---")
        separador()
        print("  1. Reporte de Ventas y Facturación del Día (Caja)")
        print("  2. Agenda del Día (Baños Programados)")
        print("  3. Reporte de Necesidad de Insumos (Alerta de Stock)")
        print("  4. Historial Clínico Completo (Todas las mascotas)")
        print("  5. Volver al Menú Principal")
        separador()

        opcion = input("  Seleccione el reporte a generar (1-5): ").strip()

        if opcion == "1":
            print()
            reporte_ventas_dia()
        elif opcion == "2":
            print()
            reporte_banos_programados()
        elif opcion == "3":
            print()
            reporte_alerta_stock()
        elif opcion == "4":
            print()
            reporte_historial_clinico()
        elif opcion == "5":
            print("\n  Volviendo al menú principal...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-5).")

        input("\n  Presione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()
