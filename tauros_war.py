import logging
from pkmn import *

def t1_select_move(user, opponent):
    attack = None
    if user.hp <= 188:
        attack = user.get_move(HyperBeam.NAME)
    elif user.hp == 353:
        attack = user.get_move(FireBlast.NAME)
    elif opponent.hp >= 188:
        attack = user.get_move(FireBlast.NAME)
    else:
        attack = user.get_move(HyperBeam.NAME)
    return attack

def t2_select_move(user, opponent):
    attack = None
    if user.hp <= 188:
        attack = user.get_move(HyperBeam.NAME)
    elif user.status == 'BRN':
        attack = user.get_move(Blizzard.NAME)
    elif opponent.hp >= 188:
        attack = user.get_move(BodySlam.NAME)
    else:
        attack = user.get_move(HyperBeam.NAME)
    return attack

iterations = 10000
#logging.basicConfig(level=logging.DEBUG)
if iterations == 1:
    logging.basicConfig(level=logging.DEBUG)
t1_wins = 0
draws = 0
for _ in range(0, iterations):
    t1 = Tauros(100, [BodySlam, Blizzard, FireBlast, HyperBeam], nickname='t1')
    t2 = Tauros(100, [BodySlam, Blizzard, FireBlast, HyperBeam], nickname='t2')
    winner = battle(t1, t2, t1_select_move, t2_select_move)
    if len(winner) == 2:
        draws += 1
    elif t1 in winner:
        t1_wins += 1
    logging.debug('================')
t1_percentage = t1_wins/float(iterations) * 100
t2_percentage = (iterations - t1_wins - draws)/float(iterations) * 100
draw_percentage = draws/float(iterations) * 100
print('Tauros 1 wins {}%'.format(t1_percentage))
print('Tauros 2 wins {}%'.format(t2_percentage))
print('Draws {}%'.format(draw_percentage))

# So Fireblast is marginally, and I mean seriously marginally better than
# bodyslam in a tauros 1v1. However! Fireblast probably gives you chances to
# switch without playing out the 1v1 entirely. So it has that advantage. But,
# that will give Tauros a chance to inflict more damage on the rest of your
# team. Honestly, I dont think fireblast tauros is great.
