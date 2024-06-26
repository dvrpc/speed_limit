# Speed Limit Setting

Exploring Speed Limit and travel speed data for the FY2024 Philadelphia Speed Limit Setting study

### Environment Setup

To set up virtual environment to allow use of plan belt:

```
python -m venv ve
ve\scripts\activate #use this to activate virtual environment after navigating to correct folder
pip install git+https://github.com/dvrpc/plan-belt
```

To save the edited virtual environment for future use:

```
pip list --format=freeze > requirements.txt
```

To use a previously saved requirements.txt files:

```
pip install -r requirements.txt
```

### Running Scripts

To run any of the scripts in this repo, activate the conda environment, change directory to the project folder, and then run the `python` command followed by the path to the file. For example:

```
d:
cd dvrpc_shared/speed_limit
ve\scripts\activate
python scripts/{script_name}.py
```

### Order of opperations

1. data_setup.py
2. conflator_bike.py
3. conflator_sidewalks.py
4. conflator_circuittrails.py
5. assign_goal_speeds_1.py
6. assign_goal_speeds_2.py
7. assign_goal_speeds_3.py
8. assign_goal_speeds_4.py
