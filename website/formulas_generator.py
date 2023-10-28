import random
import math
# Generates different formulas instead of number 404 on 404 error page


def generate_formula():
    start_number = 404
    operators_list = ['+', '/', '**(1/', '**', '*', '-']
    current_operator_index = random.randrange(len(operators_list))
    current_operator = operators_list[current_operator_index]
    current_opposite_operator = operators_list[-current_operator_index-1]
    if current_operator_index == 3: # if action is **
        action_number = random.randrange(1, 3)
    else:
        action_number = random.randrange(1, 10)
    if current_operator_index == 2: # if action is root
        action = f'{start_number} {current_operator}{action_number})'
    else:
        action = f'{start_number} {current_operator} {action_number}'
    result = round(eval(action), 2)
    if current_operator_index == 2:
        current_formula = f'{result}^{action_number}'
    elif current_operator_index == 3 and action_number == 2:
        current_formula = f'{chr(253)}√{result}'
    elif current_operator_index == 3 and action_number == 3:
        current_formula = f'{chr(252)}√{result}'
    elif current_operator_index == 3 and action_number == 1:
        current_formula = f'{result}'
    else:
        current_formula = f'{result} {current_opposite_operator} {action_number}'
    return current_formula
