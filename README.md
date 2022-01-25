# sidekus
Offline sudoku interface based on https://cracking-the-cryptic.web.app/ - to ensure that I can do my sudokus offline. The only real issue with the linked app is that either you cannot input your own sudokus, or you find those sudokus behind a paywall. Of course there will be enough and more programs that do this online, but writing this is an excuse for an easy personal project.

## Core functionality
Core functionality of this program will be to 
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
 In this sudoku, the digits in black were the givens. The 1 in box 8 was input by hand and so it shows up in blue. The middle tile of box 2 can only be 6 or 7, and is represented as such in green. The 4 in box 5 must be in the top row, and is represented as such in red. Essentially, this is the crux of Snyder notation, allowing for easier insights in solving a sudoku. 
 ![Link to image](https://github.com/nimberledge/sidekus/blob/main/images/sideuk.png "Example Sudoku")

 ## Usage
 To use this, install the requirements using pip and then run main.py using 
 ```python3 src/main.py```
 You can add your own sudoku into the data directory and load it by changing an early line of main.py that currently reads 
 ```board = SudokuBoard(input_file='data/example1.txt')```
 replacing data/example1 with data/*filename*. 

 Alternatively, you can supply the sudoku file as a command line argument, for example
```python3 src/main.py data/<filename>```


 In order to solve the sudoku, selecting a cell and just typing a number will input that number in blue, and represents that you have solved for that digit. To use the green pencil-mark, select cells using the mouse or Ctrl + click, and then use Ctrl + digits to enter the pencil-marks. Similarly, for the red pencil mark, select appropriate cells and then use Shift + digits. To delete a pencil mark, simply try to "add" it again using the same procedure and it should disappear. To delete a digit in blue, try to add a single pencil mark and it will disappear.

 Once you're finished, click Check Solution, which will then tell you if you've made an error. Note that this will only work if you have filled in all digits in blue.
