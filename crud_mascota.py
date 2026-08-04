from config import supabase
from utils import titulo, _input_no_vacio, _input_numero, _seleccionar_registro


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

    print("\n  --- Clientes disponibles ---")
    try:
        resp_cli = supabase.table("cliente").select("*").execute()
        for c in resp_cli.data:
            print(f"  {c['cedula']}  |  {c.get('nombre', 'N/A')}")
    except Exception:
        pass

    cedula = _input_no_vacio("  Cédula del dueño: ")

    try:
        existe = supabase.table("cliente").select("*").eq("cedula", cedula).execute()
        if not existe.data:
            print(f"\n  Error: No existe un cliente con cédula {cedula}.")
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
