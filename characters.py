import json
import os
import random


class Character:
    def __init__(self, name, hp, attack, energy_name, max_energy):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.energy_name = energy_name
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.potions = 3  # Start with 3 health potions

    def heal(self, heal_amount=40):
        if self.potions > 0:
            # Heal, but don't exceed max HP
            self.current_hp = min(self.max_hp, self.current_hp + heal_amount)
            self.potions -= 1
            print(f"🧪 {self.name} drinks a potion! Healed for {heal_amount} HP. ({self.potions} potions left)")
        else:
            print("❌ No potions left! You wasted your turn searching your pockets.")

    def is_alive(self):
        return self.current_hp > 0

    def basic_attack(self, target):
        # 25% chance for a critical hit!
        is_crit = random.random() < 0.25
        damage = self.attack * 2 if is_crit else self.attack
        
        target.current_hp -= damage
        if is_crit:
            print(f"💥 CRITICAL HIT! {self.name} strikes {target.name} for {damage} massive damage!")
        else:
            print(f"⚔️ {self.name} strikes {target.name} for {damage} damage!")

    def special_attack(self, target, energy_cost=30, damage_multiplier=2.5):
        if self.current_energy >= energy_cost:
            self.current_energy -= energy_cost
            damage = self.attack * damage_multiplier
            target.current_hp -= damage
            print(f"✨ {self.name} unleashes a SPECIAL ATTACK for {damage} damage!")
        else:
            print(f"Not enough {self.energy_name}! Attack fails.")
        
    def display_stats(self):
        print(f"[{self.name}] HP: {self.current_hp}/{self.max_hp} | {self.energy_name}: {self.current_energy}/{self.max_energy}")

    # ADD THIS RIGHT HERE! Make sure the "def" lines up with the "def" above it.
    def domain_expansion(self, target):
        if self.current_energy >= 50:
            self.current_energy -= 50
            damage = self.attack * 4
            target.current_hp -= damage
            print(f"🌌 {self.name} casts DOMAIN EXPANSION! Deals {damage} massive damage!")
        else:
            print(f"Not enough {self.energy_name} for Domain Expansion!")

    def level_up(self):
        self.max_hp += 20
        self.current_hp = self.max_hp
        self.attack += 5
        self.max_energy += 10
        self.current_energy = self.max_energy
        print(f"🌟 {self.name} LEVELED UP! Stats increased!")

    def save_game(self, filename="save_data.json"):
        data = {
            "name": self.name,
            "max_hp": self.max_hp,
            "current_hp": self.current_hp,
            "attack": self.attack,
            "max_energy": self.max_energy,
            "current_energy": self.current_energy,
            "potions": self.potions
        }
        with open(filename, "w") as file:
            json.dump(data, file)
        print("💾 Game Auto-Saved Successfully!")

    def load_game(self, filename="save_data.json"):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = json.load(file)
                self.max_hp = data["max_hp"]
                self.current_hp = data["current_hp"]
                self.attack = data["attack"]
                self.max_energy = data["max_energy"]
                self.current_energy = data["current_energy"]
                self.potions = data["potions"]
            print("📂 Save File Loaded! Welcome back.")
            return True
        else:
            print("❌ No save file found. Starting a new game...")
            return False