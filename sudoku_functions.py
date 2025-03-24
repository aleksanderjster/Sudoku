    
# prints 2D matrix as table.
def print_sudoku(grid):
    print(f'\n========== Sudoku ============\n')
    str = ''
    for i in range(9):       
        for j in range(9):
            if grid[i][j] == 0:
                str = str + f'_ '
            else:
                str = str + f'{grid[i][j]} '
            if j == 2 or j == 5:
                str = str + f'|| '
            else:
                str = str + f' '
        if i == 3 or i == 6:
            print(f'=============================')
        print(str)
        str = ''
    print('\n')

# create list of coordinates for rows, columns and boxes
def get_units(grid):
    """Returns all rows, columns, and 3x3 boxes as units."""
    units = []
    
    # Rows
    for row in range(9):
        units.append([(row, col) for col in range(9)])
    
    # Columns
    for col in range(9):
        units.append([(row, col) for row in range(9)])
    
    # 3x3 Boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            units.append([(box_row + i, box_col + j) for i in range(3) for j in range(3)])
    
    return units

# create list of coordinates for boxes
def get_boxes(grid):
    units = []
    
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            units.append([(box_row + i, box_col + j) for i in range(3) for j in range(3)])
            
    return units

# take out value from all candidates in given unit
def clean_unit_candidates(value, unit, candidates):
    flag = False
    
    for row, col in unit:
        
        if value in candidates[row][col]:
            candidates[row][col].remove(value)
            flag = True     # indicates that removing value is found among candidates

    return flag

# Find and eliminate candidates, from candidates for defined grid numbers in units
def clean_candidates(grid, candidates):
    flag = False
    units = get_units(grid)

    for unit in units:
        
        for row, col in unit:
            value = grid[row][col]
            
            if value > 0:
                candidates[row][col] = set() # removes all candidates from defined sudoku cell
                
                # removes value of the cell from all unit candidates
                if clean_unit_candidates(value, unit, candidates):
                    flag = True     # indicates that removing value is found among candidates
     
    
    return flag
