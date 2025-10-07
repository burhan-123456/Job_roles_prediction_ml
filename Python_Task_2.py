import os

# Ask user for file names
source = input("Enter source file name: ")
destination = input("Enter destination file name: ")

# Check if source file exists
if not os.path.exists(source):
    print("Error: Source file not found!")
else:
    # Open files and copy content
    with open(source, "r") as f1, open(destination, "w") as f2:
        data = f1.read()
        f2.write(data)
    print("File copied successfully!")
