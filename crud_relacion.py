from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


def agregar_receta():
    titulo("AGREGAR RECETA")

    print("\n  --- Consultas disponibles ---")
    try:
        resp = supabase.table("consulta").select("*").execute()
        if not resp.data:
            print("  No hay consultas registradas.")
            return
        for c in resp.data:
            print(f"  ID: {c['id_consulta']}  |  Mascota: {c.get('idmascota', '')}  |  Diagnóstico: {c.get('diagnostico', '')[:30]}")
    except Exception as e:
        print(f"  Error al cargar consultas: {e}")
        return

    id_consulta = _input_numero("  ID de la consulta: ")
    if id_consulta is None:
        return

    try:
        resp = supabase.table("consulta").select("*").eq("id_consulta", id_consulta).execute()
        if not resp.data:
            print(f"\n  No existe consulta con ID {id_consulta}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar consulta: {e}")
        return

    try:
        resp_rec = supabase.table("receta").select("*").eq("id_consulta", id_consulta).execute()
        if resp_rec.data:
            print(f"\n  Esta consulta ya tiene una receta (ID: {resp_rec.data[0].get('id_receta', '')}).")
            return
    except Exception:
        pass

    indicaciones = _input_no_vacio("  Indicaciones en casa: ")
    if indicaciones is None:
        return

    try:
        resp_max = supabase.table("receta").select("id_receta").order("id_receta", desc=True).execute()
        max_id = resp_max.data[0]["id_receta"] if resp_max.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    receta = {
        "id_receta": nuevo_id,
        "indicaciones_casa": indicaciones,
        "id_consulta": id_consulta,
    }

    try:
        supabase.table("receta").insert(receta).execute()
        print(f"\n  Receta {nuevo_id} registrada para consulta {id_consulta}.")
    except Exception as e:
        print(f"\n  Error al registrar receta: {e}")


def editar_receta():
    titulo("EDITAR RECETA")

    print("\n  --- Recetas disponibles ---")
    try:
        resp = supabase.table("receta").select("*").execute()
        if not resp.data:
            print("  No hay recetas registradas.")
            return
        for r in resp.data:
            print(f"  ID: {r['id_receta']}  |  Consulta: {r.get('id_consulta', '')}  |  Indicaciones: {r.get('indicaciones_casa', '')[:40]}")
    except Exception as e:
        print(f"  Error al cargar recetas: {e}")
        return

    id_receta = _input_numero("  ID de la receta a editar: ")
    if id_receta is None:
        return

    try:
        resp = supabase.table("receta").select("*").eq("id_receta", id_receta).execute()
        if not resp.data:
            print(f"\n  No existe receta con ID {id_receta}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar receta: {e}")
        return

    receta = resp.data[0]
    print(f"\n  Indicaciones actuales: {receta.get('indicaciones_casa', '')}")

    nuevas_ind = input("\n  Nuevas indicaciones (deje en blanco para mantener): ").strip()
    if nuevas_ind.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    if not nuevas_ind:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("receta").update({"indicaciones_casa": nuevas_ind}).eq("id_receta", id_receta).execute()
        print(f"\n  Receta {id_receta} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar receta: {e}")


