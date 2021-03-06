# A player keeps track of important resources, and can display the amount of each resource they have.
# Additionally, the player has built in ways, such as mining, docking, and working, to gain more resources.


class Player:

    def __init__(self):

        self.MAX_HULL = 10
        self.MAX_SANITY = 100

        self.resources = [300, 15, 1, self.MAX_HULL, self.MAX_SANITY, 1, 0]
        self.resource_names = ["CREDITS", "FOOD", "FLUX", "HULL", "SANITY", "CREW", "WISDOM"]
        self.name = ""
        self.score = self.calc_score()
        # Resources: Credits, Food, Fuel, Hull, Stress, Crew, Wisdom

    # Post: Returns the player's name as a String.
    def get_name(self):
        return self.name

    # Post: For each resource, outputs the name of the resource and the amount of the resource.
    # One special case is reporting stress, which is meant to be ambiguous, therefore lacking a clear value.
    def get_count(self):
        print()
        print("###RESOURCES###")
        for x in range(0, 7):
            print()
            if x == 4:
                print(self.resource_names[x] + ": " + self.stress_status())
            elif x is not 0:
                print(self.resource_names[x] + ": " + "O"*self.resources[x] + "(" + str(self.resources[x]) + " units)")
            else:
                print(self.resource_names[x] + ": " + str(self.resources[x]))
        print("###############")
        print()

    # Post: Check the player's stress, and returns a value of type String, which is a purposely ambiguous description.
    def stress_status(self):
        if self.resources[4] <= 20:
            return "Almost insane"
        elif self.resources[4] <= 40:
            return "Dangerously stressed"
        elif self.resources[4] <= 60:
            return "Acutely stressed"
        elif self.resources[4] <= 80:
            return "Moderately stressed"
        else:
            return "Nervous"

    # Pre: Given a list containing exactly 7 values, where each index matches the index of the particular resource,
    # Post: Adds the resources, returning the resulting sum as a list. Also prints the amount of each resource gained
    # or lost, and alerts the player if they've exceeded any maximums.
    def add(self, other):
        if len(other) == 7:
            for x in range(0, 7):
                self.resources[x] += other[x]
                if other[x] > 0:
                    print("You gain " + str(other[x]) + " " + self.resource_names[x] + ".")
                    if x is 3 and self.resources[x] > self.MAX_HULL:
                        print("However, you forfeit " + str(self.resources[x] - self.MAX_HULL) + " "
                              + self.resource_names[x] + " because you reached the maximum of " + str(self.MAX_HULL))
                        self.resources[x] = self.MAX_HULL
                    elif x is 4 and self.resources[x] > self.MAX_SANITY:
                        print("However, you forfeit " + str(self.resources[x] - self.MAX_SANITY) + " "
                              + self.resource_names[x] + " because you reached the maximum of " + str(self.MAX_SANITY))
                        self.resources[x] = self.MAX_SANITY
                elif other[x] < 0:
                    if (self.resources[x]) < 0 and x is not 0:
                        print("You have no more " + self.resource_names[x] + " to lose.")
                        self.resources[x] = 0
                    else:
                        print("You lose " + str(other[x]) + " " + self.resource_names[x] + ".")

    # Pre: Given a dice object in order to roll different sided dice,
    # Post: Presents dialogue to the player, where depending on a dice roll, determines the possible reward from
    # mining. A minimum of 4 Flux and 1 Crew will always be rewarded, with additional rewards depending on dice rolls.
    def mine(self, d):
        print('''
        You take your airship towards the base of the closest isle. The glimmering shine of the Flux stones can be seen 
        through the roots that once held the landmass to the ground. Taking your ship closer, you dock at the mining 
        station and attempt to convince the mining crew foreman for permission to harvest Flux. He is a scruffy looking 
        fellow, well built, and wears a sharp look on his face. Maybe you can convince him to lend you some of his 
        workers as well.
        ''')

        check = d.roll(20)
        bonus = 0
        if check >= 15:
            print('''
            \"Ho there young lad! Looking to get flush? I admire your courage to help Lugmere, so I'll help you mine 
            this here Flux on the fly!\"
            ''')
            bonus += 2
        elif check >= 10:
            print('''
            \"Hmm lad, think you can in this day take Flux? There ain't a heap of it left on this isle, but I'll let ya 
            have what I can give if it means ending The Maw.\"
            ''')
            bonus += 1
        elif check >= 5:
            print('''
            \"You scavengers are like Monkrats! Never ending supply of you lads I tell ya! Flux is precious these days, 
            take what you must but I tell ya it's scarce...\"
            ''')
        else:
            print('''
            \"Hobble yer lip! You've got the hykey to ask for MY flux on MY mining rig? I think ya got a screw loose. 
            Good luck trying to get my workers to help.\"
            ''')
            bonus -= 1
        print("You end up convincing the foreman to let you use his mine.")
        changes = [0, -d.hidden_roll(6), (4+bonus), 0, 0, (bonus), 0]
        print('''
        The day is spent mining flux. The foreman's miners stare at you as you work, their curious gaze makes you feel 
        slightly nervous. You can hear them whisper about you and The Maw. It seems that word must travel quickly on 
        this mining rig.
        ''')
        if changes[5] > 0:
            print("Also " + str(changes[5]) + " miner(s) opt to join you. You guess the life on the mining rig is "
                                              "boring.")
        self.add(changes)

    # Pre: Given a dice object in order to roll different sided dice,
    # Post: Presents dialogue to the player and gives the player resources depending on the outcome of dice rolls.
    def dock(self, d):
        print('''
        You dock your airship to a nearby traveler isle. There are several other airships also docked
        here, with a large amount of mysterious figures bustling about on the platforms that line the
        facility. You take in the shanties of the pub and turn a blind eye to the prostitution
        and drug dealings in order to take advantage of their services for yourself.
        ''')
        self.add([-10*(self.resources[5]+1), d.hidden_roll(10) + self.resources[5]*d.hidden_roll(2), 0, d.hidden_roll(4),
                  2*d.hidden_roll(10), 0, 0])

    # Pre: Given a dice object in order to roll different sided dice,
    # Post: Presents dialogue to the player and gives the player resources depending on the outcome of dice rolls.
    def work(self, d):
        print('''
        You work a random odd job.
        ''')
        self.add([10 * d.hidden_roll(14) * self.resources[5], 0, 0, 0, 0, 0, 0])

    # Pre: Given a dice object in order to roll different sided dice,
    # Post: Presents dialogue to the player and gives the player resources depending on the outcome of dice rolls.
    def recruit(self, d):
        print('''
        You recruit a handful of courageous young men and women.
        Some members bring new information about The Maw.
        ''')
        self.add([-50, 0, 0, 0, 0, d.hidden_roll(10), 1+d.hidden_roll(2)])

    # Post: Will update the player's resources
    def update(self):
        hunger = self.resources[5]+1  # Crew + yourself
        difference = self.resources[1] - hunger
        if difference < 0:
            print("You are starving. " + str(-difference) + " crew members perish and it stresses you.")
            self.add([0, 0, 0, 0, 5*difference, difference, 0])
        else:
            print("You feed your party " + str(hunger) + " " + self.resource_names[1] + ".")
            self.add([0, -hunger, 0, 0, 0, 0, 0])

    # Pre: Given an optional parameter of an int that represents a bonus to be added to the player's score,
    # Post: Returns an integer that is the result of all player's resources added up in a specific way. Everything but
    # credits and sanity are multiplied by 10 and added. Credits are added without a multiplier. Sanity is subtracted
    # because having more sanity is better. The total is returned as an integer.
    def calc_score(self):
        total = 0
        index = 0
        for x in self.resources:
            if index is 0:
                total += self.resources[index]
            elif index is 4:
                total -= self.resources[index]
            else:
                total += self.resources[index] * 10
            index += 1
        return total


            

