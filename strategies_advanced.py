from sudoku_collection import last_resolved, last_resolved_candidates
from sudoku_functions import print_sudoku, get_units, get_boxes


def xyz_wing(grid, candidates):
    """
    ======== strategy description ============
    seek in given box for 'xyz' pivotpoint candidates.
    minimal condition for pivot point is:
        sole presense of xyz in the box
        sole presense of xz candidate in the same box
        presense yz candidate in xyz row or column
        
    if yz candidate in the row then remove z 
    from all other cells of the row except pivot point
    
    if yz candidate in column then remove z
    from all other cells of the column except pivot point
    ======== end of strategy description =======    
    """
    boxes = get_boxes(grid)     # array of row, col coordinates of cells for boxes
    units = get_units(grid)     # array of row, col coordinates of cells for rows, columns & boxes
    k = 1
    flag = False                # Flag shows status if xtz wing was found in sudoku.
    
    # check xyz strategy for every box in sudoku matrix
    for box in boxes:        
        pivot_candidates = {}           # dictionary for pivot candidates
        xz_wing_candidates = {}         # dictianary for xz wing candidates
        
        # seek for potential pivot candidates and for xz-wing candidates in the box
        for row, col in box:
            cell_candidates = candidates[row][col]
            
            # if cell has 3 candidates  it is potential xyz pivot point
            if len(cell_candidates) == 3:
                key = tuple(cell_candidates)    # xyz candidate
                
                if key not in pivot_candidates:
                    pivot_candidates[key] = []  # create new empty list of positions for unique xyz candidate
                
                pivot_candidates[key].append((row, col))
            
            
            # if cell has 2 cadidates it is potential xz wing
            if len(cell_candidates) == 2:
                key = tuple(cell_candidates)    # xz candidate
                
                if key not in xz_wing_candidates:
                    xz_wing_candidates[key] = []    # create new empty list for unique xz candidate
                    
                xz_wing_candidates[key].append((row, col))
        




        # verifying box for pivot and xz candidates
        # normalizing (removing multiple instances) of pivot candidate in dictionary
        keys = []
        for key in pivot_candidates.keys():
            coordinates_list = pivot_candidates[key]
            if len(coordinates_list) > 1:       # finding all xyz candidates presented more than ones
                keys.append(key)                # save keys list for xyz to be removed.
                
        for key in keys:
            pivot_candidates.pop(key)           # removing xyz candidates presented more than ones
        
        
        # normalizing (removing multiple instances) xz-wing candidate dictionary
        keys = []
        for key in xz_wing_candidates.keys():
            coordinates_list = xz_wing_candidates[key]
            if len(coordinates_list) > 1:       # finding all xz-wing candidates presented more than ones
                keys.append(key)
                
        for key in keys:
            xz_wing_candidates.pop(key)         # removing xz-wing candidates presented more than ones

        


        # removing pivot points candidates if no xz candidates meets
        if len(xz_wing_candidates) == 0:
            pivot_candidates = {}

        

        # We can clean up pivot and wings candidates
        if len(pivot_candidates) == 0 or len(xz_wing_candidates) == 0:
            print(f'=== box {k} has no pivots ===')
            continue
        
        xz_key_to_save = []
        pivot_key_to_save = []    
        for pivot_key in pivot_candidates.keys():   # pivot_key is potential xyz candidate
            pivot_key_status = False                

            for xz_key in xz_wing_candidates.keys():

                if not set(xz_key).issubset(pivot_key):continue
                pivot_key_status = True
                xz_key_to_save.append(xz_key)


            if pivot_key_status:
                pivot_key_to_save.append(pivot_key)
        
        # removing pivots which doesn't meet xz-wings
        pivot_keys_to_remove = [key for key in pivot_candidates.keys() if key not in pivot_key_to_save]
        for key in pivot_keys_to_remove:
            pivot_candidates.pop(key)

        # removing xz-wings which doesn't meet pivots
        xz_keys_to_remove = [key for key in xz_wing_candidates.keys() if key not in xz_key_to_save] 
        for key in xz_keys_to_remove:
            xz_wing_candidates.pop(key)
        

        print(f'pivot candidates:\t{pivot_candidates}')
        print(f'xz-wing candidates:\t{xz_wing_candidates}')
        if len(pivot_candidates) == 0 or len(xz_wing_candidates) == 0: 
            print(f'=== box {k} has no pivots ===')
            continue









        # creation of wing candidates in the box
        xyz_wing_candidates = []        
        for pivot_candidate_key in pivot_candidates.keys():
            xyz_wing_cadidate = {}
            
            if pivot_candidate_key not in xyz_wing_cadidate:
                xyz_wing_cadidate[pivot_candidate_key] = pivot_candidates[pivot_candidate_key]
                
            for xz_candidate_key in xz_wing_candidates.keys():
                if set(xz_candidate_key).issubset(set(pivot_candidate_key)):
                    xyz_wing_cadidate[xz_candidate_key] = xz_wing_candidates[xz_candidate_key]
                    
            xyz_wing_candidates.append(xyz_wing_cadidate)
            
                        
            
        print(f'xyz_wing_candidates: {xyz_wing_candidates}')











        # creation list of wing candidates in the box
        box_wing_candidates = []        
        for xz_candidate_key in xz_wing_candidates.keys():
            pivot_candidates_keys = pivot_candidates.keys()
            
            # check if xz-wing meets among pivot points
            for pivot_candidate_key in pivot_candidates_keys:

                # creation of wing candidate dictionary and adding it to wing candidates list
                if set(xz_candidate_key).issubset(pivot_candidate_key):
                    wing_candidate = {}

                    wing_candidate['pivot_key'] = pivot_candidate_key
                    wing_candidate['pivot_coordinate'] = pivot_candidates[pivot_candidate_key][0]

                    wing_candidate['xz_wing_key'] = xz_candidate_key
                    wing_candidate['xz_coordinate'] = xz_wing_candidates[xz_candidate_key][0]
                    box_wing_candidates.append(wing_candidate)
            
        



        # defined potential xyz wing candidates in the box            
        for wing_candidate in box_wing_candidates:
                       
            # print(pivot_coordinate, xz_wing_coordinate)            
            pivot_row, pivot_col = wing_candidate['pivot_coordinate']          
            
            yz_column_candidates = [row[pivot_col] for row in candidates]   # extracts col values from candidates
            yz_row_candidates = candidates[pivot_row]                    # extracts row values from candidates

            # print(f'yz_column_candidates: {yz_column_candidates}')
            # print(f'yz_row_candidates: {yz_row_candidates}')

            yz_wing_key = set()
            yz_wing_coordinate = set() 

            for row in range(9):
                yz_candidate = yz_column_candidates[row]
                if yz_candidate == wing_candidate['xz_wing_key']: break # skip if yz candidate is same as xz wing    
                if len(yz_candidate) != 2: continue    # yz candidate is pair                 
                if not set(yz_candidate).issubset(wing_candidate['pivot_key']): continue    # ya candidate is subset of pivot key
                if set(yz_candidate) == set(wing_candidate['xz_wing_key']): continue

                yz_wing_key = tuple(yz_candidate)
                yz_wing_coordinate = [(row, pivot_col)]
            
            if yz_wing_key != set():
                wing_candidate['yz_wing_key'] = yz_wing_key
                wing_candidate['yz_wing_coordinate'] = yz_wing_coordinate
                print(f'wing found:\t{wing_candidate}')

            yz_wing_key = set()
            yz_wing_coordinate = set() 

            for col in range(9):
                yz_candidate = yz_row_candidates[col]
                if yz_candidate == wing_candidate['xz_wing_key']: break # skip if yz candidate is same as xz wing         
                if len(yz_candidate) != 2: continue
                if not set(yz_candidate).issubset(wing_candidate['pivot_key']): continue
                if set(yz_candidate) == set(wing_candidate['xz_wing_key']): continue

                yz_wing_key = tuple(yz_candidate)
                yz_wing_coordinate = [(pivot_row, col)]
            
            if yz_wing_key != set():
                wing_candidate['yz_wing_key'] = yz_wing_key
                wing_candidate['yz_wing_coordinate'] = yz_wing_coordinate
                print(f'wing found:\t{wing_candidate}')


            # # seek in the row of candidates
            # for col in range(9):
            #     yz_candidate = candidates[pivot_row][col]

            #     if yz_candidate != set() and yz_candidate.issubset(set(wing_candidate['pivot_key'])):
            #         yz_wing_coordinate = (pivot_row, col)
                    
            #         if yz_wing_coordinate != xz_wing_coordinate and yz_wing_coordinate != pivot_coordinate:                    
            #             print(f'yz-wing {yz_candidate} in {yz_wing_coordinate} candidate of pivot {set(pivot)} in {pivot_coordinate} found')
            
            # for row in range(9):
            #     yz_candidate = candidates[row][pivot_col]
            #     if yz_candidate != set() and yz_candidate.issubset(set(pivot)):
            #         yz_wing_coordinate = (row, pivot_col)
                    
            #         if yz_wing_coordinate != xz_wing_coordinate and yz_wing_coordinate != pivot_coordinate:                    
            #             print(f'yz-wing {yz_candidate} in {yz_wing_coordinate} candidate of pivot {set(pivot)} in {pivot_coordinate} found')
  
        
        
                    
        # for key in xz_wing_candidates.keys():
        #     if key not in keys:
        #         xz_wing_candidates.pop(key)
        
        xz_keys_to_remove = [key for key in xz_wing_candidates.keys() if key not in keys]
        pivot_keys_to_remove = [key for key in pivot_candidates.keys() if key not in keys]
        # print(f'xz-wing candidates:{xz_wing_candidates}')
        # print(f'xz-wing keys to remove:{keys_to_remove}\n')
         
        for key in xz_keys_to_remove:
            xz_wing_candidates.pop(key)
        
        for key in pivot_keys_to_remove:
            pivot_candidates.pop(key)
        
        


        if len(pivot_candidates) == 0 or len(xz_wing_candidates) == 0:
            print(f'=== box {k} has no pivots ===')
        else:        
            print(f'=== box {k} ===')    
            print(f'pivot candidates:\t{pivot_candidates}')
            print(f'xz-wing candidates:\t{xz_wing_candidates}')
                
        k += 1
        
        
        # define z which to be deleted for candidates in box with pivot point except xz wing.
        # correct code for excluding wings where all elements are in same row/column
    
    return flag




def main():
    grid = last_resolved
    candidates = last_resolved_candidates
    
    xyz_wing(grid, candidates)
    
    # print(f'tmp sudoku solver start\n')
    # print_sudoku(last_resolved)
    # print_sudoku(last_resolved_candidates)
    # print(f'\ntmp sudoku solver end\n')
    pass
    
    
if __name__ == '__main__': 
    main()