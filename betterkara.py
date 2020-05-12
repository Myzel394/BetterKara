# -*- coding: utf-8 -*-

"""
This file provides better APIs for the PythonKara project.
This code can only be copy-pasted because the Kara environment doesn't allow imports.
This may be used inside a Kara environment.

PythonKara project: https://www.swisseduc.ch/informatik/karatojava/pythonkara/
"""

__author__ = "***REMOVED***"
__copyright__ = "Copyright 2020, ***REMOVED***"
__credits__ = ["***REMOVED***"]

__license__ = "MIT"
__version__ = "0.1"
__email__ = "***REMOVED***"


class DebugClass:
    def __init__(self):
        pass
    
    def show_args(self, args):
        string = "; ".join([self.show_value(value) for value in args])
        
        tools.showMessage(string)
    
    def show_kwargs(self, kwargs):
        string = "; ".join([str(key) + ": " + self.show_value(value) for key, value in kwargs.items()])
        
        tools.showMessage(string)
    
    def show_value(self, value):
        return str(value) + " (" + str(type(value)) + ")"


Debug = DebugClass()


class View:
    """
    Handles view of kara.
    """
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    
    MIN = 1
    MAX = 4
    __value = 1
    
    def __init__(self, initial=1):
        # type: (int) -> View
        self.set(initial)
    
    def set(self, other):
        # type: (int) -> None
        if other in range(self.MIN, self.MAX + 1):
            self.__value = other
        else:
            raise ValueError('"' + str(other) + '" is not a acceptable value!')
    
    def get(self):
        # type: () -> int
        return self.__value
    
    def add(self, count=1):
        # type: (int) -> None
        for _ in range(count):
            self.__value += 1
            if self.__value > self.MAX:
                self.__value = self.MIN
    
    def subtract(self, count=1):
        # type: (int) -> None
        for _ in range(count):
            self.__value -= 1
            if self.__value < self.MIN:
                self.__value = self.MAX


class Position:
    """
    Handles relative position of Kara.
    """
    
    def __init__(self, initial=None):
        # type: (Optional[List[int, int]]) -> Position
        if initial is None:
            initial = [0, 0]
        
        self.__pos = initial
    
    def add(self, other):
        # type: (Tuple[int, int]) -> None
        if isinstance(other, list) or isinstance(other, tuple):
            self.set((self.__pos[0] + other[0], self.__pos[1] + other[1]))
    
    def subtract(self, other):
        # type: (Tuple[int, int]) -> None
        if isinstance(other, list) or isinstance(other, tuple):
            self.set((self.__pos[0] - other[0], self.__pos[1] - other[1]))
    
    def get(self):
        # type: () -> Tuple[int, int]
        return [self.__pos[0], self.__pos[1]]
    
    def set(self, value):
        # type: (Tuple[int, int]) -> None
        self.__pos[0] = value[0]
        self.__pos[1] = value[1]


