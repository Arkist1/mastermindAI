import itertools
import random


colours = ["a", "b", "c", "d"]

permutations = list(itertools.product(colours, repeat=2))

i = 0
for x in permutations:
    print("".join(x), end=' ')
    i += 1
    
    if i == len(colours):
        print()
        i = 0
        
        
solution = "".join(permutations[random.randint(0, len(permutations))])
print(solution)
guess = ""

while guess is not solution:
    guess = input()
