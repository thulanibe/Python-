file = open("hello.txt", "w")

try:
    file.write("Hello, World!")
finally:
    # Make sure to close the file after using it
    file.close()