class BetterKara:
    ABSOLUTE_VIEW_VIEW = View.UP
    
    def __init__(self, instance, view_initial=View.UP):
        self.instance = instance
        self.view = View(view_initial)
        self.position = Position()
    
    def current_position(self):
        # type: () -> Tuple[int, int]
        return self.position.get()
    
    def current_view(self):
        # type: () -> int
        return self.view.get()
    
    # Rotate
    def turn_left(self):
        # type: () -> BetterKara
        self.instance.turnLeft()
        self.view.subtract()
        return self
    
    def turn_right(self):
        # type: () -> BetterKara
        self.instance.turnRight()
        self.view.add()
        return self
    
    def turn_around(self):
        # type: () -> BetterKara
        return self.turn_right().turn_right()
    
    # Move
    
    def __update_position(self):
        view = self.view.get()
        
        if view == View.UP:
            self.position.add((0, 1))
        elif view == View.RIGHT:
            self.position.add((1, 0))
        elif view == View.DOWN:
            self.position.add((0, -1))
        elif view == View.LEFT:
            self.position.add((-1, 0))
    
    def move(self, check_empty=True):
        # type: (bool) -> BetterKara
        if check_empty and not self.is_empty_front():
            return self
        
        self.instance.move()
        self.__update_position()
        
        return self
    
    def back(self, amount=1, rotate=False):
        # type: (int, bool) -> BetterKara
        # Rotate
        self.turn_around()
        
        # Move amount
        for _ in range(amount):
            self.move()
        
        # Rotate back
        if not rotate:
            self.turn_around()
        
        return self
    
    def backward(self, *args, **kwargs):
        return self.back(*args, **kwargs)
    
    def forward(self, amount=1):
        # type: (int) -> BetterKara
        # Move amount
        for _ in range(amount):
            self.move()
        
        return self
    
    def left(self, amount=1, rotate=False):
        # type: (int, bool) -> BetterKara
        # Rotate
        self.turn_left()
        
        # Move amount
        for _ in range(amount):
            self.move()
        
        # Rotate back
        if not rotate:
            self.turn_right()
        
        return self
    
    def right(self, amount=1, rotate=False):
        # type: (int, bool) -> BetterKara
        # Rotate
        self.turn_right()
        
        # Move amount
        for _ in range(amount):
            self.move()
        
        # Rotate back
        if not rotate:
            self.turn_left()
        
        return self
    
    def __absolute_move_func(self, func, *args, **kwargs):
        current_view = self.current_view()
        
        self.set_view(self.ABSOLUTE_VIEW_VIEW)
        func(*args, **kwargs)
        self.set_view(current_view)
    
    def absolute_right(self, *args, **kwargs):
        self.__absolute_move_func(self.right, *args, **kwargs)
        return self
    
    def absolute_left(self, *args, **kwargs):
        self.__absolute_move_func(self.left, *args, **kwargs)
        return self
    
    def absolute_up(self, *args, **kwargs):
        self.__absolute_move_func(self.forward, *args, **kwargs)
        return self
    
    def absolute_down(self, *args, **kwargs):
        self.__absolute_move_func(self.backward, *args, **kwargs)
        return self
    
    # Sensors
    def is_tree_front(self):
        # type: () -> bool
        return self.instance.treeFront()
    
    def is_tree_left(self):
        # type: () -> bool
        return self.instance.treeLeft()
    
    def is_tree_right(self):
        # type: () -> bool
        return self.instance.treeRight()
    
    def is_tree_back(self):
        # type: () -> bool
        self.turn_around()
        is_tree = self.is_tree_front()
        self.turn_around()
        
        return is_tree
    
    def is_on_leaf(self):
        # type: () -> bool
        return self.instance.onLeaf()
    
    def is_leaf_front(self):
        # type: () -> bool
        self.forward()
        on_leaf = self.is_on_leaf()
        self.back()
        return on_leaf
    
    def is_leaf_left(self):
        # type: () -> bool
        self.left()
        on_leaf = self.is_on_leaf()
        self.right()
        return on_leaf
    
    def is_leaf_right(self):
        # type: () -> bool
        self.right()
        on_leaf = self.is_on_leaf()
        self.left()
        return on_leaf
    
    def is_leaf_back(self):
        # type: () -> bool
        self.back()
        on_leaf = self.is_on_leaf()
        self.forward()
        return on_leaf
    
    def is_mushroom_front(self):
        # type: () -> bool
        return self.instance.mushroomFront()
    
    def is_mushroom_left(self, rotate=False):
        # type: (bool) -> bool
        self.turn_left()
        is_tree = self.is_mushroom_front()
        
        if not rotate:
            self.turn_right()
        
        return is_tree
    
    def is_mushroom_right(self, rotate=False):
        # type: (bool) -> bool
        self.turn_right()
        is_tree = self.is_mushroom_front()
        
        if not rotate:
            self.turn_left()
        
        return is_tree
    
    def is_mushroom_back(self, rotate=False):
        # type: (bool) -> bool
        self.turn_around()
        is_tree = self.is_mushroom_front()
        
        if not rotate:
            self.turn_around()
        
        return is_tree
    
    def is_empty_front(self):
        # type: () -> bool
        return not self.is_tree_front() and not self.is_mushroom_front()
    
    def is_empty_left(self):
        # type: () -> bool
        return not self.is_tree_left() and not self.is_mushroom_left()
    
    def is_empty_right(self):
        # type: () -> bool
        return not self.is_tree_right() and not self.is_mushroom_right()
    
    def is_empty_back(self):
        # type: () -> bool
        return not self.is_tree_back() and not self.is_mushroom_back()
    
    # Handlers
    def set_leaf(self):
        # type: () -> bool
        """Returns whether a leaf was set"""
        if not self.is_on_leaf():
            self.instance.putLeaf()
            return True
        
        return False
    
    def remove_leaf(self):
        # type: () -> bool
        """Returns whether a leaf was removed"""
        if self.is_on_leaf():
            self.instance.removeLeaf()
            return True
        return False
    
    def swap_leaf(self):
        # type: () -> BetterKara
        if self.is_on_leaf():
            self.remove_leaf()
        else:
            self.set_leaf()
        
        return self
    
    # Utils
    def set_view(self, view):
        # type: (int) -> BetterKara
        """Rotates to a given view"""
        for _ in range(4):
            if self.current_view == view:
                break
            self.turn_right()
        
        return self


