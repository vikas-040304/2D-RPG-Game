from characters import Character
from combat import battle_loop
import random

# --- COLOR CODES ---
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def main():
    player = Character(name="Jujutsu Sorcerer", hp=100, attack=15, energy_name="Cursed Energy", max_energy=50)
    
    # ASCII TITLE ART
    print(f"{RED}")
    print("=====================================================")
    print("  🔥 J U J U T S U   S O R C E R E R   R P G 🔥  ")
    print("=====================================================")
    print(f"{RESET}")
    
    load_choice = input(f"{CYAN}Do you want to load your saved game? (y/n): {RESET}")
    if load_choice.lower() == 'y':
        player.load_game()
    
    enemies = [
        Character(name="Grade 3 Curse", hp=40, attack=8, energy_name="Curse Power", max_energy=30),
        Character(name="Grade 1 Curse", hp=70, attack=15, energy_name="Curse Power", max_energy=60),
        Character(name="Special Grade Curse", hp=120, attack=25, energy_name="Curse Power", max_energy=100)
    ]

    for enemy in enemies:
        if player.is_alive():
            battle_loop(player, enemy)
            
            if player.is_alive():
                print(f"\n{GREEN}--- BATTLE WON ---{RESET}")
                if random.random() < 0.5:
                    player.potions += 1
                    print(f"{YELLOW}🎁 LOOT DROP: You found a Health Potion! (Total Potions: {player.potions}){RESET}")
                
                player.level_up()
                player.save_game()
        else:
            break

    # THE FINAL BOSS ENCOUNTER
    if player.is_alive():
        print(f"\n{RED}" + "="*50)
        print(" ☠️ WARNING: THE KING OF CURSES HAS AWAKENED! ☠️ ")
        print("="*50 + f"{RESET}")
        
        boss = Character(name="Ryomen Sukuna", hp=250, attack=35, energy_name="Cursed Energy", max_energy=150)
        
        print(f"{YELLOW}✨ You sense immense danger... Your adrenaline fully restores your HP and Energy!{RESET}")
        player.current_hp = player.max_hp
        player.current_energy = player.max_energy
        
        battle_loop(player, boss)

        if player.is_alive():
            print(f"\n{GREEN}" + "🌟"*20)
            print("🎉 CONGRATULATIONS! You defeated the King of Curses!")
            print("🎉 The world is safe once again. YOU ARE A LEGEND!")
            print("🌟"*20 + f"{RESET}")

if __name__ == "__main__":
    main()