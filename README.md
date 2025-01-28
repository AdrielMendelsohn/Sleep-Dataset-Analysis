## Summary of the project:
In this project we tried to answer the research question: "Which factors have the most influence on the quality of life of students and their grades, and in particular what role does sleep play in this?"

We used data from 2 different sources, and reached conclusions according to the correlations between the different variables.

We presented our conclusions both verbally in the project documentation and visually through a variety of graphs.



## Project Data:
https://studentlife.cs.dartmouth.edu/datasets.html

/////////////////////////second dataset///////////////////////



## Project Documentation:
https://docs.google.com/document/d/1EuhUgPbQv9cm5URP9kPPVjonuXNGIupUdfYly7VrroQ/edit?usp=sharing



## To run the project follow this commands:
All command should run under project root/working-directory

```
#install Virtualenv is - a tool to set up your Python environments
pip install virtualenv
#create virtual environment (serve only this project):
python -m venv venv
#activate virtual environment
.\venv\Scripts\activate
+ (venv) should appear as prefix to all command (run next command just after activating venv)
#update venv's python package-installer (pip) to its latest version
python.exe -m pip install --upgrade pip
#install projects packages (Everything needed to run the project)
pip install -e .
#install dev packages (Additional packages for linting, testing and other developer tools)
pip install -e .[dev]
```
