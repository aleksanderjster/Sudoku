from sudoku_functions import get_units



def naked_numbers(grid, candidates):
    units = get_units(grid)
    flag = False

    for unit in units:
        
        for row,col in unit:
            
            # checks if cell has only one candidate
            if len(candidates[row][col]) == 1:
                value = list(candidates[row][col])[0]       # reads value of naked candidate
                grid[row][col] = value                      # write naked candidate into sudoku grid
                candidates[row][col] = set()                # overwrite candidates of cell with empty set
                
                flag = True                                 # indicates that naked candidate found    
                
                print(f'SOLUTION:\t "Naked number" {value} in ({row}, {col})')
    
    return flag
 

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


