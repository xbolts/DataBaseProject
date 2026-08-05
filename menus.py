from utils import separador
from crud_cliente import registrar_cliente, editar_cliente, eliminar_cliente
from crud_mascota import registrar_mascota, editar_mascota, eliminar_mascota
from crud_producto import registrar_producto, editar_producto, eliminar_producto
from crud_cita import registrar_cita, editar_cita, eliminar_cita
from crud_consulta import registrar_consulta, editar_consulta, eliminar_consulta
from crud_factura import (
    registrar_factura, agregar_detalle_factura, editar_detalle_factura, eliminar_detalle_factura,
)
from crud_relacion import (
    agregar_receta, editar_receta, eliminar_receta,
    agregar_atencion_estetica, editar_atencion_estetica, eliminar_atencion_estetica,
    agregar_medicina_detalle, editar_medicina_detalle, eliminar_medicina_detalle,
    agregar_accesorio_detalle, editar_accesorio_detalle, eliminar_accesorio_detalle,
    agregar_servicio_detalle, editar_servicio_detalle, eliminar_servicio_detalle,
)
from crud_proveedor import registrar_proveedor, editar_proveedor, eliminar_proveedor
from crud_compra import registrar_compra_insumo, editar_compra_insumo, eliminar_compra_insumo
from crud_examen import registrar_examen_lab, editar_examen_lab, eliminar_examen_lab
from crud_reserva import agregar_reserva, eliminar_reserva
from crud_consulta_producto import agregar_consulta_producto, editar_consulta_producto, eliminar_consulta_producto
from reportes import (
    reporte_ventas_dia, reporte_banos_programados, reporte_alerta_stock, reporte_historial_clinico,
)


