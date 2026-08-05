from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


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
    if id_cita is None:
        return

    print("\n  --- Servicios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").like("codigo_producto_servicio", "SER-%").execute()
        for s in resp.data:
            print(f"  {s['codigo_producto_servicio']}  |  {s.get('descripcion', '')}  |  ${s.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar servicios: {e}")
        return

    cod_servicio = _input_no_vacio("  Código del servicio: ")
    if cod_servicio is None:
        return

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
    if id_cita is None:
        return
    cod_servicio = _input_no_vacio("  Código del servicio: ")
    if cod_servicio is None:
        return

    confirmar = input(f"\n  ¿Eliminar reserva? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("reserva").delete().eq("idcita", id_cita).eq("codigo_producto_servicio", cod_servicio).execute()
        print(f"\n  Reserva eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar reserva: {e}")
