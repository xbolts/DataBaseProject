from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


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
    if id_consulta is None:
        return

    print("\n  --- Productos disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").execute()
        for p in resp.data:
            print(f"  {p['codigo_producto_servicio']}  |  {p.get('descripcion', '')}  |  ${p.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar productos: {e}")
        return

    cod_producto = _input_no_vacio("  Código del producto: ")
    if cod_producto is None:
        return
    cantidad = _input_numero("  Cantidad gastada: ", float)
    if cantidad is None:
        return

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
    if id_consulta is None:
        return
    cod_producto = _input_no_vacio("  Código del producto: ")
    if cod_producto is None:
        return

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
    if cantidad.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

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
    if id_consulta is None:
        return
    cod_producto = _input_no_vacio("  Código del producto: ")
    if cod_producto is None:
        return

    confirmar = input(f"\n  ¿Eliminar registro? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("consulta_producto").delete().eq("id_consulta", id_consulta).eq("codigo_producto_servicio", cod_producto).execute()
        print(f"\n  Registro eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar registro: {e}")
