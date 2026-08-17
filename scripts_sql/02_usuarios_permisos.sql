-- ==============================================================================
-- CREACIÓN DE USUARIOS DEL SISTEMA VETERINARIO
-- ==============================================================================

-- En PostgreSQL, 'CREATE USER' crea un rol que tiene permisos para iniciar sesión
CREATE USER app_veterinaria WITH PASSWORD 'vet_app_2026';
CREATE USER auditor_sri WITH PASSWORD 'auditoria_2026';
CREATE USER asistente_citas WITH PASSWORD 'citas_2026';
CREATE USER gestor_inventario WITH PASSWORD 'bodega_2026';
CREATE USER veterinario_jefe WITH PASSWORD 'vet_admin_2026';

-- ==============================================================================
-- ASIGNACIÓN DE PERMISOS BÁSICOS A TABLAS
-- ==============================================================================

-- 1. USUARIO: app_veterinaria (Falta 1 permiso de SP para después)
-- Permiso 1: Leer, insertar y actualizar clientes
GRANT SELECT, INSERT, UPDATE ON cliente TO app_veterinaria;

-- 2. USUARIO: auditor_sri (Falta 1 permiso de Vista para después)
-- Permiso 2: Solo lectura en facturas para temas contables
GRANT SELECT ON factura TO auditor_sri;

-- 3. USUARIO: asistente_citas
-- Permiso 3: Gestionar la agenda de citas
GRANT SELECT, INSERT, UPDATE, DELETE ON cita TO asistente_citas;
-- Permiso 4: Registrar mascotas nuevas
GRANT SELECT, INSERT, UPDATE ON mascota TO asistente_citas;

-- 4. USUARIO: gestor_inventario
-- Permiso 5: Gestionar el stock de medicinas
GRANT SELECT, INSERT, UPDATE ON medicina TO gestor_inventario;
-- Permiso 6: Registrar la llegada de compras de insumos
GRANT SELECT, INSERT ON compra_insumo TO gestor_inventario;

-- 5. USUARIO: veterinario_jefe (Falta 1 permiso de Vista para después)
-- Permiso 7: Registrar y actualizar las consultas clínicas
GRANT SELECT, INSERT, UPDATE ON consulta TO veterinario_jefe;


-- ==============================================================================
-- ASIGNACIÓN DE PERMISOS A VISTAS (Views)
-- ==============================================================================

-- Permiso a la vista de facturación detallada para auditorías
GRANT SELECT ON vw_facturacion_detallada TO auditor_sri;

-- Permiso a la vista del historial médico completo
GRANT SELECT ON vw_historial_clinico TO veterinario_jefe;


-- ==============================================================================
-- ASIGNACIÓN DE PERMISOS A PROCEDIMIENTOS ALMACENADOS (SPs)
-- ==============================================================================

-- Permisos para que la aplicación Python pueda ejecutar el CRUD de mascotas
GRANT EXECUTE ON PROCEDURE sp_mascota_insertar TO app_veterinaria;
GRANT EXECUTE ON PROCEDURE sp_mascota_actualizar TO app_veterinaria;
GRANT EXECUTE ON PROCEDURE sp_mascota_eliminar TO app_veterinaria;