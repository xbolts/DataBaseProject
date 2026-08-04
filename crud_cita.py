from config import supabase
from utils import titulo, _input_no_vacio, _input_numero, _seleccionar_registro


def registrar_cita():
    titulo("REGISTRAR CITA")

    print("\n  --- Mascotas disponibles ---")
    id_mascota = _seleccionar_registro("mascota", ["idmascota", "especie", "raza"], "ID de la mascota: ")
    if id_mascota is None:
        return

    print("\n  --- Servicios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").like("codigo_producto_servicio", "SER-%").execute()
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

    if not any(s["codigo_producto_servicio"] == cod_servicio for s in servicios):
        print(f"\n  Error: El servicio {cod_servicio} no existe.")
        return

    estado = ""
    while estado not in ("PROGRAMADA", "ATENDIDA", "CANCELADA", "NO_ASISTIO"):
        estado = input("  Estado (PROGRAMADA/ATENDIDA/CANCELADA/NO_ASISTIO): ").strip().upper()
        if estado not in ("PROGRAMADA", "ATENDIDA", "CANCELADA", "NO_ASISTIO"):
            print("  Opciones válidas: PROGRAMADA, ATENDIDA, CANCELADA, NO_ASISTIO.")

    hora = input("  Hora (HH:MM, default 09:00): ").strip() or "09:00"

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
        "estado": estado,
        "hora": hora,
    }

    try:
        supabase.table("cita").insert(cita).execute()
        print(f"\n  Cita {nuevo_id} registrada exitosamente (Mascota {id_mascota} - {cod_servicio}).")
    except Exception as e:
        print(f"\n  Error al registrar cita: {e}")


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
        print(f"  ID: {c['idcita']}  |  Mascota: {c.get('idmascota', '')}  |  Hora: {c.get('hora', 'N/A')}  |  Estado: {c.get('estado', '')}")

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
    print(f"  Hora: {cita.get('hora', 'N/A')}")
    print(f"  Estado: {cita.get('estado', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    print(f"  Estado actual: {cita.get('estado', '')}")
    print("  Opciones: PROGRAMADA, ATENDIDA, CANCELADA, NO_ASISTIO")
    estado = input("  Nuevo estado: ").strip().upper()

    datos = {}
    if estado and estado in ("PROGRAMADA", "ATENDIDA", "CANCELADA", "NO_ASISTIO"):
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
        print(f"  ID: {c['idcita']}  |  Mascota: {c.get('idmascota', '')}  |  Hora: {c.get('hora', 'N/A')}  |  Estado: {c.get('estado', '')}")

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
    print(f"  Hora: {cita.get('hora', 'N/A')}")
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
