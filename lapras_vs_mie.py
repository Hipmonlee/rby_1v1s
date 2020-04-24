import logging
from pkmn import *

#TODO: need to get PP working

def lapras_select_attack(lapras, opponent):
    attack = lapras.get_move(Thunderbolt.NAME)
    if attack is not None:
        return attack
    return Struggle()

def mie_select_attack(starmie, opponent):
    attack = None
    if opponent.hp < 148:
        attack = starmie.get_move(Thunderbolt.NAME)
    if attack is None and opponent.status is None:
        attack = starmie.get_move(ThunderWave.NAME)
    if attack is None and starmie.hp < 160:
       attack = starmie.get_move(Recover.NAME)
    if attack is None:
        attack = starmie.get_move(Thunderbolt.NAME)
    if attack is None:
        attack = starmie.get_move(Psychic.NAME)
    if attack is not None:
        return attack
    return Struggle()

iterations = 10000
#logging.basicConfig(level=logging.DEBUG)
if iterations == 1:
    logging.basicConfig(level=logging.DEBUG)
mie_wins = 0
draws = 0
for _ in range(0, iterations):
    lapras = Lapras(100, [Thunderbolt, Thunder])
    mie = Starmie(100, [Thunderbolt, ThunderWave, Recover, Psychic])
    #mie.status = 'PAR'
    #lapras.status = 'PAR'
    #mie.hp = 22
    #mie.status_mod = {'speed': 4}
    #lapras.status_mod = {'speed': 4}
    winner = battle(lapras, mie, lapras_select_attack, mie_select_attack)
    if len(winner) == 2:
        draws += 1
    elif mie in winner:
        mie_wins += 1
    logging.debug('================')
mie_percentage = mie_wins/float(iterations) * 100
lapras_percentage = (iterations - mie_wins - draws)/float(iterations) * 100
draw_percentage = draws/float(iterations) * 100
print('Starmie wins {}%'.format(mie_percentage))
print('Lapras wins {}%'.format(lapras_percentage))
print('Draws {}%'.format(draw_percentage))

# Outcome: Starmie is slightly favoured (60%). It should thunderwave and
# recover when lower than around 210 hp

# Thunderbolt is only marginally better than psychic for Starmie as an extra
# move.

# If starmie is paralysed before the fight starts then lapras has an 80% chance
# of winning
