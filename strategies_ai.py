# to be verified and checked.
def find_xyz_wing(grid, candidates):
    """
    Identifies and applies the XYZ-Wing technique to eliminate candidates.
    :param grid: 9x9 Sudoku grid with 0 for unknown values.
    :param candidates: A dictionary mapping (row, col) -> set of possible values.
    :return: True if any elimination is made, False otherwise.
    """
    eliminations = False
    
    for (r, c), xyz in candidates.items():
        if len(xyz) == 3:  # Look for pivot cell with three candidates (X, Y, Z)
            xyz_list = list(xyz)
            
            # Find potential pincers (XY and XZ cells)
            for (r1, c1), xy in candidates.items():
                if len(xy) == 2 and set(xy).issubset(xyz) and (r, c) != (r1, c1):
                    for (r2, c2), xz in candidates.items():
                        if len(xz) == 2 and set(xz).issubset(xyz) and (r, c) != (r2, c2) and (r1, c1) != (r2, c2):
                            
                            # Check if both pincers and pivot share a unit (row, column, or box)
                            if shares_unit((r, c), (r1, c1)) and shares_unit((r, c), (r2, c2)):
                                common_candidate = xy.intersection(xz)
                                if len(common_candidate) == 1:
                                    x = common_candidate.pop()
                                    
                                    # Find cells that see both pincers and remove X
                                    for (er, ec) in intersecting_peers((r1, c1), (r2, c2)):
                                        if x in candidates.get((er, ec), set()):
                                            candidates[(er, ec)].remove(x)
                                            eliminations = True
                                            print(f"XYZ-Wing: Removed {x} from ({er}, {ec})")
    
    return eliminations

def find_xy_wing(grid, candidates):
    """
    Identifies and applies the XY-Wing technique (both right-angled and non-right-angled).
    :param grid: 9x9 Sudoku grid with 0 for unknown values.
    :param candidates: A dictionary mapping (row, col) -> set of possible values.
    :return: True if any elimination is made, False otherwise.
    """
    eliminations = False
    
    for (r, c), pivot in candidates.items():
        if len(pivot) == 2:  # Look for a pivot cell with exactly two candidates (X, Y)
            x, y = pivot
            
            # Find potential pincers (XY and YZ cells)
            for (r1, c1), xy in candidates.items():
                if (r1, c1) != (r, c) and xy == {x, y} and shares_unit((r, c), (r1, c1)):
                    for (r2, c2), yz in candidates.items():
                        if (r2, c2) != (r, c) and (r2, c2) != (r1, c1) and yz == {y, z} and shares_unit((r, c), (r2, c2)):
                            
                            if shares_unit((r1, c1), (r2, c2)):
                                # Valid XY-Wing structure
                                for (er, ec) in intersecting_peers((r1, c1), (r2, c2)):
                                    if x in candidates.get((er, ec), set()):
                                        candidates[(er, ec)].remove(x)
                                        eliminations = True
                                        print(f"XY-Wing: Removed {x} from ({er}, {ec})")
    
    return eliminations

def shares_unit(cell1, cell2):
    """Returns True if two cells share a row, column, or box."""
    r1, c1 = cell1
    r2, c2 = cell2
    return r1 == r2 or c1 == c2 or (r1 // 3 == r2 // 3 and c1 // 3 == c2 // 3)

def intersecting_peers(cell1, cell2):
    """Finds cells that are peers of both cell1 and cell2."""
    r1, c1 = cell1
    r2, c2 = cell2
    return {(r, c) for r in range(9) for c in range(9) if shares_unit(cell1, (r, c)) and shares_unit(cell2, (r, c))}




def find_xyz_wing(grid, candidates):
    """
    Identifies and applies the XYZ-Wing technique to eliminate candidates.
    :param grid: 9x9 Sudoku grid with 0 for unknown values.
    :param candidates: A dictionary mapping (row, col) -> set of possible values.
    :return: True if any elimination is made, False otherwise.
    """
    eliminations = False
    
    for (r, c), xyz in candidates.items():
        if len(xyz) == 3:  # Look for pivot cell with three candidates (X, Y, Z)
            xyz_list = list(xyz)
            
            # Find potential pincers (XY and XZ cells)
            for (r1, c1), xy in candidates.items():
                if len(xy) == 2 and set(xy).issubset(xyz) and (r, c) != (r1, c1):
                    for (r2, c2), xz in candidates.items():
                        if len(xz) == 2 and set(xz).issubset(xyz) and (r, c) != (r2, c2) and (r1, c1) != (r2, c2):
                            
                            # Check if both pincers and pivot share a unit (row, column, or box)
                            if shares_unit((r, c), (r1, c1)) and shares_unit((r, c), (r2, c2)):
                                common_candidate = xy.intersection(xz)
                                if len(common_candidate) == 1:
                                    x = common_candidate.pop()
                                    
                                    # Find cells that see both pincers and remove X
                                    for (er, ec) in intersecting_peers((r1, c1), (r2, c2)):
                                        if x in candidates.get((er, ec), set()):
                                            candidates[(er, ec)].remove(x)
                                            eliminations = True
                                            print(f"XYZ-Wing: Removed {x} from ({er}, {ec})")
    
    return eliminations

def shares_unit(cell1, cell2):
    """Returns True if two cells share a row, column, or box."""
    r1, c1 = cell1
    r2, c2 = cell2
    return r1 == r2 or c1 == c2 or (r1 // 3 == r2 // 3 and c1 // 3 == c2 // 3)

def intersecting_peers(cell1, cell2):
    """Finds cells that are peers of both cell1 and cell2."""
    r1, c1 = cell1
    r2, c2 = cell2
    return {(r, c) for r in range(9) for c in range(9) if shares_unit(cell1, (r, c)) and shares_unit(cell2, (r, c))}
