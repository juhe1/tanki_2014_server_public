def same_sign(num1, num2):
    return (num1 >= 0) == (num2 >= 0)

# this function will make add_value smaller if it is too big. and it is too big if current_value + add_value is more that value_limit
def trim_add_value(current_value, add_value, value_limit):
    if abs(current_value) >= abs(value_limit):
        return 0
        
    result = add_value + (value_limit - (current_value + add_value))
    
    if current_value > 0:
        return min(add_value, result)
    else:
        return max(add_value, result)

# this function will make sub_value smaller if it is too big. and it is too big if current_value - sub_value is less that value_limit
def trim_subtract_value(current_value, sub_value, value_limit):
    if abs(current_value) <= abs(value_limit):
        return 0
        
    result = sub_value + ((current_value - value_limit) - sub_value)
    
    if current_value > 0:
        return min(sub_value, result)
    else:
        return max(sub_value, result)

# example1: map_factor_to_range(_from=10, to=20, factor=1) -> 20
# example2: map_factor_to_range(_from=10, to=20, factor=0) -> 10
def map_factor_to_range(_from, to, factor):
    return factor * (to-_from) + _from

