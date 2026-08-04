from config import supabase
from utils import separador, titulo
from datetime import date


def _mostrar_facturas(facturas, etiqueta_fecha):
    print(f"\n  Fecha: {etiqueta_fecha}")
    print(f"\n  {'N° Comp.':<16} {'Cédula':<12} {'Estado Pago':<15} {'Forma Pago':<18}")
    print(f"  {'-'*14:<16} {'-'*10:<12} {'-'*13:<15} {'-'*16:<18}")

    total_general = 0.0

    for f in facturas:
        num = f["num_comprobante"]
        cedula = f["cedula_cliente"]
        estado = f.get("estado_pago", "N/A") or "N/A"
        forma = f.get("forma_pago", "N/A") or "N/A"

        try:
            det = supabase.table("factura_detalle").select("*").eq("num_comprobante", num).execute()
            detalles = det.data
        except Exception:
            detalles = []

        total_factura = 0.0
        for d in detalles:
            subtotal = d.get("subtotal") or 0
            total_factura += float(subtotal)

        total_general += total_factura
        print(f"  {str(num):<16} {cedula:<12} {estado:<15} {forma:<18}  Total: ${total_factura:,.2f}")

    separador()
    print(f"  TOTAL: ${total_general:,.2f}")
    separador()


def reporte_ventas_dia():
    titulo("REPORTE DE VENTAS Y FACTURACIÓN DEL DÍA")
    hoy = date.today().isoformat()

    try:
        resp = supabase.table("factura").select("*").eq("fecha_emision", hoy).execute()
    except Exception as e:
        print(f"\n  Error al consultar facturas: {e}")
        return

    facturas = resp.data

    if facturas:
        _mostrar_facturas(facturas, f"Hoy ({hoy})")
        return

    print(f"\n  No existen facturas registradas el día de hoy ({hoy}).")

    try:
        resp_all = supabase.table("factura").select("*").order("fecha_emision", desc=True).execute()
    except Exception as e:
        print(f"  Error al buscar última fecha: {e}")
        return

    todas = resp_all.data
    if not todas:
        print("  No existen facturas registradas en el sistema.")
        return

    ultima_fecha = todas[0].get("fecha_emision")
    facturas_ultima = [f for f in todas if f.get("fecha_emision") == ultima_fecha]

    print(f"  Mostrando facturas de la última fecha disponible:")
    _mostrar_facturas(facturas_ultima, ultima_fecha)


def reporte_banos_programados():
    titulo("AGENDA DEL DÍA (BAÑOS PROGRAMADOS)")

    try:
        resp = supabase.table("atencion_estetica").select("*").execute()
    except Exception as e:
        print(f"  Error al consultar atenciones estéticas: {e}")
        return

    registros = resp.data

    if not registros:
        print("\n  No existen baños programados registrados.")
        return

    nombres_mascotas = {}
    try:
        resp_m = supabase.table("mascota").select("idmascota,nombre").execute()
        for m in resp_m.data:
            nombres_mascotas[m["idmascota"]] = m.get("nombre", "N/A") or "N/A"
    except Exception:
        pass

    print(f"\n  {'ID Atención':<12} {'Mascota':<18} {'Hora Inicio':<14} {'Hora Fin':<14} {'Observaciones'}")
    print(f"  {'-'*10:<12} {'-'*16:<18} {'-'*12:<14} {'-'*12:<14} {'-'*25}")

    for r in registros:
        id_atencion = r["id_atencion_estetica"]
        id_mascota = r["idmascota"]
        nombre_mascota = nombres_mascotas.get(id_mascota, f"ID {id_mascota}")
        h_inicio = r.get("hora_inicio", "N/A") or "N/A"
        h_fin = r.get("hora_fin", "N/A") or "N/A"
        obs = r.get("observaciones", "") or ""

        print(f"  {str(id_atencion):<12} {nombre_mascota:<18} {h_inicio:<14} {h_fin:<14} {obs}")

    separador()
    print(f"  Total de registros: {len(registros)}")
    separador()


