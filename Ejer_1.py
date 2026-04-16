if __name__ == "__main__":
    n = int(input("ingresa un numero mayor a 5 y menor a 20: "))

    if n <= 5 or n >= 20:
        print("Error: el número debe ser mayor a 5 y menor a 20")
    else:
        i = 0
        while i < n:
            j = 0
            print("# ", end="")
            while j < i:
                print("*", end="")
                j += 1
            num = n - i
            while num > 0:
                print(num, end="")
                num -= 1
            print() 
            i += 1