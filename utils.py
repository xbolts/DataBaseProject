from config import supabase


def separador():
    print("-" * 56)


def titulo(texto):
    separador()
    print(f"  {texto}")
    separador()


def _input_no_vacio(msg):
    while True:
        valor = input(msg).strip()
        if valor.lower() in ("cancelar", "c", "salir"):
            print("\n  Operacion cancelada.")
            return None
        if valor:
            return valor
        print("  Este campo es obligatorio. Ingrese un valor o 'cancelar' para salir.")


def _input_numero(msg, tipo=int):
    while True:
        valor = input(msg).strip()
        if valor.lower() in ("cancelar", "c", "salir"):
            print("\n  Operacion cancelada.")
            return None
        try:
            return tipo(valor)
        except (ValueError, TypeError):
            print(f"  Ingrese un numero valido ({tipo.__name__}) o 'cancelar' para salir.")


def _input_opcional(msg):
    valor = input(msg).strip()
    if valor.lower() in ("cancelar", "c", "salir"):
        print("\n  Operacion cancelada.")
        return None
    return valor


def _seleccionar_registro(tabla, campos_mostrar, msg="Seleccione el ID: "):
    try:
        resp = supabase.table(tabla).select("*").execute()
        registros = resp.data
    except Exception as e:
        print(f"  Error al cargar {tabla}: {e}")
        return None

    if not registros:
        print(f"  No hay registros en {tabla}.")
        return None

    print()
    for r in registros:
        partes = [str(r.get(c, "")) for c in campos_mostrar]
        print(f"  ID: {r.get(campos_mostrar[0], '')}  |  {'  |  '.join(partes)}")

    return _input_numero(f"\n  {msg}")
