# Speed Limit Setting

Exploring Speed Limit and travel speed data for the FY2024 Philadelphia Speed Limit Setting study

### Environment Setup

To create the python environment, run the next line in a conda prompt from the project directory:

`conda env create -f environment.yml`

To activate the new environment, run the following line:

`conda activate speed_limit_setting`

To update the environment as changes are needed, run the following line:

`conda env update -f environment.yml`

### Running Scripts

To run any of the scripts in this repo, activate the conda environment, change directory to the project folder, and then run the `python` command followed by the path to the file. For example:

```
conda activate speed_limit_setting
d:
cd dvrpc_shared/speed_limit
python /scripts/{script_name}.py
```

python -m venv ve
ve\scripts\activate #use this to activate virtual environment after navigating to correct folder
pip install git+https://github.com/dvrpc/plan-belt

#

pip list --format=freeze > requirements.txt

#to use a previously saved requirements.txt files
pip install -r requirements.txt
