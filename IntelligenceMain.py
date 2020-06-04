import operator
import collections
import random
import copy

from PuzzleObjects import Tile, Board;

# ------------------------------- Forward Check -------------------------------------

def updateRowDomain(currTile, board):
    '''
    helper function for `fwdCheck`. Passes in the current tile
    and updates the domain of that row to ensure that if 
    the current tile has a value, it wouldn't be in the domain of
    the rest of the tiles in that row
    '''
    rowLoc = int(str(currTile.loc)[0]);   # 1 - 5
    for i in range( len(board.lstRows) ): # 0 - 4
        if i == (rowLoc -1):
            for tile in board.lstRows[i]:
                if tile.data == currTile.data:
                    continue
                else:
                    if currTile.data in tile.domain:
                        tile.domain.remove(currTile.data);

def updateColDomain(currTile, board):
    '''
    helper function for `fwdCheck`. Passes in the current tile
    and updates the domain of that column to ensure that if 
    the current tile has a value, it wouldn't be in the domain of
    the rest of the tiles in that column
    '''
    colLoc = currTile.loc%10; # 1 - 5
    for i in range( len(board.lstCols) ): # 0 - 4
        if i == (colLoc -1):
            for tile in board.lstCols[i]:
                if tile.data == currTile.data:
                    continue;
                else:
                    if currTile.data in tile.domain:
                        tile.domain.remove(currTile.data);

def removeMinValDomain(domain, val):
    '''
    helper function for `updateLhsInequal`and `updateUhsInequal`.
    deletes elements in list <= val
    '''
    removeLst = []
    for elem in domain:
        if elem <= val:
            removeLst.append(elem)
    for elem in removeLst:
        domain.remove(elem);

def removeMaxValDomain(domain, val):
    '''
    helper function for `updateLhsInequal`and `updateUhsInequal`.
    deletes elements in list >= val
    '''
    removeLst = []
    for elem in domain:
        if elem >= val:
            removeLst.append(elem)
    for elem in removeLst:
        domain.remove(elem);

def updateLhsInequal(currTile):
    '''
    helper function for `updateInequal`. Checks horizontal 
    inequality constraints and updates domain of the two tiles
    based on that.
    '''
    rhs = currTile.right;

    if currTile.data != 0:
        if currTile.constraintsDict["lhs"] == "<" :
            removeMinValDomain(rhs.domain, currTile.data)
        elif currTile.constraintsDict["lhs"] == ">" :
            removeMaxValDomain(rhs.domain, currTile.data)
    
    elif currTile.data == 0:
        if rhs.data != 0 :
            if rhs.constraintsDict["rhs"] == "<" :
                removeMaxValDomain(currTile.domain, rhs.data)
            elif rhs.constraintsDict["rhs"] == ">" :
                removeMinValDomain(currTile.domain, rhs.data)

def updateUhsInequal(currTile):
    '''
    helper function for `updateInequal`. Checks vertical
    inequality constraints and updates domain of the two tiles
    based on that.
    '''
    dhs = currTile.down;
    if currTile.data != 0:
        if currTile.constraintsDict["uhs"] == "^" :
            removeMinValDomain(dhs.domain, currTile.data)
        elif currTile.constraintsDict["uhs"] == "v" :
            removeMaxValDomain(dhs.domain, currTile.data)
    
    elif currTile.data == 0:
        if dhs.data != 0 :
            if dhs.constraintsDict["dhs"] == "^" :
                removeMaxValDomain(currTile.domain, dhs.data)
            elif dhs.constraintsDict["dhs"] == "v" :
                removeMinValDomain(currTile.domain, dhs.data)

def updateInequal(currTile):
    '''
    helper function for fwdCheck. As fwdCheck iterates 
    through the board, it makes sure the domains are trimmed
    based on the inequality constrains. Board moves left to right,
    up to down. So only the lhs (left hand side) and uhs (up hand side)
    are checked - bc they can consider everything.
    '''
    if "lhs" in currTile.constraintsDict:
        updateLhsInequal(currTile);

    if "uhs" in currTile.constraintsDict:
        updateUhsInequal(currTile);

