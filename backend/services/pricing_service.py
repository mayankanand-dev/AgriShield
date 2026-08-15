def calculate_premium(area_m2: float, crop: str) -> dict:
    """
    Demo Logic: Base rate of $10 per hectare, multiplied by a crop risk factor.
    Returns a dict with premium_amount and coverage_amount.
    """
    area_ha = area_m2 / 10000.0
    
    # Simple risk factors
    risk_factors = {
        "rice": 1.5,
        "wheat": 1.0,
        "cotton": 1.8,
        "corn": 1.2,
        "sugarcane": 1.1,
    }
    
    # Default risk factor if crop not in list
    crop_lower = crop.lower() if crop else ""
    risk_factor = risk_factors.get(crop_lower, 1.2)
    
    base_rate_per_ha = 10.0
    
    premium_amount = area_ha * base_rate_per_ha * risk_factor
    
    # Demo coverage logic: 50x the premium
    coverage_amount = premium_amount * 50.0
    
    return {
        "premium_amount": round(premium_amount, 2),
        "coverage_amount": round(coverage_amount, 2)
    }
