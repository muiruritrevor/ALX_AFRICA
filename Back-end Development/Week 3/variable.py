#Global keyword
''' 
X = 15

def change():

    global X

    X = X + 5
    print(f"Value of X inside function: {X}")

change()
print(f"Value of X outside function: {X}")

'''

count = 0 

def increment_global():
    global count
    count += 1
increment_global()
print(count)