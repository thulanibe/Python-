from random   import randrange 
def main ():
    number = randrange(100)
    while True:
        guess = int(input("?"))
        if guess == number :
            print("You win!")
            break

        if __name__ == '__main__':
            main()
