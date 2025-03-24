from itertools import combinations



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

def get_boxes(grid):
    # Returns 3x3 boxes as units.
    units = []
    # 3x3 Boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            units.append([(box_row + i, box_col + j) for i in range(3) for j in range(3)])

    return units

    
# prints 2D matrix as table.
def print_sudoku(mtrx):
    print(f'\n========== Sudoku ============\n')
    str = ''
    for i in range(9):       
        for j in range(9):
            if mtrx[i][j] == 0:
                str = str + f'_ '
            else:
                str = str + f'{mtrx[i][j]} '
            if j == 2 or j == 5:
                str = str + f'|| '
            else:
                str = str + f' '
        if i == 3 or i == 6:
            print(f'=============================')
        print(str)
        str = ''
    print('\n')






def naked_pairs_tuples(grid, candidates):
    """Find and eliminate Naked Pairs, Triples, and Quadruples from candidates."""
    flag = False
    units = get_units(grid)
    
    for unit in units:
        value_counts = {}  # Dictionary to track candidate sets
        
        # Count occurrences of each candidate set
        for row, col in unit:
            if len(candidates[row][col]) > 1:  # Only check multi-value cells
                key = tuple(sorted(candidates[row][col]))  # Convert to tuple
                value_counts[key] = value_counts.get(key, []) + [(row, col)]
        
        # Process Naked Pairs/Tuples
        for key, cells in value_counts.items():
            if len(cells) == len(key):  # Naked Pair/Triple/etc. found
                print(f'Solution: Found naked combination {key} for cells {cells}')
                for row, col in unit:
                    if (row, col) not in cells:
                        # Remove the Naked Pair/Tuple values from other cells
                        print(f'INFO: {set(key)} removed from {candidates[row][col]} of ({row}, {col})')
                        candidates[row][col] -= set(key)
                        flag = True
                        
    
    return flag


def hidden_pairs_tuples(grid, candidates):
    """Find and eliminate Hidden Pairs, Triples, and Quadruples."""
    units = get_units(grid)  # Rows, Columns, and Boxes
    flag = False

    k = 0
    for unit in units:
        candidate_positions = {}  # Dictionary to track occurrences
        
        # Count occurrences of each candidate in the unit
        for row, col in unit:
            for num in candidates[row][col]:
                if num not in candidate_positions:
                    candidate_positions[num] = []
                candidate_positions[num].append((row, col))

        # print(f'candidate positions')
        # print(candidate_positions)
            
        # Identify Hidden Pairs/Tuples
        for n in range(2, 5):  # Pairs (2), Triples (3), Quadruples (4)
            possible_tuples = [nums for nums in candidate_positions if len(candidate_positions[nums]) == n]

            # print(f'possible_tuples for n= {n}')
            # print(possible_tuples)

            # Check for valid sets of N numbers appearing in N cells
            for combo in combinations(possible_tuples, n):
                # print(f'combo for n= {n}')
                # print(combo)

                affected_cells = set()
                for num in combo:
                    affected_cells.update(candidate_positions[num])

                # print(f'affected cells')
                # print(affected_cells)
                
                if len(affected_cells) == n:  # Found Hidden Pair/Tuple
                    for row, col in affected_cells:
                        candidates[row][col] = set(combo)  # Keep only these numbers
                        # print(f'INFO: Found combo {set(combo)} in ({row}, {col}) of unit {k}')
                        flag = True
        k += 1
    return flag


def clean_unit_candidates(value, unit, candidates):
    flag = False
    for row, col in unit:
        if value in candidates[row][col]:
            candidates[row][col].remove(value)
            flag = True

    return flag


def clean_candidates(grid, candidates):
    """Find and eliminate candidates, from candidates for defined grid numbers."""
    flag = False
    units = get_units(grid)

    for unit in units:
        for row, col in unit:
            value = grid[row][col]
            if value > 0:
                candidates[row][col] = set() # removes 
                if clean_unit_candidates(value, unit, candidates):
                    flag = True
     
    
    return flag


