import tkinter as tk
import time
import sys

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

class Direction(object):

    Right = 'Right'
    Left = 'Left'
    Up = 'Up'
    Down = 'Down'

    @classmethod
    def reverse(cls, direction):
        if direction == cls.Right:
            return cls.Left
        if direction == cls.Left:
            return cls.Right
        if direction == cls.Up:
            return cls.Down
        if direction == cls.Down:
            return cls.Up

DIR_DICT = {'d': Direction.Right, 'a':Direction.Left, 'w':Direction.Up, 's':Direction.Down}

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
            x, y = self.cellIndexToPosition(i)
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

    def cellIndexToPosition(self, index):
        x = index // self.width
        y = index % self.height
        return x, y

    def positionToCellIndex(self, x, y):
        return x * self.width + y

    def _addFoodToGrid(self, x, y):
        self._data[x][y].addFood()
        self._foodPosSet.add((x, y))

    def removeFoodFromGrid(self, x, y):
        self._data[x][y].removeFood()
        self._foodPosSet.remove((x, y))
    
    def __getitem__(self, i):
        return self._data[i]

    def __setitem__(self, key, item):
        self._data[key] = item

    def getNeighborsList(self, x, y):
        left = ((x-1) % self.width, y)
        right = ((x+1) % self.width, y)
        up = (x, (y-1) % self.height)
        down = (x, (y+1) % self.height)
        lst = [left, right, up, down]
        return lst

    def getSafeNeighborsList(self, x, y):
        neighbors = self.getNeighborsList(x, y)
        ret = []
        for n in neighbors:
            if self[x][y].isSafe():
                ret.append(n)
        return ret


class Snake:

    def __init__(self, _board, _speed = 1, _pos_lst = None, _direction = Direction.Right, color=SNAKE_COLOR):
        if _pos_lst:
            self._pos_lst = _pos_lst
        else:
            self._pos_lst = [(0, 0), (0, 1)]
        self._direction = _direction
        self._speed = _speed
        self._color = color
        self._size = len(self._pos_lst)
        self._board = _board
        self._prevTail = None

    @property
    def board(self):
        return self._board

    @property
    def speed(self):
        return self._speed

    @property
    def size(self):
        return self._size

    @property
    def direction(self):
        return self._direction

    def head(self):
        return self._pos_lst[self.size - 1]

    def prevTail(self):
        return self._prevTail

    @property
    def color(self):
        return self._color

    def setDirection(self, direction):
        self._direction = direction

    def move(self, food=False):

        """ 
        Move towards one direction, for one step. 
        Only need to record the routine of the snake head. The rest just follows.
        """
        x, y = self._pos_lst[self.size - 1]
        new_x, new_y = self._move_by_direction(x, y, self._direction, self._speed)

        self._pos_lst.append((new_x, new_y))
        self._size += 1

        if not food:
            self._size -= 1
            self._prevTail = self._pos_lst[0]
            self._pos_lst.pop(0)

        return self

    def bfs(self, start, target):
        """
        Using breadth first to get next move until get food
        return a map recording path
        """
        import queue
        prev = [0 for i in range(self.board.width * self.board.height)]
        visited = set()
        
        q = queue.Queue()
        q.put(start)
        visited.add(start)
        index_n = self.board.positionToCellIndex(*start)
        prev[index_n] = (start, 0)
        found = False
        while not q.empty():
            node = q.get()
            index_n = self.board.positionToCellIndex(*node)
            neighbors = self.board.getSafeNeighborsList(*node)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor != self.head:
                    # For bfs we can skip distance check.
                    index = self.board.positionToCellIndex(*neighbor)
                    dist = prev[index_n][1] + 1
                    prev[index] = (node, dist)
                    visited.add(neighbor)
                    q.put(neighbor)
            if target in visited:
                return prev
        return None

    def reconstruct_path_lst(self, lst, start, target):

        index_s = self.board.positionToCellIndex(*start)
        index_t = self.board.positionToCellIndex(*target)
        path = [target]
        while index_t != index_s:
            node = lst[index_t]
            prev = node[0]
            path.append(prev)
            index_t = self.board.positionToCellIndex(*prev)
        return path[::-1]

    def get_direction_from_pos(self, scr, dst):
        
        """
        Get the direction from scr to dst.
        """
        det_x = dst[0] - scr[0]
        det_y = dst[1] - scr[1]
        width = self.board.width
        height = self.board.height
        if det_x == 0:
            if det_y % height == 1:
                return Direction.Down
            if det_y % height == height - 1:
                return Direction.Up
        if det_y == 0:
            if det_x % width == 1:
                return Direction.Right
            if det_x % width == width - 1:
                return Direction.Left
        return -1




    def _move_by_direction(self, x, y, direction, speed):

        """
        Given direction and current x, y.
        return a new (x, y) pair.
        """
        w = self.board.width
        h = self.board.height

        if direction == Direction.Left:
            return x % w, (y - speed) % h
        if direction == Direction.Up:
            return (x - speed) % w, y % h
        if direction == Direction.Right:
            return x % w, (y + speed) % h
        if direction == Direction.Down:
            return (x + speed) % w, y % h
        else:
            print("Invalid direction parameter.")
            return None

    def getNextStep(self):
        x, y = self._pos_lst[self.size - 1]
        new_x, new_y = self._move_by_direction(x, y, self._direction, self._speed)
        return new_x, new_y

    def getPositions(self):
        return self._pos_lst

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

        def snake_action(event):
            if event.char in DIR_DICT:
                direction = DIR_DICT[event.char]
                self.snake.setDirection(direction)

        self.win.geometry('+{0}+{1}'.format(APP_WIN_XPOS, APP_WIN_YPOS))
        self.win.geometry('{0}x{1}'.format(APP_WIN_WIDTH, APP_WIN_HEIGHT))
        self.win.config(bg=APP_BACK_GND)
        self.drawBoard()
        self.drawSnake()
        self.win.bind('<Key>', snake_action)

        while True:
            time.sleep(0.3)
            self._runGameStep()
            self.drawSnake()
            self.drawFood()
            self.win.update()

    def _isEnd(self):

        # Case 1: Snake hit itself:
        _isEnd = False
        if self.snake.head() in self.snake.getPositions()[0:self.snake.size - 1]:
            return True

        # Case 2: Snake hit wall:
        x, y = self.snake.head()
        if not self.board[x][y].isSafe():
            return True

    def _listenToKey(self):
        pass
        
    
    def _runGameStep(self, step=1):
        x, y = self.snake.getNextStep();
        food_var = (self.board[x][y].getFood() is not None)
        self.snake.move(food_var)
        x, y = self.snake.head()
        if self._isEnd():
            print("Game ended.")
            sys.exit()
        if food_var:
            self.board.removeFoodFromGrid(x, y)

    def _drawGrids(self, grids, color, tail_pos=None, px=3, py=3):

        # Option for snake's tail;
        w = self.board.width
        h = self.board.height
        if tail_pos:
            x, y = tail_pos
            orig_color = self.board[x][y].getColor()
            self.label_array[x][y].configure(bg = orig_color)

        for i, j in grids:
            self.label_array[i][j].configure(bg = color)


    def drawSnake(self):
        color = self.snake.color
        pos_lst = self.snake.getPositions()
        self._drawGrids(pos_lst, color, tail_pos = self.snake.prevTail())

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
test_str = ".........................................##########.......................................................................................................##########............................................................................................................................................................................................................................................"

