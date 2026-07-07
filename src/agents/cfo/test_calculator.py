from src.agents.cfo.calculator import calculate_breakeven, calculate_simple_projection

def test_calculate_breakeven():
    result = calculate_breakeven(fixed_costs=10000.0, price_per_unit=50.0, variable_cost_per_unit=30.0)
    assert result["breakeven_units"] == 500.0
    
    result_inf = calculate_breakeven(10000.0, 30.0, 30.0)
    assert result_inf["breakeven_units"] == float('inf')

def test_calculate_simple_projection():
    result = calculate_simple_projection(units_per_month=100, price_per_unit=20.0, months=3, growth_rate=0.1)
    assert len(result) == 3
    assert result[0]["revenue"] == 2000.0
    assert result[1]["revenue"] == 2200.0
    assert result[2]["revenue"] == 2420.0