def write_hidden_numbers(grid, candidates):
    """Seek for single candidate inside unit."""
    flag = False
    units = get_units(grid)

    
    k = 0 # unit counter
    for unit in units:
        candidate_positions = {}

        # looks through all candidate numbers in the unit:
        for row, col in unit:
            for num in candidates[row][col]:

                # create new empty list for 
                if num not in candidate_positions:
                    candidate_positions[num] = []
                
                candidate_positions[num].append((row, col))

        # print(f'INFO: {candidate_positions}')
        
        for num in candidate_positions.keys():

            # print(f'INFO: in unit {k} for {num} len= {len(candidate_positions[num])}')
            
            if len(candidate_positions[num]) == 1:

                row, col = candidate_positions[num][0]
                grid[row][col] = num
                #candidates[row][col].clear()
                flag = True

                print(f'Solution: Found hidden single  number: {num} in ({row}, {col}) of unit {k}')
        k += 1

    return flag


def write_naked_numbers(grid, candidates):
    units = get_units(grid)
    flag = False

    for unit in units:
        for row,col in unit:
            if len(candidates[row][col]) == 1:
                value = list(candidates[row][col])[0]     # reads value of naked candidate
                grid[row][col] = value      # write naked candidate into sudoku grid
                candidates[row][col] = set()        # overwrite candidates with empty set
                print(f'Solution: Found naked single {value} in ({row}, {col})')
                flag = True
    
    return flag
    

def strike_out_candidates(grid, candidates):
    # take possibility number    
    flag = False
    
    # Returns 3x3 boxes as units.
    # units = []
    # # 3x3 Boxes
    # for box_row in range(0, 9, 3):
    #     for box_col in range(0, 9, 3):
    #         units.append([(box_row + i, box_col + j) for i in range(3) for j in range(3)])
    units = get_boxes(grid)        
    
    # Defines candidates positions are met in unit/boxes
    k = 0
    for unit in units:
        candidate_positions = {}
        
        for row, col in unit:
            
            for num in candidates[row][col]:
                
                if num not in candidate_positions:
                    candidate_positions[num] = []
                    
                candidate_positions[num].append((row, col))     # fills position in set for candidate met in box
            

        # check if all candidates have equal row or column
        for num in candidate_positions.keys():
            
            row_list = []
            col_list = []
            for row, col in candidate_positions[num]:
                
                row_list.append(row)
                col_list.append(col)
            # print(f'\n row list is {row_list}')
            # print(f'\n col list is {col_list}')
            
            # number met in one row of the box    
            if len(set(row_list)) == 1:
                print(f'INFO: Found number {num} in box {k} is row {row} strike')
                
                # iteration through all cells in row
                row = row_list[0]
                for col in range(9):
                    
                    # if column not in strike set
                    if col not in col_list:
                        if num in candidates[row][col]:
                            candidates[row][col].remove(num)
                            flag = True
            
            # number met in one col of the box    
            if len(set(col_list)) == 1:
                print(f'INFO: Found number {num} in box {k} is column {col} strike')
                
                # iteration through all cells in column
                col = col_list[0]
                for row in range(9):
                    
                    if row not in row_list:
                        if num in candidates[row][col]:
                            candidates[row][col].remove(num)
                            flag = True

        k += 1

    return flag


def clean_xyz_wing(grid, candidates):
    flag = False        # flag for identication of xyz wing is found

    # get array of boxes
    units = get_boxes(grid)

    # for every box define cells with triple xyz candidates
    for unit in units:
        xyz = {}        # array for candidates to xyz-wing pivot points
        xz = {}         # array for candidates to x-wing

        for row, col in unit:
            key = tuple(candidates[row][col])

            # 
            if len(key) == 3:                
                if key not in xyz:
                    xyz[key] = []               # if combination with this key is not exist new list is created
                xyz[key].append((row, col))     # position of combination writes in dictionnary

            if len(key) == 2:
                if key not in xz:
                    xz[key] = []
                xz[key].append((row, col))

        print(f'xyz: {xyz}\t xz: {xz}')

        
    # seek in same bax for xz (X-Wing) or yz (Y-Wing) pairs
    # if xz or yz is found let xyz to be a pivot cell
    # in corresponding row/col of pivot cell seek for corresponding wing pair
    # if other wing pair found and it is not in same row/col as the other wing then
    # remove Z from candidates to all cells in the box except XYZ and XZ cells
    # remove Z from candidates in Y-wing
    
    
    
    return flag







# Example of initializing a candidate matrix
# Each empty cell contains {1-9}, filled cells have an empty set
# sudoku_grid = [
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],

#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],

#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0]
#     ]

# sudoku resolved successfully
# sudoku_grid = [
#         [0, 0, 0,  2, 0, 0,  0, 4, 0],
#         [0, 8, 7,  0, 3, 0,  0, 0, 5],
#         [0, 6, 0,  1, 0, 0,  9, 0, 0],
        
