from sudoku_collection import last_resolved, last_resolved_candidates
from sudoku_functions import print_sudoku, get_units, get_boxes

def xyz_wing_1(grid, candidates):

    boxes = get_boxes(grid) # get boxes coordinates 
    units = get_units(grid) # get row/col/box coordinates     
    n = 0
    for box in boxes:
        box_candidates = {}
        # print(f'box {n} coordinates: {box}')
        for row, col in box:        
            key = tuple(candidates[row][col])
            if key not in box_candidates:
                box_candidates[key] = []
            box_candidates[key].append((row, col))

        # removing candidates which have more then 2 and 3 candidates
        # removing candidates which have more than 1 instance in box
        keys_to_remove = []
        for key in box_candidates.keys():
            if len(box_candidates[key]) != 1:
                keys_to_remove.append(key)
            if  len(key) != 2 and len(key) != 3:
                keys_to_remove.append(key)

        keys_to_remove = list(set(keys_to_remove))  # removing dublicates in the list.

        for key in keys_to_remove:
            box_candidates.pop(key)


        # Filtering out potential pairs of xyz wings in box
        keys_to_save = []
        for key in box_candidates.keys():
            for key2 in box_candidates.keys():
                if set(key).issubset(key2) and set(key) != set(key2):
                    keys_to_save.append([key, key2])


        # check every potential pair of xyz wing in the box for existance of yz wing.
        yz_candidates = []
        xyz_wing = []
        for wing_candidate in keys_to_save:            
            pivot_candidate = ()
            xz_wing_candidate = ()

            # filter out pivot and xz candidate for future operations
            if len(wing_candidate[0]) == 3:
                pivot_candidate = wing_candidate[0]
                xz_wing_candidate = wing_candidate[1]
            else:
                pivot_candidate = wing_candidate[1]
                xz_wing_candidate = wing_candidate[0]
            
            # print out result wing candidates in the box
            # print(f'box {n} pivot: {pivot_candidate} xz: {xz_wing_candidate}')
        

            # seek for yz wing 
            pivot_row, pivot_col = list(box_candidates[pivot_candidate])[0]
            xz_row, xz_col = list(box_candidates[xz_wing_candidate])[0]


            yz_coordinates = []
            yz_wing_candidate = {}
            yz_wing_unit = []           # list coordinates on which affects the yz wing
            # seek yz candidate in pivot row if pivot and xz not in same row.
            if pivot_row != xz_row:
                yz_wing_unit.append(units[pivot_row])
                for point in units[pivot_row]:
                    yz_coordinates.append(point)                     

            # seek yz candidate in pivot row if pivot and xz not in same row.
            if pivot_col != xz_col:
                yz_wing_unit.append(units[pivot_col + 9])
                for point in units[pivot_col + 9]:
                    yz_coordinates.append(point)
            

            # verification candidate for yz wing candidate.
            for row, col in yz_coordinates:
                yz_key_candidate = candidates[row][col]
                if yz_key_candidate == set(): continue                          # not empty candidates
                if set(yz_key_candidate) == set(pivot_candidate): continue      # not itself
                if set(yz_key_candidate) == set(xz_wing_candidate): continue    # not like as xz candidate

                # verifying candidate for yz wing
                if set(yz_key_candidate).issubset(set(pivot_candidate)):
                    yz_wing_candidate[tuple(yz_key_candidate)] = (row, col)
                    
            # forming xyz wings for box if they are
            for yz_wing_key in yz_wing_candidate.keys():
                wing = {
                    pivot_candidate: (pivot_row, pivot_col),
                    xz_wing_candidate: (xz_row, xz_col),
                    yz_wing_key: yz_wing_candidate[yz_wing_key]
                    }
                xyz_wing.append(wing)  
            
        
        if len(xyz_wing) != 3: continue     # skip step if no wings found

        # cleaning box from unnesesary candidates
        for wing in xyz_wing:
            for row, col in box:
                clean_candidate = candidates[row][col]
                if set(clean_candidate) == set(): continue              #not for empty keys
                wing_keys = wing.keys()
                if set(clean_candidate) == set(wing_keys[0]):continue
                if set(clean_candidate) == set(wing_keys[1]):continue



        # print(f'box {n} candidates: {box_candidates}')
        print(f'box {n} wings: {xyz_wing}')
        n += 1












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
        


        # =============== info =========================
        #this code could be updated with control of lis
        # keys to delete.

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

        #================================================================
        # 
        


        #================================================================
        # # creation of wing candidates in the box
        # xyz_wing_candidates = []        # list of potential xyz witngs which has pivot adn xz wing
        # for pivot_candidate_key in pivot_candidates.keys():
        #     xyz_wing_cadidate = {}      # member/element of xyz wings list
            
        #     if pivot_candidate_key not in xyz_wing_cadidate:
        #         xyz_wing_cadidate[pivot_candidate_key] = pivot_candidates[pivot_candidate_key][0]   # we get first and single candidate
                
        #     for xz_candidate_key in xz_wing_candidates.keys():
        #         if set(xz_candidate_key).issubset(set(pivot_candidate_key)):
        #             xyz_wing_cadidate[xz_candidate_key] = xz_wing_candidates[xz_candidate_key][0]   # we get first and single candidate
                    
        #     xyz_wing_candidates.append(xyz_wing_cadidate)
            
                        
        #  # list of xyz wings with one xz wing are prepeared
        # print(f'xyz_wing_candidates: {xyz_wing_candidates}')

        # for wing_candidate in xyz_wing_candidates:
        #     pivot_key = list(wing_candidate.keys())[0]
        #     pivot_row, pivot_col = wing_candidate[pivot_key]

        #     xz_wing_key = list(wing_candidate.keys())[1]
        #     xz_wing_row, xz_wing_col = wing_candidate[xz_candidate_key]

        #     yz_wing_candidate_positions = []

        #     if pivot_row != xz_wing_row:                            # if pivot and xz not in the same row
        #         yz_wing_candidate_positions = units[pivot_row]      # candidates taken from row

        #     for r, c in yz_wing_candidate_positions:
                              
        #         if len(candidates[r][c]) != 2: continue # only pair can be candidate
        #         yz_candidate = tuple(candidates[r][c])
        #         if set(yz_candidate).issubset(pivot_key) and set(yz_candidate) != set(xz_wing_key):
        #             wing_candidate[yz_candidate] = (r, c)
        #             wing_candidate['row'] = r
            
        #     if pivot_col != xz_wing_col:                             # if pivot and xz not in the same col
        #         yz_wing_candidate_positions = units[pivot_col + 9]     

        #     for r, c in yz_wing_candidate_positions:
                              
        #         if len(candidates[r][c]) != 2: continue # only pair can be candidate
        #         yz_candidate = tuple(candidates[r][c])
        #         if set(yz_candidate).issubset(pivot_key) and set(yz_candidate) != set(xz_wing_key):
        #             wing_candidate[yz_candidate] = (r, c)
        #             wing_candidate['col'] = c

        
        # print(f'[upd] xyz_wing_candidates: {xyz_wing_candidates}')





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
    
    xyz_wing_1(grid, candidates)
    
    # print(f'tmp sudoku solver start\n')
    # print_sudoku(last_resolved)
    # print_sudoku(last_resolved_candidates)
    # print(f'\ntmp sudoku solver end\n')
    pass
    
    
if __name__ == '__main__': 
    main()