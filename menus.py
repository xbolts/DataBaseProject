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
from crud_admin import (
    registrar_proveedor, editar_proveedor, eliminar_proveedor,
    registrar_compra_insumo, editar_compra_insumo, eliminar_compra_insumo,
    registrar_examen_lab, editar_examen_lab, eliminar_examen_lab,
    agregar_reserva, eliminar_reserva,
    agregar_consulta_producto, editar_consulta_producto, eliminar_consulta_producto,
)
from reportes import (
    reporte_ventas_dia, reporte_banos_programados, reporte_alerta_stock, reporte_historial_clinico,
)


def menu_editar_eliminar():
    while True:
        print()
        separador()
        print("    --- EDITAR / ELIMINAR REGISTROS ---")
        separador()
        print("  --- Tablas Principales ---")
        print("  1. Editar Cliente")
        print("  2. Editar Mascota")
        print("  3. Editar Producto / Servicio")
        print("  4. Editar Cita")
        print("  5. Editar Consulta Clínica")
        print("  ---")
        print("  6. Eliminar Cliente")
        print("  7. Eliminar Mascota")
        print("  8. Eliminar Producto / Servicio")
        print("  9. Eliminar Cita")
        print("  10. Eliminar Consulta Clínica")
        print("  --- Tablas de Relación ---")
        print("  11. Agregar Detalle a Factura")
        print("  12. Editar Detalle de Factura")
        print("  13. Eliminar Detalle de Factura")
        print("  ---")
        print("  14. Agregar Receta")
        print("  15. Editar Receta")
        print("  16. Eliminar Receta")
        print("  ---")
        print("  17. Agregar Atención Estética")
        print("  18. Editar Atención Estética")
        print("  19. Eliminar Atención Estética")
        print("  ---")
        print("  20. Agregar Detalle de Medicina")
        print("  21. Editar Detalle de Medicina")
        print("  22. Eliminar Detalle de Medicina")
        print("  ---")
        print("  23. Agregar Detalle de Accesorio")
        print("  24. Editar Detalle de Accesorio")
        print("  25. Eliminar Detalle de Accesorio")
        print("  ---")
        print("  26. Agregar Detalle de Servicio")
        print("  27. Editar Detalle de Servicio")
        print("  28. Eliminar Detalle de Servicio")
        print("  --- Tablas Administrativas ---")
        print("  29. Registrar Proveedor")
        print("  30. Editar Proveedor")
        print("  31. Eliminar Proveedor")
        print("  ---")
        print("  32. Registrar Compra de Insumo")
        print("  33. Editar Compra de Insumo")
        print("  34. Eliminar Compra de Insumo")
        print("  ---")
        print("  35. Registrar Examen de Laboratorio")
        print("  36. Editar Examen de Laboratorio")
        print("  37. Eliminar Examen de Laboratorio")
        print("  ---")
        print("  38. Agregar Reserva")
        print("  39. Eliminar Reserva")
        print("  ---")
        print("  40. Agregar Producto a Consulta")
        print("  41. Editar Producto de Consulta")
        print("  42. Eliminar Producto de Consulta")
        print("  ---")
        print("  43. Volver")
        separador()

        opcion = input("  Seleccione una opción (1-43): ").strip()

        if opcion == "1":
            print()
            editar_cliente()
        elif opcion == "2":
            print()
            editar_mascota()
        elif opcion == "3":
            print()
            editar_producto()
        elif opcion == "4":
            print()
            editar_cita()
        elif opcion == "5":
            print()
            editar_consulta()
        elif opcion == "6":
            print()
            eliminar_cliente()
        elif opcion == "7":
            print()
            eliminar_mascota()
        elif opcion == "8":
            print()
            eliminar_producto()
        elif opcion == "9":
            print()
            eliminar_cita()
        elif opcion == "10":
            print()
            eliminar_consulta()
        elif opcion == "11":
            print()
            agregar_detalle_factura()
        elif opcion == "12":
            print()
            editar_detalle_factura()
        elif opcion == "13":
            print()
            eliminar_detalle_factura()
        elif opcion == "14":
            print()
            agregar_receta()
        elif opcion == "15":
            print()
            editar_receta()
        elif opcion == "16":
            print()
            eliminar_receta()
        elif opcion == "17":
            print()
            agregar_atencion_estetica()
        elif opcion == "18":
            print()
            editar_atencion_estetica()
        elif opcion == "19":
            print()
            eliminar_atencion_estetica()
        elif opcion == "20":
            print()
            agregar_medicina_detalle()
        elif opcion == "21":
            print()
            editar_medicina_detalle()
        elif opcion == "22":
            print()
            eliminar_medicina_detalle()
        elif opcion == "23":
            print()
            agregar_accesorio_detalle()
        elif opcion == "24":
            print()
            editar_accesorio_detalle()
        elif opcion == "25":
            print()
            eliminar_accesorio_detalle()
        elif opcion == "26":
            print()
            agregar_servicio_detalle()
        elif opcion == "27":
            print()
            editar_servicio_detalle()
        elif opcion == "28":
            print()
            eliminar_servicio_detalle()
        elif opcion == "29":
            print()
            registrar_proveedor()
        elif opcion == "30":
            print()
            editar_proveedor()
        elif opcion == "31":
            print()
            eliminar_proveedor()
        elif opcion == "32":
            print()
            registrar_compra_insumo()
        elif opcion == "33":
            print()
            editar_compra_insumo()
        elif opcion == "34":
            print()
            eliminar_compra_insumo()
        elif opcion == "35":
            print()
            registrar_examen_lab()
        elif opcion == "36":
            print()
            editar_examen_lab()
        elif opcion == "37":
            print()
            eliminar_examen_lab()
        elif opcion == "38":
            print()
            agregar_reserva()
        elif opcion == "39":
            print()
            eliminar_reserva()
        elif opcion == "40":
            print()
            agregar_consulta_producto()
        elif opcion == "41":
            print()
            editar_consulta_producto()
        elif opcion == "42":
            print()
            eliminar_consulta_producto()
        elif opcion == "43":
            print("\n  Volviendo al menú anterior...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-43).")

        input("\n  Presione Enter para continuar...")


