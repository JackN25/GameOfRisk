import random
import os
import time

class Player:
    def __init__(self, name, health=100, attack_power=20):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.shield = 0
        self.ability_cooldowns = {
            "heavy_strike": 0,
            "heal": 0,
            "shield": 0
        }

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        if self.shield > 0:
            absorbed = min(self.shield, damage)
            damage -= absorbed
            self.shield -= absorbed
            print(f"{self.name}'s shield absorbs {absorbed} damage!")
        
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def regular_attack(self, target):
        damage = random.randint(1, self.attack_power)
        target.take_damage(damage)
        return f"regular attack dealing {damage} damage"

    def heavy_strike(self, target):
        if self.ability_cooldowns["heavy_strike"] > 0:
            return "failed - Heavy Strike on cooldown"
        damage = random.randint(self.attack_power, self.attack_power * 2)
        target.take_damage(damage)
        self.ability_cooldowns["heavy_strike"] = 3
        return f"Heavy Strike dealing {damage} damage"

    def heal(self):
        if self.ability_cooldowns["heal"] > 0:
            return "failed - Heal on cooldown"
        heal_amount = random.randint(20, 35)
        self.health = min(self.max_health, self.health + heal_amount)
        self.ability_cooldowns["heal"] = 4
        return f"Heal restoring {heal_amount} HP"

    def shield_up(self):
        if self.ability_cooldowns["shield"] > 0:
            return "failed - Shield on cooldown"
        shield_amount = random.randint(15, 25)
        self.shield += shield_amount
        self.ability_cooldowns["shield"] = 3
        return f"Shield Up gaining {shield_amount} shield points"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_stats(player1, player2):
    print("\n" + "="*60)
    print(f"{player1.name}: HP {player1.health}/{player1.max_health} | Shield: {player1.shield}")
    print(f"Cooldowns: Heavy Strike: {player1.ability_cooldowns['heavy_strike']}, "
          f"Heal: {player1.ability_cooldowns['heal']}, "
          f"Shield: {player1.ability_cooldowns['shield']}")
    print("-"*60)
    print(f"{player2.name}: HP {player2.health}/{player2.max_health} | Shield: {player2.shield}")
    print(f"Cooldowns: Heavy Strike: {player2.ability_cooldowns['heavy_strike']}, "
          f"Heal: {player2.ability_cooldowns['heal']}, "
          f"Shield: {player2.ability_cooldowns['shield']}")
    print("="*60 + "\n")

def get_player_choice(player):
    while True:
        print(f"\n{player.name}'s turn!")
        print("1: Regular Attack (No cooldown)")
        print("2: Heavy Strike (Deals 1-2x damage, Cooldown: 3 turns)")
        print("3: Heal (Restores 20-35 HP, Cooldown: 4 turns)")
        print("4: Shield Up (Blocks 15-25 damage, Cooldown: 3 turns)")
        choice = input("Choose your action (1-4): ")
        if choice in ['1', '2', '3', '4']:
            return choice

def main():
    # Get player names
    print("Welcome to the Battle Arena!")
    print("\nAbilities:")
    print("- Regular Attack: Basic damage")
    print("- Heavy Strike: Powerful attack with 3 turn cooldown")
    print("- Heal: Restore HP with 4 turn cooldown")
    print("- Shield Up: Gain temporary shield with 3 turn cooldown")
    
    player1_name = input("\nEnter Player 1's name: ")
    player2_name = input("Enter Player 2's name: ")

    # Initialize players
    player1 = Player(player1_name)
    player2 = Player(player2_name)

    clear_screen()
    print("Battle begins!")
    
    current_turn = 1
    
    while player1.is_alive() and player2.is_alive():
        current_player = player1 if current_turn % 2 == 1 else player2
        target = player2 if current_turn % 2 == 1 else player1
        
        display_stats(player1, player2)
        
        # Get player's choice
        choice = get_player_choice(current_player)
        
        # Execute action
        result = ""
        if choice == '1':
            result = current_player.regular_attack(target)
        elif choice == '2':
            result = current_player.heavy_strike(target)
        elif choice == '3':
            result = current_player.heal()
        elif choice == '4':
            result = current_player.shield_up()
        
        clear_screen()
        print(f"{current_player.name} uses {result}!")
        
        # Reduce cooldowns
        for player in [player1, player2]:
            for ability in player.ability_cooldowns:
                if player.ability_cooldowns[ability] > 0:
                    player.ability_cooldowns[ability] -= 1
            
        current_turn += 1
        time.sleep(2)
        clear_screen()

    # Game over
    display_stats(player1, player2)
    print("\nBattle Over!")
    winner = player1 if player1.is_alive() else player2
    print(f"{winner.name} wins!")

if __name__ == "__main__":
    main()
