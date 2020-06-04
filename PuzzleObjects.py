class Tile:
    '''
    The Tile class is basically a node that holds the value(data), domain, and constraints.
    It basically functions as a 2D array. This was done to minimize the amount of times
    I would have to loop through the array.
    '''

    def __init__ (self, data = 0, loc = None, up  = None , down  = None, left  = None, right  = None, next = None) :
        self.data            = data               ;
        self.loc             = loc                ;
        self.up              = up                 ;
        self.down            = down               ;
        self.left            = left               ;
        self.right           = right              ;
        self.next            = next               ;
        self.domain          = [1, 2, 3, 4, 5]    ;
        self.constraintsDict = {}                 ; # pos = {rhs, lhs, uhs, dhs} : constraints = {<, >, ^, v}

    def hasNext (self):
        '''
        In the times where the boards need to be iterated, the next is ordered from left to right
        and up to down. Has next returns true if it is not the last tile on the board (bottom right tile)
        '''
        return self.next != None;

    def __repr__ (self):
        '''
        A repr function was nice to have when debugging
        '''
        ret_str =  "\nNODE:\n\tData       : " + str(self.data);
        ret_str += "\n\tLoc        : "      + str(self.loc);
        ret_str += "\n\tDomain     : "      + str(self.domain);
        ret_str += "\n\tConstraints: "      + str(self.constraintsDict);
        return ret_str;

