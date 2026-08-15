-- ==============================================================================
-- TRIGGER 1: RESTAR STOCK AL CONSUMIR UN PRODUCTO (CON VALIDACIÓN DE NEGATIVOS)
-- ==============================================================================

-- PARTE 1: La función lógica
CREATE OR REPLACE FUNCTION actualizar_stock_salida()
RETURNS TRIGGER AS $$
DECLARE
    -- Variable temporal para guardar el stock antes de restar
    stock_actual INT;
BEGIN
    -- 1. Intentar buscar el stock si es MEDICINA
    SELECT stock_disponible INTO stock_actual 
    FROM medicina 
    WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
    
    -- La variable mágica FOUND evalúa si el SELECT anterior encontró algo
    IF FOUND THEN
        -- Validar que la cantidad gastada no supere el stock
        IF stock_actual < NEW.cantidad_gastada THEN
            RAISE EXCEPTION 'Error: Stock insuficiente. Intenta gastar %, pero solo quedan % unidades en inventario.', NEW.cantidad_gastada, stock_actual;
        END IF;
        
        -- Si pasa la validación, hace la resta
        UPDATE medicina
        SET stock_disponible = stock_disponible - NEW.cantidad_gastada
        WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
        
        RETURN NEW;
    END IF;

    -- 2. Si no fue medicina, intentar buscar el stock si es ACCESORIO
    SELECT stock_disponible INTO stock_actual 
    FROM accesorio 
    WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
    
    IF FOUND THEN
        IF stock_actual < NEW.cantidad_gastada THEN
            RAISE EXCEPTION 'Error: Stock insuficiente. Intenta gastar %, pero solo quedan % unidades en inventario.', NEW.cantidad_gastada, stock_actual;
        END IF;
        
        UPDATE accesorio
        SET stock_disponible = stock_disponible - NEW.cantidad_gastada
        WHERE codigo_producto_servicio = NEW.codigo_producto_servicio;
        
        RETURN NEW;
    END IF;

    -- Si es un SERVICIO, simplemente pasa de largo
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- PARTE 2: El disparador asociado a la tabla
CREATE TRIGGER trg_restar_stock_consulta
AFTER INSERT ON consulta_producto
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_salida();