from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


def registrar_factura():
    titulo("REGISTRAR FACTURA")

    print("\n  --- Clientes disponibles ---")
    resp_cli = supabase.table("cliente").select("*").execute()
    if not resp_cli.data:
        print("  No hay clientes registrados. Registre uno primero.")
        return

    for c in resp_cli.data:
        print(f"  {c['cedula']}  |  {c.get('nombre', 'N/A')}")

    cedula = _input_no_vacio("  Cédula del cliente: ")

    if not any(cl["cedula"] == cedula for cl in resp_cli.data):
        print(f"\n  Error: No existe un cliente con cédula {cedula}.")
        return

    estado_pago = ""
    while estado_pago not in ("Pagado", "Pendiente", "Anulado"):
        estado_pago = input("  Estado de pago (Pagado/Pendiente/Anulado): ").strip().capitalize()
        if estado_pago not in ("Pagado", "Pendiente", "Anulado"):
            print("  Opciones válidas: Pagado, Pendiente, Anulado.")

    forma_pago = ""
    while forma_pago not in ("Efectivo", "Tarjeta", "Transferencia", "Ninguna"):
        forma_pago = input("  Forma de pago (Efectivo/Tarjeta/Transferencia/Ninguna): ").strip().capitalize()
        if forma_pago not in ("Efectivo", "Tarjeta", "Transferencia", "Ninguna"):
            print("  Opciones válidas: Efectivo, Tarjeta, Transferencia, Ninguna.")

    try:
        resp = supabase.table("factura").select("num_comprobante").order("num_comprobante", desc=True).execute()
        max_id = resp.data[0]["num_comprobante"] if resp.data else 0
        nuevo_num = max_id + 1
    except Exception as e:
        print(f"\n  Error al obtener número de comprobante: {e}")
        return

    detalles = []
    print("\n  --- Agregar productos/servicios a la factura ---")
    print("  (Escriba 'fin' en el código del producto para terminar)\n")

    while True:
        cod = input("  Código del producto/servicio (o 'fin'): ").strip()
        if cod.lower() == "fin":
            break

        try:
            resp_prod = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", cod).execute()
            if not resp_prod.data:
                print(f"  Error: No existe producto con código {cod}.")
                continue
        except Exception:
            print(f"  Error al verificar producto {cod}.")
            continue

        prod = resp_prod.data[0]
        print(f"    -> {prod['descripcion']} (${prod.get('precio', 0)})")

        cantidad = _input_numero("    Cantidad: ")

        precio_unitario = float(prod.get("precio", 0))
        subtotal = round(precio_unitario * cantidad, 2)

        detalles.append({
            "codigo_producto_servicio": cod,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal,
        })
        print(f"    Agregado: {cantidad} x ${precio_unitario} = ${subtotal}")

    if not detalles:
        print("\n  No se agregaron productos. Factura cancelada.")
        return

    total = sum(d["subtotal"] for d in detalles)
    print(f"\n  --- RESUMEN FACTURA {nuevo_num} ---")
    print(f"  Cliente: {cedula}")
    print(f"  Productos: {len(detalles)}")
    print(f"  Total: ${total:,.2f}")

    confirmar = input("\n  ¿Confirmar factura? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Factura cancelada.")
        return

    factura = {
        "num_comprobante": nuevo_num,
        "cedula": cedula,
        "estado_pago": estado_pago,
        "forma_pago": forma_pago,
    }

    try:
        supabase.table("factura").insert(factura).execute()

        for d in detalles:
            d["num_comprobante"] = nuevo_num
            supabase.table("factura_detalle").insert(d).execute()

        print(f"\n  Factura {nuevo_num} registrada exitosamente. Total: ${total:,.2f}")
    except Exception as e:
        print(f"\n  Error al registrar factura: {e}")