def fwdCheck(board):
    '''
    fwdCheck iterates through the entire board in  order.
    It updates the row and column domains once it finds a 
    tile that has a value and also trims domain based on 
    inequality constraints.
    It uses the following helper functions : `updateRowDomain`,
    `updateColDomain`, and `updateInequal`
    '''
    curr = board.t11;
    while curr.hasNext():
        if curr.data != 0:
            updateRowDomain(curr, board);
            updateColDomain(curr, board);
        if ("lhs" in curr.constraintsDict) or ("uhs" in curr.constraintsDict):
            updateInequal(curr);
        curr = curr.next;

# --------------------------------- Backtrack ----------------------------------------

def checkCol(move,currTile, board):
    '''
    helper function for `checkMove`. Takes the move
    current tile, and the board and returns a bool
    in seeing if the move interferes the the column
    constriant. Returns True if it doesn't, false
    otherwise.
    '''
    colLoc = currTile.loc%10;             # 1 - 5
    for i in range( len(board.lstCols) ): # 0 - 4
        if i == (colLoc -1):
            for tile in board.lstCols[i]:
                if tile.data == move:
                    return False;
    return True;

def checkRow(move,currTile, board):
    '''
    helper function for `checkMove`. Takes the move
    current tile, and the board and returns a bool
    in seeing if the move interferes the the row
    constriant. Returns True if it doesn't, false 
    otherwise.
    '''
    rowLoc = int(str(currTile.loc)[0]);   # 1 - 5
    for i in range( len(board.lstRows) ): # 0 - 4
        if i == (rowLoc -1):
            for tile in board.lstRows[i]:
                if tile.data == move:
                    return False
    return True;

def checkIneq(move,currTile, board):
    '''
    helper function for `checkMove`. Takes the move
    current tile, and the board and returns a bool
    in seeing if the move interferes the the inequality
    constriants. Returns True if it does, false otherwise.
    It goes through the entire constraint dictionary of 
    the current time and sees if the move sataisfies
    every possible inequality case if there is one.
    '''
    for key, val in currTile.constraintsDict.items():
        
        if key == "lhs":
            rhs = currTile.right;
            if rhs.data == 0:
                continue
            elif val == ">":
                if move < rhs.data:
                    return False;
            elif val == "<":
                if move > rhs.data:
                    return False;
        
        elif key == "rhs":
            lhs = currTile.left;
            if lhs.data == 0:
                continue
            elif val == ">":
                if lhs.data < move:
                    return False
            elif val == "<":
                if lhs.data > move:
                    return False;
        
        elif key == "uhs":
            dhs = currTile.down;
            if dhs.data == 0:
                continue
            elif val == "^":
                if move > dhs.data:
                    return False;
            elif val == "v":
                if move < dhs.data:
                    return False;
        
        elif key == "dhs":
            uhs = currTile.up;
            if uhs.data == 0:
                continue
            elif val == "^":
                if uhs.data > move:
                    return False;
            elif val == "v":
                if uhs.data < move:
                    return False;
    return True;

def checkMove(move,currTile, board):
    '''
    helper function for `backTrack`. Takes the move,
    current tile, and the board to check all the possible 
    constraints it can have. If it doesn't tip off any 
    constraints it returns True and returns False otherwise.
    `checkCol`, `checkRow`, and `checkIneq` are called here.
    '''
    if len(currTile.constraintsDict) != 0:
        ineqBool = checkIneq(move,currTile, board)
    colBool = checkCol(move,currTile, board)
    rowBool = checkRow(move,currTile, board)
    if len(currTile.constraintsDict) != 0:
        return (ineqBool==True) and (colBool == True) and (rowBool==True)
    return (colBool == True) and (rowBool==True)

def sortTilesByMrv(board):
    '''
    helper function for `sortTiles`. mrv is calculated by the
    length of the domain. This function takes in the board to
    and sorts the tiles based on their mrv value. It does so 
    by making a dictions {tile : mrc} and returning the 
    dictionary once sorted.
    '''
    mrvDict = {}
    for tile in board.lstTiles:
        mrvDict[tile] = len(tile.domain)
    sort = sorted(mrvDict.items(), key=operator.itemgetter(1))
    sorted_dict = collections.OrderedDict(sort)
    return sorted_dict

