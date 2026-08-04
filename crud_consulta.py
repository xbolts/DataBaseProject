from config import supabase
from utils import titulo, _input_no_vacio, _input_numero, _seleccionar_registro


def registrar_consulta():
    titulo("REGISTRAR CONSULTA CLÍNICA")

    print("\n  --- Mascotas disponibles ---")
    id_mascota = _seleccionar_registro("mascota", ["idmascota", "especie", "raza"], "ID de la mascota: ")
    if id_mascota is None:
        return

    diagnostico = _input_no_vacio("  Diagnóstico: ")
    tratamiento = _input_no_vacio("  Tratamiento clínico: ")

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
