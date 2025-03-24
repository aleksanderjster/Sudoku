from pprint import pprint

from sudoku_collection import sudoku_grid, last_resolved_candidates
from sudoku_functions import get_boxes, get_units




def clean_candidates_except_only_possible(grid, candidates) -> bool: 
    # get list of coordinates for row, col & boxes of sud-table
    units = get_units(grid)
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
            
            print(row, num, box)
            
            for r, c in box:
                if row == r: continue   # we do nothing with candidates in same row in the box
                if {num}.issubset(candidates[r][c]):
                    print(f'SOLUTION: candidate: {num} removed in row {r} in col  {c} from candidates {candidates[r][c]}')
                    flag = True
                    candidates[r][c].remove(num)
    
    
    # #candidates array by columns
    # candidates_by_col = []
    # for col in range(9):
    #     candidates_by_col.append([candidates[row][col] for row in range(9)])
        

    
    
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
                    print(f'SOLUTION: candidate: {num} removed in row {r} in col  {c} from candidates {candidates[r][c]}')
                    flag = True
                    candidates[r][c].remove(num)
    
    return flag                
                    
                


if __name__ == '__main__':
    clean_candidates_except_only_possible(sudoku_grid, last_resolved_candidates)