def reporte_alerta_stock():
    titulo("REPORTE DE NECESIDAD DE INSUMOS (ALERTA DE STOCK)")

    medicinas = []
    accesorios = []

    try:
        resp_med = supabase.table("medicina").select("*").execute()
        medicinas = resp_med.data
    except Exception as e:
        print(f"\n  Error al consultar medicinas: {e}")

    try:
        resp_acc = supabase.table("accesorio").select("*").execute()
        accesorios = resp_acc.data
    except Exception as e:
        print(f"  Error al consultar accesorios: {e}")

    alertas_med = [m for m in medicinas if (m.get("stock_disponible") or 0) <= 5]
    alertas_acc = [a for a in accesorios if (a.get("stock_disponible") or 0) <= 5]

    if alertas_med:
        print("\n  --- MEDICINAS CON STOCK BAJO (<= 5) ---")
        print(f"  {'Código Producto':<20} {'Stock':<10} {'Presentación':<20} {'Fecha Caducidad'}")
        print(f"  {'-'*18:<20} {'-'*6:<10} {'-'*14:<20} {'-'*16}")

        for m in alertas_med:
            cod = m["codigo_producto_servicio"]
            stock = m.get("stock_disponible", 0) or 0
            pres = m.get("presentacion", "N/A") or "N/A"
            cad = m.get("fecha_caducidad", "N/A") or "N/A"
            print(f"  {cod:<20} {str(stock):<10} {pres:<20} {cad}")

    if alertas_acc:
        print("\n  --- ACCESORIOS CON STOCK BAJO (<= 5) ---")
        print(f"  {'Código Producto':<20} {'Stock':<10} {'Categoría':<20} {'Marca'}")
        print(f"  {'-'*18:<20} {'-'*6:<10} {'-'*12:<20} {'-'*15}")

        for a in alertas_acc:
            cod = a["codigo_producto_servicio"]
            stock = a.get("stock_disponible", 0) or 0
            cat = a.get("categoria", "N/A") or "N/A"
            mar = a.get("marca", "N/A") or "N/A"
            print(f"  {cod:<20} {str(stock):<10} {cat:<20} {mar}")

    total_alertas = len(alertas_med) + len(alertas_acc)

    if total_alertas == 0:
        print("\n  No existen insumos con stock bajo (<= 5 unidades).")
        print("\n  --- RESUMEN: 5 INSUMOS CON MENOR STOCK ---")
        todos = []
        for m in medicinas:
            todos.append({
                "codigo": m["codigo_producto_servicio"],
                "stock": m.get("stock_disponible", 0) or 0,
                "detalle": m.get("presentacion", ""),
                "tipo": "Medicina",
            })
        for a in accesorios:
            todos.append({
                "codigo": a["codigo_producto_servicio"],
                "stock": a.get("stock_disponible", 0) or 0,
                "detalle": a.get("categoria", ""),
                "tipo": "Accesorio",
            })

        todos_ordenados = sorted(todos, key=lambda x: x["stock"])[:5]

        print(f"\n  {'Código':<20} {'Stock':<10} {'Tipo':<12} {'Detalle'}")
        print(f"  {'-'*18:<20} {'-'*6:<10} {'-'*10:<12} {'-'*20}")
        for item in todos_ordenados:
            print(f"  {item['codigo']:<20} {str(item['stock']):<10} {item['tipo']:<12} {item['detalle']}")

    separador()
    print(f"  Total de alertas activas: {total_alertas}")
    separador()


