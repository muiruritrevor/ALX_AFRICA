#for loop
#Control statements that can be used with for loop
# 1. continue statement
'''returns the control to the beginning of the loop'''

# Prints all letters except 'e' and 's'
'''

for letter in 'trevorking':
    if letter == 'e' or letter == 'r':
        continue
    print('Current letter:', letter)

'''

# 2.break statement
'''brings control out of the loop'''

'''
for letter in 'trevorking':
    # break the loop as soon as it sees 'e'
    # or 'r'
    if letter == 'e' or letter == 's':
        break
print('Current letter:', letter)

'''
