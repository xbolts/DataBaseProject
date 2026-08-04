from config import supabase
from utils import titulo, _input_no_vacio, _input_numero


def registrar_producto():
    titulo("REGISTRAR PRODUCTO / SERVICIO")

    codigo = _input_no_vacio("  Código (ej: SER-004, MED-004, ACC-005): ")
    descripcion = _input_no_vacio("  Descripción: ")

    precio = _input_numero("  Precio: ", float)
    porcentaje_iva = _input_numero("  Porcentaje IVA (%): ", float)

    try:
        existe = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", codigo).execute()
        if existe.data:
            print(f"\n  Error: Ya existe un producto con código {codigo}.")
            return
    except Exception:
        pass

    producto = {
        "codigo_producto_servicio": codigo,
        "descripcion": descripcion,
        "precio": precio,
        "porcentaje_iva": porcentaje_iva,
    }

    try:
        supabase.table("producto_servicio").insert(producto).execute()
        print(f"\n  Producto '{descripcion}' registrado exitosamente.")

        if codigo.upper().startswith("MED-"):
            stock = _input_numero("  Stock disponible: ")
            cad = input("  Fecha de caducidad (YYYY-MM-DD): ").strip()
            pres = input("  Presentación: ").strip()
            supabase.table("medicina").insert({
                "codigo_producto_servicio": codigo,
                "stock_disponible": stock,
                "fecha_caducidad": cad or None,
                "presentacion": pres or None,
            }).execute()
            print("  Detalles de medicina registrados.")

        elif codigo.upper().startswith("ACC-"):
            stock = _input_numero("  Stock disponible: ")
            cat = input("  Categoría: ").strip()
            mar = input("  Marca: ").strip()
            supabase.table("accesorio").insert({
                "codigo_producto_servicio": codigo,
                "stock_disponible": stock,
                "categoria": cat or None,
                "marca": mar or None,
            }).execute()
            print("  Detalles de accesorio registrados.")

        elif codigo.upper().startswith("SER-"):
            duracion = _input_numero("  Duración estimada (minutos): ")
            requiere = input("  ¿Requiere cita? (s/n): ").strip().lower() == "s"
            supabase.table("servicio").insert({
                "codigo_producto_servicio": codigo,
                "duracion_estimada": duracion,
                "requiere_cita": requiere,
            }).execute()
            print("  Detalles de servicio registrados.")

    except Exception as e:
        print(f"\n  Error al registrar producto: {e}")


def editar_producto():
    titulo("EDITAR PRODUCTO / SERVICIO")

    codigo = _input_no_vacio("  Código del producto a editar: ")

    try:
        resp = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", codigo).execute()
        if not resp.data:
            print(f"\n  No existe un producto con código {codigo}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar producto: {e}")
        return

    prod = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Descripción: {prod.get('descripcion', '')}")
    print(f"  Precio: ${prod.get('precio', 0)}")
    print(f"  Porcentaje IVA: {prod.get('porcentaje_iva', '')}%")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    descripcion = input(f"  Descripción [{prod.get('descripcion', '')}]: ").strip()
    precio = input(f"  Precio [{prod.get('precio', 0)}]: ").strip()
    porcentaje_iva = input(f"  Porcentaje IVA [{prod.get('porcentaje_iva', '')}]: ").strip()

    datos = {}
    if descripcion:
        datos["descripcion"] = descripcion
    if precio:
        try:
            datos["precio"] = float(precio)
        except ValueError:
            print("  Precio inválido, se mantendrá el anterior.")
    if porcentaje_iva:
        try:
            datos["porcentaje_iva"] = float(porcentaje_iva)
        except ValueError:
            print("  IVA inválido, se mantendrá el anterior.")

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("producto_servicio").update(datos).eq("codigo_producto_servicio", codigo).execute()
        print(f"\n  Producto {codigo} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar producto: {e}")


def eliminar_producto():
    titulo("ELIMINAR PRODUCTO / SERVICIO")

    codigo = _input_no_vacio("  Código del producto a eliminar: ")

    try:
        resp = supabase.table("producto_servicio").select("*").eq("codigo_producto_servicio", codigo).execute()
        if not resp.data:
            print(f"\n  No existe un producto con código {codigo}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar producto: {e}")
        return

    prod = resp.data[0]
    print(f"\n  Producto a eliminar:")
    print(f"  Código: {prod.get('codigo_producto_servicio', '')}")
    print(f"  Descripción: {prod.get('descripcion', '')}")
    print(f"  Precio: ${prod.get('precio', 0)}")

    confirmar = input("\n  ¿Está seguro de eliminar este producto? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("producto_servicio").delete().eq("codigo_producto_servicio", codigo).execute()
        print(f"\n  Producto {codigo} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar producto: {e}")
