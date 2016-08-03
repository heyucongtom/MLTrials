class GridType(object):
	
	Wall = 1
	Space = 2

class Direction(object):

	Left = 1
	Up = 2
	Right = 3
	Down = 4


l_dict = {GridType.Wall: 'Wall', GridType.Space: 'Space'}
print_dict = {GridType.Wall: '@', GridType.Space: '.'}



class Grid(object):

	def __init__(self, grid_type=GridType.Space):
		self.grid_type = grid_type

	def __repr__(self):
		return l_dict[self.grid_type]

	def getType(self):
		return self.grid_type

	def isSafe(self):
		return self.grid_type == GridType.Space

class Board(object):

	def __init__(self, input_string, r = 20, c = 20):

		assert(len(input_string) == r * c), "Wrong format."
		self.row = r
		self.col = c
		self.grid_lst = []
		for s in input_string:
			grid_type = None
			if s == '.':
				grid_type = GridType.Space
			elif s == '@':
				grid_type = GridType.Wall
			else:
				print("Wrong parameter.")

			self.grid_lst.append(Grid(grid_type))

	def __repr__(self):
		return self._display_grid()

	def getGrid(self, r, c):
		grid = self.grid_lst[r * self.row + c]
		return grid

	def _display_grid(self):
		s = ""
		for i in range(self.row):
			for j in range(self.col):
				grid = self.grid_lst[i * self.row + j]
				s += print_dict[grid.grid_type]
			s += '\n'
		return s

	def _get_grid_type(self, r, c):
		assert(r < self.row), "Wrong row."
		assert(c < self.col), "Wrong column."

		selected_grid = self.grid_lst[r * self.row + c]
		grid_type = l_dict[selected_grid.getType()]
		return grid_type


class Snake:



	def __init__(self, _board, _speed = 1, _pos_lst = None, _direction = Direction.Right):
		if _pos_lst:
			self._pos_lst = _pos_lst
		else:
			self._pos_lst = [(0, 0), (0, 1)]
		self._direction = _direction
		self._board = _board
		self._speed = _speed

	def getDirection(self):
		return self._direction

	def setDirection(self, keystroke):
		

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

	def _get_positions(self):
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




import unittest
test_str = "....................@@@@@@@@@@.................................................................................................................................................................................................................................................................................................................................................................................."
b = Board(test_str)

class TestSnake(unittest.TestCase):	

	def testSnakeInit(self):

		snake1 = Snake(b)
		self.assertEqual(snake1.getSpeed(), 1)
		self.assertEqual(snake1._get_positions(), [(0, 0), (0, 1)])
		self.assertEqual(snake1.getDirection(), Direction.Right)

	def testSnakeMove(self):

		snake2 = Snake(b)
		snake2.move(food = False)
		self.assertEqual(snake2._get_positions(), [(0, 1), (0, 2)])
		snake2.move(food = True)
		self.assertEqual(snake2._get_positions(), [(0, 1), (0, 2), (0, 3)])
		snake2.move(food = False)
		self.assertEqual(snake2._get_positions(), [(0, 2), (0, 3), (0, 4)])

	def testSnakeTurn(self):
		snake2 = Snake(b)
		snake2.move(food = False)
		self.assertEqual(snake2._get_positions(), [(0, 1), (0, 2)])
		snake2.move(food = True)
		self.assertEqual(snake2._get_positions(), [(0, 1), (0, 2), (0, 3)])
		snake2._direction = Direction.Down
		snake2.move(food = True)
		self.assertEqual(snake2._get_positions(), [(0, 1), (0, 2), (0, 3), (1, 3)])



if __name__ == '__main__':
    unittest.main()







