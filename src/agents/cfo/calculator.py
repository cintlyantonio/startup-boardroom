def calculate_breakeven(fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float) -> dict:
    """Calculates the breakeven point in units based on fixed costs, price, and variable cost.
    
    Args:
        fixed_costs: Total fixed costs (e.g., rent, salaries).
        price_per_unit: The selling price of one unit of product or service.
        variable_cost_per_unit: The variable cost to produce or deliver one unit.
    """
    if price_per_unit <= variable_cost_per_unit:
        return {
            "breakeven_units": float('inf'),
            "breakeven_explanation": "Breakeven is impossible because variable cost per unit is greater than or equal to price per unit."
        }
    
    breakeven_units = fixed_costs / (price_per_unit - variable_cost_per_unit)
    return {
        "breakeven_units": breakeven_units,
        "breakeven_explanation": f"Fixed costs ({fixed_costs}) divided by contribution margin ({price_per_unit} - {variable_cost_per_unit})."
    }

def calculate_simple_projection(units_per_month: int, price_per_unit: float, months: int, growth_rate: float = 0.0) -> list[dict]:
    """Calculates a simple month-by-month revenue projection.
    
    Args:
        units_per_month: Starting number of units sold per month.
        price_per_unit: The selling price of one unit.
        months: Number of months to project.
        growth_rate: Monthly growth rate for units sold (e.g., 0.05 for 5% growth).
    """
    projection = []
    current_units = float(units_per_month)
    
    for month in range(1, months + 1):
        revenue = current_units * price_per_unit
        projection.append({
            "month": month,
            "units": round(current_units, 2),
            "revenue": round(revenue, 2)
        })
        current_units = current_units * (1.0 + growth_rate)
        
    return projection