class BetterKaraWorld:
    TREE = "tree"
    MUSHROOM = "mushroom"
    LEAF = "leaf"
    EMPTY = "empty"
    
    def __init__(self, instance):
        self.instance = instance
    
    def clear(self):
        # type: () -> None
        self.instance.clearAll()
    
    def get_size(self):
        # type: () -> Tuple[int, int]
        return self.instance.getSizeX(), self.instance.getSizeY()
    
    def set_size(self, x, y):
        # type: (int, int) -> None
        self.instance.setSize(x, y)
    
    def check_position(self, x, y):
        # type: (int, int) -> bool
        """Checks whether a given `x` and `y` coordinate exists."""
        size = self.get_size()
        
        # Check if x and y exists
        if x in range(size[0]) and y in range(size[1]):
            return True
        return False
    
    def __set_element(self, x, y, func):
        # Check whether position exists
        if self.check_position(x, y):
            self.set_empty(x, y)
            func(x, y, True)
            return True
        return False
    
    def __remove_element(self, x, y, func):
        if self.check_position(x, y):
            func(x, y, False)
            return True
        return False
    
    def __iterate_positions_do_func(self, func, start_x=None, start_y=None, end_x=None, end_y=None, *args, **kwargs):
        # type: (Callable, Optional[int], Optional[int], Optional[int], Optional[int], *args, **kwargs) -> int
        """
        :param func: The function that should be executed
        :param start_x: The start x position
        :param start_y: The start y position
        :param end_x: The end x position. If None, the field's x size will be taken.
        :param end_y: The end y position. If None, the field's y size will be taken.
        :return: Amount
        """
        counter = 0  # type: int
        size = self.get_size()
        
        if start_x is None:
            start_x = 0
        
        if start_y is None:
            start_y = 0
        
        if end_x is None:
            end_x = size[0]
        
        if end_y is None:
            end_y = size[1]
        
        # Constrain values
        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x = min(size[0], end_x)
        end_y = min(size[1], end_y)
        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if func(x, y, *args, **kwargs):
                    counter += 1
        
        return counter
    
    #
    # Leaf
    #
    
    def set_leaf(self, x, y):
        # type: (int, int) -> bool
        return self.__set_element(x, y, self.instance.setLeaf)
    
    def remove_leaf(self, x, y):
        # type: (int, int) -> bool
        return self.__remove_element(x, y, self.instance.setLeaf)
    
    def remove_all_leafs(self, *args, **kwargs):
        # type: (*args, **kwargs) -> int
        """
        Removes all leafs in a given size.
        :return: Amount of leafs removed
        """
        return self.__iterate_positions_do_func(self.remove_leaf, *args, **kwargs)
    
    #
    # Tree
    #
    
    def set_tree(self, x, y):
        # type: (int, int) -> bool
        return self.__set_element(x, y, self.instance.setTree)
    
    def remove_tree(self, x, y):
        # type: (int, int) -> bool
        return self.__remove_element(x, y, self.instance.setTree)
    
    def remove_all_trees(self, *args, **kwargs):
        # type: (*args, **kwargs) -> int
        """
        Removes all trees in a given size.
        :return: Amount of trees removed
        """
        return self.__iterate_positions_do_func(self.remove_tree, *args, **kwargs)
    
    #
    # Mushroom
    #
    
    def set_mushroom(self, x, y):
        # type: (int, int) -> bool
        return self.__set_element(x, y, self.instance.setMushroom)
    
    def remove_mushroom(self, x, y):
        # type: (int, int) -> bool
        return self.__remove_element(x, y, self.instance.setMushroom)
    
    def remove_all_mushrooms(self, *args, **kwargs):
        # type: (*args, **kwargs) -> int
        """
        Removes all mushrooms in a given size.
        :return: Amount of mushrooms removed
        """
        return self.__iterate_positions_do_func(self.remove_mushroom, *args, **kwargs)
    
    #
    # Utils
    #
    
    def set_empty(self, x, y):
        # type: (int, int) -> bool
        field_type = self.get_field_type(x, y)
        
        if field_type:
            # Get method and execute it
            getattr(self, "remove_" + field_type)(x, y)
            return True
        
        return False
    
    def get_field_type(self, x, y):
        # type: (int, int) -> Optional[str]
        if self.check_position(x, y):
            # Check empty first, because it will be probably the most common field
            if self.instance.isEmpty(x, y):
                return self.EMPTY
            elif self.instance.isTree(x, y):
                return self.TREE
            elif self.instance.isLeaf(x, y):
                return self.LEAF
            elif self.instance.isMushroom(x, y):
                return self.MUSHROOM
        return
    
    def set_field_type(self, x, y, field_type):
        # type: (int, int, str) -> bool
        
        if field_type == self.EMPTY:
            self.set_empty(x, y)
            return True
        elif field_type == self.LEAF:
            self.set_leaf(x, y)
            return True
        elif field_type == self.TREE:
            self.set_tree(x, y)
            return True
        elif field_type == self.MUSHROOM:
            self.set_mushroom(x, y)
            return True
        
        return False
    
    def replace_field_type(self, x, y, old, new):
        # type: (int, int, str, str) -> bool
        """
        Replaces a field with `new` type if the current type is `old`.
        :param x: X position
        :param y: Y position
        :param old: The current field type
        :param new: The new field type
        :return: Whether the field got replaced
        """
        field_type = self.get_field_type(x, y)
        
        if field_type == old:
            self.set_field_type(x, y, new)
            return True
        return False
    
    def replace_all_field_types(self, old, new, *args, **kwargs):
        # type: (str, str, *args, **kwargs) -> counter
        kwargs["old"] = old
        kwargs["new"] = new
        
        return self.__iterate_positions_do_func(self.replace_field_type, *args, **kwargs)


