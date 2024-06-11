# Chess Tournaments Manager

This project is used to manage chess tournaments.
You start by creating players and then tournaments. 
You then ‘play’ a tournament to register players and launch the match generator. 
All that remains is to enter the Win/Loss results of each match to determine a winner. 
The manager can also generate tournament reports.

This project uses flake8 to analyse Python code and generate an HTML report of style errors and warnings.


## Project Structure


├── Main.py

├── controllers/

├── data/

├── flake8_rapport

├── models/

├── venv/

├── views/

└── run_flake8.py
└── main.py


## Prerequisites

- Python 3.x
- pip
- virtualenv

## How to use the programme
### 1. Run the main.py script
### 2. Follow the on-screen commands

You can add or consult the player database, create tournaments, register players and enter scores. You can also generate tournament reports. 
Players and tournaments are stored as JSON data for the time being, but can be integrated into HTML views or an application interface.


## Steps to configure and run flake8

### 1. create and activate a virtual environment

1. Open a terminal or command prompt.
2. Navigate to your project directory :

    ```bash
    cd your\path\echecs
    ```

3. Create a virtual environment :

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

### 2. install dependencies

With the virtual environment enabled, install flake8 and flake8-html :

    
    pip install flake8 flake8-html
    

### 3. run flake8

    
    python run_flake8.py
    

