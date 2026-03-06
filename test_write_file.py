import os
from functions.write_file import write_file
def run_test(working_directory, file_path, content, description):
    print(f'write_file("{working_directory}", "{file_path}", "{content}"):')
    result = write_file(working_directory, file_path, content)
    print(f"Result for {description}:")
    print(result)
    print()
# Test 1: write to existing file
run_test("calculator", "lorem.txt", "wait, this isn't lorem ipsum", "write to existing file")
# Test 2: write to new file in existing directory
run_test("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet", "write to new file in existing directory")
# Test 3: write to new file in new directory
run_test("calculator", "newdir/newfile.txt", "this is a new file in a new directory", "write to new file in new directory")
# Test 4: write to file outside working directory
run_test("calculator", "/tmp/temp.txt", "this should not be allowed", "write to file outside working directory")
# Cleanup: remove the new files and directories created during testing
try:
    os.remove("calculator/pkg/morelorem.txt")
    os.remove("calculator/newdir/newfile.txt")
    os.rmdir("calculator/newdir")
except Exception as e:
    print(f"Cleanup error: {e}")