#         [5, 0, 0,  9, 0, 0,  0, 0, 1],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [8, 0, 0,  0, 0, 3,  0, 0, 7],
        
#         [0, 0, 3,  0, 0, 5,  0, 8, 0],
#         [6, 0, 0,  0, 4, 0,  5, 2, 0],
#         [0, 4, 0,  0, 0, 6,  0, 0, 0]
#     ]

# sudoku resolved successfully
# sudoku_grid = [
#         [0, 0, 8,  3, 9, 0,  0, 4, 0],
#         [0, 0, 0,  7, 0, 0,  1, 6, 0],
#         [0, 0, 2,  1, 0, 0,  0, 0, 9],
        
#         [8, 1, 0,  0, 0, 0,  0, 0, 4],
#         [4, 0, 5,  0, 0, 0,  6, 0, 2],
#         [6, 0, 0,  0, 0, 0,  0, 7, 1],
        
#         [2, 0, 0,  0, 0, 7,  5, 0, 0],
#         [0, 7, 1,  0, 0, 8,  0, 0, 0],
#         [0, 4, 0,  0, 2, 3,  7, 0, 0]
#     ]

sudoku_grid = [
        [0, 0, 8,  0, 0, 0,  0, 3, 0],
        [0, 0, 0,  2, 4, 0,  1, 0, 0],
        [0, 0, 0,  0, 0, 6,  0, 8, 0],

        [4, 2, 0,  5, 0, 0,  0, 0, 0],
        [6, 0, 0,  9, 0, 2,  0, 7, 0],
        [0, 0, 0,  0, 3, 0,  8, 0, 0],

        [7, 4, 9,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  7, 6, 0],
        [1, 0, 0,  0, 0, 0,  5, 0, 0]
    ]

# # most hardest sudoku
# sudoku_grid = [
#         [8, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 3,  6, 0, 0,  0, 0, 0],
#         [0, 7, 0,  0, 9, 0,  2, 0, 0],

#         [0, 5, 0,  0, 0, 7,  0, 0, 0],
#         [0, 0, 0,  0, 4, 5,  7, 0, 0],
#         [0, 0, 0,  1, 0, 0,  0, 3, 0],

#         [0, 0, 1,  0, 0, 0,  0, 6, 8],
#         [0, 0, 8,  5, 0, 0,  0, 1, 0],
#         [0, 9, 0,  0, 0, 0,  4, 0, 0]
#     ]

candidates = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in sudoku_grid]

# Run Naked Pairs/Tuples strategy
# candidates = naked_pairs_tuples(sudoku_grid, candidates)
print_sudoku(sudoku_grid)


safety_counter = 0

while True:
    loop_status = False
    clean_candidates(sudoku_grid, candidates) # initial candidates cleaning
    

    # runs until naked singles are found
    while True:

        status = False        
        if write_naked_numbers(sudoku_grid, candidates):
            status = clean_candidates(sudoku_grid, candidates) # True if something cleaned
            loop_status = status
            print_sudoku(sudoku_grid)

        
        # no candidates were cleaned
        if not status: break
    
    
    # loop_status = clean_candidates(sudoku_grid, candidates)

    while True:
        status = False
        if write_hidden_numbers(sudoku_grid, candidates):
            status = clean_candidates(sudoku_grid, candidates)
            loop_status = status
            print_sudoku(sudoku_grid)
        
        # no candidates were cleaned
        if not status: break



    
    hidden_pairs_tuples(sudoku_grid, candidates)
    
    while True:
        status = strike_out_candidates(sudoku_grid, candidates)
        if status: loop_status = status        
        if not status: break

    
    
    print(f'Safety factor {safety_counter}')
    if not loop_status: 
        print_sudoku(sudoku_grid)
        break

    safety_counter += 1

    if safety_counter > 100: 
        print(f'WARNING: Emergency exit of programm!')
        break # emergency exit:
    

# while True:
#     tatus = naked_pairs_tuples(sudoku_grid, candidates)
#     if status == False: break

# for candidate in candidates:
#     print(candidate)

# candidates = hidden_pairs_tuples(sudoku_grid, candidates)

# print_sudoku(sudoku_grid)

for candidate in candidates:
    print(candidate)

for line in sudoku_grid:
    print(line)

clean_xyz_wing(sudoku_grid, candidates)
# clean_candidates(sudoku_grid, candidates)

# print('\n\n')
# for candidate in candidates:
#     print(candidate)