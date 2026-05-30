import random

def battle_loop(player, enemy):
    print(f"\n🔥 BATTLE START: {player.name} vs {enemy.name} 🔥")
    turn = 1
    
    # The loop continues as long as BOTH characters are alive
    while player.is_alive() and enemy.is_alive():
        print(f"\n=== TURN {turn} ===")
        player.display_stats()
        enemy.display_stats()
        
        # --- PLAYER'S TURN ---
        print("\nYour Move:")
        print("1. Basic Attack")
        print("2. Charge Energy")
        print("3. Special Attack (Cost: 30)")
        print("4. Use Potion ({} left)".format(player.potions))
        print("5. Domain Expansion (Cost: 50)")
        choice = input("Enter choice (1/2/3/4/5): ")
        
        if choice == '1':
            player.basic_attack(enemy)
        elif choice == '2':
            player.current_energy = min(player.max_energy, player.current_energy + 20)
            print(f"⚡ {player.name} charges {player.energy_name}! (+20)")
        elif choice == '3':
            player.special_attack(enemy)
        elif choice == '4':
            player.heal()
        elif choice == '5':
            player.domain_expansion(enemy)
        else:
            print("Invalid choice! You stumbled and lost your turn.")
        
        # Check if the enemy died from your attack
        if not enemy.is_alive():
            print(f"\n🏆 {enemy.name} is exorcised! YOU WIN!")
            break
            
        # --- ENEMY'S TURN ---
        print("\nEnemy's Move:")
        if random.choice([True, False]) and enemy.current_energy >= 30:
            enemy.special_attack(player)
        else:
            enemy.basic_attack(player)
        
        # Check if you died from the enemy's attack
        if not player.is_alive():
            print(f"\n💀 {player.name} was defeated. GAME OVER.")
            break
        
        turn += 1