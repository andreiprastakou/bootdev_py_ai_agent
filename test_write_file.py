import os

from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
if os.path.exists("calculator/lorem.txt"):
    os.remove("calculator/lorem.txt")

print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
if os.path.exists("calculator/pkg/morelorem.txt"):
    os.remove("calculator/pkg/morelorem.txt")

print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
