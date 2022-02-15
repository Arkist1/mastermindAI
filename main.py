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
    def __init__(self, kleuren=['R', 'O', 'Y', 'G', 'C', 'B'], lengte=4, duplicates=True, max_guesses=10):
        self.kleuren = kleuren
        self.lengte = lengte
        self.duplicates = duplicates
        self.max_guesses = max_guesses
        
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
    
    # Geef feedback aan de speler over de code
    def geef_feedback(self, guess):
        
        # Zet de guess om naar een lijst
        guess = list(guess)
        
        # Maak een tijdelijke kopie van de juiste code,
        # deze kunnen we dan aanpassen om dubbele feedback te voorkomen
        kopie_code = list(self.code)
        
        # Juiste kleur op de juiste positie
        helemaal_goed = 0
        
        # Juiste kleur op de verkeerde positie
        juiste_kleur = 0
        
        # Loop over de code om de juiste kleur verkeerde positie te bepalen
        for i in range(self.lengte):
            
            # Exacte match?
            if (kopie_code[i] == guess[i]):
                # Een match qua kleur en positie
                helemaal_goed += 1
                
                # Vervang het stukje code, zodat we deze niet
                # als juiste kleur verkeerde positie kunnen markeren
                kopie_code[i] = 'X'
        
        # Nu we alle juiste eruit gefilterd hebben kunnen we kijken
        # naar wat nog op de verkeerde plek staat.
        for i in range(self.lengte):
            
            # Zit de kleur ergens anders in de code
            if guess[i] in kopie_code:
                # Verhoog de counter
                juiste_kleur += 1
                
                # Vervang het element, zodat we geen dubbele feedback krijgen
                kopie_code[kopie_code.index(guess[i])] = 'X'
        
        return (helemaal_goed, juiste_kleur)
    
    # Pas de overgebleven opties voor de code aan
    def update_mogelijkheden(self):
        
        # Loop over alle overgebleven codes
        # for code in self.potential:
        
        # Bevat het de kleuren die erin moeten zitten?
        
        # Heeft hij geen kleuren op posities waar we weten dat ze niet kunnen staan
        return
    
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
            guess = input("Raad de code: ")
            
            # Laat de speler opnieuw input invoeren zo lang we geen geldige gok hebben
            while (not self.valide(guess)):
                print("De code die je hebt ingevoerd is niet geldig, probeer het opnieuw")
                guess = input("Raad de code: ")
            
            # Is het goed? Dan laten we de speler weten dat hij heeft gewonnen
            if (''.join(self.code) == guess):
                gewonnen = True
            else:
                feedback = self.geef_feedback(guess)
                print("Kleuren op de juiste positie: " + str(feedback[0]))
                print("Kleuren op de verkeerde positie: " + str(feedback[1]))
                # self.update_mogelijkheden()
                self.guesses.append(guess)
            
            # Een poging gedaan
            no_guesses += 1
        
        if (gewonnen):
            print("Yay! je hebt gewonnen.")
        else:
            print("Helaas, je hebt geen pogingen meer.")
            print("De code was: " + str(self.code))
        
        # Zet een spelletje mastermind klaar


game = Mastermind()

# Start een nieuwe ronde
# game.reset()
