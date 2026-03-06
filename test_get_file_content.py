from functions.get_file_content import get_file_content
import config

def run_test(working_directory, file_path, description):
    print(f'get_file_content("{working_directory}", "{file_path}"):')
    result = get_file_content(working_directory, file_path)
    print(f"Result for {description}:")
    print(result)
    print()
# Test 1: calculator lorem.txt
run_test("calculator", "lorem.txt", "lorem.txt content")
# Test 2: calculator main.py
run_test("calculator", "main.py", "main.py content")
# Test 3: calculator pkg/calculator.py
run_test("calculator", "pkg/calculator.py", "pkg/calculator.py content")
# Test 4: calculator /bin/cat
run_test("calculator", "/bin/cat", "/bin/cat content")
# Test 5: calculator pkg/does_not_exist.py
run_test("calculator", "pkg/does_not_exist.py", "pkg/does_not_exist.py content")