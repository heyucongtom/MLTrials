import Tkinter as tk
import time

APP_WIN_XPOS = 100
APP_WIN_YPOS = 100
APP_WIN_WIDTH = 500
APP_WIN_HEIGHT = 500
APP_WIN_TITLE = "Snake Game"
APP_BACK_GND = 'white'
FOOD_COLOR = 'palegoldenrod'
WALL_COLOR = "black"
SPACE_COLOR = "white"
SNAKE_COLOR = "grey"

class Grid(object):

    def __init__(self, color=None):
        self.color = color
        self.food = None

    def isSafe(self):
        pass

    def getColor(self):
        if self.food:
            return FOOD_COLOR
        return self.color

    def getFood(self):
        return self.food

    def addFood(self):
        self.food = Food()

    def removeFood(self):
        if self.getFood():
            self.food = None


class Wall(Grid):

    def __init__(self, color=WALL_COLOR):
        Grid.__init__(self, color)

    def isSafe(self):
        return False

class Space(Grid):

    def __init__(self, color=SPACE_COLOR):
        Grid.__init__(self, color)

    def isSafe(self):
        return True

class Food(object):

    def __init__(self):
        pass


class Board(object):
    """
    A 2-dimensional array of objects backed by a list of lists. 
    Data is accessed via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented like a pacman board.

    construct a board with character in teststr:
        . -> space
        # -> wall
    """

    def __init__(self, width, height, config_str):
        self._width = width
        self._height = height
        self._data = [[None for i in range(width)] for j in range(height)]
        assert(len(config_str) == self._width * self._height), "Wrong config params."
        for i, ch in enumerate(config_str):
            x, y = self._cellIndexToPosition(i)
            if ch == ".":
                self._data[x][y] = Space()
            if ch == "#":
                self._data[x][y] = Wall()
        self._foodPosSet = set()

    def getFoodPositions(self):
        return self._foodPosSet

    def getBoardData(self):
        """
        Get the current data of the board as a 2-D array.
        """
        return self._data

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    def getHeight(self):
        return self._height

    def _cellIndexToPosition(self, index):
        x = index / self._height
        y = index % self._height
        return x, y

    def _addFoodToGrid(self, x, y):
        self._data[x][y].addFood()
        self._foodPosSet.add((x, y))

    def _removeFoodFromGrid(self, x, y):
        self._data[x][y].removeFood()
        self._foodPosSet.remove((x, y))
    
    def __getitem__(self, i):
        return self._data[i]

    def __setitem__(self, key, item):
        self._data[key] = item

class Direction(object):

    Right = 'Right'
    Left = 'Left'
    Up = 'Up'
    Down = 'Down'

class Snake:

    def __init__(self, _speed = 1, _pos_lst = None, _direction = Direction.Right, color=SNAKE_COLOR):
        if _pos_lst:
            self._pos_lst = _pos_lst
        else:
            self._pos_lst = [(0, 0), (0, 1)]
        self._direction = _direction
        self._speed = _speed
        self._color = color

    def getSpeed(self):
        return self._speed

    def getDirection(self):
        return self._direction

    def getColor(self):
        return self._color

    def setDirection(self, keystroke):
        pass
        

    def move(self, food):

        """ 
        Move towards one direction, for one step. 
        Only need to record the routine of the snake head. The rest just follows.
        """
        x, y = self._pos_lst[self._length - 1]
        new_x, new_y = self._move_by_direction(x, y, self._direction, self._speed)

        self._pos_lst.append((new_x, new_y))
        if not food:
            self._pos_lst.pop(0)
        return self

    def _move_by_direction(self, x, y, direction, speed):

        """
        Given direction and current x, y.
        return a new (x, y) pair.
        """

        if direction == Direction.Left:
            return x, y - speed
        if direction == Direction.Up:
            return x - speed, y
        if direction == Direction.Right:
            return x, y + speed
        if direction == Direction.Down:
            return x + speed, y
        else:
            print("Invalid direction parameter.")
            return None

    def getPositions(self):
        return self._pos_lst

    @property
    def _length(self):
        return len(self._pos_lst)

    def _legal_grid(self, x, y):
        board = self._board
        grid = board.getGrid(x, y)
        if grid.isSafe():
            return True
        return False

