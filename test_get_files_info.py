from functions.get_files_info import get_files_info

def run_test(working_directory, directory, description):
    print(f"get_files_info(\"{working_directory}\", \"{directory}\"):")
    result = get_files_info(working_directory, directory)
    print(f"Result for {description}:")
    if isinstance(result, list):
        for item in result:
            print(f"  {item}")
    else:
        print(f"    {result}")
    print()

# Test 1: calculator .
run_test("calculator", ".", "current directory")

# Test 2: calculator pkg
run_test("calculator", "pkg", "'pkg' directory")

# Test 3: calculator /bin
run_test("calculator", "/bin", "'/bin' directory")

# Test 4: calculator ../
run_test("calculator", "../", "'../' directory")
