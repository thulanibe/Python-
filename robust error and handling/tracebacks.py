
import traceback

A = [1, 2, 3, 4]

try:
	value = A[5]
	
except:
	traceback.print_exc()


print("end of program")
