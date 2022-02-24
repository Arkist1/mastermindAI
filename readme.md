# Mastermind

A few algorithms for the game mastermind.

## Example code for human game:
    from main import Mastermind
    
    # create a human game
    Mastermind(method="human")


## Example code calculating averages
    from main import Mastermind

    # calculate accuracy:
    averages = []
    
    # play 100 games
    for x in range(0, 100):
        averages.append(len(Mastermind(method="simple").guesses))

    # calculate result
    result = sum(averages) / len(averages)
        
    # print result
    print(f"The simple algorithm gets the answer in an average of {result} tries)