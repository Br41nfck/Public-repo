# Count and show files in dir
import os
path = input("Enter path: ")
total_files = 0
total_dirs = 0

obj = os.scandir(path)
print("Files and dirs in '% s':" % path)
for entry in obj:
    if entry.is_dir() or entry.is_file():
        print(entry.name)

print("\n\n")

for base, dirs, files in os.walk(path):
    print("Searching in:", base)
    for directory in dirs:
        total_dirs += 1
    for file in files:
        total_files += 1
        
print("\n\nTotal files:", total_files)
print("Total dirs:", total_dirs)
print("Total:", total_dirs + total_files)