def eliminar_receta():
    titulo("ELIMINAR RECETA")

    print("\n  --- Recetas disponibles ---")
    try:
        resp = supabase.table("receta").select("*").execute()
        if not resp.data:
            print("  No hay recetas registradas.")
            return
        for r in resp.data:
            print(f"  ID: {r['id_receta']}  |  Consulta: {r.get('id_consulta', '')}  |  Indicaciones: {r.get('indicaciones_casa', '')[:40]}")
    except Exception as e:
        print(f"  Error al cargar recetas: {e}")
        return

    id_receta = _input_numero("  ID de la receta a eliminar: ")
    if id_receta is None:
        return

    confirmar = input(f"\n  ¿Eliminar receta {id_receta}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("receta").delete().eq("id_receta", id_receta).execute()
        print(f"\n  Receta {id_receta} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar receta: {e}")


def agregar_atencion_estetica():
    titulo("AGREGAR ATENCIÓN ESTÉTICA")

    print("\n  --- Mascotas disponibles ---")
    try:
        resp = supabase.table("mascota").select("*").execute()
        for m in resp.data:
            print(f"  ID: {m['idmascota']}  |  {m.get('nombre', '')}  |  {m.get('especie', '')}  |  {m.get('raza', '')}")
    except Exception as e:
        print(f"  Error al cargar mascotas: {e}")
        return

    id_mascota = _input_numero("  ID de la mascota: ")
    if id_mascota is None:
        return

    try:
        resp = supabase.table("mascota").select("*").eq("idmascota", id_mascota).execute()
        if not resp.data:
            print(f"\n  No existe mascota con ID {id_mascota}.")
            return
    except Exception as e:
        print(f"  Error al verificar mascota: {e}")
        return

    hora_inicio = _input_no_vacio("  Hora de inicio (HH:MM): ")
    if hora_inicio is None:
        return
    hora_fin = _input_no_vacio("  Hora de fin (HH:MM): ")
    if hora_fin is None:
        return
    observaciones = input("  Observaciones: ").strip()
    if observaciones.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    try:
        resp_max = supabase.table("atencion_estetica").select("id_atencion_estetica").order("id_atencion_estetica", desc=True).execute()
        max_id = resp_max.data[0]["id_atencion_estetica"] if resp_max.data else 0
        nuevo_id = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener ID: {e}")
        return

    atencion = {
        "id_atencion_estetica": nuevo_id,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "observaciones": observaciones or None,
        "idmascota": id_mascota,
    }

    try:
        supabase.table("atencion_estetica").insert(atencion).execute()
        print(f"\n  Atención estética {nuevo_id} registrada para mascota {id_mascota}.")
    except Exception as e:
        print(f"\n  Error al registrar atención: {e}")


def editar_atencion_estetica():
    titulo("EDITAR ATENCIÓN ESTÉTICA")

    try:
        resp = supabase.table("atencion_estetica").select("*").execute()
        if not resp.data:
            print("  No hay atenciones estéticas registradas.")
            return
        for a in resp.data:
            print(f"  ID: {a['id_atencion_estetica']}  |  Mascota: {a.get('idmascota', '')}  |  Inicio: {a.get('hora_inicio', '')}  |  Fin: {a.get('hora_fin', '')}")
    except Exception as e:
        print(f"  Error al cargar atenciones: {e}")
        return

    id_atencion = _input_numero("  ID de la atención a editar: ")
    if id_atencion is None:
        return

    try:
        resp = supabase.table("atencion_estetica").select("*").eq("id_atencion_estetica", id_atencion).execute()
        if not resp.data:
            print(f"\n  No existe atención con ID {id_atencion}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar atención: {e}")
        return

    atencion = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Hora inicio: {atencion.get('hora_inicio', '')}")
    print(f"  Hora fin: {atencion.get('hora_fin', '')}")
    print(f"  Observaciones: {atencion.get('observaciones', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    hora_inicio = input(f"  Hora inicio [{atencion.get('hora_inicio', '')}]: ").strip()
    if hora_inicio.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    hora_fin = input(f"  Hora fin [{atencion.get('hora_fin', '')}]: ").strip()
    if hora_fin.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    observaciones = input(f"  Observaciones [{atencion.get('observaciones', '')}]: ").strip()
    if observaciones.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    datos = {}
    if hora_inicio:
        datos["hora_inicio"] = hora_inicio
    if hora_fin:
        datos["hora_fin"] = hora_fin
    if observaciones:
        datos["observaciones"] = observaciones

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("atencion_estetica").update(datos).eq("id_atencion_estetica", id_atencion).execute()
        print(f"\n  Atención {id_atencion} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar atención: {e}")


def eliminar_atencion_estetica():
    titulo("ELIMINAR ATENCIÓN ESTÉTICA")

    try:
        resp = supabase.table("atencion_estetica").select("*").execute()
        if not resp.data:
            print("  No hay atenciones estéticas registradas.")
            return
        for a in resp.data:
            print(f"  ID: {a['id_atencion_estetica']}  |  Mascota: {a.get('idmascota', '')}  |  Inicio: {a.get('hora_inicio', '')}")
    except Exception as e:
        print(f"  Error al cargar atenciones: {e}")
        return

    id_atencion = _input_numero("  ID de la atención a eliminar: ")
    if id_atencion is None:
        return

    confirmar = input(f"\n  ¿Eliminar atención {id_atencion}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("atencion_estetica").delete().eq("id_atencion_estetica", id_atencion).execute()
        print(f"\n  Atención {id_atencion} eliminada exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar atención: {e}")


def agregar_medicina_detalle():
    titulo("AGREGAR DETALLE DE MEDICINA")

    print("\n  --- Medicinas disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").like("codigo_producto_servicio", "MED-%").execute()
        if not resp.data:
            print("  No hay medicinas registradas.")
            return
        for m in resp.data:
            print(f"  {m['codigo_producto_servicio']}  |  {m.get('descripcion', '')}  |  ${m.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar medicinas: {e}")
        return

    cod = _input_no_vacio("  Código de la medicina: ")
    if cod is None:
        return

    try:
        resp = supabase.table("medicina").select("*").eq("codigo_producto_servicio", cod).execute()
        if resp.data:
            print(f"\n  Esta medicina ya tiene detalles registrados.")
            return
    except Exception:
        pass

    stock = _input_numero("  Stock disponible: ")
    if stock is None:
        return
    caducidad = input("  Fecha de caducidad (YYYY-MM-DD): ").strip()
    if caducidad.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    presentacion = input("  Presentación: ").strip()
    if presentacion.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    detalle = {
        "codigo_producto_servicio": cod,
        "stock_disponible": stock,
        "fecha_caducidad": caducidad or None,
        "presentacion": presentacion or None,
    }

    try:
        supabase.table("medicina").insert(detalle).execute()
        print(f"\n  Detalle de medicina {cod} registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar detalle: {e}")


def editar_medicina_detalle():
    titulo("EDITAR DETALLE DE MEDICINA")

    try:
        resp = supabase.table("medicina").select("*").execute()
        if not resp.data:
            print("  No hay detalles de medicinas registrados.")
            return
        for m in resp.data:
            print(f"  Código: {m.get('codigo_producto_servicio', '')}  |  Stock: {m.get('stock_disponible', 0)}  |  Presentación: {m.get('presentacion', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código de la medicina a editar: ")
    if cod is None:
        return

    try:
        resp = supabase.table("medicina").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para medicina {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Stock: {det.get('stock_disponible', 0)}")
    print(f"  Caducidad: {det.get('fecha_caducidad', '')}")
    print(f"  Presentación: {det.get('presentacion', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    stock = input(f"  Stock [{det.get('stock_disponible', 0)}]: ").strip()
    if stock.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    caducidad = input(f"  Caducidad [{det.get('fecha_caducidad', '')}]: ").strip()
    if caducidad.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    presentacion = input(f"  Presentación [{det.get('presentacion', '')}]: ").strip()
    if presentacion.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    datos = {}
    if stock:
        try:
            datos["stock_disponible"] = int(stock)
        except ValueError:
            print("  Stock inválido.")
    if caducidad:
        datos["fecha_caducidad"] = caducidad
    if presentacion:
        datos["presentacion"] = presentacion

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("medicina").update(datos).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Medicina {cod} actualizada exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar medicina: {e}")


def eliminar_medicina_detalle():
    titulo("ELIMINAR DETALLE DE MEDICINA")

    try:
        resp = supabase.table("medicina").select("*").execute()
        if not resp.data:
            print("  No hay detalles de medicinas registrados.")
            return
        for m in resp.data:
            print(f"  Código: {m.get('codigo_producto_servicio', '')}  |  Stock: {m.get('stock_disponible', 0)}  |  Presentación: {m.get('presentacion', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código de la medicina a eliminar: ")
    if cod is None:
        return

    confirmar = input(f"\n  ¿Eliminar detalle de medicina {cod}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("medicina").delete().eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle de medicina {cod} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")


def agregar_accesorio_detalle():
    titulo("AGREGAR DETALLE DE ACCESORIO")

    print("\n  --- Accesorios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").like("codigo_producto_servicio", "ACC-%").execute()
        if not resp.data:
            print("  No hay accesorios registrados.")
            return
        for a in resp.data:
            print(f"  {a['codigo_producto_servicio']}  |  {a.get('descripcion', '')}  |  ${a.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar accesorios: {e}")
        return

    cod = _input_no_vacio("  Código del accesorio: ")
    if cod is None:
        return

    try:
        resp = supabase.table("accesorio").select("*").eq("codigo_producto_servicio", cod).execute()
        if resp.data:
            print(f"\n  Este accesorio ya tiene detalles registrados.")
            return
    except Exception:
        pass

    stock = _input_numero("  Stock disponible: ")
    if stock is None:
        return
    categoria = input("  Categoría: ").strip()
    if categoria.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    marca = input("  Marca: ").strip()
    if marca.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    detalle = {
        "codigo_producto_servicio": cod,
        "stock_disponible": stock,
        "categoria": categoria or None,
        "marca": marca or None,
    }

    try:
        supabase.table("accesorio").insert(detalle).execute()
        print(f"\n  Detalle de accesorio {cod} registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar detalle: {e}")


def editar_accesorio_detalle():
    titulo("EDITAR DETALLE DE ACCESORIO")

    try:
        resp = supabase.table("accesorio").select("*").execute()
        if not resp.data:
            print("  No hay detalles de accesorios registrados.")
            return
        for a in resp.data:
            print(f"  Código: {a.get('codigo_producto_servicio', '')}  |  Stock: {a.get('stock_disponible', 0)}  |  Categoría: {a.get('categoria', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del accesorio a editar: ")
    if cod is None:
        return

    try:
        resp = supabase.table("accesorio").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para accesorio {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Stock: {det.get('stock_disponible', 0)}")
    print(f"  Categoría: {det.get('categoria', '')}")
    print(f"  Marca: {det.get('marca', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    stock = input(f"  Stock [{det.get('stock_disponible', 0)}]: ").strip()
    if stock.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    categoria = input(f"  Categoría [{det.get('categoria', '')}]: ").strip()
    if categoria.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    marca = input(f"  Marca [{det.get('marca', '')}]: ").strip()
    if marca.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

    datos = {}
    if stock:
        try:
            datos["stock_disponible"] = int(stock)
        except ValueError:
            print("  Stock inválido.")
    if categoria:
        datos["categoria"] = categoria
    if marca:
        datos["marca"] = marca

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("accesorio").update(datos).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Accesorio {cod} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar accesorio: {e}")


def eliminar_accesorio_detalle():
    titulo("ELIMINAR DETALLE DE ACCESORIO")

    try:
        resp = supabase.table("accesorio").select("*").execute()
        if not resp.data:
            print("  No hay detalles de accesorios registrados.")
            return
        for a in resp.data:
            print(f"  Código: {a.get('codigo_producto_servicio', '')}  |  Stock: {a.get('stock_disponible', 0)}  |  Categoría: {a.get('categoria', '')}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del accesorio a eliminar: ")
    if cod is None:
        return

    confirmar = input(f"\n  ¿Eliminar detalle de accesorio {cod}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("accesorio").delete().eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle de accesorio {cod} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")


def agregar_servicio_detalle():
    titulo("AGREGAR DETALLE DE SERVICIO")

    print("\n  --- Servicios disponibles ---")
    try:
        resp = supabase.table("producto_servicio").select("*").like("codigo_producto_servicio", "SER-%").execute()
        if not resp.data:
            print("  No hay servicios registrados.")
            return
        for s in resp.data:
            print(f"  {s['codigo_producto_servicio']}  |  {s.get('descripcion', '')}  |  ${s.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar servicios: {e}")
        return

    cod = _input_no_vacio("  Código del servicio: ")
    if cod is None:
        return

    try:
        resp = supabase.table("servicio").select("*").eq("codigo_producto_servicio", cod).execute()
        if resp.data:
            print(f"\n  Este servicio ya tiene detalles registrados.")
            return
    except Exception:
        pass

    duracion = _input_numero("  Duración estimada (minutos): ")
    if duracion is None:
        return
    requiere = input("  ¿Requiere cita? (s/n): ").strip()
    if requiere.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    requiere = requiere.lower() == "s"

    detalle = {
        "codigo_producto_servicio": cod,
        "duracion_estimada": duracion,
        "requiere_cita": requiere,
    }

    try:
        supabase.table("servicio").insert(detalle).execute()
        print(f"\n  Detalle de servicio {cod} registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar detalle: {e}")


def editar_servicio_detalle():
    titulo("EDITAR DETALLE DE SERVICIO")

    try:
        resp = supabase.table("servicio").select("*").execute()
        if not resp.data:
            print("  No hay detalles de servicios registrados.")
            return
        for s in resp.data:
            req = "Sí" if s.get("requiere_cita") else "No"
            print(f"  Código: {s.get('codigo_producto_servicio', '')}  |  Duración: {s.get('duracion_estimada', 0)} min  |  Requiere cita: {req}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del servicio a editar: ")
    if cod is None:
        return

    try:
        resp = supabase.table("servicio").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para servicio {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    req_actual = "Sí" if det.get("requiere_cita") else "No"
    print(f"\n  Datos actuales:")
    print(f"  Duración: {det.get('duracion_estimada', 0)} minutos")
    print(f"  Requiere cita: {req_actual}")

    duracion = input(f"\n  Nueva duración [{det.get('duracion_estimada', 0)}]: ").strip()
    if duracion.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    requiere = input(f"  Requiere cita (s/n) [{req_actual}]: ").strip()
    if requiere.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    requiere = requiere.lower()

    datos = {}
    if duracion:
        try:
            datos["duracion_estimada"] = int(duracion)
        except ValueError:
            print("  Duración inválida.")
    if requiere in ("s", "n"):
        datos["requiere_cita"] = requiere == "s"

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("servicio").update(datos).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Servicio {cod} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar servicio: {e}")


def eliminar_servicio_detalle():
    titulo("ELIMINAR DETALLE DE SERVICIO")

    try:
        resp = supabase.table("servicio").select("*").execute()
        if not resp.data:
            print("  No hay detalles de servicios registrados.")
            return
        for s in resp.data:
            req = "Sí" if s.get("requiere_cita") else "No"
            print(f"  Código: {s.get('codigo_producto_servicio', '')}  |  Duración: {s.get('duracion_estimada', 0)} min  |  Requiere cita: {req}")
    except Exception as e:
        print(f"  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del servicio a eliminar: ")
    if cod is None:
        return

    confirmar = input(f"\n  ¿Eliminar detalle de servicio {cod}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("servicio").delete().eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle de servicio {cod} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")
