def calculate_damage_with_resistance(damage, resistance_percent):
    return damage - damage / 100 * resistance_percent
