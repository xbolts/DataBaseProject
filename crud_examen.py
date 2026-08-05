from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


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
    if id_consulta is None:
        return

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
    tipo_muestra = _input_no_vacio("  Tipo de muestra: ")
    if tipo_muestra is None:
        return
    resultados = _input_no_vacio("  Resultados: ")
    if resultados is None:
        return

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
    if id_examen is None:
        return

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
    if resultados.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    tipo_muestra = input(f"  Tipo muestra [{examen.get('tipo_muestra', '')}]: ").strip()
    if tipo_muestra.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

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
    if id_examen is None:
        return

    confirmar = input(f"\n  ¿Eliminar examen {id_examen}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("examen_lab").delete().eq("id_examen", id_examen).execute()
        print(f"\n  Examen {id_examen} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar examen: {e}")