class Game(object):
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, snake=None, board=None, win=None):
        
        self.snake = snake
        self.board = board
        self.label_array = [[None for i in range(self.board.width)] for j in range(self.board.height)]
        self.win = win or tk.Tk()

    def run(self):
        self.win.geometry('+{0}+{1}'.format(APP_WIN_XPOS, APP_WIN_YPOS))
        self.win.geometry('{0}x{1}'.format(APP_WIN_WIDTH, APP_WIN_HEIGHT))
        self.win.config(bg=APP_BACK_GND)
        self.drawBoard()
        self.drawSnake()

        while True:
            time.sleep(1)
            self.snake.move(False)
            self.drawSnake()
            # self.drawFood()
            self.win.update()
            

    def _drawGrids(self, grids, color, tail_pos=None, px=3, py=3):

        # Option for snake's tail;
        if tail_pos:
            i, j = tail_pos
            self.label_array[i+1][j].configure(bg = APP_BACK_GND)
            self.label_array[i-1][j].configure(bg = APP_BACK_GND)
            self.label_array[i][j+1].configure(bg = APP_BACK_GND)
            self.label_array[i][j-1].configure(bg = APP_BACK_GND)

        for i, j in grids:
            self.label_array[i][j].configure(bg = color)


    def drawSnake(self):
        color = self.snake.getColor()
        pos_lst = self.snake.getPositions()
        self._drawGrids(pos_lst, color, tail_pos = pos_lst[0])

    def drawFood(self):
        color = FOOD_COLOR
        self._drawGrids(self.board.getFoodPositions(), color)

    def drawBoard(self):
        board_config = self.board.getBoardData()
        for i in range(self.board.width):
            for j in range(self.board.height):
                color = board_config[i][j].getColor()
                L = tk.Label(self.win, text = "    ", bg = color, padx=3, pady=3)
                self.label_array[i][j] = L
                L.grid(row=i, column=j)


import unittest
test_str = "..........................................................................................................................................................##########............................................................................................................................................................................................................................................"

class TestSnake(unittest.TestCase): 

    def testSnakeInit(self):

        snake1 = Snake()
        self.assertEqual(snake1.getSpeed(), 1)
        self.assertEqual(snake1.getPositions(), [(0, 0), (0, 1)])
        self.assertEqual(snake1.getDirection(), Direction.Right)

    def testSnakeMove(self):

        snake2 = Snake()
        snake2.move(food = False)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2)])
        snake2.move(food = True)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2), (0, 3)])
        snake2.move(food = False)
        self.assertEqual(snake2.getPositions(), [(0, 2), (0, 3), (0, 4)])

    def testSnakeTurn(self):
        snake2 = Snake()
        snake2.move(food = False)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2)])
        snake2.move(food = True)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2), (0, 3)])
        snake2._direction = Direction.Down
        snake2.move(food = True)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2), (0, 3), (1, 3)])

class TestBoard(unittest.TestCase):

    def testBoardConstruction(self):

        board1 = Board(width = 20, height = 20, config_str = test_str)
        self.assertEqual(type(board1[1][0]), Wall)
        self.assertEqual(board1[1][1].isSafe(), False)
        self.assertEqual(board1[2][1].isSafe(), True)
        self.assertEqual(board1[1][3].getColor(), "black")
        self.assertEqual(board1[0][3].getColor(), "white")

    def testAddAndRemoveFood(self):

        board2 = Board(width = 20, height= 20, config_str = test_str)
        board2._addFoodToGrid(3,5)
        board2._addFoodToGrid(4,6)
        self.assertEqual((board2._data[3][5].getFood() is not None), True)
        self.assertEqual(((3,5) in board2._foodPosSet), True)
        board2._removeFoodFromGrid(3,5)
        self.assertEqual(((3,5) in board2._foodPosSet), False)
        self.assertEqual((board2._data[3][5].getFood() is None), True)


if __name__ == '__main__':
    # unittest.main()
    board = Board(width = 20, height = 20, config_str = test_str)
    board._addFoodToGrid(3,5)
    board._addFoodToGrid(4,6)
    snake = Snake(_pos_lst = [(0, 1), (0, 2), (0, 3), (1, 3)])
    g = Game(snake, board)
    g.run()
    board._addFoodToGrid(5,7)




# heyucong







