# Import de random module
import random

# Itertools voor de codepermutaties
import itertools


class Mastermind():
    # Spelopties
    kleuren = []
    lengte = 0
    duplicates = True
    max_guesses = 10
    
    # De huidige code
    code = ('R', 'R', 'R', 'R')
    
    # De antwoorden die nog mogelijk zijn
    potential = []
    
    # Houdt de vorige geraden antwoorden bij
    guesses = []
    
    # Constructor
    def __init__(self, kleuren=['R', 'O', 'Y', 'G', 'C', 'B'], lengte=4, duplicates=True, max_guesses=10,
                 method="human"):
        self.kleuren = kleuren
        self.lengte = lengte
        self.duplicates = duplicates
        self.max_guesses = max_guesses
        self.method = method
        self.expectedfeedback = {}
        
        # Reset de code, guesses, etc.
        self.reset()
        
        # Print informatie voor de speler
        print("De mogelijke kleuren zijn: " + str(self.kleuren))
        print("De code heeft lengte: " + str(self.lengte))
        if duplicates:
            print("De code kan meerdere keren dezelfde kleur bevatten.")
        else:
            print("Elke kleur komt maar een keer voor in de code.")
        print("Aantal pogingen beschikbaar: " + str(self.max_guesses))
        
        # Start het spel
        self.play()
    
    # Genereer alle permutaties voor de codes
    def permutaties(self):
        
        # Mogen we dubbele kleuren gebruiken?
        if (self.duplicates):
            perms = itertools.product(self.kleuren, repeat=self.lengte)
        else:
            perms = itertools.permutations(self.kleuren, self.lengte)
        
        # Zet de permutaties om naar een lijst i.p.v. itertools object
        return [p for p in perms]
    
    # Genereer een code voor Mastermind (zonder permutaties)
    def generate_code(self):
        
        # Mogen er dubbele kleuren in de code zitten?
        if (self.duplicates):
            # Geef code met eventueel dubbele kleuren terug
            return tuple(random.choices(self.kleuren, k=self.lengte))
        else:
            # Geef code met unieke kleuren terug
            return tuple(random.sample(self.kleuren, k=self.lengte))
    
    # Start een nieuw spel
    def reset(self):
        
        # Maak een code
        self.code = self.generate_code()
        print("De supergeheime code is: " + str(self.code))
        
        # Verwijder de oude geraden antwoorden
        self.guesses = []
        
        # Stel alle mogelijke overgebleven antwoorden in
        self.potential = self.permutaties()
    
    # Kijk of een antwoord valide is
    def valide(self, guess):
        
        # Is de guess van de juiste lengte?
        if (self.lengte != len(guess)):
            print("De code moet lengte " + str(self.lengte) + " hebben.")
            return False
        
        # Bevat de guess wel de goede kleuren?
        for c in guess:
            if (not c in self.kleuren):
                print("De mogelijke kleuren zijn " + str(self.kleuren))
                return False
        
        # Code is valide
        return True
    
    # Pas de overgebleven opties voor de code aan
    def update_mogelijkheden(self, feedback, guess):
        if self.method == "AI":
            # Loop over alle overgebleven codes
            newcodes = []
            
            for code in self.potential:
                if geef_feedback(code, guess) == feedback:
                    newcodes.append(code)
            
            # nieuwe codes
            self.potential = newcodes
            return
        
        # self.potential gelijkstellen aan de waarde die we eerder hadden gegenereerd
        elif self.method == "expected" or self.method == "unexpected":
            self.potential = self.expectedfeedback[feedback]
    
    # Speel het spel
    def play(self):
        
        # Heeft de speler al gewonnen?
        gewonnen = False
        
        # Houd het aantal pogingen bij
        no_guesses = 0
        
        # Het spel gaat door tot de speler of de code goed heeft
        # of geen pogingen meer over heeft.
        while (not gewonnen and no_guesses < self.max_guesses):
            
            # Laat de speler raden
            print("Aantal overgebleven pogingen: " + str(self.max_guesses - no_guesses))
            
            # method voor menselijk gebruik
            if self.method == "human":
                guess = input("Raad de code: ")
            
            # het simpel algoritme
            elif self.method == "AI":
                print(len(self.potential))
                randelement = random.randint(0, len(self.potential) - 1)
                guess = "".join(self.potential[randelement])
                print(guess)
            
            # expected algoritme
            elif self.method == "expected":
                guess = ''.join(self.expectedguess())
                print(guess)
                
            # unexpected algoritme
            elif self.method == "unexpected":
                guess = ''.join(self.expectedguess(method="unexpected"))
                print(guess)
                
            # bogo algoritme
            elif self.method == "bogo":
                randelement = random.randint(0, len(self.potential) - 1)
                guess = "".join(self.potential[randelement])
            
            # Laat de speler opnieuw input invoeren zo lang we geen geldige gok hebben
            while (not self.valide(guess)):
                print("De code die je hebt ingevoerd is niet geldig, probeer het opnieuw")
                guess = input("Raad de code: ")
            
            # Is het goed? Dan laten we de speler weten dat hij heeft gewonnen
            if (''.join(self.code) == guess):
                gewonnen = True
            else:
                feedback = geef_feedback(self.code, guess)
                print("Kleuren op de juiste positie: " + str(feedback[0]))
                print("Kleuren op de verkeerde positie: " + str(feedback[1]))
                self.update_mogelijkheden(feedback, guess)
                self.guesses.append(guess)
            
            # Een poging gedaan
            no_guesses += 1
        
        if (gewonnen):
            print("Yay! je hebt gewonnen.")
        else:
            print("Helaas, je hebt geen pogingen meer.")
            print("De code was: " + str(self.code))
        
        # Zet een spelletje mastermind klaar
    
    def expectedguess(self, method="expect"):
        # dicts aanmaken voor de data
        averages = {}
        freqs = {}
        
        # alle mogelijke guesses die je nog kan geven
        for guess in self.potential:
            # dict leegmaken
            freq = {}
            
            # voor alle mogelijke codes
            for code in self.potential:
                # feedback vragen over mogelijk code bij mogelijke guess
                feedback = geef_feedback(code, guess)
                
                # als de feedback al terug is gegeven dan stop je hem in de dict erbij
                if feedback in freq.keys():
                    freq[feedback].append(code)
                    
                # anders maak je een nieuwe index
                else:
                    freq[feedback] = [code]
            
            # gemiddelde voor een guess berekenen
            averages[guess] = sum([len(y) / len(list(self.potential)) * len(y) for y in freq.values()])
            freqs[guess] = freq
        
        # de feedback opslaan voor later gebruik
        self.expectedfeedback = freqs[min(averages)] if method == "expect" else freqs[max(averages)]
        
        # het element meet de laasgste waarde heb je nodig
        return min(averages) if method == "expected" else max(averages)


