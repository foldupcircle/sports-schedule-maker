# Schedule Maker

## Overview
The goal of this project is to create optimal schedules for sports leagues based on team info, playing locations, matchup restrictions, fan attendance, travel time, and other constraints. 

## Features
* **Matchup Generation**: Automatically generate matchups for teams in a league.
* **High-Level Schedule Solver**: Utilize a Gurobi solver to create optimized combination of matchups per week.
* **Low-Level Schedule Solver**: Utilize a Gurobi solver to create optimized combination of matchups within a certain week, dependent on fan attendance, stadium availability, TV time slots, etc.
* **GUI Integration**: A user-friendly GUI to visualize and interact with the generated schedules.

## Usage Guide

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/your-organization/schedule-maker.git
    cd schedule-maker/backend
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Acquire Gurobi License
To run the solver you're going to need a Gurobi Optimization License. This is free for academics users, paid otherwise.

1. Navigate to [this link](https://support.gurobi.com/hc/en-us/articles/12684663118993-How-do-I-obtain-a-Gurobi-license) to acquire your license.

2. 
### Using the GUI
Run the GUI application from within the backend folder:
```sh
python -m gui
```

This will execute the main solver and generate the schedule based on the provided constraints and team information.
