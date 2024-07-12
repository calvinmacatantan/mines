import typing
import doctest


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible")
    # ^ Uses only default game keys. If you modify this you will need
    # to update the docstrings in other functions!
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION

def is_visible(game, row, col):
    """
    Returns whether the given location is visible
    """
    return game["visible"][row][col]


def is_bomb(game, row, col):
    """
    Returns whether there is a bomb or not at the given location
    """
    return game["board"][row][col] == "."


around = (-1, 0, 1)


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    dimensions = (nrows, ncolumns)

    return new_game_nd(dimensions, mines)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """
    coordinates = (row, col)
    return dig_nd(game, coordinates)


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = {'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}
    >>> render_2d_locations(game, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations(game, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, all_visible)


def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    locations = render_2d_locations(game, all_visible)
    nrow, mcol = game["dimensions"]
    board = ""
    for row in range(nrow):
        for col in range(mcol):
            board += locations[row][col]
        if row is not nrow - 1:
            board += "\n"

    return board


# N-D IMPLEMENTATION


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """

    def create_board(dim):
        """
        returns board
        dim: a tuple of arbitrary length
        """
        if len(dim) == 1:
            return [0 for _ in range(dim[0])]
        else:
            return [create_board(dim[1:]).copy() for _ in range(dim[0])]

    def create_visible(dim):
        """
        returns board
        dim: a tuple of arbitrary length
        """
        if len(dim) == 1:
            return [False for _ in range(dim[0])]
        else:
            return [create_visible(dim[1:]).copy() for _ in range(dim[0])]

    def assign_mine(board, mine_loc):
        """
        board: a list representation of the minesweeper board
        mine_loc: a tuple of arbitraty length containing the coordinates of a mine
        """
        if len(mine_loc) == 1:
            board[mine_loc[0]] = "."
        else:
            assign_mine(board[mine_loc[0]], mine_loc[1:])

    # new board
    board = create_board(dimensions)

    # sets mines in board
    for location in mines:
        assign_mine(board, location)

    # creates board of tile visibility
    visible = create_visible(dimensions)

    # sets values for all tiles adjacent to mines
    for location in mines:
        for coordinate in get_neighbors(location, dimensions):
            value = get_value(coordinate, board)
            if value != ".":
                set_value(coordinate, board, value + 1)

    return {
        "dimensions": dimensions,
        "board": board,
        "visible": visible,
        "state": "ongoing",
        "mines": len(mines),
        "not_visible": len(get_all_coordinates(dimensions)),
    }


def get_all_coordinates(dimensions):
    """
    returns a set of all the coordinates given a bound of dimensions
    in the form of a tuple
    """
    # lower bound coordinates are 0
    # upper bound coordinates are the dimensions of the board, minus one
    dim_bound = tuple(val - 1 for val in dimensions)

    coordinates = {dim_bound}

    to_visit = {dim_bound}

    while to_visit:
        to_add = set()
        for i, dim in enumerate(dimensions):
            for coord in to_visit:
                minus = coord[i] - 1
                if 0 <= minus < dim:
                    to_add.add(coord[:i] + (minus,) + coord[i + 1 :])
        coordinates |= to_visit
        to_visit = to_add.copy()

    return coordinates


def get_neighbors(coordinate, dimensions):
    """
    returns the neighbors of a given coordinate in the form of a tuple and
    dimensional bounds in the form of a tuple
    """
    to_visit = {coordinate}
    neighbors = set()
    for i in range(len(coordinate) - 1):
        for coord in to_visit:
            minus = coord[i] - 1
            plus = coord[i] + 1
            if minus in range(dimensions[i]):
                neighbors.add(coord[:i] + (minus,) + coord[i + 1 :])
            if plus in range(dimensions[i]):
                neighbors.add(coord[:i] + (plus,) + coord[i + 1 :])
        to_visit |= neighbors
    i = len(coordinate) - 1
    for coord in to_visit:
        minus = coord[i] - 1
        plus = coord[i] + 1
        if minus in range(dimensions[i]):
            neighbors.add(coord[:i] + (minus,) + coord[i + 1 :])
        if plus in range(dimensions[i]):
            neighbors.add(coord[:i] + (plus,) + coord[i + 1 :])
    to_visit |= neighbors
    return neighbors