# 2 codes met elkaar vergelijken
def geef_feedback(secret, guess):
    # Zet de gok om naar een lijst
    guess = list(guess)
    
    # De code om de gok mee te vergelijken
    kopie_code = list(secret)
    
    # Juiste kleur op de juiste positie
    helemaal_goed = 0
    
    # Juiste kleur op de verkeerde positie
    juiste_kleur = 0
    
    # Loop over de code om de juiste kleur verkeerde positie te bepalen
    for i in range(len(secret)):
        
        # Exacte match?
        if (kopie_code[i] == guess[i]):
            # Een match qua kleur en positie
            helemaal_goed += 1
            
            # Vervang het stukje code, zodat we deze niet
            # als juiste kleur verkeerde positie kunnen markeren
            kopie_code[i] = '-'
            guess[i] = ''
    
    # Nu we alle juiste eruit gefilterd hebben kunnen we kijken
    # naar wat nog op de verkeerde plek staat.
    for i in range(len(secret)):
        
        # Zit de kleur ergens anders in de code
        if guess[i] in kopie_code:
            # Verhoog de counter
            juiste_kleur += 1
            
            # Vervang het element, zodat we geen dubbele feedback krijgen
            kopie_code[kopie_code.index(guess[i])] = '-'
            guess[i] = ''
    
    return (helemaal_goed, juiste_kleur)


Mastermind(method="unexpected")

# Start een nieuwe ronde
# game.reset()