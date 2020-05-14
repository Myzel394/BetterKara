# What does this script provide you?
This script enables you to use an easier API for the [PythonKara](https://www.swisseduc.ch/informatik/karatojava/pythonkara/) Project. You can use commands like `kara.is_tree_left()`, `kara.is_mushroom_back()` or `kara.left(4)` which helps you writing code easier.

# Quickstart
Copy the code of [betterkara.py](betterkara.py) and paste it into your file. Some variables are overwritten, these provide you the better API.

# Examples

    # Here is the copy-pasted code...  
      
    # Sets leafs until Kara hits a tree  
    while not kara.is_tree_front():  
        kara.set_leaf()  
        kara.forward()  
      
      
    # If a mushroom is behind Kara, he will be moved behind it  
    if kara.is_mushroom_back():  
        kara.left()  
        kara.back(2)  
        kara.right()  
      
      
    # Moves Kara to the next hole on the left side  
    while True:  
        if not kara.is_empty_left():  
            kara.forward()  
        else:  
            kara.left()  
      
      
    # Lets Kara fill out a closed figure with leafs  
    while True:  # Do-While  
      if not kara.is_tree_front():  
            if kara.is_tree_left():  
                # Tree is left, fill out everything on the right  
      kara.turn_right()  
                move_and_set_leaves()  
                kara.turn_left()  
                  
                # Forward for next step  
      kara.forward()  
            else:  
                # No tree in front, fill out everything in front  
      move_and_set_leaves()  
                  
                # To left for next step  
      kara.turn_left()  
                kara.forward()  
        else:  
            # To the left if there is no tree  
      if not kara.is_tree_left():  
                kara.turn_left()  
                kara.forward()  
            else:  
                # Turn around  
      kara.turn_around()  
          
        if kara.current_position() == start_position:  # Do-While  
     # Kara is on start position  break  
      
      
    # Moves Kara out of a maze  
    while not kara.is_on_leaf():  
        if kara.is_tree_left():  
            if kara.is_tree_front():  
                kara.turn_right()  
        else:  
            kara.turn_left()  
          
        kara.forward()

# Code
## Main classes
### Kara
#### Attributes
|Value|Description|
|--|--|
|instance|The "old" kara instance|
|view|The view handler (handles the current view of Kara)|
|position|The relative position handler (handles the current position of Kara)|
#### Methods
Move functions will automatically check for trees, etc. If there is an immovable object in the way, Kara won't be moved.
|Value|Description|Parameters|Return|
|--|--|--|--|
| **Rotate**
| `turn_left`, `turn_right` | Turns Kara to the left | - | None |
| turn_around | Turns Kara around | - | None |
| **Move**
| `forward` `backward` `left` `right` | Moves Kara x steps to the correlating direction| `amount` - The amount of steps that should be moved | None |
| absolute_up | Moves Kara x steps up, not relative to Kara but to the grid | `amount` - The amount that should be moved | None |
| absolute_down | Moves Kara x steps down, not relative to Kara but to the grid | `amount` - The amount that should be moved | None |
| absolute_left | Moves Kara x steps left, not relative to Kara but to the grid | `amount` - The amount that should be moved | None |
| absolute_right | Moves Kara x steps right, not relative to Kara but to the grid | `amount` - The amount that should be moved | None |
| **Sensors**
| `is_tree_front` `is_tree_back` `is_tree_left` `is_tree_right` | Checks whether a tree at this side of Kara | - | `bool` - Whether there is a tree |
| `is_leaf_front` `is_leaf_back` `is_leaf_left` `is_leaf_right` | Checks whether a leaf at this side of Kara | - | `bool` - Whether there is a leaf|
| `is_on_leaf` | Checks whether Kara is on a leaf | - | `bool` - Whether Kara is on leaf|
| `is_mushroom_front` `is_mushroom_back` `is_mushroom_left` `is_mushroom_right` | Checks whether a mushroom at this side of Kara | - | `bool` - Whether there is a mushroom|
| `is_empty_front` `is_empty_back` `is_empty_left` `is_empty_right` | Checks whether the side is empty | - | `bool` - Whether there is nothing|
| **Handlers**
| `set_leaf` `remove_leaf` | Sets/Removes a leaf  | - | `bool` - Whether the leaf got placed/removed |
| `swap_leaf` | Swaps the leaf, i.e. Kara is on leaf -> removes it,   | - | `bool` - Whether the leaf got placed/removed |