def get_value(coordinate, iterable):
    """
    returns the value of an n dimensional iterable given
    a coordinate in the form of a tuple with n elements
    """
    if len(coordinate) == 1:
        return iterable[coordinate[0]]
    else:
        return get_value(coordinate[1:], iterable[coordinate[0]])


def set_value(coordinate, iterable, value):
    """
    sets the value of an n dimensional iterable at a given
    coordinate in the form of a tuple with n elements
    """
    if len(coordinate) == 1:
        iterable[coordinate[0]] = value
    else:
        return set_value(coordinate[1:], iterable[coordinate[0]], value)


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    all_coordinates = get_all_coordinates(game["dimensions"])

    game["mines"] = 0
    game["not_visible"] = 0
    for coord in all_coordinates:
        if get_value(coord, game["board"]) == ".":
            game["mines"] += 1
        if get_value(coord, game["visible"]) is False:
            game["not_visible"] += 1

    def _dig_nd(coordinates):
        if game["state"] == "defeat" or game["state"] == "victory":
            return 0

        # if we find a mine
        if get_value(coordinates, game["board"]) == ".":
            set_value(coordinates, game["visible"], True)
            game["not_visible"] -= 1
            game["state"] = "defeat"
            return 1

        # if it was not visible before -> make it visible
        # else do nothing
        if get_value(coordinates, game["visible"]) is False:
            set_value(coordinates, game["visible"], True)
            game["not_visible"] -= 1
            revealed = 1
        else:
            return 0

        # if the value we dig is empty and has no bombs around it
        if get_value(coordinates, game["board"]) == 0:
            # look at neighbors
            for neighbor in get_neighbors(coordinates, game["dimensions"]):
                # if the value is not a bomb and it was not visible before
                # if get_value(neighbor, game["board"]) != ".":
                if get_value(neighbor, game["visible"]) is False:
                    # apply the dig function to it and add what we revealed to it
                    revealed += _dig_nd(neighbor)

        num_revealed_squares = game["not_visible"] - game["mines"]

        game["state"] = "ongoing" if num_revealed_squares > 0 else "victory"

        return revealed

    return _dig_nd(coordinates)


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    def create_render(dim):
        """
        returns board
        dim: a tuple of arbitrary length
        """
        if len(dim) == 1:
            return [0 for _ in range(dim[0])]
        else:
            return [create_render(dim[1:]).copy() for _ in range(dim[0])]

    render = create_render(game["dimensions"])
    all_coordinates = get_all_coordinates(game["dimensions"])

    def translate(val):
        if val == 0:
            return " "
        elif val == ".":
            return val
        else:
            return str(val)

    for coord in all_coordinates:
        visibility = get_value(coord, game["visible"]) or all_visible
        set_value(
            coord,
            render,
            translate(get_value(coord, game["board"])) if visibility else "_",
        )

    return render


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
    # game = new_game_nd((3, 3, 2), [(1, 2, 0)])
    # print(game)
    # print(get_value((0, 0, 0), game))
    # game = new_game_nd((2, 4, 2), [(0,0,0)])
    # print(game['visible'])
    # print(get_value((0, 1, 0), game['visible']))
    # set_value((0,1,0),game['visible'], 5)
    # print(game['visible'])
    # print(get_value((0, 1, 0), game['visible']))

    # def get_neighbors(coordinate, dimensions):
    #     to_visit = {coordinate}
    #     neighbors = set()
    #     for i in range(len(coordinate)-1):
    #         for coord in to_visit:
    #             minus = coord[i] - 1
    #             plus = coord[i] + 1
    #             if minus in range(dimensions[i]):
    #                 neighbors.add(coord[:i] + (minus,) + coord[i+1:])
    #             if plus in range(dimensions[i]):
    #                 neighbors.add(coord[:i] + (plus,) + coord[i+1:])
    #         to_visit |= neighbors
    #     i = len(coordinate)-1
    #     for coord in to_visit:
    #         minus = coord[i] - 1
    #         plus = coord[i] + 1
    #         if minus in range(dimensions[i]):
    #             neighbors.add(coord[:i] + (minus,) + coord[i+1:])
    #         if plus in range(dimensions[i]):
    #             neighbors.add(coord[:i] + (plus,) + coord[i+1:])
    #     to_visit |= neighbors
    #     return neighbors
    # print(get_neighbors((5, 13, 0), (10, 20, 3)))
    # coords = get_all_coordinates((10, 20, 3))
    # print(coords)
    # print(len(coords))
