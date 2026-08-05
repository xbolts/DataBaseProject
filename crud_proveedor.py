from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


def registrar_proveedor():
    titulo("REGISTRAR PROVEEDOR")

    id_prov = _input_numero("  ID del proveedor: ")
    if id_prov is None:
        return
    nombre = _input_no_vacio("  Nombre del proveedor: ")
    if nombre is None:
        return
    contacto = _input_no_vacio("  Contacto (teléfono): ")
    if contacto is None:
        return

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
    if id_prov is None:
        return

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
    if nombre.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    contacto = input(f"  Contacto [{prov.get('contacto', '')}]: ").strip()
    if contacto.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

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
    if id_prov is None:
        return

    confirmar = input(f"\n  ¿Eliminar proveedor {id_prov}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("proveedor").delete().eq("id_proveedor", id_prov).execute()
        print(f"\n  Proveedor {id_prov} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar proveedor: {e}")
