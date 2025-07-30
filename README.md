# Sports Schedule Maker

## Overview
The goal of this project is to create optimal schedules for sports leagues based on team info, playing locations, matchup restrictions, fan attendance, travel time, and other constraints. 

## Features
* **Matchup Generation**: Automatically generate matchups for teams in a league.
* **High-Level Schedule Solver**: Utilize a Gurobi solver to create optimized combination of matchups per week.
* **Low-Level Schedule Solver**: Utilize a Gurobi solver to create optimized combination of matchups within a certain week, dependent on fan attendance, stadium availability, TV time slots, etc.
* **GUI Integration**: A user-friendly GUI to visualize and interact with the generated schedules.

## Usage Guide

### Clone
Clone the repository:
```sh
git clone https://github.com/foldupcircle/sports-schedule-maker.git
cd backend
```

### Acquire Gurobi License
To run the solver you're going to need a Gurobi Optimization License. This is free for academics users, paid otherwise.

1. Navigate to the [Gurobi User Portal](https://portal.gurobi.com/iam/login/?target=https%3A%2F%2Fportal.gurobi.com%2F) and make an account.

2. Navigate to the Licenses Tab on the Left Panel and click (+) Request. Choose a license that is appropriate for you. I chose the "Named-User Academic" one.

3. Once your license has been created, go to the Licenses/Licenses Tab and click the TV-Download Button on the right side of your license to see installation instructions. Follow this to finish getting Gurobi on your machine.

### Installation
Install the required packages:
```sh
pip install -r requirements.txt
```

### Using the GUI
Run the GUI application from within the backend folder:
```sh
python -m gui
```

Click "Generate Schedule" to run the optimization. This will execute the main solver and generate the schedule based on the provided constraints and team information (currently set internally to NFL requirements). It will take 3-4 minutes to finish.

And that's it!
