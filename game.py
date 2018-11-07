from random import randint

class Game():
    def speak(self, stage):
        # will take the stage, get the dialouge and run it
        # returns nothing
        pass

    combat_library = {
        'cq' : {
            'text' : "You will choose a weapon for each round of attack.\nYour weapons are the dagger, sword, and mace. Bigger weapons do more damage but are more likely to miss.",
            'weapons' : {
                'dagger' : (2,1),
                'mace' : (5,3),
                'sword' : (3,2)
            },
            'enemy' : {
                'health' : 15,
                'accuracy' : 2,
                'attack' : (1,4)
            }
        },
        'range' : {
            'text' : "You will choose a weapon for each round of attack.\nYour weapons are throwing knives and the bow. The knives do more damage but are more likely to miss.",
            'weapons' : {
                'throwing knives' : (5,3),
                'bow' : (3,2)
            },
            'enemy' : {
                'health' : 10,
                'accuracy' : 3,
                'attack' : (2,5)
            }
        },
        'quiet' : {
            'text' : "The enemy is currently not aware of your presence.\nYou will choose a weapon for each round of attack.\nYour weapons are a dagger and a mace. The mace is a guaranteed hit, the dagger is a one hit KO but is more likely to miss.",
            'weapons' : {
                'dagger' : (10,2),
                'mace' : (5,1)
            },
            'enemy' : {
                'health' : 10,
                'accuracy' : 2,
                'attack' : (5,8)
            }
        }
    }

    def combat(self, health, combat_type = 'cq'):
        # will take current health and combat type
        # returns a value for health
        text = self.combat_library[combat_type]['text']
        weapons_list = self.combat_library[combat_type]['weapons'].keys()
        weapons = []
        for w in weapons_list:
            weapons.append(w) 
        enemy_health = self.combat_library[combat_type]['enemy']['health']
        enemy_accuracy = self.combat_library[combat_type]['enemy']['accuracy']
        enemy_attack1, enemy_attack2 = self.combat_library[combat_type]['enemy']['attack']
        print(text)
        while health > 0 and enemy_health > 0:
            weapon_choice = self.choice(weapons, '\n> ')
            d, a = self.combat_library[combat_type]['weapons'][weapon_choice]
            hit = randint(1,a) == 1
            enemy_hit = randint(1,enemy_accuracy) == 1
            if hit:
                enemy_health -= d
                if enemy_health <= 0:
                    print(f"You hit the enemy and dealt {d} damage. The enemy has 0 life left")
                    return health 
                else: 
                    print(f"You hit the enemy and dealt {d} damage, the enemy now has {enemy_health} health")
            else:
                print(f"You missed the enemy, the enemy has {enemy_health} health.")
            if enemy_hit:
                d = randint(enemy_attack1, enemy_attack2)
                health -= d
                if health <= 0:
                    print(f"The enemy's attack hit and did {d} damage. You have 0 life.")
                    return health
                else:
                    print(f"The enemy's attack hit and did {d} damage. Your have {health} health.")
            else:
                print("The enemy's attack missed.")
                

    def choice(self, acceptable_choices, prompt = 'What would you like to do next?\n'):
        # accepts an array of possible choices and an optional prompt
        # returns the choice the user gave
        i = input(prompt).lower()
        for choice in acceptable_choices:
            words = choice.split(' ')
            for word in words:
                if word in i:
                    return choice
        else:
            print(f"'{i}' is not a recognized command.\n")
            return self.choice(acceptable_choices, prompt)
