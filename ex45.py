import game
from textwrap import dedent
from random import randint

class Stage():
    def __init__(self):
        self.game = game.Game()
        # game module has methods for combat and handling user input

    def enter(self):
        pass


class Castle_wall(Stage):
    def __init__(self):
        super(Castle_wall, self).__init__()

    def enter(self, health):
        print(dedent("""
        You approach the castle wall, it is approximately 80ft high.
        There is a gate to your right. There appear to be some climbing holds in the wall, and you also have a grappling hook.
        """))
        c = self.game.choice(['gate right walk','climb holds','grappling'])
        if 'grappling' in c:
            print("A guard hears the grappling hook land and cuts the rope while you are climbing.")
            return 'dth', 0, False
        elif 'climb' in c:
            print("You find good holds and make your way up the wall quickly.")
            return 'crt', health, False
        elif 'walk' in c:
            print("You walk through the gate and are immediately confronted by a guard.")
            health = self.game.combat(health)
            if health:
                print(f"You defeat the guard in combat, you have {health} health")
                return 'crt', health, False
            else:
                print("The gaurd defeated you in combat")
                return 'dth', health, False  
        
class Death(Stage):
    def __init__(self):
        super(Death, self).__init__()

    def enter(self, health):
        print("You have died.")
        return '', 0, True

class Courtyard(Stage):
    def __init__(self):
        super(Courtyard, self).__init__()

    def enter(self, health):
        print(dedent("""
        You step out into the courtyard, you have to cross to get to the towers on the other side.
        There are a lot of people walking around, you may be able to hide in plain sight. 
        There are some trees on the other side of the courtyard that make a lot of shadows, or you could walk through the castle corridors.
        """))
        c = self.game.choice(['plain sight hide', 'shadow tree trees other', 'castle corridor'])
        if 'sight' in c:
            print("You are quickly confronted by several guards")
            return 'dth', health, False
        elif 'tree' in c:
            print("You through the shady trees to the tower without being noticed.")
            return 'twr', health, False
        else:
            print("In the corridor there is a guard blocking your path 20 yards away")
            health = self.game.combat(health, 'range')
            if health:
                print("You defeat the guard and continue down the corridor.")
                return 'twr', health, False
            else:
                print("The guard has defeated you.")
                return 'dth', health, False

class Tower(Stage):
    def __init__(self):
        super(Tower, self).__init__()
    
    def enter(self, health, second_attempt = False):
        if second_attempt:
            print("You walk back out to the room with three doors.")
        else:
            print("You enter a room with three doors.")
        print(dedent("""
        There is a door with a metal coin, a door with the royal seal, and an unmarked door.
        Which do you choose?
        """))
        c = self.game.choice(['coin first','royal seal second','unmarked blank third third'],'\n> ')
        if 'coin' in c:
            print("You open the door and the room is filled with guards.")
            return 'dth', health, False
        elif 'royal' in c:
            print("You open the door, the room is royal clerk room. There is one guard inside.")
            health = self.game.combat(health)
            if health:
                print("You defeat the guard.")
                return 'twr', health, False, True
            else:
                print("The guard has defeated you.")
                return 'dth', health, False
        else:
            print("You open the door and there is a staircase that leads down.")
            c = self.game.choice(['back other door','down stair continue'],"Do you try another door or continue down the stairs?\n")
            if 'back' in c:
                return 'twr', health, False, True
            else:
                print("You continue down the stairs")
                return 'vlt', health, False, False

class Vault(Stage):
    def __init__(self):
        super(Vault, self).__init__()

    def enter(self, health):
        print("You see the vault ahead, there is a gaurd but he is facing the other way.")
        health = self.game.combat(health, 'quiet')
        if health:
            print("You have defeated the guard.")
            return 'lck', health, False
        else:
            print("The guard has defeated you.")
            return 'dth', health, False

class Lock(Stage):
    def __init__(self):
        super(Lock, self).__init__()
    
    def enter(self, health):
        print(dedent("""
        There is a lock on the vault, a combination of three numbers 1 - 3.
        Example '123'
        There is only enough time for 10 attempts before the guards realize you are here.
        """))
        a, b, c = randint(1,3), randint(1,3), randint(1,3)
        combination = str(a) + str(b) + str(c)
        attempts = 0
        guess = ''
        while combination != guess and attempts < 10:
            guess = input("Enter a combination\n> ")
            attempts += 1
        if attempts == 10:
            print("That is 10 attempts, you are discovered by the guards.")
            return 'dth', health, False
        else:
            print("Correct guess. The door opens and you take the piece of treasure.")
            return 'trs', health, False
            
class Treasure(Stage):
    def __init__(self):
        super(Treasure, self).__init__()

    def enter(self, health):
        print(dedent("""
        Now you have to escape the castle.
        You can continue deeper into the vault, or return through the courtyard.
        """))
        c = self.game.choice(['deeper continue vault', 'back up courtyard'])
        if 'back' in c:
            print("You return through the courtyard and are quickly captured by guards.")
            return 'dth', health, False
        else:
            print("You continue deeper into the vault and find a door that leads outside the castle.")
            return '', health, True
            

class Play():
    def __init__(self, starting_stage, difficulty = 'medium'):
        self.starting_stage = starting_stage
        self.difficulty = difficulty
        self.health = 20

    stages = {
        'cw' : Castle_wall(),
        'dth' : Death(),
        'crt' : Courtyard(),
        'twr' : Tower(),
        'vlt' : Vault(),
        'lck' : Lock(),
        'trs' : Treasure()
    }

    def restart(self):
        i = input("Would you like to play again?\nYes/no> ")
        if 'y' in i.lower():
            self.start()
        else:
            print("Thank you for playing.")

    def cont(self, stage, second_attempt = False):
        # starts the next scene
        s = self.stages[stage]
        if second_attempt:
            output = list(s.enter(self.health, second_attempt))
        else:
            output = list(s.enter(self.health))
        try:
            nx, health, end, second_attempt = tuple(output)
        except:
            nx, health, end = tuple(output)
        if end:
            self.restart()
        else:
            self.health = health
            self.cont(nx, second_attempt)


    def start(self):
        if self.difficulty == 'easy':
            self.health = 30
        elif self.difficulty == 'hard':
            self.health = 15
        elif self.difficulty == 'expert':
            self.health = 5
        else: 
            self.health = 20

        s = self.starting_stage()
        nx, health, end = s.enter(self.health)
        if end:
            self.restart()
        else:
            self.health = health
            self.cont(nx)

p = Play(Castle_wall)
p.start()