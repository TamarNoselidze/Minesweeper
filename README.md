# Minesweeper in Python

A classic Minesweeper game built with Python using the Tkinter library for the graphical interface. 
This version allows players to reveal squares, place flags, and win by flagging all mines without triggering any of them.


## Features

- Customizable board size and number of mines
- Graphical interface built with Tkinter
- Visual representation of mines, flags, and adjacent mine counts
- Game restart and help functionality
- Simple recursive algorithm for revealing empty squares


## Prerequisites

To run this program, you'll need to have Python installed, along with the following libraries:

  - Tkinter (Standard GUI library in Python, comes pre-installed)
  - Pillow (For handling image files)

You can install the required libraries using pip:

`pip install pillow`



## How to Run the Game

  - Clone the Repository
  - Clone this repository to your local machine using:
     `git clone https://github.com/yourusername/minesweeper-python.git`

  - Navigate to the Project Directory: `cd minesweeper-python`
  - Run the Program: execute the following command to start the game: `python3 minesweeper.py`


Make sure the following files are in the same directory as the Python file:

    rules.txt (Contains the game's help text)
    flag.png (Image used for flags)
    mine.png (Image used for mines)


## Play the Game

    Left Click on squares to reveal them.
    Right Click to place a flag where you suspect a mine.
    Restart the game using the "Restart" button.
    Access the game rules by clicking the "?" button.