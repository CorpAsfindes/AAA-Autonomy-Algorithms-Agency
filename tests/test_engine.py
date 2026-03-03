import sys
import os
import json

# Configuración de rutas para importar el motor principal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sistema_aaa import run_aaa_diagnostic

def test_full_diagnostic_integrity():
    """
    Suite de pruebas integral para validar el motor AAA:
    1. Importación y ejecución.
    2. Validación de estructura JSON.
    3. Verificación de campos obligatorios.
    4. Comprobación de tipos de datos.
    """
    
    # Insumo de prueba: Una organización con métricas críticas
    sample_input = [
        {"name": "Test Organization", "autonomy": 7.0, "algorithms": 7.0, "agency": 7.0}
    ]
    
    # Ejecución del motor
    output = run_aaa_diagnostic(sample_input)
    
    # --- PRUEBAS DE INTEGRIDAD ---
    
    # 1. ¿Es una lista lo que devuelve?
    assert isinstance(output, list), "Error: La salida debe ser una lista."
    assert len(output) > 0, "Error: La salida está vacía."
    
    result = output[0]
    
    # 2. ¿Contiene todos los campos esperados (Esquema JSON)?
    expected_keys = ["org_id", "name", "metrics", "analysis"]
    for key in expected_keys:
        assert key in result, f"Error: Falta el campo obligatorio '{key}' en la salida."
    
    # 3. ¿El análisis contiene el índice compuesto y las alertas?
    assert "composite_score" in result["analysis"], "Error: No se calculó el Composite Score."
    assert "active_alerts" in result["analysis"], "Error: No existe el campo de alertas."
    assert "recommendations" in result["analysis"], "Error: No se generaron recomendaciones."
    
    # 4. ¿La lógica de riesgo funciona? (Si es 7.0, debe ser riesgo HIGH)
    assert result["analysis"]["risk_level"] == "HIGH", "Error: No detectó el nivel de riesgo HIGH para métricas bajas."
    assert len(result["analysis"]["active_alerts"]) == 3, "Error: No identificó las 3 alertas críticas esperadas."
    
    # 5. ¿Es serializable a JSON válido?
    try:
        json_string = json.dumps(output)
        json.loads(json_string)
    except (ValueError, TypeError):
        assert False, "Error: La salida no es un formato JSON válido."

    print("✅ TEST PASSED: All structural and logic integrity checks successful.")

if __name__ == "__main__":
    test_full_diagnostic_integrity()
