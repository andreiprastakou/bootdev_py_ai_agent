from functions.run_python_file import run_python_file

print("(should print the calculator's usage instructions)")
print(run_python_file("calculator", "main.py"))
print("(should run the calculator... which gives a kinda nasty rendered result)")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("(should run the tests.py file)")
print(run_python_file("calculator", "tests.py"))
print("(this should return an error)")
print(run_python_file("calculator", "../main.py"))
print("(this should return an error)")
print(run_python_file("calculator", "nonexistent.py"))
print("(this should return an error)")
print(run_python_file("calculator", "lorem.txt"))