class BetterKaraTools:
    def __init__(self, instance):
        self.instance = instance
    
    def __build_string(self, message, sep=" "):
        # type: (str, str) -> str
        if type(message) is list:
            string = sep.join(message)
        else:
            string = message
        
        return string
    
    def show_message(self, message, sep=" "):
        # type: (str, str) -> None
        self.instance.showMessage(self.__build_string(message, sep))
    
    def print(self, message, sep=" "):
        # type: (str, str) -> None
        # println doesn't work for me.
        self.instance.println(self.__build_string(message, sep))
    
    def random_int(self, max, min=0):
        # type: (int, int) -> int
        """Returns a random integer between `min` and `max`"""
        return self.instance.random(max - min) + min
    
    def input(self, type="string", title="Input"):
        """
        Shows an input prompt and casts the value to a given type.
        :param type: The type the value should be cast to. Available types:
            - string
            - int
            - float
            - bool
        :param title: The title
        :return: The value
        """
        # type: (str, str) -> Union[str, int, float, bool]
        value = self.instance.stringInput(title)  # type: str
        
        if type == "string":
            return value
        elif type == "int":
            return int(value)
        elif type == "float":
            return float(value)
        elif type == "bool":
            value = value.lower()
            
            return value == "1" or value == "true" or value == "y"
    
    def sleep(self, duration):
        # type: (int) -> None
        self.isntance.sleep(duration)


kara = BetterKara(kara, View.UP)  # Edit `View.UP` to your correct value
world = BetterKaraWorld(world)
tools = BetterKaraTools(tools)
