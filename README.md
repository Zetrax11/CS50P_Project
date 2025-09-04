# Expense tracker

## Description:

The expense tracker helps you record monthly spending, visualize expenses by category and compare costs across different months to better manage your budget.

## Project tree
```
. 
├─ icon.png
├─ my_classes.py
├─ project.py
├─ README.md
├─ requirements.txt
├─ test_project.py
└─ users.txt
```
## Files content
- `my_classes.py` contains PyQt5 class which implements GUI interface and relations between each widget.
- `project.py` contains `main` function with 3 additional functions: `save_file`, `load_expenses` and `log_in`.

`save_file` - takes two arguments: `path` and `expenses` and writes data (expenses added to GUI in session) into a passed file.

`load_expenses` - takes one argument: `path` and loads data from that specific path.

`log_in` - takes no arguments, but calls for user input `username` and `password` (password is inputed by getpass function, so it shows no marks in terminal window).
Once user inputs their data, function validates it's credentials (comparing it with the data from `users.txt` file). User has three login attempts, if they fail to enter the correct configuration three times, function will return `False` and program will terminate.

- `test_project.py` contains pytest test cases for 3 additional functions
- `requirements.txt` contains all necessary libraries
- `users.txt` contains valid user credentials

## Setup
1. **Git clone project**

2. **Install all necessary libraries**
```
pip install -r requirements.txt
```
3. **Create account**
- In users.txt file add
```
username|password
```
4. **Run project**
- Windows
```
python project.py
```
- Linux
```
python3 project.py
```

## Functionality
- Creating our own profile, protected by password.

To make a new profile type [Username]|[Password] in a new line in users.txt file.

- Adding expenses into a list, divided by category and month.

In order to do that, type in form amount of spent PLN, select a category and pick in which month that spending was made.

- Added expenses will be saved into a json file with username suffix, so it will be accessable between sessions.

Each user has he's own json file called "expenses_[user].json".

- Deleting picked expense.

Choose an item from the list and click "Usuń wiersz" button.

- Deleting all expenses.

Click red button "Wyczyść listę".

- Expenses are added to a pie chart by month, to switch between pie charts, select another month in a form above.

Pie chart is on second page called "Wykresy kołowe", to change selected month click on a dropdown list with "Miesiąc:" label and select different month.

- Expenses are added to a bar chart, on which monthly spendings are compared by category

Bar chart is on thrid page called "Porównanie m->m". It's purpose is to show difference in amount spent by category in each month.

- Above the list of added expenses there's a label that shows total amount of PLN spent in selected month.

To change selected month click on a dropdown list with "Miesiąc:" label and select different month.

## Design
- The expense tracking tool GUI was created using the `PyQt5` library, `Tkinter` was also considered for the GUI. Due to the greater capabilities of PyQt5, I decided it would be worthwhile to learn its syntax and methods. PyQt6 was rejected due to a lack of sufficient documentation.