def calculateDeg(currTile, board):
    '''
    helper function for sortTilesByDeg. Iterates through
    row and column of the current tile and counts the 
    number of unoccupied spaces. The count is returned.
    '''
    rowLoc = int(str(currTile.loc)[0]);   # 1 - 5
    count = 0
    for i in range( len(board.lstRows) ): # 0 - 4
        if i == (rowLoc -1):
            for tile in board.lstRows[i]:
                if tile.data == currTile.data:
                    continue
                else:
                    if currTile.data == 0:
                        count += 1
    colLoc = currTile.loc%10;             # 1 - 5
    for i in range( len(board.lstCols) ): # 0 - 4
        if i == (colLoc -1):
            for tile in board.lstCols[i]:
                if tile.data == currTile.data:
                    continue;
                else:
                    if currTile.data == 0:
                        count += 1;
    return count;

def sortTilesByDeg(lstTiles, board):
    '''
    helper function for `sortTiles`. Take a list
    of tiles and the board and sorts the tile on
    on the basis of is deg value. Calls the 
    `calculateDeg` function. This function returns
    a list of keys in the order of the deg heruristic.
    '''
    degDict = {}
    for tile in board.lstTiles:
        degDict[tile] = calculateDeg(tile, board)
    sort = sorted(degDict.items(), key=operator.itemgetter(1))
    sorted_dict = collections.OrderedDict(sort)
    return list(sorted_dict.keys());

def removeDups(lst):
    '''
    helper function for `sortTiles`. Returns a
    list of all unique values in a list. This 
    function was used to find all the unique
    mrv values.
    '''
    res = [] 
    for i in lst: 
        if i not in res: 
            res.append(i) 
    return res;

def sortTiles(board):
    '''
    helper function for `getTile`. It takes in the board
    and sorts it by mrv value first by calling `sortTilesByMrv`.
    Then it calls `removeDups` to get a list of uniq mrv values.
    It sorts by making a dictionary based on the different mrv
    values {mrv : lstOfKeys}. Then it sorts each list for every
    key in the mrv dictionary. Then it iterate through the 
    dictionary to get a list of all the keys in the correct order.
    The sorted keys (tiles) are then returned.
    '''
    tilesMrvSortDict = sortTilesByMrv(board);
    lstMrvs = removeDups(tilesMrvSortDict.values());
    mrvDict = {}
    for mrv in lstMrvs:
        temp = []
        for k,v in tilesMrvSortDict.items():
            if tilesMrvSortDict[k] == mrv:
                temp.append(k)
        mrvDict[mrv] = temp

    for k,v in mrvDict.items():
        k = sortTilesByDeg(v, board)

    sortedTiles = []
    for k,v in mrvDict.items():
        for tile in v:
            sortedTiles.append(tile)

    return sortedTiles;

def getTile(board):
    '''
    helper function for `backTrack`. It gets the first tile
    in the sorted Tiles list that was gotten through the 
    `sortTiles` function. It ensures that the tile it gets
    has a domain that's not empty and has not been filled yet.
    It does so by iterating through the list until it finds a 
    tile that meets that criteria.
    '''
    lst = sortTiles(board)
    for tile in lst:
        if len(tile.domain) != 0 and tile.data == 0:
            return tile

def backTrack(board):
    '''
    Back tack is where the intelligence comes in and
    how the program solves the input board. First it checks
    if all the tiles are filled. The it gets the next tile
    by calling the `getTile` function. Then it iterates
    through all the possible moves in its domain to see if 
    any satisfies the constraints using the `checkMove`
    function. It would then recurse. If the move isn't kosher,
    then the data and domain of the tile will be set. When
    theres a dead end or if its unsolvable False will be returned
    other wise the solved board will be returned.
    '''
    if board.isComplete():
        return True;

    tile = getTile(board)

    for move in tile.domain:
        if checkMove(move, tile, board):
            tile.data = move;
            oldDomain = copy.deepcopy(tile.domain)
            tile.domain = [];

            res = backTrack(board);
            if res:
                return True;
            
            tile.data = 0;
            tile.domain = oldDomain;

    return False;

# ------------------------------------------------------------------------------------