def reporte_historial_clinico():
    titulo("HISTORIAL CLÍNICO COMPLETO")

    busqueda = input("  Ingrese el Nombre de la Mascota o Cédula del Dueño: ").strip()
    if not busqueda:
        print("  Debe ingresar un valor de búsqueda.")
        return

    print("\n  Recopilando historial médico...")

    mascota_encontrada = None
    cliente_encontrado = None
    es_cedula = busqueda.isdigit()

    if es_cedula:
        try:
            resp_cli = supabase.table("cliente").select("*").eq("cedula_cliente", busqueda).execute()
            if resp_cli.data:
                cliente_encontrado = resp_cli.data[0]
        except Exception:
            pass

        try:
            resp_m = supabase.table("mascota").select("*").eq("cedula_cliente", busqueda).execute()
            mascotas_dueño = resp_m.data
        except Exception:
            mascotas_dueño = []

        if len(mascotas_dueño) == 1:
            mascota_encontrada = mascotas_dueño[0]
        elif len(mascotas_dueño) > 1:
            print(f"\n  Cliente: {cliente_encontrado.get('nombre', 'N/A') if cliente_encontrado else busqueda}")
            print("  Mascotas registradas:")
            print(f"  {'ID':<8} {'Nombre':<15} {'Especie':<12} {'Raza':<20} {'Fecha Nac.'}")
            print(f"  {'-'*6:<8} {'-'*13:<15} {'-'*10:<12} {'-'*18:<20} {'-'*12}")
            for m in mascotas_dueño:
                fecha_nac = m.get("fecha_nacimiento", "N/A") or "N/A"
                nom = m.get("nombre", "N/A") or "N/A"
                print(f"  {str(m['idmascota']):<8} {nom:<15} {m.get('especie', 'N/A'):<12} {m.get('raza', 'N/A'):<20} {fecha_nac}")
            seleccion = input("\n  Ingrese el ID de la mascota: ").strip()
            try:
                mascota_encontrada = next(
                    (m for m in mascotas_dueño if m["idmascota"] == int(seleccion)), None
                )
            except (ValueError, StopIteration):
                pass
    else:
        try:
            resp_mascotas = supabase.table("mascota").select("*").execute()
            for m in resp_mascotas.data:
                nombre_m = (m.get("nombre") or "").lower()
                especie = (m.get("especie") or "").lower()
                raza = (m.get("raza") or "").lower()
                busq = busqueda.lower()
                if busq in nombre_m or busq in especie or busq in raza:
                    mascota_encontrada = m
                    break
        except Exception:
            pass

        if mascota_encontrada is None:
            try:
                resp_m = supabase.table("mascota").select("*").eq("idmascota", int(busqueda)).execute()
                if resp_m.data:
                    mascota_encontrada = resp_m.data[0]
            except (ValueError, Exception):
                pass

        if mascota_encontrada and mascota_encontrada.get("cedula_cliente"):
            try:
                resp_cli = supabase.table("cliente").select("*").eq("cedula_cliente", mascota_encontrada["cedula_cliente"]).execute()
                if resp_cli.data:
                    cliente_encontrado = resp_cli.data[0]
            except Exception:
                pass

    if mascota_encontrada is None:
        print(f"\n  No se encontraron resultados para '{busqueda}'.")
        return

    try:
        resp_cons = supabase.table("consulta").select("*").eq("idmascota", mascota_encontrada["idmascota"]).order("fecha", desc=True).execute()
        consultas = resp_cons.data
    except Exception:
        consultas = []

    recetas = {}
    for cons in consultas:
        try:
            resp_rec = supabase.table("receta").select("*").eq("id_consulta", cons["id_consulta"]).execute()
            if resp_rec.data:
                recetas[cons["id_consulta"]] = resp_rec.data[0]
        except Exception:
            pass

    separador()
    print("  HISTORIAL CLÍNICO")
    separador()

    nombre_mascota = mascota_encontrada.get("nombre", "N/A") or "N/A"
    esp = mascota_encontrada.get("especie", "N/A") or "N/A"
    fecha_nac = mascota_encontrada.get("fecha_nacimiento", "N/A") or "N/A"
    raza = mascota_encontrada.get("raza", "N/A") or "N/A"
    sexo = mascota_encontrada.get("sexo", "N/A") or "N/A"
    print(f"\n  PACIENTE: {nombre_mascota} ({raza} {esp})    NACIMIENTO: {fecha_nac}    SEXO: {sexo}")
    print(f"  ID MASCOTA: {mascota_encontrada['idmascota']}")

    if cliente_encontrado:
        nombre = cliente_encontrado.get("nombre", "N/A") or "N/A"
        tel = cliente_encontrado.get("telefono", "N/A") or "N/A"
        dir_ = cliente_encontrado.get("direccion", "N/A") or "N/A"
        print(f"\n  PROPIETARIO: {nombre}    CONTACTO: {tel}")
        print(f"  CÉDULA: {cliente_encontrado['cedula_cliente']}    DIRECCIÓN: {dir_}")

    separador()

    if not consultas:
        print("\n  No existen consultas registradas para esta mascota.")
        separador()
        return

    print(f"\n  {'FECHA':<14} | {'DIAGNÓSTICO':<35} | {'TRATAMIENTO Y RECETA'}")
    print(f"  {'-'*12:<14}-+-{'-'*33:<35}-+-{'-'*30}")

    for c in consultas:
        fecha = c.get("fecha", "N/A") or "N/A"
        diag = c.get("diagnostico", "N/A") or "N/A"
        trat = c.get("tratamiento_clinico", "N/A") or "N/A"

        rec = recetas.get(c["id_consulta"])
        receta_texto = ""
        if rec and rec.get("indicaciones_casa"):
            receta_texto = f"\n  {'':14} | {'':35} | Casa: {rec['indicaciones_casa']}"

        diag_corto = diag[:33] + "..." if len(diag) > 35 else diag
        trat_corto = trat[:30] + "..." if len(trat) > 33 else trat

        print(f"  {fecha:<14} | {diag_corto:<35} | {trat_corto}")
        if receta_texto:
            print(receta_texto)

    separador()
    print(f"  Total de consultas: {len(consultas)}")
    separador()
