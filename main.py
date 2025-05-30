# pylint: disable=import-error,no-member,invalid-name,missing-class-docstring,missing-function-docstring,missing-module-docstring,unused-import
import sys
import random
from typing import Literal, TypeAlias
import pygame
from enum import IntEnum

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Turn-Based Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)

# Types:

number: TypeAlias = int | float


class Temporary:
    def __init__(self, caller: "Entity", attr_name: str, value: number):
        self.temp = value
        self.attr_name = attr_name
        self.caller = caller
        self.orig = None

    def __enter__(self):
        self.orig = getattr(self.caller, self.attr_name)
        setattr(self.caller, self.attr_name, self.temp)
        return self

    def __exit__(self, *_):
        setattr(self.caller, self.attr_name, self.orig)
        return False


class State(IntEnum):
    NOT_ENOUGH_MP = -1
    NOT_ENOUGH_ENERGY = -2


# Base Entity class
class Entity:
    def __init__(
        self, name: str, hp: number, atk: number, defense: number, spd: number
    ):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.spd = spd

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg: number):
        actual_dmg = max(0, dmg - self.defense)
        self.hp = max(0, self.hp - actual_dmg)
        return actual_dmg

    def attack(self, target: "Entity"):
        return target.take_damage(self.atk)

    def heal(self, value: number):
        self.hp = min(self.hp + value, self.max_hp)

    def temp(self, attr: str, value: number):
        return Temporary(self, attr, value)


# Player character class
class Player(Entity):
    def __init__(
        self,
        name: str,
        hp: number,
        atk: number,
        defense: number,
        spd: number,
        mp: number,
    ):
        super().__init__(name, hp, atk, defense, spd)
        self.max_mp = mp
        self.mp = mp
        self.max_energy = 150
        self.energy = 0
        self.crit_rate = 0.75
        self.crit_dmg = 1.5
        self.skill_mpcost = 20
        self.ult_encost = self.max_energy

    def burn(self, value: number):
        if 0 < value < 1:
            value = 1
        self.hp = max(min(self.hp, self.hp - value), 1)

    def generic_regen(self, type_: Literal["energy", "mp"], mult: number = -1, raw=-1):
        if mult == -1 and raw == -1:
            print("Error: Either provide raw value or multiplier increase")
            return
        match type_:
            case "energy":
                if mult != -1:
                    base = self.max_energy * mult
                else:
                    base = raw
                self.energy = min(self.energy + base, self.max_energy)
                return
            case "mp":
                if mult != -1:
                    base = self.max_mp * mult
                else:
                    base = raw
                self.mp = min(self.mp + base, self.max_mp)
                return

    def basic_attack(self, target: Entity):
        self.generic_regen("energy", raw=10)
        self.generic_regen("mp", raw=20)
        log_action(f"[{self.name}] Invoke: Slash!", (270, 50))
        self.heal(0.4 * self.atk)
        mult = self.impose_crit(4 * self.atk)
        return target.take_damage(mult)

    def skill(self, target: Entity):
        if self.mp < self.skill_mpcost:
            return State.NOT_ENOUGH_MP
        self.mp -= self.skill_mpcost
        self.generic_regen("energy", raw=15)

        log_action(f"[{self.name}] Invoke: Harder Slash!", (270, 50))
        self.heal(0.4 * self.atk)
        mult = self.impose_crit(6 * self.atk)
        return target.take_damage(mult)

    def ultimate(self, target: Entity):
        if self.energy < self.max_energy:
            return State.NOT_ENOUGH_MP
        self.energy = 0
        log_action(f'[{self.name}] Invoke: "Take This!"', (270, 50))
        self.burn(self.hp * 0.8)
        with self.temp("crit_dmg", 4.2):
            mult = self.impose_crit(12 * self.atk)
        self.generic_regen("mp", raw=100)
        return target.take_damage(mult)

    def impose_crit(self, base_dmg: number):
        if random.random() <= self.crit_rate:
            crit = base_dmg * (1 + self.crit_dmg)
            log_action(
                f"Does CRIT! from {round(base_dmg):,} to {round(crit):,} ({self.crit_dmg*100:,.2f}%)",
                (270, 75),
            )
            return crit
        return base_dmg


# Enemy class (inherits from Entity directly)
class Enemy(Entity):
    pass


# Demo characters
player = Player("Hero", hp=3210, atk=2135, defense=490, spd=10, mp=100)
enemy = Enemy("Dummy", hp=13_299_791_000, atk=500, defense=0, spd=5)

# Turn state
turn_order = sorted([player, enemy], key=lambda x: x.spd, reverse=True)
turn_index = 0

# Draw UI


def draw_basic(entity: Entity, current_index: int):
    y = 50 + current_index * 100
    name_text = font.render(f"{entity.name}", True, WHITE)
    hp_text = font.render(
        f"HP: {round(entity.hp):,}/{round(entity.max_hp):,} ({round(entity.hp/entity.max_hp*100)}%)",
        True,
        RED,
    )
    screen.blit(name_text, (50, y))
    screen.blit(hp_text, dest=(50, y + 25))
    return y


def draw_player(entity: Player, current_index: int):
    y = draw_basic(entity, current_index)
    mp_text = font.render(f"MP: {round(entity.mp)}/{round(entity.max_mp)}", True, GREEN)
    energy_text = font.render(
        f"Energy: {round(entity.energy)}/{round(entity.max_energy)} ({round(entity.energy/entity.max_energy*100)}%)",
        True,
        GREEN,
    )
    screen.blit(mp_text, dest=(50, y + 50))
    screen.blit(energy_text, dest=(50, y + 65))


def draw_bars():
    for i, entity in enumerate([player, enemy]):
        if isinstance(entity, Enemy):
            draw_basic(entity, i)
        if isinstance(entity, Player):
            draw_player(entity, i)


def log_action(value: str, dest: tuple[int, int]):
    # print(value)
    text = font.render(value, True, WHITE)
    screen.blit(text, dest=dest)


# Game loop
running = True
combat_log = ""
skill_set = [1, 1, 2, 1, 1, 2]
attack_index = 0

while running:
    screen.fill(BLACK)
    draw_bars()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    attacker = turn_order[turn_index % 2]
    defender = turn_order[(turn_index + 1) % 2]
    skill_name = "Null"
    this_dmg = 0

    if not attacker.is_alive() or not defender.is_alive():
        winner = attacker.name if attacker.is_alive() else defender.name
        print(f"Game Over. {winner} wins!")
        pygame.time.wait(2000)
        running = False
        continue

    if isinstance(attacker, Enemy):
        pygame.time.wait(1000)
        this_dmg = attacker.attack(defender)
        skill_name = "Enemy: Basic Attack"
    if isinstance(attacker, Player):
        pygame.time.wait(750 + random.randint(0, 500))
        if attacker.energy == attacker.ult_encost:
            this_dmg = attacker.ultimate(defender)
        elif attacker.mp >= attacker.skill_mpcost:
            this_dmg = attacker.skill(target=defender)
        else:
            this_dmg = attacker.basic_attack(defender)
    log_action(
        f"{attacker.name} attacks {defender.name} for {round(this_dmg):,} damage",
        (50, 5),
    )

    turn_index += 1
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