class Board:
    '''
    A board holds tiles. 25 nodes are made and ordered in the Board object.
    '''
    def __init__ (self, boardLst, horizContraintLst = [], vertContraintLst = [] ):
        '''
        The constructor holds each tile. So if I need to access a tile directly,
        I could call it directly instead of having to iterate through to find it.
        The user inputs the three lists found in the Input file, and the contructor
        immediadelt sets up the board based on that using its private methods.
        '''

        self.boardLst = boardLst;
        self.horizContraintLst = horizContraintLst;
        self.vertContraintLst  = vertContraintLst;

        self.t11 = Tile(loc = 11);
        self.t12 = Tile(loc = 12);
        self.t13 = Tile(loc = 13);
        self.t14 = Tile(loc = 14);
        self.t15 = Tile(loc = 15);
        self.t21 = Tile(loc = 21);
        self.t22 = Tile(loc = 22);
        self.t23 = Tile(loc = 23);
        self.t24 = Tile(loc = 24);
        self.t25 = Tile(loc = 25);
        self.t31 = Tile(loc = 31);
        self.t32 = Tile(loc = 32);
        self.t33 = Tile(loc = 33);
        self.t34 = Tile(loc = 34);
        self.t35 = Tile(loc = 35);
        self.t41 = Tile(loc = 41);
        self.t42 = Tile(loc = 42);
        self.t43 = Tile(loc = 43);
        self.t44 = Tile(loc = 44);
        self.t45 = Tile(loc = 45);
        self.t51 = Tile(loc = 51);
        self.t52 = Tile(loc = 52);
        self.t53 = Tile(loc = 53);
        self.t54 = Tile(loc = 54);
        self.t55 = Tile(loc = 55);

        self.lstRow1  = [self.t11,self.t12,self.t13,self.t14,self.t15]
        self.lstRow2  = [self.t21,self.t22,self.t23,self.t24,self.t25]
        self.lstRow3  = [self.t31,self.t32,self.t33,self.t34,self.t35]
        self.lstRow4  = [self.t41,self.t42,self.t43,self.t44,self.t45]
        self.lstRow5  = [self.t51,self.t52,self.t53,self.t54,self.t55]

        self.lstCol1  = [self.t11,self.t21,self.t31,self.t41,self.t51]
        self.lstCol2  = [self.t12,self.t22,self.t32,self.t42,self.t52]
        self.lstCol3  = [self.t13,self.t23,self.t33,self.t43,self.t53]
        self.lstCol4  = [self.t14,self.t24,self.t34,self.t44,self.t54]
        self.lstCol5  = [self.t15,self.t25,self.t35,self.t45,self.t55]

        self.lstRows  = [self.lstRow1, self.lstRow2, self.lstRow3, self.lstRow4, self.lstRow5]
        self.lstCols  = [self.lstCol1, self.lstCol2, self.lstCol3, self.lstCol4, self.lstCol5]

        self.lstTiles = [self.t11,self.t12,self.t13,self.t14,self.t15,
                         self.t21,self.t22,self.t23,self.t24,self.t25,
                         self.t31,self.t32,self.t33,self.t34,self.t35,
                         self.t41,self.t42,self.t43,self.t44,self.t45,
                         self.t51,self.t52,self.t53,self.t54,self.t55 ]

        # private methods      
        self.__constructBoard();
        self.__fillBoardFromLst(self.boardLst);
        self.__addConstraintsFromLsts(self.horizContraintLst, self.vertContraintLst)

    def __constructBoard(self):
        '''
        This is a private function that makes the board by setting up all the pointers
        of all the tiles.
        '''
        for lst in self.lstRows:
            for i in range( len(lst) ):
                if ( i < (len(lst) - 1) ):
                    lst[i].right = lst[i+1];
                    lst[i].next  = lst[i+1];

                if ( i > 0 ):
                    lst[i].left = lst[i-1];

        for i in range (5) :
            self.lstRow2[i].up   = self.lstRow1[i];
            self.lstRow3[i].up   = self.lstRow2[i];
            self.lstRow4[i].up   = self.lstRow3[i];
            self.lstRow5[i].up   = self.lstRow4[i];
            self.lstRow1[i].down = self.lstRow2[i];
            self.lstRow2[i].down = self.lstRow3[i];
            self.lstRow3[i].down = self.lstRow4[i];
            self.lstRow4[i].down = self.lstRow5[i];

        for i in range( len(self.lstCol5) ):
            if (i != (len(self.lstCol5) - 1) ):
                self.lstCol5[i].next = self.lstCol1[i+1];

    def __fillBoardFromLst (self, lst):
        '''
        This is a private function that that uses the board list that the user provides in
        the constructor to fill the board with the correct initial values.
        '''
        for i in range ( len(lst) ) :
            self.lstTiles[i].data = lst[i];

    def __addHorizConstraints(self, horizContraintsLst):
        '''
        Private function. Adds horizontal constraints from list provided in constructor.
        '''
        horizContraints1 = horizContraintsLst[0 : 4]
        horizContraints2 = horizContraintsLst[4 : 8]
        horizContraints3 = horizContraintsLst[8 : 12]
        horizContraints4 = horizContraintsLst[12 : 16]
        horizContraints5 = horizContraintsLst[16 : 20]

        
        for i in range( len(horizContraints1) ):
            if str(horizContraints1[i]) in "<>":
                self.lstRow1[i].constraintsDict["lhs"]   = horizContraints1[i];
                self.lstRow1[i+1].constraintsDict["rhs"] = horizContraints1[i];

        for i in range( len(horizContraints2) ):
            if str(horizContraints2[i]) in "<>":
                self.lstRow2[i].constraintsDict["lhs"]   = horizContraints2[i];
                self.lstRow2[i+1].constraintsDict["rhs"] = horizContraints2[i];

        for i in range( len(horizContraints3) ):
            if str(horizContraints3[i]) in "<>":
                self.lstRow3[i].constraintsDict["lhs"]   = horizContraints3[i];
                self.lstRow3[i+1].constraintsDict["rhs"] = horizContraints3[i];

        for i in range( len(horizContraints4) ):
            if str(horizContraints4[i]) in "<>":
                self.lstRow4[i].constraintsDict["lhs"]   = horizContraints4[i];
                self.lstRow4[i+1].constraintsDict["rhs"] = horizContraints4[i];

        for i in range( len(horizContraints5) ):
            if str(horizContraints5[i]) in "<>":
                self.lstRow5[i].constraintsDict["lhs"]   = horizContraints5[i];
                self.lstRow5[i+1].constraintsDict["rhs"] = horizContraints5[i];

    def __addVertConstraints(self, vertConstraintsLst):
        '''
        Private function. Adds vertical constraints from list provided in constructor.
        '''
        vertContraints1 = vertConstraintsLst[0 : 5]
        vertContraints2 = vertConstraintsLst[5 : 10]
        vertContraints3 = vertConstraintsLst[10 : 15]
        vertContraints4 = vertConstraintsLst[15 : 20]

        for i in range( len(vertContraints1) ):
            if str(vertContraints1[i]) in "^v":
                self.lstRow1[i].constraintsDict["uhs"] = vertContraints1[i];
                self.lstRow2[i].constraintsDict["dhs"] = vertContraints1[i];

        for i in range( len(vertContraints2) ):
            if str(vertContraints2[i]) in "^v":
                self.lstRow2[i].constraintsDict["uhs"] = vertContraints2[i];
                self.lstRow3[i].constraintsDict["dhs"] = vertContraints2[i];

        for i in range( len(vertContraints3) ):
            if str(vertContraints3[i]) in "^v":
                self.lstRow3[i].constraintsDict["uhs"] = vertContraints3[i];
                self.lstRow4[i].constraintsDict["dhs"] = vertContraints3[i];

        for i in range( len(vertContraints4) ):
            if str(vertContraints4[i]) in "^v":
                self.lstRow4[i].constraintsDict["uhs"] = vertContraints4[i];
                self.lstRow5[i].constraintsDict["dhs"] = vertContraints4[i];

    def __addConstraintsFromLsts (self, horizContraintsLst, vertConstraintsLst) :
        '''
        private method called in the constructor that calls `__addHorizConstraints` and 
        `__addVertConstraints`
        '''
        self.__addHorizConstraints(horizContraintsLst);
        self.__addVertConstraints(vertConstraintsLst);

    def isComplete(self):
        '''
        isComplete is a public method that returns True if all the tiles are filled
        and False otherwise
        '''
        for tile in self.lstTiles:
            if tile.data == 0:
                return False
        return True

    def __repr__ (self):
        '''
        repr was nice to write for debugging
        '''
        retStr = ""

        for row in self.lstRows :
            for i in range(len(row)) :
                retStr += str(row[i].data) + " ";
                
                if i == ( len(row) - 1 ):    
                    retStr += "\n";
        return retStr;
    
    def __str__ (self):
        '''
        str method was copied from the repr's code. Made it easy
        to write out the Output files that hold the solutions.
        In hindsight perhaps the repr was redundant.
        '''
        string = ""

        for row in self.lstRows :
            for i in range(len(row)) :
                string += str(row[i].data) + " ";
                
                if i == ( len(row) - 1 ):    
                    string += "\n";
        return string;

    def resetBoard(self):
        '''
        resetBoard is a public method that resets the board back to its initial state.
        This function was not used to solve the board.
        '''
        initBoard = type(self)(boardLst = self.boardLst, horizContraintLst = self.horizContraintLst , vertContraintLst = self.vertContraintLst )
        self.__dict__.update(initBoard.__dict__)


