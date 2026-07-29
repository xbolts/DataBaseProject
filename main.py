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
        print("  3. Salir")
        separador()

        opcion = input("  Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            print()
            menu_reportes()
        elif opcion == "2":
            print()
            menu_registros()
        elif opcion == "3":
            print("\n  Saliendo del sistema...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-3).")

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
