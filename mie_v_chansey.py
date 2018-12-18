import logging
from pkmn import *

def mie_select_move(user, opponent):
    attack = None
    if opponent.status is None:
        attack = user.get_move(ThunderWave.NAME)
    if attack is None and user.hp <= 160:
        attack = user.get_move(Recover.NAME)
    if attack is None and user.hp <= 290 and user.get_move(Recover.NAME)\
    and user.get_move(Recover.NAME).pp > 3:
        attack = user.get_move(Recover.NAME)
    if attack is None:
        attack = user.get_move(Surf.NAME)
    if attack is None:
        attack = user.get_move(ThunderWave.NAME)
    if attack is None:
        attack = user.get_move(Thunderbolt.NAME)
    if attack is None:
        attack = user.get_move(Recover.NAME)
    if attack is None:
        return Struggle()
    return attack

def chansey_select_move(user, opponent):
    attack = None
    if opponent.status is None:
        attack = user.get_move(ThunderWave.NAME)
    if attack is None and user.hp <= 350:
        attack = user.get_move(SoftBoiled.NAME)
    if attack is None:
        attack = user.get_move(SeismicToss.NAME)
    if attack is None:
        attack = user.get_move(ThunderWave.NAME)
    if attack is None:
        attack = user.get_move(Reflect.NAME)
    if attack is None:
        return Struggle()
    return attack

def check_result(p1, p2):
    if all(m.pp == 0 for m in p1.moves.values())\
    and all(m.pp == 0 for m in p2.moves.values()):
        return (p1, p2)
    return ()

iterations = 1000
#logging.basicConfig(level=logging.DEBUG)
if iterations == 1:
    logging.basicConfig(level=logging.DEBUG)
mie_wins = 0
draws = 0
for _ in range(0, iterations):
    mie = Starmie(100, [Surf, ThunderWave, Thunderbolt, Recover])
    chan = Chansey(100, [SeismicToss, ThunderWave, Reflect, SoftBoiled])
    winner = battle(
        mie, chan, mie_select_move, chansey_select_move, check_result)
    if len(winner) == 2:
        draws += 1
    elif mie in winner:
        mie_wins += 1
    logging.debug('================')
mie_percentage = mie_wins/float(iterations) * 100
chan_percentage = (iterations - mie_wins - draws)/float(iterations) * 100
draw_percentage = draws/float(iterations) * 100
print('Starmie wins {}%'.format(mie_percentage))
print('Chansey wins {}%'.format(chan_percentage))
print('Draws {}%'.format(draw_percentage))

# Seems like Starmie has a slightly less than 50/50 shot at surviving
# everything Chansey has to offer. But only a 1/3 chance of actually taking a
# win, and I assume for most of those wins it is in pretty bad shape
