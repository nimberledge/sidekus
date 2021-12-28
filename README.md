# sidekus
Offline sudoku interface based on https://cracking-the-cryptic.web.app/ - to ensure that I can do my sudokus offline. The only real issue with the linked app is that either you cannot input your own sudokus, or you find those sudokus behind a paywall. Of course there will be enough and more programs that do this online, but writing this is an excuse for an easy personal project.

## Core functionality
Core functionality of this program will be to 
* Be able to input an arbitrary sudoku and check if it has a unique solution
* Be able to use the interface to solve the sudoku, allowing for Snyder notation pencil-marking (why is it so difficult to find a decent reference?)
* Be able to undo and redo actions (?)
* Be able to time the solve and reset the puzzle to initial state
* Be able to check the final answer for repeats

## Extended functionality
Once the above are implemented, we can maybe
* Start adding human logic solvers that sort of explain a thought process
* Allow for more advanced sudoku rules and graphics
* Maybe make this some sort of online interface

## Install
All packages needed will end up in requirements.txt but in my head it just looks like pygame + pure python should be plenty since speed is not really an issue when your problem size is never realistically larger than 9x9. So I guess 
```python3 -m pip install -r requirements.txt```
 and you're off to the races.

 ## Example
 In this sudoku, the blue 7s in box 8 indicate that the seven lives in one of those two squares. In contrast, in row 9 column 7, the only 2 possibilities for that box are a 6 and 8 indicated by the center pencil-marking.
 ![Alt text](https://github.com/nimberledge/sidekus/tree/main/images/sidekus.png "Example Sudoku")