def _accion_cliente():
    while True:
        print()
        separador()
        print("    --- CLIENTE ---")
        separador()
        print("  1. Editar Cliente")
        print("  2. Eliminar Cliente")
        print("  3. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            print()
            editar_cliente()
        elif opcion == "2":
            print()
            eliminar_cliente()
        elif opcion == "3":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_mascota():
    while True:
        print()
        separador()
        print("    --- MASCOTA ---")
        separador()
        print("  1. Editar Mascota")
        print("  2. Eliminar Mascota")
        print("  3. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            print()
            editar_mascota()
        elif opcion == "2":
            print()
            eliminar_mascota()
        elif opcion == "3":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_producto():
    while True:
        print()
        separador()
        print("    --- PRODUCTO / SERVICIO ---")
        separador()
        print("  1. Editar Producto")
        print("  2. Eliminar Producto")
        print("  3. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            print()
            editar_producto()
        elif opcion == "2":
            print()
            eliminar_producto()
        elif opcion == "3":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_cita():
    while True:
        print()
        separador()
        print("    --- CITA ---")
        separador()
        print("  1. Editar Cita")
        print("  2. Eliminar Cita")
        print("  3. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            print()
            editar_cita()
        elif opcion == "2":
            print()
            eliminar_cita()
        elif opcion == "3":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_consulta():
    while True:
        print()
        separador()
        print("    --- CONSULTA CLINICA ---")
        separador()
        print("  1. Editar Consulta")
        print("  2. Eliminar Consulta")
        print("  3. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            print()
            editar_consulta()
        elif opcion == "2":
            print()
            eliminar_consulta()
        elif opcion == "3":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_factura():
    while True:
        print()
        separador()
        print("    --- FACTURA ---")
        separador()
        print("  1. Agregar Detalle a Factura")
        print("  2. Editar Detalle de Factura")
        print("  3. Eliminar Detalle de Factura")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_detalle_factura()
        elif opcion == "2":
            print()
            editar_detalle_factura()
        elif opcion == "3":
            print()
            eliminar_detalle_factura()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_proveedor():
    while True:
        print()
        separador()
        print("    --- PROVEEDOR ---")
        separador()
        print("  1. Editar Proveedor")
        print("  2. Eliminar Proveedor")
        print("  3. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            print()
            editar_proveedor()
        elif opcion == "2":
            print()
            eliminar_proveedor()
        elif opcion == "3":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def menu_tablas_principales():
    while True:
        print()
        separador()
        print("    --- TABLAS PRINCIPALES ---")
        separador()
        print("  1. Cliente")
        print("  2. Mascota")
        print("  3. Producto / Servicio")
        print("  4. Cita")
        print("  5. Consulta Clinica")
        print("  6. Factura")
        print("  7. Proveedor")
        print("  8. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-8): ").strip()

        if opcion == "1":
            _accion_cliente()
        elif opcion == "2":
            _accion_mascota()
        elif opcion == "3":
            _accion_producto()
        elif opcion == "4":
            _accion_cita()
        elif opcion == "5":
            _accion_consulta()
        elif opcion == "6":
            _accion_factura()
        elif opcion == "7":
            _accion_proveedor()
        elif opcion == "8":
            break
        else:
            print("\n  Opcion no valida.")


def _accion_detalle_factura():
    while True:
        print()
        separador()
        print("    --- DETALLE DE FACTURA ---")
        separador()
        print("  1. Agregar Detalle")
        print("  2. Editar Detalle")
        print("  3. Eliminar Detalle")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_detalle_factura()
        elif opcion == "2":
            print()
            editar_detalle_factura()
        elif opcion == "3":
            print()
            eliminar_detalle_factura()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_receta():
    while True:
        print()
        separador()
        print("    --- RECETA ---")
        separador()
        print("  1. Agregar Receta")
        print("  2. Editar Receta")
        print("  3. Eliminar Receta")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_receta()
        elif opcion == "2":
            print()
            editar_receta()
        elif opcion == "3":
            print()
            eliminar_receta()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_atencion_estetica():
    while True:
        print()
        separador()
        print("    --- ATENCION ESTETICA ---")
        separador()
        print("  1. Agregar Atencion Estetica")
        print("  2. Editar Atencion Estetica")
        print("  3. Eliminar Atencion Estetica")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_atencion_estetica()
        elif opcion == "2":
            print()
            editar_atencion_estetica()
        elif opcion == "3":
            print()
            eliminar_atencion_estetica()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_medicina():
    while True:
        print()
        separador()
        print("    --- DETALLE DE MEDICINA ---")
        separador()
        print("  1. Agregar Detalle")
        print("  2. Editar Detalle")
        print("  3. Eliminar Detalle")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_medicina_detalle()
        elif opcion == "2":
            print()
            editar_medicina_detalle()
        elif opcion == "3":
            print()
            eliminar_medicina_detalle()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_accesorio():
    while True:
        print()
        separador()
        print("    --- DETALLE DE ACCESORIO ---")
        separador()
        print("  1. Agregar Detalle")
        print("  2. Editar Detalle")
        print("  3. Eliminar Detalle")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_accesorio_detalle()
        elif opcion == "2":
            print()
            editar_accesorio_detalle()
        elif opcion == "3":
            print()
            eliminar_accesorio_detalle()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_servicio():
    while True:
        print()
        separador()
        print("    --- DETALLE DE SERVICIO ---")
        separador()
        print("  1. Agregar Detalle")
        print("  2. Editar Detalle")
        print("  3. Eliminar Detalle")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_servicio_detalle()
        elif opcion == "2":
            print()
            editar_servicio_detalle()
        elif opcion == "3":
            print()
            eliminar_servicio_detalle()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_reserva():
    while True:
        print()
        separador()
        print("    --- RESERVA ---")
        separador()
        print("  1. Agregar Reserva")
        print("  2. Eliminar Reserva")
        print("  3. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            print()
            agregar_reserva()
        elif opcion == "2":
            print()
            eliminar_reserva()
        elif opcion == "3":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def menu_tablas_relacion():
    while True:
        print()
        separador()
        print("    --- TABLAS DE RELACION ---")
        separador()
        print("  1. Detalle de Factura")
        print("  2. Receta")
        print("  3. Atencion Estetica")
        print("  4. Medicina (Detalle)")
        print("  5. Accesorio (Detalle)")
        print("  6. Servicio (Detalle)")
        print("  7. Reserva")
        print("  8. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-8): ").strip()

        if opcion == "1":
            _accion_detalle_factura()
        elif opcion == "2":
            _accion_receta()
        elif opcion == "3":
            _accion_atencion_estetica()
        elif opcion == "4":
            _accion_medicina()
        elif opcion == "5":
            _accion_accesorio()
        elif opcion == "6":
            _accion_servicio()
        elif opcion == "7":
            _accion_reserva()
        elif opcion == "8":
            break
        else:
            print("\n  Opcion no valida.")


def _accion_compra_insumo():
    while True:
        print()
        separador()
        print("    --- COMPRA DE INSUMO ---")
        separador()
        print("  1. Registrar Compra")
        print("  2. Editar Compra")
        print("  3. Eliminar Compra")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            registrar_compra_insumo()
        elif opcion == "2":
            print()
            editar_compra_insumo()
        elif opcion == "3":
            print()
            eliminar_compra_insumo()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_examen_lab():
    while True:
        print()
        separador()
        print("    --- EXAMEN DE LABORATORIO ---")
        separador()
        print("  1. Registrar Examen")
        print("  2. Editar Examen")
        print("  3. Eliminar Examen")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            registrar_examen_lab()
        elif opcion == "2":
            print()
            editar_examen_lab()
        elif opcion == "3":
            print()
            eliminar_examen_lab()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def _accion_consulta_producto():
    while True:
        print()
        separador()
        print("    --- PRODUCTO EN CONSULTA ---")
        separador()
        print("  1. Agregar Producto a Consulta")
        print("  2. Editar Producto de Consulta")
        print("  3. Eliminar Producto de Consulta")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            agregar_consulta_producto()
        elif opcion == "2":
            print()
            editar_consulta_producto()
        elif opcion == "3":
            print()
            eliminar_consulta_producto()
        elif opcion == "4":
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def menu_tablas_admin():
    while True:
        print()
        separador()
        print("    --- TABLAS ADMINISTRATIVAS ---")
        separador()
        print("  1. Compra de Insumo")
        print("  2. Examen de Laboratorio")
        print("  3. Producto en Consulta")
        print("  4. Proveedor")
        print("  5. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-5): ").strip()

        if opcion == "1":
            _accion_compra_insumo()
        elif opcion == "2":
            _accion_examen_lab()
        elif opcion == "3":
            _accion_consulta_producto()
        elif opcion == "4":
            _accion_proveedor()
        elif opcion == "5":
            break
        else:
            print("\n  Opcion no valida.")


def menu_editar_eliminar():
    while True:
        print()
        separador()
        print("    --- EDITAR / ELIMINAR REGISTROS ---")
        separador()
        print("  1. Tablas Principales")
        print("  2. Tablas de Relacion")
        print("  3. Tablas Administrativas")
        print("  4. Volver")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            menu_tablas_principales()
        elif opcion == "2":
            menu_tablas_relacion()
        elif opcion == "3":
            menu_tablas_admin()
        elif opcion == "4":
            print("\n  Volviendo al menu anterior...")
            break
        else:
            print("\n  Opcion no valida.")


def menu_registros():
    while True:
        print()
        separador()
        print("    --- MODULO DE REGISTRO DE DATOS ---")
        separador()
        print("  1. Registrar Cliente")
        print("  2. Registrar Mascota")
        print("  3. Registrar Producto / Servicio")
        print("  4. Registrar Cita")
        print("  5. Registrar Consulta Clinica")
        print("  6. Registrar Factura")
        print("  7. Volver al Menu Principal")
        separador()

        opcion = input("  Seleccione una opcion (1-7): ").strip()

        if opcion == "1":
            print()
            registrar_cliente()
        elif opcion == "2":
            print()
            registrar_mascota()
        elif opcion == "3":
            print()
            registrar_producto()
        elif opcion == "4":
            print()
            registrar_cita()
        elif opcion == "5":
            print()
            registrar_consulta()
        elif opcion == "6":
            print()
            registrar_factura()
        elif opcion == "7":
            print("\n  Volviendo al menu principal...")
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def menu_reportes():
    while True:
        print()
        separador()
        print("    --- MODULO DE REPORTES GERENCIALES ---")
        separador()
        print("  1. Reporte de Ventas y Facturacion del Dia")
        print("  2. Agenda del Dia (Banos Programados)")
        print("  3. Reporte de Necesidad de Insumos (Alerta de Stock)")
        print("  4. Historial Clinico Completo")
        print("  5. Volver al Menu Principal")
        separador()

        opcion = input("  Seleccione el reporte a generar (1-5): ").strip()

        if opcion == "1":
            print()
            reporte_ventas_dia()
        elif opcion == "2":
            print()
            reporte_banos_programados()
        elif opcion == "3":
            print()
            reporte_alerta_stock()
        elif opcion == "4":
            print()
            reporte_historial_clinico()
        elif opcion == "5":
            print("\n  Volviendo al menu principal...")
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")


def menu_principal():
    while True:
        print()
        separador()
        print("    --- SISTEMA VETERINARIO ---")
        separador()
        print("  1. Modulo de Reportes Gerenciales")
        print("  2. Modulo de Registro de Datos")
        print("  3. Editar / Eliminar Registros")
        print("  4. Salir")
        separador()

        opcion = input("  Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            print()
            menu_reportes()
        elif opcion == "2":
            print()
            menu_registros()
        elif opcion == "3":
            print()
            menu_editar_eliminar()
        elif opcion == "4":
            print("\n  Saliendo del sistema...")
            break
        else:
            print("\n  Opcion no valida.")

        input("\n  Presione Enter para continuar...")
