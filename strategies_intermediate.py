from itertools import combinations

from sudoku_functions import get_units, get_boxes




"""Find and eliminate Hidden Pairs, Triples, and Quadruples."""
def hidden_pairs_tuples(grid, candidates):    
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
            
        # Identify Hidden Pairs/Tuples
        for n in range(2, 5):  # Pairs (2), Triples (3), Quadruples (4)
            possible_tuples = [nums for nums in candidate_positions if len(candidate_positions[nums]) == n]

            # Check for valid sets of N numbers appearing in N cells
            for combo in combinations(possible_tuples, n):
                affected_cells = set()
                
                for num in combo:
                    affected_cells.update(candidate_positions[num])
                
                if len(affected_cells) == n:  # Found Hidden Pair/Tuple
                    for row, col in affected_cells:
                        
                        if candidates[row][col] != set(combo):  # if cell to be updated
                            candidates[row][col] = set(combo)   # Keep only these numbers
                            print(f'SOLUTION: "Found combo" {set(combo)} in ({row}, {col}) of unit {k}')
                            flag = True
        k += 1
    return flag


"""Seek for hidden single candidate inside unit."""
def hidden_numbers(grid, candidates):    
    flag = False
    units = get_units(grid)

    
    k = 0 # unit counter
    for unit in units:
        candidate_positions = {}

        # looks through all candidate numbers in the unit:
        for row, col in unit:
            
            # iterates throgh all candidates for cell
            for num in candidates[row][col]:

                # create new empty list for number doesn't meet in dictionary
                if num not in candidate_positions:
                    candidate_positions[num] = []
                
                candidate_positions[num].append((row, col)) # adds position for candidate in unit

        # iteretes through all candidate numbers found in the unit
        for num in candidate_positions.keys():
            
            # check if number meets only ones in the unit
            if len(candidate_positions[num]) == 1:

                row, col = candidate_positions[num][0]  # defines coordinates of hidden number
                grid[row][col] = num                    # writes hidden number in the cell
                
                flag = True                             # indicates that hidden number was found

                print(f'SOLUTION: "Hidden number": {num} in ({row}, {col}) of unit {k}')
        k += 1

    return flag



""" Removes candidates from row or column if all candidates are in row
    or column of one box"""
def strike_out_row_column_candidates(grid, candidates):
    # take possibility number    
    flag = False
    
    # Returns 3x3 boxes as units.
    boxes = get_boxes(grid)
            
    
    # Defines candidates positions are met in unit/boxes
    k = 0
    for box in boxes:
        candidate_positions = {}
        
        # creates dictionary of candidates with list of their position in box
        for row, col in box:
            
            for num in candidates[row][col]:
                
                if num not in candidate_positions:
                    candidate_positions[num] = []   # create new dict instance for candidate not yet in dictionary
                    
                candidate_positions[num].append((row, col))     # fills position in set for candidate met in box
            

        # check if all candidates have equal row or column
        for num in candidate_positions.keys():
            
            row_list = []
            col_list = []
            for row, col in candidate_positions[num]:
                
                row_list.append(row)
                col_list.append(col)
            
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


""" Removes candidates from other cell in the box except 
    row or column of the box """
def clean_row_column_only_possible_in_box_candidates(grid, candidates) -> bool: 
    # get list of coordinates for row, col & boxes of sud-table
    boxes = get_boxes(grid)

    # get list of coordinates for boxes grouped by boxes in row & col.
    boxes_by_rows = [[boxes[row * 3 + col] for col in range(3)] for row in range(3)]
    boxes_by_col = [[row[col] for row in boxes_by_rows] for col in range(3)]

    flag = False
    
    # check candidates in rows as only possible in the box
    for row in range(9):
        
        # create dictionary of candidates in the row with their position
        row_candidates = {}
        for col in range(9):
            
            for num in candidates[row][col]:
                
                if num not in row_candidates:
                    row_candidates[num] = []
                    
                row_candidates[num].append((row, col))
            
        # print(f' row {row}:{row_candidates}')
        # check candidate number for belonging to different boxes    
        for num in row_candidates.keys():
            # print(row, num, len(row_candidates[num]))
            if len(row_candidates[num]) > 3: continue   # candidate meets in several boxes
            
            boxes = set()
            for r, c in row_candidates[num]:
                if 0 <= c < 3: boxes.add(0)
                if 3 <= c < 6: boxes.add(1)
                if 6 <= c < 9: boxes.add(2)
            
            # print(row, num, boxes)
            
            if len(boxes) > 1: continue                 # candidate meets in several boxes
            
            col_boxes = boxes_by_col[list(boxes)[0]]
            if 0 <= row < 3: box = col_boxes[0]
            if 3 <= row < 6: box = col_boxes[1]
            if 6 <= row < 9: box = col_boxes[2]
                        
            for r, c in box:
                if row == r: continue   # we do nothing with candidates in same row in the box
                if {num}.issubset(candidates[r][c]):
                    print(f'SOLUTION: "Row only in box" candidate: {num} removed in row {r} in col {c}')
                    flag = True
                    candidates[r][c].remove(num)

    
    # check candidates in columns as only possible in the box
    for col in range(9):
        
        # creates col candidates with their positions
        col_candidates = {}     # dictionary of coordinates for candidates in column
        for row in range(9):
            
            for num in candidates[row][col]:
                if num not in col_candidates:
                    col_candidates[num] = []
                
                col_candidates[num].append((row, col))
        
        
        # verification of candidates for box only candidates in column
        for num in col_candidates.keys():
            
            # check 1: in one box max 3 positions are available.
            if len(col_candidates[num]) > 3: continue # skip candidate numbers which are meets in more than 1 box
            
            
            #check 2: Candidate meets in in one box only
            boxes = set()
            for r, c in col_candidates[num]:
                
                if 0 <= r < 3: boxes.add(0)
                if 3 <= r < 6: boxes.add(1)
                if 6 <= r < 9: boxes.add(2)
            
            if len(boxes) > 1: continue # candidate meets in more than one box
            
            
            # check 3: is any other candidates in the box except already defined
            row_boxes = boxes_by_rows[list(boxes)[0]]
            box = []
            if 0 <= col < 3: box = row_boxes[0]
            if 3 <= col < 6: box = row_boxes[1]
            if 6 <= col < 9: box = row_boxes[2]
            

            # clean candidates if candidate found in box cells candidates
            for r, c in box:
                if col == c: continue # skip on same column as candidates for verification
                if {num}.issubset(candidates[r][c]):
                    print(f'SOLUTION: "Column only" candidate: {num} removed in row {r} in col {c}')
                    flag = True
                    candidates[r][c].remove(num)
    
    return flag
