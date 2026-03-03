import sys
import os
# Permite importar el motor desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sistema_aaa import run_aaa_diagnostic

def test_risk_detection():
    """Verifica que el sistema detecte correctamente un riesgo alto."""
    # Caso de prueba: Una organización con métricas muy bajas
    test_data = [{"name": "Critical JAC", "autonomy": 5.0, "algorithms": 5.0, "agency": 5.0}]
    
    output = run_aaa_diagnostic(test_data)
    
    # Verificaciones (Assertions)
    assert output[0]["analysis"]["risk_level"] == "HIGH"
    assert "LOW_INFRASTRUCTURE_CONTROL" in output[0]["analysis"]["active_alerts"]
    print("Test Passed: Risk Engine accurately identifies critical vulnerabilities.")

if __name__ == "__main__":
    test_risk_detection()
