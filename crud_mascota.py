from config import supabase
from utils import titulo, _input_no_vacio, _input_numero, _seleccionar_registro


def registrar_mascota():
    titulo("REGISTRAR MASCOTA")

    nombre = _input_no_vacio("  Nombre de la mascota: ")
    if nombre is None:
        return

    sexo = ""
    while sexo not in ("M", "H"):
        raw = input("  Sexo (M/H): ").strip()
        if raw.lower() in ("cancelar", "c", "salir"):
            print("\n  Operacion cancelada.")
            return
        sexo = raw.upper()
        if sexo not in ("M", "H"):
            print("  Ingrese 'M' o 'H'.")

    fecha_nacimiento = _input_no_vacio("  Fecha de nacimiento (YYYY-MM-DD): ")
    if fecha_nacimiento is None:
        return
    especie = _input_no_vacio("  Especie (Perro, Gato, etc.): ")
    if especie is None:
        return
    raza = _input_no_vacio("  Raza: ")
    if raza is None:
        return

    print("\n  --- Clientes disponibles ---")
    try:
        resp_cli = supabase.table("cliente").select("*").execute()
        for c in resp_cli.data:
            print(f"  {c['cedula_cliente']}  |  {c.get('nombre', 'N/A')}")
    except Exception:
        pass

    cedula_cliente = _input_no_vacio("  Cédula del dueño: ")
    if cedula_cliente is None:
        return

    try:
        existe = supabase.table("cliente").select("*").eq("cedula_cliente", cedula_cliente).execute()
        if not existe.data:
            print(f"\n  Error: No existe un cliente con cédula {cedula_cliente}.")
            return
    except Exception:
        pass

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
        "fecha_nacimiento": fecha_nacimiento,
        "especie": especie,
        "raza": raza,
        "cedula_cliente": cedula_cliente,
    }

    try:
        supabase.table("mascota").insert(mascota).execute()
        print(f"\n  Mascota '{nombre}' ({especie} - {raza}) registrada con ID {nuevo_id} (Dueño: {cedula_cliente}).")
    except Exception as e:
        print(f"\n  Error al registrar mascota: {e}")


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
    print(f"  Fecha nacimiento: {mascota.get('fecha_nacimiento', '')}")
    print(f"  Especie: {mascota.get('especie', '')}")
    print(f"  Raza: {mascota.get('raza', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    nombre = input(f"  Nombre [{mascota.get('nombre', '')}]: ").strip()
    if nombre.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    sexo = input(f"  Sexo [{mascota.get('sexo', '')}]: ").strip()
    if sexo.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    sexo = sexo.upper()
    fecha_nacimiento = input(f"  Fecha nacimiento [{mascota.get('fecha_nacimiento', '')}]: ").strip()
    if fecha_nacimiento.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    especie = input(f"  Especie [{mascota.get('especie', '')}]: ").strip()
    if especie.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    raza = input(f"  Raza [{mascota.get('raza', '')}]: ").strip()
    if raza.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    datos = {}
    if nombre:
        datos["nombre"] = nombre
    if sexo and sexo in ("M", "H"):
        datos["sexo"] = sexo
    if fecha_nacimiento:
        datos["fecha_nacimiento"] = fecha_nacimiento
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
