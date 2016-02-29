import itertools

def n_queens(n):
    """Return a solution to the n-queens problem for an nxn board.
    This uses E. Pauls' explicit solution, which solves n > 3.
    A solution is possible for all n > 3 and n = 1.

    Pauls' solution gives back 1-based indices, and we want 0-based, so all
    points have an extra -1 from the original.

    :n: A nonnegative integer.
    :returns: A list of solutions, where the solutions are a list of 2-tuples
              representing points, where the origin is in the upper-left of the
              board, the positive x-axis to the right, and the positive y-axis
              below.
        [[(x0, y0), (x1, y1), ...], [(x'0, y'0), ...]]

    """

    if n < 0:
        raise ValueError("cannot place negative queens on a board")

    if n == 0 or n == 2 or n == 3:
        return []

    fix = lambda x, y: (x - 1, y - 1)
    mod = n % 6
    if mod == 0 or mod == 4:
        # n is even, so we may integer divide by 2.
        A1 = [(2*k, k) for k in range(1, n//2+1)]
        A2 = [(2*k - 1, n//2 + k) for k in range(1, n//2+1)]
        return [fix(x, y) for (x, y) in A1 + A2]
    elif mod == 1 or mod == 5:
        # n is odd, so we may integer divide n - 1 by 2.
        B1 = [(n, 1)]
        B2 = [(2*k, k + 1) for k in range(1, (n-1)//2 + 1)]
        B3 = [(2*k - 1, (n+1)//2 + k) for k in range(1, (n-1)//2 + 1)]
        return [fix(x, y) for (x, y) in B1 + B2 + B3]
    elif mod == 2:
        # n is even, so we may integer divide by 2.
        C1 = [(4, 1)]
        C2 = [(n, n//2 - 1)]
        C3 = [(2, n//2)]
        C4 = [(n-1, n//2 + 1)]
        C5 = [(1, n//2 + 2)]
        C6 = [(n - 3, n)]
        C7 = [(n - 2*k, k + 1) for k in range(1, n//2 - 2)]
        C8 = [(n - 2*k - 3, n//2 + k + 2) for k in range(1, n//2 - 2)]
        return [fix(x, y) for (x, y) in C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8]
    elif mod == 3:
        return [fix(x, y) for (x, y) in [(n, n)] + n_queens(n - 1)]

    return []

def n_queens_comb(n):
    """Return a solution to the n-queens problem for an nxn board.
    This uses the combinatoric brute force solution.

    :n: Nonnegative integer.
    :returns: See n_queens().

    """
    board = itertools.product(range(n), range(n))
    is_good = True

    for queens in itertools.combinations(board, n):
        is_good = True
        for point in queens:
            effective = [q for q in queens if q != point]
            if is_guarded(point, effective, n):
                is_good = False
                break

        if is_good:
            return queens

    return []

def n_queens_bt(n):
    """Return a solution to the n-queens problem for an nxn board.
    This uses the naive backtracking solution.

    :n: A nonnegative integer.
    :returns: See n_queens() for a description.

    """
    queens = []
    row, col = 0, 0

    while len(queens) != n:
        if not is_guarded((row, col), queens, n):
            # This point is safe, so place a queen and start at the beginning
            # of the next row.
            queens.append((row, col))
            row += 1
            col = 0
        else:
            while col == n - 1:
                # At the end of the current row; have to backtrack until we can
                # place a new queen.
                try:
                    row, col = queens.pop()
                except IndexError:
                    # We went back to the first row and were at the end, so
                    # there are no solutions possible.
                    return []

            # We aren't at the end or in a safe spot, so move to the next point.
            col += 1

    return queens

def is_guarded(point, queens,  n):
    """Check if a given point is guarded by any queens in a given list.

    A point is guarded iff there are any queens in `queens` that are on the
    same row or column, or are on the same sum or difference diagonals.

    :queens: A list of (row, col) points where queens are on the board.
    :point: A (row, col) point to check.
    :n: A nonnegative integer denoting the size of the board.

    """
    # There are probably a couple different ways to do this.
    #
    # For now, this is the naive "look if any points that could attack us are
    # in the list" method.
    row, col = point

    for queen in queens:
        queen_row, queen_col = queen
        # Check the rows and columns.
        if queen_row == row or queen_col == col:
            return True

        # Check the sum and difference diagonals.
        if (queen_row + queen_col == row + col or
            queen_row - queen_col == row - col):
            return True

    return False

def check_solution(queens, n):
    if (n == 2 or n == 3) and len(queens) == 0:
        # n = 2, 3 has no solution.
        return True

    if len(queens) != n:
        return False

    for queen in queens:
        split = [x for x in queens if x != queen]
        if is_guarded(queen, split, n):
            return False

    return True

def print_solution(queens, n):
    print("--"*n + "-")
    for row in range(n):
        for col in range(n):
            print("|{}".format("Q" if (row, col) in queens else " "),
                  end="")
        print("|\n" + "--"*n + "-")