def agregar_detalle_factura():
    titulo("AGREGAR DETALLE A FACTURA")

    try:
        resp = supabase.table("factura").select("*").execute()
        if not resp.data:
            print("  No hay facturas registradas.")
            return
        print("\n  --- Facturas disponibles ---")
        for f in resp.data:
            print(f"  N° {f['num_comprobante']}  |  Cliente: {f.get('cedula', '')}  |  Estado: {f.get('estado_pago', '')}")
    except Exception as e:
        print(f"  Error al cargar facturas: {e}")
        return

    num_comp = _input_numero("  N° de comprobante: ")

    try:
        resp = supabase.table("factura").select("*").eq("num_comprobante", num_comp).execute()
        if not resp.data:
            print(f"\n  No existe factura con N° {num_comp}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar factura: {e}")
        return

    print("\n  --- Productos/Servicios disponibles ---")
    try:
        resp_prod = supabase.table("producto_servicio").select("*").execute()
        for p in resp_prod.data:
            print(f"  {p['codigo_producto_servicio']}  |  {p.get('descripcion', '')}  |  ${p.get('precio', 0)}")
    except Exception as e:
        print(f"  Error al cargar productos: {e}")
        return

    cod = _input_no_vacio("  Código del producto: ")

    try:
        resp_p = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", cod).execute()
        if not resp_p.data:
            print(f"\n  No existe producto con código {cod}.")
            return
    except Exception as e:
        print(f"\n  Error al verificar producto: {e}")
        return

    prod = resp_p.data[0]
    print(f"  -> {prod['descripcion']} (${prod.get('precio', 0)})")

    cantidad = _input_numero("  Cantidad: ")
    precio_unitario = float(prod.get("precio", 0))
    subtotal = round(precio_unitario * cantidad, 2)

    detalle = {
        "num_comprobante": num_comp,
        "codigo_producto_servicio": cod,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "subtotal": subtotal,
    }

    try:
        supabase.table("factura_detalle").insert(detalle).execute()
        print(f"\n  Detalle agregado: {cantidad} x ${precio_unitario} = ${subtotal}")
    except Exception as e:
        print(f"\n  Error al agregar detalle: {e}")


def editar_detalle_factura():
    titulo("EDITAR DETALLE DE FACTURA")

    num_comp = _input_numero("  N° de comprobante: ")

    try:
        resp = supabase.table("factura_detalle").select("*").eq("num_comprobante", num_comp).execute()
        if not resp.data:
            print(f"\n  No hay detalles para la factura {num_comp}.")
            return
        print(f"\n  --- Detalles de factura {num_comp} ---")
        for d in resp.data:
            print(f"  Producto: {d.get('codigo_producto_servicio', '')}  |  Cant: {d.get('cantidad', 0)}  |  Subtotal: ${d.get('subtotal', 0)}")
    except Exception as e:
        print(f"\n  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del producto a editar: ")

    try:
        resp = supabase.table("factura_detalle").select("*").eq("num_comprobante", num_comp).eq("codigo_producto_servicio", cod).execute()
        if not resp.data:
            print(f"\n  No existe detalle para producto {cod} en factura {num_comp}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar detalle: {e}")
        return

    det = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Cantidad: {det.get('cantidad', 0)}")
    print(f"  Precio unitario: ${det.get('precio_unitario', 0)}")

    cantidad = input(f"\n  Nueva cantidad [{det.get('cantidad', 0)}]: ").strip()
    precio = input(f"  Nuevo precio unitario [{det.get('precio_unitario', 0)}]: ").strip()

    datos = {}
    if cantidad:
        try:
            datos["cantidad"] = int(cantidad)
        except ValueError:
            print("  Cantidad inválida.")
    if precio:
        try:
            datos["precio_unitario"] = float(precio)
        except ValueError:
            print("  Precio inválido.")

    if "cantidad" in datos or "precio_unitario" in datos:
        cant = datos.get("cantidad", det.get("cantidad", 0))
        prec = datos.get("precio_unitario", det.get("precio_unitario", 0))
        datos["subtotal"] = round(cant * prec, 2)

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("factura_detalle").update(datos).eq("num_comprobante", num_comp).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar detalle: {e}")


def eliminar_detalle_factura():
    titulo("ELIMINAR DETALLE DE FACTURA")

    num_comp = _input_numero("  N° de comprobante: ")

    try:
        resp = supabase.table("factura_detalle").select("*").eq("num_comprobante", num_comp).execute()
        if not resp.data:
            print(f"\n  No hay detalles para la factura {num_comp}.")
            return
        print(f"\n  --- Detalles de factura {num_comp} ---")
        for d in resp.data:
            print(f"  Producto: {d.get('codigo_producto_servicio', '')}  |  Cant: {d.get('cantidad', 0)}  |  Subtotal: ${d.get('subtotal', 0)}")
    except Exception as e:
        print(f"\n  Error al cargar detalles: {e}")
        return

    cod = _input_no_vacio("  Código del producto a eliminar: ")

    confirmar = input(f"\n  ¿Eliminar detalle {cod} de factura {num_comp}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("factura_detalle").delete().eq("num_comprobante", num_comp).eq("codigo_producto_servicio", cod).execute()
        print(f"\n  Detalle eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar detalle: {e}")
