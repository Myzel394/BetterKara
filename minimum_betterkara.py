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

kara = BetterKara(kara, View.UP)
