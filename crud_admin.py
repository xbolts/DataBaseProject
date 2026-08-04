from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


# ===================== PROVEEDOR =====================


def registrar_proveedor():
    titulo("REGISTRAR PROVEEDOR")

    id_prov = _input_numero("  ID del proveedor: ")
    nombre = _input_no_vacio("  Nombre del proveedor: ")
    contacto = _input_no_vacio("  Contacto (teléfono): ")

    try:
        existe = supabase.table("proveedor").select("*").eq("id_proveedor", id_prov).execute()
        if existe.data:
            print(f"\n  Error: Ya existe un proveedor con ID {id_prov}.")
            return
    except Exception:
        pass

    proveedor = {
        "id_proveedor": id_prov,
        "nombre": nombre,
        "contacto": contacto,
    }

    try:
        supabase.table("proveedor").insert(proveedor).execute()
        print(f"\n  Proveedor '{nombre}' registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar proveedor: {e}")


def editar_proveedor():
    titulo("EDITAR PROVEEDOR")

    print("\n  --- Proveedores disponibles ---")
    try:
        resp = supabase.table("proveedor").select("*").execute()
        if not resp.data:
            print("  No hay proveedores registrados.")
            return
        for p in resp.data:
            print(f"  ID: {p['id_proveedor']}  |  {p.get('nombre', '')}  |  {p.get('contacto', '')}")
    except Exception as e:
        print(f"  Error al cargar proveedores: {e}")
        return

    id_prov = _input_numero("  ID del proveedor a editar: ")

    try:
        resp = supabase.table("proveedor").select("*").eq("id_proveedor", id_prov).execute()
        if not resp.data:
            print(f"\n  No existe proveedor con ID {id_prov}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar proveedor: {e}")
        return

    prov = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Nombre: {prov.get('nombre', '')}")
    print(f"  Contacto: {prov.get('contacto', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    nombre = input(f"  Nombre [{prov.get('nombre', '')}]: ").strip()
    contacto = input(f"  Contacto [{prov.get('contacto', '')}]: ").strip()

    datos = {}
    if nombre:
        datos["nombre"] = nombre
    if contacto:
        datos["contacto"] = contacto

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("proveedor").update(datos).eq("id_proveedor", id_prov).execute()
        print(f"\n  Proveedor {id_prov} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar proveedor: {e}")


def eliminar_proveedor():
    titulo("ELIMINAR PROVEEDOR")

    print("\n  --- Proveedores disponibles ---")
    try:
        resp = supabase.table("proveedor").select("*").execute()
        if not resp.data:
            print("  No hay proveedores registrados.")
            return
        for p in resp.data:
            print(f"  ID: {p['id_proveedor']}  |  {p.get('nombre', '')}  |  {p.get('contacto', '')}")
    except Exception as e:
        print(f"  Error al cargar proveedores: {e}")
        return

    id_prov = _input_numero("  ID del proveedor a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar proveedor {id_prov}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("proveedor").delete().eq("id_proveedor", id_prov).execute()
        print(f"\n  Proveedor {id_prov} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar proveedor: {e}")


# ===================== COMPRA INSUMO =====================


def registrar_compra_insumo():
    titulo("REGISTRAR COMPRA DE INSUMO")

    print("\n  --- Proveedores disponibles ---")
    try:
        resp = supabase.table("proveedor").select("*").execute()
        for p in resp.data:
            print(f"  ID: {p['id_proveedor']}  |  {p.get('nombre', '')}")
    except Exception as e:
        print(f"  Error al cargar proveedores: {e}")
        return

    id_proveedor = _input_numero("  ID del proveedor: ")

    print("\n  --- Productos disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").execute()
        for p in resp.data:
            print(f"  {p['codigo_producto_servicio']}  |  {p.get('descripcion', '')}")
    except Exception as e:
        print(f"  Error al cargar productos: {e}")
        return

    cod_producto = _input_no_vacio("  Código del producto: ")
    cantidad = _input_numero("  Cantidad recibida: ")

    try:
        resp_max = supabase.table("compra_insumo").select("id_compra").order("id_compra", desc=True).execute()
        max_id = resp_max.data[0]["id_compra"] if resp_max.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    compra = {
        "id_compra": nuevo_id,
        "cantidad_recibida": cantidad,
        "id_proveedor": id_proveedor,
        "codigo_producto_servicio": cod_producto,
    }

    try:
        supabase.table("compra_insumo").insert(compra).execute()
        print(f"\n  Compra {nuevo_id} registrada exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar compra: {e}")


def editar_compra_insumo():
    titulo("EDITAR COMPRA DE INSUMO")

    print("\n  --- Compras registradas ---")
    try:
        resp = supabase.table("compra_insumo").select("*").execute()
        if not resp.data:
            print("  No hay compras registradas.")
            return
        for c in resp.data:
            print(f"  ID: {c['id_compra']}  |  Producto: {c.get('codigo_producto_servicio', '')}  |  Cantidad: {c.get('cantidad_recibida', 0)}")
    except Exception as e:
        print(f"  Error al cargar compras: {e}")
        return

    id_compra = _input_numero("  ID de la compra a editar: ")

    try:
        resp = supabase.table("compra_insumo").select("*").eq("id_compra", id_compra).execute()
        if not resp.data:
            print(f"\n  No existe compra con ID {id_compra}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar compra: {e}")
        return

    compra = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Cantidad: {compra.get('cantidad_recibida', 0)}")

    cantidad = input(f"\n  Nueva cantidad [{compra.get('cantidad_recibida', 0)}]: ").strip()

    if not cantidad:
        print("\n  No se realizaron cambios.")
        return

    try:
        datos = {"cantidad_recibida": int(cantidad)}
        supabase.table("compra_insumo").update(datos).eq("id_compra", id_compra).execute()
        print(f"\n  Compra {id_compra} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar compra: {e}")


def eliminar_compra_insumo():
    titulo("ELIMINAR COMPRA DE INSUMO")

    print("\n  --- Compras registradas ---")
    try:
        resp = supabase.table("compra_insumo").select("*").execute()
        if not resp.data:
            print("  No hay compras registradas.")
            return
        for c in resp.data:
            print(f"  ID: {c['id_compra']}  |  Producto: {c.get('codigo_producto_servicio', '')}  |  Cantidad: {c.get('cantidad_recibida', 0)}")
    except Exception as e:
        print(f"  Error al cargar compras: {e}")
        return

    id_compra = _input_numero("  ID de la compra a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar compra {id_compra}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("compra_insumo").delete().eq("id_compra", id_compra).execute()
        print(f"\n  Compra {id_compra} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar compra: {e}")


# ===================== EXAMEN LAB =====================


def registrar_examen_lab():
    titulo("REGISTRAR EXAMEN DE LABORATORIO")

    print("\n  --- Consultas disponibles ---")
    try:
        resp = supabase.table("consulta").select("*").execute()
        for c in resp.data:
            print(f"  ID: {c['id_consulta']}  |  Mascota: {c.get('idmascota', '')}  |  Diagnóstico: {c.get('diagnostico', '')[:30]}")
    except Exception as e:
        print(f"  Error al cargar consultas: {e}")
        return

    id_consulta = _input_numero("  ID de la consulta: ")

    print("\n  --- Proveedores disponibles ---")
    try:
        resp = supabase.table("proveedor").select("*").execute()
        for p in resp.data:
            print(f"  ID: {p['id_proveedor']}  |  {p.get('nombre', '')}")
    except Exception as e:
        print(f"  Error al cargar proveedores: {e}")
        return

    id_proveedor = _input_numero("  ID del proveedor: ")
    tipo_muestra = _input_no_vacio("  Tipo de muestra: ")
    resultados = _input_no_vacio("  Resultados: ")

    try:
        resp_max = supabase.table("examen_lab").select("id_examen").order("id_examen", desc=True).execute()
        max_id = resp_max.data[0]["id_examen"] if resp_max.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    examen = {
        "id_examen": nuevo_id,
        "resultados": resultados,
        "tipo_muestra": tipo_muestra,
        "id_consulta": id_consulta,
        "id_proveedor": id_proveedor,
    }

    try:
        supabase.table("examen_lab").insert(examen).execute()
        print(f"\n  Examen {nuevo_id} registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar examen: {e}")


def editar_examen_lab():
    titulo("EDITAR EXAMEN DE LABORATORIO")

    print("\n  --- Exámenes disponibles ---")
    try:
        resp = supabase.table("examen_lab").select("*").execute()
        if not resp.data:
            print("  No hay exámenes registrados.")
            return
        for e in resp.data:
            print(f"  ID: {e['id_examen']}  |  Consulta: {e.get('id_consulta', '')}  |  Muestra: {e.get('tipo_muestra', '')}")
    except Exception as e:
        print(f"  Error al cargar exámenes: {e}")
        return

    id_examen = _input_numero("  ID del examen a editar: ")

    try:
        resp = supabase.table("examen_lab").select("*").eq("id_examen", id_examen).execute()
        if not resp.data:
            print(f"\n  No existe examen con ID {id_examen}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar examen: {e}")
        return

    examen = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Resultados: {examen.get('resultados', '')}")
    print(f"  Tipo muestra: {examen.get('tipo_muestra', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    resultados = input(f"  Resultados [{examen.get('resultados', '')}]: ").strip()
    tipo_muestra = input(f"  Tipo muestra [{examen.get('tipo_muestra', '')}]: ").strip()

    datos = {}
    if resultados:
        datos["resultados"] = resultados
    if tipo_muestra:
        datos["tipo_muestra"] = tipo_muestra

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("examen_lab").update(datos).eq("id_examen", id_examen).execute()
        print(f"\n  Examen {id_examen} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar examen: {e}")


def eliminar_examen_lab():
    titulo("ELIMINAR EXAMEN DE LABORATORIO")

    print("\n  --- Exámenes disponibles ---")
    try:
        resp = supabase.table("examen_lab").select("*").execute()
        if not resp.data:
            print("  No hay exámenes registrados.")
            return
        for e in resp.data:
            print(f"  ID: {e['id_examen']}  |  Consulta: {e.get('id_consulta', '')}  |  Muestra: {e.get('tipo_muestra', '')}")
    except Exception as e:
        print(f"  Error al cargar exámenes: {e}")
        return

    id_examen = _input_numero("  ID del examen a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar examen {id_examen}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("examen_lab").delete().eq("id_examen", id_examen).execute()
        print(f"\n  Examen {id_examen} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar examen: {e}")


# ===================== RESERVA =====================


def agregar_reserva():
    titulo("AGREGAR RESERVA")

    print("\n  --- Citas disponibles ---")
    try:
        resp = supabase.table("cita").select("*").execute()
        for c in resp.data:
            print(f"  ID: {c['idcita']}  |  Mascota: {c.get('idmascota', '')}  |  Estado: {c.get('estado', '')}")
    except Exception as e:
        print(f"  Error al cargar citas: {e}")
        return

    id_cita = _input_numero("  ID de la cita: ")

    print("\n  --- Servicios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").eq("tipo", "Servicio").execute()
        for s in resp.data:
            print(f"  {s['codigo_producto_servicio']}  |  {s.get('descripcion', '')}  |  ${s.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar servicios: {e}")
        return

    cod_servicio = _input_no_vacio("  Código del servicio: ")

    try:
        resp = supabase.table("reserva").select("*").eq("idcita", id_cita).eq("codigo_producto_servicio", cod_servicio).execute()
        if resp.data:
            print(f"\n  Esta reserva ya existe.")
            return
    except Exception:
        pass

    reserva = {
        "idcita": id_cita,
        "codigo_producto_servicio": cod_servicio,
    }

    try:
        supabase.table("reserva").insert(reserva).execute()
        print(f"\n  Reserva agregada exitosamente (Cita {id_cita} - {cod_servicio}).")
    except Exception as e:
        print(f"\n  Error al agregar reserva: {e}")


def eliminar_reserva():
    titulo("ELIMINAR RESERVA")

    print("\n  --- Reservas disponibles ---")
    try:
        resp = supabase.table("reserva").select("*").execute()
        if not resp.data:
            print("  No hay reservas registradas.")
            return
        for r in resp.data:
            print(f"  Cita: {r.get('idcita', '')}  |  Servicio: {r.get('codigo_producto_servicio', '')}")
    except Exception as e:
        print(f"  Error al cargar reservas: {e}")
        return

    id_cita = _input_numero("  ID de la cita: ")
    cod_servicio = _input_no_vacio("  Código del servicio: ")

    confirmar = input(f"\n  ¿Eliminar reserva? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("reserva").delete().eq("idcita", id_cita).eq("codigo_producto_servicio", cod_servicio).execute()
        print(f"\n  Reserva eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar reserva: {e}")


# ===================== CONSULTA PRODUCTO =====================


def agregar_consulta_producto():
    titulo("AGREGAR PRODUCTO A CONSULTA")

    print("\n  --- Consultas disponibles ---")
    try:
        resp = supabase.table("consulta").select("*").execute()
        for c in resp.data:
            print(f"  ID: {c['id_consulta']}  |  Mascota: {c.get('idmascota', '')}  |  Diagnóstico: {c.get('diagnostico', '')[:30]}")
    except Exception as e:
        print(f"  Error al cargar consultas: {e}")
        return

    id_consulta = _input_numero("  ID de la consulta: ")

    print("\n  --- Productos disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").execute()
        for p in resp.data:
            print(f"  {p['codigo_producto_servicio']}  |  {p.get('descripcion', '')}  |  ${p.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar productos: {e}")
        return

    cod_producto = _input_no_vacio("  Código del producto: ")
    cantidad = _input_numero("  Cantidad gastada: ", float)

    try:
        resp = supabase.table("consulta_producto").select("*").eq("id_consulta", id_consulta).eq("codigo_producto_servicio", cod_producto).execute()
        if resp.data:
            print(f"\n  Este producto ya está registrado en esta consulta.")
            return
    except Exception:
        pass

    registro = {
        "id_consulta": id_consulta,
        "codigo_producto_servicio": cod_producto,
        "cantidad_gastada": cantidad,
    }

    try:
        supabase.table("consulta_producto").insert(registro).execute()
        print(f"\n  Producto agregado a consulta exitosamente.")
    except Exception as e:
        print(f"\n  Error al agregar producto: {e}")


def editar_consulta_producto():
    titulo("EDITAR PRODUCTO DE CONSULTA")

    print("\n  --- Productos en consultas ---")
    try:
        resp = supabase.table("consulta_producto").select("*").execute()
        if not resp.data:
            print("  No hay registros.")
            return
        for cp in resp.data:
            print(f"  Consulta: {cp.get('id_consulta', '')}  |  Producto: {cp.get('codigo_producto_servicio', '')}  |  Cantidad: {cp.get('cantidad_gastada', 0)}")
    except Exception as e:
        print(f"  Error al cargar registros: {e}")
        return

    id_consulta = _input_numero("  ID de la consulta: ")
    cod_producto = _input_no_vacio("  Código del producto: ")

    try:
        resp = supabase.table("consulta_producto").select("*").eq("id_consulta", id_consulta).eq("codigo_producto_servicio", cod_producto).execute()
        if not resp.data:
            print(f"\n  No existe registro para consulta {id_consulta} y producto {cod_producto}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar registro: {e}")
        return

    reg = resp.data[0]
    print(f"\n  Cantidad actual: {reg.get('cantidad_gastada', 0)}")

    cantidad = input(f"\n  Nueva cantidad [{reg.get('cantidad_gastada', 0)}]: ").strip()

    if not cantidad:
        print("\n  No se realizaron cambios.")
        return

    try:
        datos = {"cantidad_gastada": float(cantidad)}
        supabase.table("consulta_producto").update(datos).eq("id_consulta", id_consulta).eq("codigo_producto_servicio", cod_producto).execute()
        print(f"\n  Registro actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar registro: {e}")


def eliminar_consulta_producto():
    titulo("ELIMINAR PRODUCTO DE CONSULTA")

    print("\n  --- Productos en consultas ---")
    try:
        resp = supabase.table("consulta_producto").select("*").execute()
        if not resp.data:
            print("  No hay registros.")
            return
        for cp in resp.data:
            print(f"  Consulta: {cp.get('id_consulta', '')}  |  Producto: {cp.get('codigo_producto_servicio', '')}  |  Cantidad: {cp.get('cantidad_gastada', 0)}")
    except Exception as e:
        print(f"  Error al cargar registros: {e}")
        return

    id_consulta = _input_numero("  ID de la consulta: ")
    cod_producto = _input_no_vacio("  Código del producto: ")

    confirmar = input(f"\n  ¿Eliminar registro? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("consulta_producto").delete().eq("id_consulta", id_consulta).eq("codigo_producto_servicio", cod_producto).execute()
        print(f"\n  Registro eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar registro: {e}")
