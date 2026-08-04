from config import supabase
from utils import titulo, _input_no_vacio


def registrar_cliente():
    titulo("REGISTRAR CLIENTE")
    cedula_cliente = _input_no_vacio("  Cédula: ")
    nombre = _input_no_vacio("  Nombre completo: ")
    direccion = input("  Dirección: ").strip()
    telefono = input("  Teléfono: ").strip()
    correo = input("  Correo electrónico: ").strip()

    try:
        existe = supabase.table("cliente").select("*").eq("cedula_cliente", cedula_cliente).execute()
        if existe.data:
            print(f"\n  Error: Ya existe un cliente con cédula {cedula_cliente}.")
            return
    except Exception:
        pass

    cliente = {
        "cedula_cliente": cedula_cliente,
        "nombre": nombre,
        "direccion": direccion or None,
        "telefono": telefono or None,
        "correo": correo or None,
    }

    try:
        supabase.table("cliente").insert(cliente).execute()
        print(f"\n  Cliente '{nombre}' registrado exitosamente.")
    except Exception as e:
        print(f"\n  Error al registrar cliente: {e}")


def editar_cliente():
    titulo("EDITAR CLIENTE")

    cedula_cliente = _input_no_vacio("  Cédula del cliente a editar: ")

    try:
        resp = supabase.table("cliente").select("*").eq("cedula_cliente", cedula_cliente).execute()
        if not resp.data:
            print(f"\n  No existe un cliente con cédula {cedula_cliente}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cliente: {e}")
        return

    cliente = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Nombre: {cliente.get('nombre', '')}")
    print(f"  Dirección: {cliente.get('direccion', '')}")
    print(f"  Teléfono: {cliente.get('telefono', '')}")
    print(f"  Correo: {cliente.get('correo', '')}")

    print("\n  Deje en blanco para mantener el valor actual:\n")
    nombre = input(f"  Nombre [{cliente.get('nombre', '')}]: ").strip()
    direccion = input(f"  Dirección [{cliente.get('direccion', '')}]: ").strip()
    telefono = input(f"  Teléfono [{cliente.get('telefono', '')}]: ").strip()
    correo = input(f"  Correo [{cliente.get('correo', '')}]: ").strip()

    datos = {}
    if nombre:
        datos["nombre"] = nombre
    if direccion:
        datos["direccion"] = direccion
    if telefono:
        datos["telefono"] = telefono
    if correo:
        datos["correo"] = correo

    if not datos:
        print("\n  No se realizaron cambios.")
        return

    try:
        supabase.table("cliente").update(datos).eq("cedula_cliente", cedula_cliente).execute()
        print(f"\n  Cliente {cedula_cliente} actualizado exitosamente.")
    except Exception as e:
        print(f"\n  Error al actualizar cliente: {e}")


def eliminar_cliente():
    titulo("ELIMINAR CLIENTE")

    cedula_cliente = _input_no_vacio("  Cédula del cliente a eliminar: ")

    try:
        resp = supabase.table("cliente").select("*").eq("cedula_cliente", cedula_cliente).execute()
        if not resp.data:
            print(f"\n  No existe un cliente con cédula {cedula_cliente}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cliente: {e}")
        return

    cliente = resp.data[0]
    print(f"\n  Cliente a eliminar:")
    print(f"  Cédula: {cliente.get('cedula_cliente', '')}")
    print(f"  Nombre: {cliente.get('nombre', '')}")
    print(f"  Teléfono: {cliente.get('telefono', '')}")

    confirmar = input("\n  ¿Está seguro de eliminar este cliente? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminación cancelada.")
        return

    try:
        supabase.table("cliente").delete().eq("cedula_cliente", cedula_cliente).execute()
        print(f"\n  Cliente {cedula_cliente} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar cliente: {e}")
