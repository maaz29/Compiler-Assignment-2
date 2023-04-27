# LR(1) parser implementation for the given grammar

# Define the LR(1) parsing table
parsing_table = {
    0: {'id': ('s', 2), '-': None, '×': None, '$': None, 'E': ('s', 1), 'T': None},
    1: {'id': None, '-': None, '×': None, '$': 'acc', 'E': None, 'T': None},
    2: {'id': ('s', 2), '-': ('s', 5), '×': ('s', 3), '$': None, 'E': None, 'T': ('s', 4)},
    3: {'id': ('r', 5), '-': None, '×': None, '$': ('r', 5), 'E': None, 'T': None},
    4: {'id': ('r', 4), '-': ('r', 4), '×': ('s', 3), '$': ('r', 4), 'E': None, 'T': None},
    5: {'id': ('r', 3), '-': ('s', 2), '×': None, '$': ('r', 3), 'E': None, 'T': None},
}

# Define the productions of the grammar
productions = {
    0: ('S\'', 'E'),
    1: ('E', 'T - E'),
    2: ('E', 'T'),
    3: ('T', 'F × T'),
    4: ('T', 'F'),
    5: ('F', 'id'),
}

# Define the LR(1) parser function
def parse(input_string):
    # Initialize the stack and the state
    stack = [0]
    state = 0
    
    # Add the end of input marker to the input string
    input_string += '$'
    
    # Loop until the stack is empty or the input string is fully parsed
    while stack:
        # Get the current lookahead symbol
        lookahead = input_string[0] if input_string else '$'
        
        # Get the current action from the parsing table
        action = parsing_table[state][lookahead]
        
        if action is None:
            # The parsing table has no entry for the current state and lookahead symbol
            print('Error: invalid input')
            return False
        
        if action[0] == 's':
            # Shift the lookahead symbol onto the stack and update the state
            stack.append(lookahead)
            stack.append(action[1])
            input_string = input_string[1:]
            state = action[1]
        elif action[0] == 'r':
            # Reduce by the specified production and update the stack and state
            production = productions[action[1]]
            for _ in range(2 * len(production[1])):
                stack.pop()
            old_state = state
            state = stack[-1]
            stack.append(production[0])
            stack.append(parsing_table[state][production[0]][1])
            print(f'{old_state}, {input_string}: Reduce {production[1]} to {production[0]}')
        elif action[0] == 'acc':
            # Accept the input as valid
            print(f'{state}, {input_string}: Accept')
            return True
    else:
        # The stack is empty and the input string is not fully parsed
        print('Error: invalid input')
        return False

# Test the LR(1) parser with some inputs
print(f'Input: {"a b c d"}')
parse("a b c d")
print('-' * 40)