try:
  file = open('file_name.txt')
except IOError as error:
  print('File not found')