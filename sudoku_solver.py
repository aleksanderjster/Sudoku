from itertools import combinations

from sudoku_collection import sudoku_grid
from sudoku_functions import print_sudoku, clean_candidates
from strategies_simple import naked_numbers
from strategies_intermediate import hidden_numbers, hidden_pairs_tuples, strike_out_row_column_candidates
from strategies_intermediate import clean_row_column_only_possible_in_box_candidates


# seeks all available naked numbers in sudoku grid
def find_naked_numbers(grid, candidates):
    naked_numbers_found = False
    
    while True:
        status = False        
        if naked_numbers(grid, candidates):
            naked_numbers_found = True
            status = clean_candidates(grid, candidates) # True if something was removed from candidates
                    
        # no candidates were cleaned
        if not status: break

    return naked_numbers_found


# seeks all available hidden numbers in sudoku grid
def find_hidden_numbers(grid, candidates):
    hidden_number_found = False
    
    while True:
        status = False
        if hidden_numbers(grid, candidates):
            hidden_number_found = True
            status = clean_candidates(grid, candidates)
                    
        # no candidates were cleaned
        if not status: break
    
    return hidden_number_found


# seeks all hidden pairs/triples in sudoku grid
def find_hidden_pairs_tuples(grid, candidates):
    hidden_pairs_triples_found = False
    
    while True:
        status = False
        if hidden_pairs_tuples(grid, candidates):
            hidden_pairs_triples_found = True
            status = True
            
        if not status: break
    
    return hidden_pairs_triples_found



# clean candidates for row or col possible in the box
def clean_row_col_candidates_in_box(grid, candidates):
    row_col_candidates_found = False
    
    while True:
        status = False
        if clean_row_column_only_possible_in_box_candidates(grid, candidates):
            row_col_candidates_found = True
            status = True
            
        if not status: break
    
    return row_col_candidates_found


def main ():
    candidates = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in sudoku_grid]

    # Run Naked Pairs/Tuples strategy
    # candidates = naked_pairs_tuples(sudoku_grid, candidates)
    print_sudoku(sudoku_grid)

    safety_counter = 0
    
    # initial candidates cleaning
    clean_candidates(sudoku_grid, candidates) 
    
    while True:
        
        if safety_counter > 100: 
            print(f'WARNING: Emergency exit of programm!')
            break # emergency exit:
        
        safety_counter += 1
        
        loop_status = False      
        
        # runs until all naked numbers are found on this cycle
        naked_numbers_found = find_naked_numbers(sudoku_grid, candidates)
        if naked_numbers_found:
            loop_status = True
            print_sudoku(sudoku_grid)
        
        # runs until all hidden numbers are found on this cycle
        hidden_number_found = find_hidden_numbers(sudoku_grid, candidates)
        if hidden_number_found:
            loop_status = True
            print_sudoku(sudoku_grid) 
            continue        # starts loop again if hidden numbers found
        
        
        # runs until all hidden pairs/triples are found on this cycle        
        hidden_pair_tuples_found = hidden_pairs_tuples(sudoku_grid, candidates)
        if hidden_pair_tuples_found:
            loop_status = True 
            print_sudoku(candidates)
            continue   # starts loop again if hidden pairs/triples are found
        
        
        
        strike_out_candidates_found = strike_out_row_column_candidates(sudoku_grid, candidates)
        if strike_out_candidates_found:
            loop_status = True
            print_sudoku(candidates)
            continue
        
        row_col_candidates_in_box_found = clean_row_col_candidates_in_box(sudoku_grid, candidates)
        if row_col_candidates_in_box_found:
            loop_status = True
            print_sudoku(candidates)
            continue

        # XZY-Wing strategies


        if not loop_status: 
            print(f'\nINFO: All strategies fails to resolve sudoku')
            print(sudoku_grid)
            print(candidates)
            break # exits the loop if all strategies fails






if __name__ == '__main__': 
    main()