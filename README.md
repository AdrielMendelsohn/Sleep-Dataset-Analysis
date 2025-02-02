# Summary of the project:
In this project we tried to answer the research question: "Which factors have the most influence on the quality of life of students and their grades, and in particular what role does sleep play in them?"

We used data from 2 different sources, and reached conclusions according to the correlations and other statistical analysis between the different variables.

We presented our conclusions both verbally in the project documentation and visually through a variety of graphs.

We created a simple GUI to allow the user to perform the analysis like we did, and to save/show the results.



# Project Data:
https://studentlife.cs.dartmouth.edu/datasets.html

https://www.kaggle.com/datasets/mexwell/cmu-sleep



# Project Documentation:
https://docs.google.com/document/d/1EuhUgPbQv9cm5URP9kPPVjonuXNGIupUdfYly7VrroQ/edit?usp=sharing



# Setting Up This Python Project with Virtualenv

## To run the project, follow these commands:
All commands should be run under the project root/working directory.

## 1. Install Virtualenv
Virtualenv is a tool that helps create isolated Python environments.

```bash
pip install virtualenv
```

## 2. Create a Virtual Environment
This command creates a virtual environment named `venv` (you can replace `venv` with any name you prefer).

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment
- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```

- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

You should see `(venv)` as a prefix in your terminal after activation.

## 4. Update `pip` (Python Package Installer)
Ensure that `pip` inside your virtual environment is up to date.

```bash
python -m pip install --upgrade pip
```

## 5. Install Project Dependencies
Install all the necessary packages for running the project.

```bash
pip install -e .
```

## 5.5. (Optional) Install Development Dependencies
These include tools for testing, linting, and other development-related tasks.

```bash
pip install -e .[dev]
```

## 6. (Optional) Adding the 'Student Lifestyle' data
In order to run the code we wrote to extract data from the 'Student Lifestyle' data, download it from the attached link and add the resulting 'StudentLife' folder into the 'data' folder in the project.

```bash
https://studentlife.cs.dartmouth.edu/datasets.html
```
After that, all you have to do to run the code is to select the 'Create Excel' option in the interactive window that opens when you run the program.

## 7. (Optional) Running tests
Run the unit tests included in the project using the following command.

```bash
tox
```

## 8. Running the Program
### On Windows:
```bash
python src\main.py
```

### On Linux/Mac:
```bash
python3 src/main.py
```

---
You are now ready to develop and run your project within this isolated environment! Happy coding!
