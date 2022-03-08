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
    def __init__(self, kleuren=['R', 'O', 'Y', 'G', 'C', 'B'], lengte=4, duplicates=True, max_guesses=20,
                 method="human"):
        self.kleuren = kleuren
        self.lengte = lengte
        self.duplicates = duplicates
        self.max_guesses = max_guesses
        self.method = method
        self.expectedfeedback = {}
        self.poscolours = {}
        self.trycolours = kleuren.copy()
        
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
            if (c not in self.kleuren):
                print("De mogelijke kleuren zijn " + str(self.kleuren))
                return False
        
        # Code is valide
        return True
    
    # Pas de overgebleven opties voor de code aan
    def update_mogelijkheden(self, feedback, guess):
        if self.method == "simple":
            # Loop over alle overgebleven codes
            newcodes = []
            
            for code in self.potential:
                if geef_feedback(code, guess) == feedback:
                    newcodes.append(code)
            
            # nieuwe codes
            self.potential = newcodes
            return
        
        if self.method == "verysimple":
            # als we een aantal kleuren hebben dat gelijk is aan de lengte van de code hebben we alle kleuren
            if sum([x for x in self.poscolours.values()]) < self.lengte:
                self.poscolours[guess[0]] = feedback[0]
                self.trycolours.remove(guess[0])
                newpotential = []
                
                # als we de kleur goed hebben
                if feedback[0] > 0:
                    
                    # loopen door alle mogelijkheden
                    for x in self.potential:
                        
                        # als de kleur er niet in zit is de guess niet goed
                        if guess[0] not in x:
                            continue
                            
                        # als de code teveel of teweinig van die kleur bevat
                        if feedback[0] != countcode(x)[guess[0]]:
                            continue
                        else:
                            # guess toevoegen aan de nieuwe guesses
                            newpotential.append(x)
                
                # als de we de kleur niet hebben halen we alle codes eruit met die kleur
                else:
                    for x in self.potential:
                        if guess[0] in x:
                            continue
                        else:
                            newpotential.append(x)
            
                self.potential = newpotential
        
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
            elif self.method == "simple":
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
            
            # verysimple algoritme
            elif self.method == "verysimple":
                # als we nog niet alle kleuren hebben dan gaan we een kleur raden
                if sum([x for x in self.poscolours.values()]) < self.lengte:
                    colour = self.trycolours[0]
                    guess = colour * self.lengte
                else:
                    # random guess als we alle kleuren hebben
                    guess = ''.join(self.potential[random.randint(0, len(self.potential) - 1)])
                print(guess)
            
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
    
    def expectedguess(self):
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
        self.expectedfeedback = freqs[min(averages)] if self.method == "expected" else freqs[max(averages)]
        
        # het element meet de laasgste waarde heb je nodig
        return min(averages) if self.method == "expected" else max(averages)


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


def countcode(code):
    # simpele count functie om de kleuren in codes op te tellen
    counts = {}
    for x in code:
        if x in counts.keys():
            counts[x] += 1
        else:
            counts[x] = 1
            
    return counts
    
    
Mastermind(method="verysimple", max_guesses=9999999, lengte=5)
