from functions.run_python import run_python_file

print("Testing calculator main.py:")
print(run_python_file("calculator", "main.py"))
print()

print("Testing calculator main.py with args [\"3 + 5\"]:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print()

print("Testing calculator tests.py:")
print(run_python_file("calculator", "tests.py"))
print()

print("Testing attempt to run code outside of working directory (should error):")
print(run_python_file("calculator", "../main.py"))
print()

print("Testing attempt to run nonexistent file (should error):")
print(run_python_file("calculator", "nonexistent.py"))
print()
