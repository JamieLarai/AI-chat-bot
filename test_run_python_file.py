import os
from functions.run_python_file import run_python_file
def run_test(working_directory, file_path, args, description):
    print(f'run_python_file("{working_directory}", "{file_path}", {args}):')
    result = run_python_file(working_directory, file_path, args)
    print(f"Result for {description}:")
    print(result)
    print()
# Test 1: calculator main.py
run_test("calculator", "main.py", None, "main.py without args")
# Test 2: calculator main.py with args
run_test("calculator", "main.py", ["3 + 5"], "main.py with args")
# Test 3: calculator tests.py
run_test("calculator", "tests.py", None, "tests.py")
# Test 4: calculator ../main.py
run_test("calculator", "../main.py", None, "../main.py")
# Test 5: calculator nonexistent.py
run_test("calculator", "nonexistent.py", None, "nonexistent.py")
# Test 6: calculator lorem.txt
run_test("calculator", "lorem.txt", None, "lorem.txt")