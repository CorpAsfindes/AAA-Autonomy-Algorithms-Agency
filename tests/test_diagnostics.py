import pytest
from sistema_aaa import run_aaa_diagnostic

def test_diagnostic_math_accuracy():
    """Valida que el cálculo del Composite Score sea exacto (Promedio AAA)."""
    data = [{"name": "Test JAC", "autonomy": 10.0, "algorithms": 10.0, "agency": 10.0}]
    output = run_aaa_diagnostic(data)
    # 10 + 10 + 10 / 3 = 10.0
    assert output[0]["analysis"]["composite_score"] == 10.0

def test_risk_logic_trigger():
    """Confirma que el sistema dispara alertas cuando los valores bajan de 9.0."""
    data = [{"name": "At-Risk JAC", "autonomy": 8.0, "algorithms": 12.0, "agency": 12.0}]
    output = run_aaa_diagnostic(data)
    # Al ser 8.0 en autonomía, debe generar la alerta de infraestructura
    assert "LOW_INFRASTRUCTURE_CONTROL" in output[0]["analysis"]["active_alerts"]
    assert output[0]["analysis"]["risk_level"] == "MEDIUM"

def test_json_structure_fields():
    """Verifica que el JSON generado contenga todos los campos para interoperabilidad."""
    data = [{"name": "Check JAC", "autonomy": 10, "algorithms": 10, "agency": 10}]
    output = run_aaa_diagnostic(data)
    keys = output[0].keys()
    # Deben existir estas 4 llaves maestras
    for key in ["org_id", "name", "metrics", "analysis"]:
        assert key in keys