class TestSnake(unittest.TestCase): 

    def testSnakeInit(self):

        
        board = Board(width=20, height=20, config_str=test_str)
        snake1 = Snake(board)
        self.assertEqual(snake1.speed, 1)
        self.assertEqual(snake1.getPositions(), [(0, 0), (0, 1)])
        self.assertEqual(snake1.direction, Direction.Right)

    def testSnakeMove(self):

        board = Board(width=20, height=20, config_str=test_str)
        snake2 = Snake(board)
        snake2.move(food = False)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2)])
        snake2.move(food = True)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2), (0, 3)])
        snake2.move(food = False)
        self.assertEqual(snake2.getPositions(), [(0, 2), (0, 3), (0, 4)])

    def testSnakeTurn(self):
        board = Board(width=20, height=20, config_str=test_str)
        snake2 = Snake(board)
        snake2.move(food = False)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2)])
        snake2.move(food = True)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2), (0, 3)])
        snake2._direction = Direction.Down
        snake2.move(food = True)
        self.assertEqual(snake2.getPositions(), [(0, 1), (0, 2), (0, 3), (1, 3)])

class TestBoard(unittest.TestCase):

    # def testBoardConstruction(self):

    #     board1 = Board(width = 20, height = 20, config_str = test_str)
    #     self.assertEqual(type(board1[1][0]), Wall)
    #     self.assertEqual(board1[1][1].isSafe(), False)
    #     self.assertEqual(board1[2][1].isSafe(), True)
    #     self.assertEqual(board1[1][3].color, "black")
    #     self.assertEqual(board1[0][3].color, "white")

    def testAddAndRemoveFood(self):

        board2 = Board(width = 20, height= 20, config_str = test_str)
        board2._addFoodToGrid(3,5)
        board2._addFoodToGrid(4,6)
        self.assertEqual((board2._data[3][5].getFood() is not None), True)
        self.assertEqual(((3,5) in board2._foodPosSet), True)
        board2.removeFoodFromGrid(3,5)
        self.assertEqual(((3,5) in board2._foodPosSet), False)
        self.assertEqual((board2._data[3][5].getFood() is None), True)

    def testBFS(self):
        teststr = "........................."
        board = Board(width = 5, height = 5, config_str = teststr)
        snake = Snake(_board = board)
        start = (0,0)
        target = (2,3)
        lst = snake.bfs(start, target)
        print("LST:")
        print(lst)
        print("RE:")
        print(snake.reconstruct_path_lst(lst, start, target))

    def testGetDirectionFromPos(self):
        teststr = "................"
        board = Board(width = 4, height = 4, config_str = teststr)
        snake = Snake(_board = board)
        self.assertEqual(snake.get_direction_from_pos((0, 1), (1, 1)), Direction.Right)
        self.assertEqual(snake.get_direction_from_pos((0, 1), (0, 0)), Direction.Up)
        self.assertEqual(snake.get_direction_from_pos((0, 1), (3, 1)), Direction.Left)
        self.assertEqual(snake.get_direction_from_pos((0, 1), (0, 2)), Direction.Down)
        self.assertEqual(snake.get_direction_from_pos((3, 3), (0, 3)), Direction.Right)
        self.assertEqual(snake.get_direction_from_pos((3, 3), (3, 0)), Direction.Down)
        self.assertEqual(snake.get_direction_from_pos((3, 3), (2, 3)), Direction.Left)
        self.assertEqual(snake.get_direction_from_pos((3, 3), (3, 2)), Direction.Up)


if __name__ == '__main__':
    unittest.main()
    # board = Board(width = 20, height = 20, config_str = test_str)
    # board._addFoodToGrid(3,5)
    # board._addFoodToGrid(1,6)
    # board._addFoodToGrid(4,6)
    # snake = Snake(_pos_lst = [(0, 1), (0, 2), (0, 3), (1, 3)], _board = board)
    # g = Game(snake, board)
    # g.run()
    # board._addFoodToGrid(5,7)




# heyucong