def menu_registros():
    while True:
        print()
        separador()
        print("    --- MÓDULO DE REGISTRO DE DATOS ---")
        separador()
        print("  1. Registrar Cliente")
        print("  2. Registrar Mascota")
        print("  3. Registrar Producto / Servicio")
        print("  4. Registrar Cita")
        print("  5. Registrar Consulta Clínica")
        print("  6. Registrar Factura")
        print("  7. Volver al Menú Principal")
        separador()

        opcion = input("  Seleccione una opción (1-7): ").strip()

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
            print("\n  Volviendo al menú principal...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-7).")

        input("\n  Presione Enter para continuar...")


def menu_reportes():
    while True:
        print()
        separador()
        print("    --- MÓDULO DE REPORTES GERENCIALES ---")
        separador()
        print("  1. Reporte de Ventas y Facturación del Día (Caja)")
        print("  2. Agenda del Día (Baños Programados)")
        print("  3. Reporte de Necesidad de Insumos (Alerta de Stock)")
        print("  4. Historial Clínico Completo (Todas las mascotas)")
        print("  5. Volver al Menú Principal")
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
            print("\n  Volviendo al menú principal...")
            break
        else:
            print("\n  Opción no válida. Intente de nuevo (1-5).")

        input("\n  Presione Enter para continuar...")


def menu_principal():
    while True:
        print()
        separador()
        print("    --- SISTEMA VETERINARIO ---")
        separador()
        print("  1. Módulo de Reportes Gerenciales")
        print("  2. Módulo de Registro de Datos")
        print("  3. Editar / Eliminar Registros")
        print("  4. Salir")
        separador()

        opcion = input("  Seleccione una opción (1-4): ").strip()

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
            print("\n  Opción no válida. Intente de nuevo (1-4).")

        input("\n  Presione Enter para continuar...")
