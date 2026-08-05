from config import supabase
from utils import titulo, _input_no_vacio, _input_opcional


def registrar_cliente():
    titulo("REGISTRAR CLIENTE")
    cedula_cliente = _input_no_vacio("  Cedula: ")
    if cedula_cliente is None:
        return
    nombre = _input_no_vacio("  Nombre completo: ")
    if nombre is None:
        return
    direccion = _input_opcional("  Direccion: ")
    if direccion is None:
        return
    telefono = _input_opcional("  Telefono: ")
    if telefono is None:
        return
    correo = _input_opcional("  Correo electronico: ")
    if correo is None:
        return

    try:
        existe = supabase.table("cliente").select("*").eq("cedula_cliente", cedula_cliente).execute()
        if existe.data:
            print(f"\n  Error: Ya existe un cliente con cedula {cedula_cliente}.")
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

    cedula_cliente = _input_no_vacio("  Cedula del cliente a editar: ")
    if cedula_cliente is None:
        return

    try:
        resp = supabase.table("cliente").select("*").eq("cedula_cliente", cedula_cliente).execute()
        if not resp.data:
            print(f"\n  No existe un cliente con cedula {cedula_cliente}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cliente: {e}")
        return

    cliente = resp.data[0]
    print(f"\n  Datos actuales:")
    print(f"  Nombre: {cliente.get('nombre', '')}")
    print(f"  Direccion: {cliente.get('direccion', '')}")
    print(f"  Telefono: {cliente.get('telefono', '')}")
    print(f"  Correo: {cliente.get('correo', '')}")

    print("\n  Deje en blanco para mantener el valor actual (o escriba 'cancelar'):\n")
    nombre = input(f"  Nombre [{cliente.get('nombre', '')}]: ").strip()
    if nombre.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    direccion = input(f"  Direccion [{cliente.get('direccion', '')}]: ").strip()
    if direccion.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    telefono = input(f"  Telefono [{cliente.get('telefono', '')}]: ").strip()
    if telefono.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return
    correo = input(f"  Correo [{cliente.get('correo', '')}]: ").strip()
    if correo.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return

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

    cedula_cliente = _input_no_vacio("  Cedula del cliente a eliminar: ")
    if cedula_cliente is None:
        return

    try:
        resp = supabase.table("cliente").select("*").eq("cedula_cliente", cedula_cliente).execute()
        if not resp.data:
            print(f"\n  No existe un cliente con cedula {cedula_cliente}.")
            return
    except Exception as e:
        print(f"\n  Error al buscar cliente: {e}")
        return

    cliente = resp.data[0]
    print(f"\n  Cliente a eliminar:")
    print(f"  Cedula: {cliente.get('cedula_cliente', '')}")
    print(f"  Nombre: {cliente.get('nombre', '')}")
    print(f"  Telefono: {cliente.get('telefono', '')}")

    confirmar = input("\n  Esta seguro de eliminar este cliente? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Eliminacion cancelada.")
        return

    try:
        supabase.table("cliente").delete().eq("cedula_cliente", cedula_cliente).execute()
        print(f"\n  Cliente {cedula_cliente} eliminado exitosamente.")
    except Exception as e:
        print(f"\n  Error al eliminar cliente: {e}")
