from sudoku_collection import last_resolved, last_resolved_candidates
from sudoku_functions import print_sudoku, get_units, get_boxes

def xyz_wing(grid, candidates):

    flag = False
    boxes = get_boxes(grid) # get boxes coordinates 
    units = get_units(grid) # get row/col/box coordinates     
    n = 0
    for box in boxes:
        box_candidates = {}
        xyz_wing = []

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
                    yz_wing_candidate['yz_wing'] = yz_coordinates
                    
            # forming xyz wings for box if they are
            for yz_wing_key in yz_wing_candidate.keys():
                wing = {
                    pivot_candidate: (pivot_row, pivot_col),
                    xz_wing_candidate: (xz_row, xz_col),
                    yz_wing_key: yz_wing_candidate[yz_wing_key],
                    'yz_wing': yz_wing_candidate['yz_wing'] 
                    }
                xyz_wing.append(wing)  
            
        
        # if len(xyz_wing) != 3: continue     # skip step if no wings found

        # cleaning box from unnesesary candidates
        for wing in xyz_wing:
            yz_wing_coordinates = wing['yz_wing']
            zz = 0
            pivot = list(wing.keys())[0]
            xz_wing = list(wing.keys())[1]
            yz_wing = list(wing.keys())[2]

            # defining z number to be removed from yz wing candidates for optimization
            for num in xz_wing:
                if set([num]).issubset(set(yz_wing)): zz = num
            

            # removing z from yz wing candidates
            for row, col in yz_wing_coordinates:
                to_clean_candidate = candidates[row][col]
                if set(to_clean_candidate) == set(): continue              #not for empty keys
                wing_keys = wing.keys()
                if set(to_clean_candidate) == set(pivot):continue
                if set(to_clean_candidate) == set(yz_wing):continue
                if set([zz]).issubset(set(to_clean_candidate)):
                    print(f'SOLUTION: "XYZ-Wing" - {zz} removed from candidates {candidates[row][col]} in ({row}, {col})')
                    candidates[row][col].remove(zz)
                    flag = True
                    



        # print(f'box {n} candidates: {box_candidates}')
        # print(f'box {n} wings: {xyz_wing}')
        n += 1

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