def flattenList(listOfList):
    '''
    Helper function for `fixInputLst`. Takes a
    nested list and returns it as a single list.
    Getting inputs from files gives us a list for
    every line. This function helps fix that problem.
    '''
    flatList = [ item for elem in listOfList for item in elem ]
    return flatList;

def fixTypesinInputLst(lst):
    '''
    helper function for `fixInputLst`. Reading in
    a file gives us lists of strings. This converts
    strings to ints if they are a number or keeps it 
    as a string if its a constriant. Returns lst.
    '''
    numString = "012345"
    for i in range( len(lst) ):
        if lst[i] in numString:
            lst[i] = int(lst[i]);
    return lst;

def fixInputLst(lstOfLst):
    '''
    helper function for `getBoardsFromInputFile`.
    takes in the nested list we get when we read in
    a file and returns a flattened list with the 
    corrected element types. It does so by calling
    `flattenList` and `fixTypesinInputLst`.
    '''
    lst = flattenList(lstOfLst)
    lst = fixTypesinInputLst(lst)
    return lst;

def getBoardsFromInputFile(file):
    '''
    helper function for `solveBoardFromFile`. A
    file is passed in where the lines are read one
    at a time and it contents are being stored in
    its appropiate list. Then `fixInputLst` is called
    to flatten and corect the types for every element
    in all three input lists. All three boards are returned.
    '''
    boardLst = []
    horizBoardLst = []
    vertBoardLst = []
    
    counter = -1;
    f_lines = file.readlines();

    for i in f_lines:
        
        counter+=1;
        
        if counter < 5:
            boardLst.append(i.strip().split(" "));

        elif (counter < 11) and (counter > 5):
            horizBoardLst.append(i.strip().split(" "));

        elif (counter < 16) and (counter > 11):
            vertBoardLst.append(i.strip().split(" "));
    
    boardLst = fixInputLst(boardLst)
    horizBoardLst = fixInputLst(horizBoardLst)
    vertBoardLst = fixInputLst(vertBoardLst)

    return (boardLst, horizBoardLst, vertBoardLst )

def solveBoardFromFile(file):
    '''
    called in main. The file is passed in.
    `getBoardsFromInputFile` gets the input
    list. A Board object is then made with this
    list.  `fwdCheck` is then called to trim
    the domains. Then backTrack is called to
    solve the board. Then it is checked if it
    was solved. If it was then, the baord is 
    returned otherwise False is returned.
    '''
    lst1, lst2, lst3 = getBoardsFromInputFile(file)
    board1 = Board(boardLst = lst1, horizContraintLst = lst2, vertContraintLst = lst3 );
    fwdCheck(board1);
    if (backTrack(board1)):
        return board1;
    else:
        return False    

def outputSolutionFile(outFile, solutionBoard):
    '''
    called in main. Once the board is solved, then
    the outFile and the solved board is passed in 
    to write the soltion to the file. It checks if
    there is a solution. If there is, then it writes
    the board to the file, else it would write 
    "No Solution". Because a __str__ method was made
    in the Board class, if could just convert the 
    board to a string and write that to the file.
    '''
    if type(solutionBoard) == bool: # would be false if no solutions
        outFile.write("No Solution")
    else:
        outFile.write(str(solutionBoard))

def main():
    # get input files
    f_i_1 = open("Input1.txt", "r");
    f_i_2 = open("Input2.txt", "r");
    f_i_3 = open("Input3.txt", "r");
    f_i_4 = open("test.txt"  , "r");
    
    # solve boards from the input file
    solutionBoard1 = solveBoardFromFile(f_i_1)
    solutionBoard2 = solveBoardFromFile(f_i_2)
    solutionBoard3 = solveBoardFromFile(f_i_3)
    solutionBoard4 = solveBoardFromFile(f_i_4)

    # create output files
    f_o_1 = open("Output1.txt","w+");
    f_o_2 = open("Output2.txt","w+");
    f_o_3 = open("Output3.txt","w+");
    f_o_4 = open("OutTest.txt","w+");


    # write solution to output file.
    outputSolutionFile(f_o_1, solutionBoard1)
    outputSolutionFile(f_o_2, solutionBoard2)
    outputSolutionFile(f_o_3, solutionBoard3)
    outputSolutionFile(f_o_4, solutionBoard3)

main();
