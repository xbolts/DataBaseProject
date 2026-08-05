from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


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
    if id_proveedor is None:
        return

    print("\n  --- Productos disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").execute()
        for p in resp.data:
            print(f"  {p['codigo_producto_servicio']}  |  {p.get('descripcion', '')}")
    except Exception as e:
        print(f"  Error al cargar productos: {e}")
        return

    cod_producto = _input_no_vacio("  Código del producto: ")
    if cod_producto is None:
        return
    cantidad = _input_numero("  Cantidad recibida: ")
    if cantidad is None:
        return

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
    if id_compra is None:
        return

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
    if cantidad.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

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
    if id_compra is None:
        return

    confirmar = input(f"\n  ¿Eliminar compra {id_compra}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("compra_insumo").delete().eq("id_compra", id_compra).execute()
        print(f"\n  Compra {id_compra} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar compra: {e}")
