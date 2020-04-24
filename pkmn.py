import random
import logging

def effectiveness(move, opponent):
    INDEXES = ('Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Roc', 'Bug',
               'Ghost', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice',
               'Dragon')
    TYPE_CHART = (
        (4, 4, 4, 4, 4, 2, 4, 0, 4, 4, 4, 4, 4, 4, 4),
        (8, 4, 2, 2, 4, 8, 2, 0, 4, 4, 4, 4, 2, 8, 4),
        (4, 8, 4, 4, 4, 2, 8, 4, 4, 4, 8, 2, 4, 4, 4),
        (4, 4, 4, 2, 2, 2, 8, 2, 4, 4, 8, 4, 4, 4, 4),
        (4, 4, 0, 8, 4, 8, 2, 4, 8, 4, 2, 8, 4, 4, 4),
        (4, 2, 8, 4, 2, 4, 8, 4, 8, 4, 4, 4, 4, 8, 4),
        (4, 2, 2, 8, 4, 4, 4, 2, 2, 4, 8, 4, 8, 4, 4),
        (0, 4, 4, 4, 4, 4, 4, 8, 4, 4, 4, 4, 0, 4, 4),
        (4, 4, 4, 4, 4, 2, 8, 4, 2, 2, 8, 4, 4, 8, 2),
        (4, 4, 4, 4, 8, 8, 4, 4, 8, 2, 2, 4, 4, 4, 2),
        (4, 4, 2, 2, 8, 8, 2, 4, 2, 8, 2, 4, 4, 4, 2),
        (4, 4, 8, 4, 0, 4, 4, 4, 4, 8, 2, 2, 4, 4, 2),
        (4, 8, 4, 8, 4, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4),
        (4, 4, 8, 4, 8, 4, 4, 4, 4, 2, 8, 4, 4, 2, 8),
        (4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8),
        )
    move_i = INDEXES.index(move.TYPE)
    result = 4
    for t in opponent.TYPES:
        opponent_i = INDEXES.index(t)
        result = (result * TYPE_CHART[move_i][opponent_i]) // 4
    if result == 0:
        logging.debug('It doesnt affect {}!'.format(opponent.nickname))
    elif result < 4:
        logging.debug("It's not very effective!")
    elif result > 4:
        logging.debug("It's super effective!")
    return result

def rng(target):
    return random.randint(0, 255) < target

def check_hp(p1, p2):
    #TODO: figure out draws
    if p1.hp <= 0 and p2.hp <= 0:
        return (p1, p2)
    elif p2.hp <= 0:
        return (p1,)
    elif p1.hp <= 0:
        return (p2,)
    else:
        return ()

def battle(pokemon1, pokemon2, pokemon1_select_attack,
           pokemon2_select_attack, check_result=None):
    winner = ()
    while winner is ():
        # select moves
        pokemon1_move = pokemon1_select_attack(pokemon1, pokemon2)
        pokemon2_move = pokemon2_select_attack(pokemon2, pokemon1)
        if pokemon1.get_stat('speed') > pokemon2.get_stat('speed')\
        or pokemon1.get_stat('speed') == pokemon2.get_stat('speed') and random.randint(0, 1):
            logging.debug('--')
            pokemon1.attack(pokemon1_move, pokemon2)
            winner = check_hp(pokemon1, pokemon2)
            if winner:
                break
            pokemon2.attack(pokemon2_move, pokemon1)
            winner = check_hp(pokemon1, pokemon2)
            if winner:
                break
            logging.debug('{} at {}, {} at {}'.format(
                    pokemon1.nickname, pokemon1.hp, pokemon2.nickname, pokemon2.hp))
        else:
            logging.debug('--')
            pokemon2.attack(pokemon2_move, pokemon1)
            winner = check_hp(pokemon1, pokemon2)
            if winner:
                break
            pokemon1.attack(pokemon1_move, pokemon2)
            winner = check_hp(pokemon1, pokemon2)
            if winner:
                break
            logging.debug('{} at {}, {} at {}'.format(
                pokemon1.nickname, pokemon1.hp, pokemon2.nickname, pokemon2.hp))
        if check_result is not None:
            winner = check_result(pokemon1, pokemon2)
    if len(winner) == 1:
        logging.debug('{} wins!'.format(winner[0].nickname))
    else:
        logging.debug('draw')
    return winner

class PPError(Exception):
    pass

class Pokemon:
    def __init__(self, level, moves, nickname=None):
        self.level = level
        if nickname:
            self.nickname = nickname
        else:
            self.nickname = self.NAME
        self.max_hp = 10 + level + (((self.BASE_HP + 15) * 2 + 63) * level) // 100
        self.hp = self.max_hp
        self.moves = {move.NAME: move() for move in moves}
        self.stats = {
            'attack': self._calc_stat(level, self.BASE_ATTACK),
            'defence': self._calc_stat(level, self.BASE_DEFENCE),
            'speed': self._calc_stat(level, self.BASE_SPEED),
            'special': self._calc_stat(level, self.BASE_SPECIAL),
            }
        # tuple of numerator and denominator
        self.stat_mods = {
            'attack': (2, 2),
            'defence': (2, 2),
            'speed': (2, 2),
            'special': (2, 2),
            }
        self.status = None
        self.status_mod = {}
        self.reflect = False
        self.light_screen = False
        self.ch_attempts = 0
        self.ches = 0
        self.fp_turns = 0
        self.fps = 0
        self.sleep_count = 0
        self.recharge = False

    def get_move(self, move_name):
        move = self.moves[move_name]
        if move.pp > 0:
            return move
        else:
            return None

    def get_stat(self, stat):
        if stat not in self.stats:
            raise ValueError('bad stat name')
        value = self.stats[stat]
        value = value // self.status_mod.get(stat, 1)
        mod_numerator, mod_denominator = self.stat_mods[stat]
        value = (value * mod_numerator) // mod_denominator
        return value

    def raise_stat(self, stat, levels):
        numerator, denominator = self.stat_mods[stat]
        for _ in range(levels):
            if denominator == 2:
                numerator = min(8, numerator + 1)
            else:
                denominator = denominator - 1
        self.stat_mods[stat] = (numerator, denominator)

    def lower_stat(self, stat, levels):
        numerator, denominator = self.stat_mods[stat]
        for _ in range(levels):
            if numerator == 2:
                denominator = min(8, denominator + 1)
            else:
                numerator = numerator - 1
        self.stat_mods[stat] = (numerator, denominator)

    def critical_hit(self, high_ch=False):
        self.ch_attempts += 1
        target = self.BASE_SPEED // 2
        if high_ch:
            target = target * 8
        target = min(target, 255)
        if rng(target):
            self.ches += 1
            return True
        else:
            return False

    def attack(self, move, opponent):
        # TODO: This system of requesting a move from a pokemon then passing it
        # back to the pokemon is a little weird. try and think of another way
        # to do this
        if self.recharge:
            self.recharge = False
            logging.debug('{} must recharge'.format(self.nickname))
            return
        if self.status == 'FRZ':
            logging.debug('{} is frozen solid!'.format(self.nickname))
            return
        if self.status == 'SLP':
            if self.sleep_count == 0:
                self.status = None
                logging.debug('{} woke up!'.format(self.nickname))
                return
            else:
                self.sleep_count -= 1
                logging.debug('{} is fast asleep!'.format(self.nickname))
                return
        if self.status == 'PAR':
            self.fp_turns += 1
            if rng(64):
                self.fps += 1
                logging.debug('{} is fully paralysed!'.format(self.nickname))
                return
        move.use(self, opponent)
        if self.status == 'BRN':
            self.hp -= self.max_hp // 16

    def _calc_stat(self, level, base_stat):
        return 5 + (((base_stat + 15) * 2 + 63) * level) // 100

class Lapras(Pokemon):
    BASE_HP = 130
    BASE_ATTACK = 85
    BASE_DEFENCE = 80
    BASE_SPECIAL = 95
    BASE_SPEED = 60
    TYPES = ('Water', 'Ice')
    NAME = 'Lapras'

class Articuno(Pokemon):
    BASE_HP = 90
    BASE_ATTACK = 85
    BASE_DEFENCE = 100
    BASE_SPECIAL = 125
    BASE_SPEED = 85
    TYPES = ('Ice', 'Flying')
    NAME = 'Articuno'

class Moltres(Pokemon):
    BASE_HP = 90
    BASE_ATTACK = 100
    BASE_DEFENCE = 90
    BASE_SPECIAL = 125
    BASE_SPEED = 90
    TYPES = ('Fire', 'Flying')
    NAME = 'Moltres'

class Starmie(Pokemon):
    BASE_HP = 60
    BASE_ATTACK = 75
    BASE_DEFENCE = 85
    BASE_SPECIAL = 100
    BASE_SPEED = 115
    TYPES = ('Water', 'Psychic')
    NAME = 'Starmie'

class Alakazam(Pokemon):
    BASE_HP = 55
    BASE_ATTACK = 50
    BASE_DEFENCE = 45
    BASE_SPECIAL = 135
    BASE_SPEED = 120
    TYPES = ('Psychic',)
    NAME = 'Alakazam'

class Tauros(Pokemon):
    BASE_HP = 75
    BASE_ATTACK = 100
    BASE_DEFENCE = 95
    BASE_SPECIAL = 70
    BASE_SPEED = 110
    TYPES = ('Normal',)
    NAME = 'Tauros'

class Zapdos(Pokemon):
    BASE_HP = 90
    BASE_ATTACK = 90
    BASE_DEFENCE = 85
    BASE_SPECIAL = 125
    BASE_SPEED = 100
    TYPES = ('Electric', 'Flying')
    NAME = 'Zapdos'

class Clefable(Pokemon):
    BASE_HP = 95
    BASE_ATTACK = 70
    BASE_DEFENCE = 73
    BASE_SPECIAL = 85
    BASE_SPEED = 60
    TYPES = ('Normal',)
    NAME = 'Clefable'

class Snorlax(Pokemon):
    BASE_HP = 160
    BASE_ATTACK = 110
    BASE_DEFENCE = 65
    BASE_SPECIAL = 65
    BASE_SPEED = 35
    TYPES = ('Normal',)
    NAME = 'Snorlax'

class Chansey(Pokemon):
    BASE_HP = 250
    BASE_ATTACK = 5
    BASE_DEFENCE = 5
    BASE_SPECIAL = 105
    BASE_SPEED = 50
    TYPES = ('Normal',)
    NAME = 'Chansey'

class Move:
    # some sensible defaults
    BASE_POWER = 0
    ALWAYS_EFFECT = False
    EFFECT_CHANCE = 0
    ACCURACY = 255
    TYPE = 'Normal'
    HIGH_CH = False
    NAME = 'Move'
    MAX_PP = 8
    SPECIAL = False
    EXPLOSION = False
    RECOIL = False

    def __init__(self):
        self.pp = self.MAX_PP

    def use(self, user, opponent):
        if self.pp <= 0:
            raise PPError()
        self.pp -= 1
        logging.debug('{} used {}'.format(user.nickname, self.NAME))
        self.main_effect(user, opponent)
        if rng(self.ACCURACY):
            if self.BASE_POWER:
                self.do_damage(user, opponent)
            if self.ALWAYS_EFFECT or rng(self.EFFECT_CHANCE):
                self.side_effect(user, opponent)
        else:
            logging.debug('But it missed!')

    def calc_damage(self, user, opponent, crit=False, rand_val=None):
        basepower = self.BASE_POWER
        if self.SPECIAL:
            attack_stat = 'special'
            defence_stat = 'special'
        else:
            attack_stat = 'attack'
            defence_stat = 'defence'
        if crit:
            attack = user.stats[attack_stat]
            defence = opponent.stats[defence_stat]
        else:
            attack = user.get_stat(attack_stat)
            defence = opponent.get_stat(defence_stat)
        if self.SPECIAL:
            if opponent.light_screen:
                defence = (defence * 2) % 1024
        elif opponent.reflect:
            defence = (defence * 2) % 1024
        if self.EXPLOSION:
            attack = attack // 2
            defence = defence // 4
        if crit:
            level = user.level * 2
        else:
            level = user.level
        if self.TYPE in user.TYPES:
            stab = 3
        else:
            stab = 2
        if rand_val is None:
            rand_val = random.randint(217, 255)
        damage = (level * 2) // 5
        damage = (damage * attack * basepower) // defence
        damage = damage // 50 + 2
        damage = (damage * stab) // 2
        damage = (damage * effectiveness(self, opponent)) // 4
        damage = (damage * rand_val) // 255
        return max(damage, 1)

    def do_damage(self, user, opponent):
        if self.BASE_POWER == 0:
            return
        crit = user.critical_hit(self.HIGH_CH)
        if crit:
            logging.debug("It's a critical hit!")
        damage = self.calc_damage(user, opponent, crit)
        opponent.hp -= damage
        if self.RECOIL:
            user.hp -= damage // 4
        logging.debug('{} damage'.format(damage))

    def side_effect(self, user, opponent):
        """Effects that may occur after a successful accuracy check"""
        raise NotImplementedError

    def main_effect(self, user, opponent):
        """Effects that always occur without requiring an accuracy check"""
        return ''

class ParalysingMove(Move):
    def side_effect(self, user, opponent):
        if self.TYPE not in opponent.TYPES and opponent.status is None:
            opponent.status = 'PAR'
            opponent.status_mod = {'speed': 4}
            logging.debug('{} is paralysed! It may be unable to move!'.format(
                opponent.nickname))

class FreezingMove(Move):
    def side_effect(self, user, opponent):
        if self.TYPE not in opponent.TYPES and opponent.status is None:
            opponent.status = 'FRZ'
            logging.debug('{} is Frozen Solid!'.format(
                opponent.nickname))

class BurnMove(Move):
    def side_effect(self, user, opponent):
        if self.TYPE not in opponent.TYPES and opponent.status is None:
            opponent.status = 'BRN'
            opponent.status_mod = {'attack': 2}
            logging.debug('{} is Burnt!'.format(opponent.nickname))

class SelfDestruct(Move):
    BASE_POWER = 130
    TYPE = 'Normal'
    EXPLOSION = 'True'
    NAME = 'Self-Destruct'

    def main_effect(self, user, opponent):
        user.hp = 0

class BodySlam(ParalysingMove):
    BASE_POWER = 85
    TYPE = 'Normal'
    NAME = 'Body Slam'
    EFFECT_CHANCE = 76
    MAX_PP = 24

class MegaKick(ParalysingMove):
    BASE_POWER = 120
    TYPE = 'Normal'
    NAME = 'Mega Kick'
    MAX_PP = 8
    ACCURACY = 179

class DrillPeck(Move):
    BASE_POWER = 80
    TYPE = 'Flying'
    NAME = 'Drill Peck'
    MAX_PP = 32

class Blizzard(FreezingMove):
    BASE_POWER = 120
    TYPE = 'Ice'
    NAME = 'Blizzard'
    EFFECT_CHANCE = 25
    ACCURACY = 231
    MAX_PP = 8
    SPECIAL = True

class IceBeam(FreezingMove):
    BASE_POWER = 95
    TYPE = 'Ice'
    NAME = 'Blizzard'
    EFFECT_CHANCE = 25
    ACCURACY = 255
    MAX_PP = 16
    SPECIAL = True

class FireBlast(BurnMove):
    BASE_POWER = 120
    TYPE = 'Fire'
    NAME = 'Fire Blast'
    EFFECT_CHANCE = 76
    ACCURACY = 218
    MAX_PP = 8
    SPECIAL = True

class Psychic(Move):
    BASE_POWER = 90
    TYPE = 'Psychic'
    NAME = 'Psychic'
    EFFECT_CHANCE = 76
    ACCURACY = 255
    MAX_PP = 16
    SPECIAL = True

    def side_effect(self, user, opponent):
        logging.debug("{}'s special fell!".format(opponent.nickname))
        opponent.lower_stat('special', 1)
        if opponent.status == 'PAR':
            opponent.status_mod['speed'] *= 4
        elif opponent.status == 'BRN':
            opponent.status_mod['attack'] *= 2

class HyperBeam(Move):
    BASE_POWER = 150
    TYPE = 'Normal'
    NAME = 'Hyper Beam'
    ALWAYS_EFFECT = True
    MAX_PP = 8

    def side_effect(self, user, opponent):
        user.recharge = True

class Surf(Move):
    BASE_POWER = 95
    TYPE = 'Water'
    NAME = 'Surf'
    SPECIAL = True
    MAX_PP = 24

class ThunderWave(Move):
    ALWAYS_EFFECT = True
    TYPE = 'Electric'
    NAME = 'Thunder Wave'
    MAX_PP = 32

    def side_effect(self, user, opponent):
        if opponent.status is None:
            opponent.status = 'PAR'
            opponent.status_mod = {'speed': 4}
            logging.debug('{} is paralysed! It may be unable to move!'.format(opponent.nickname))
        else:
            logging.debug('But it Failed!')

class Thunderbolt(ParalysingMove):
    BASE_POWER = 95
    TYPE = 'Electric'
    NAME = 'Thunderbolt'
    EFFECT_CHANCE = 26 # not sure if effect chances should be out of 255 or not? If so 25 or 26??
    SPECIAL = True
    MAX_PP = 24

class Thunder(ParalysingMove):
    BASE_POWER = 120
    TYPE = 'Electric'
    NAME = 'Thunder'
    EFFECT_CHANCE = 26 # not sure if effect chances should be out of 255 or not? If so 25 or 26??
    SPECIAL = True
    MAX_PP = 24
    ACCURACY = 179

class SeismicToss(Move):
    TYPE = 'Fighting'
    NAME = 'Seismic Toss'
    BASE_POWER = 1
    MAX_PP = 32

    def do_damage(self, user, opponent):
        opponent.hp -= user.level
        logging.debug('{} damage!'.format(user.level))

class Amnesia(Move):
    NAME = 'Amnesia'
    MAX_PP = 32

    def main_effect(self, user, opponent):
        logging.debug("{}'s special greatly rose!".format(user.nickname))
        user.raise_stat('special', 2)
        if opponent.status == 'PAR':
            opponent.status_mod['speed'] *= 4
        elif opponent.status == 'BRN':
            opponent.status_mod['attack'] *= 2

class Recover(Move):
    NAME = 'Recover'
    MAX_PP = 32

    def main_effect(self, user, opponent):
        if user.max_hp - user.hp % 256 != 0:
            user.hp = min(user.max_hp, user.hp + user.max_hp // 2)
        else:
            logging.debug('But it Failed!')

class Rest(Move):
    NAME = 'Rest'
    MAX_PP = 16

    def main_effect(self, user, opponent):
        if user.max_hp - user.hp % 256 != 0:
            user.hp = user.max_hp
            user.status = 'SL{'
            user.sleep_count = 1
        else:
            logging.debug('But it Failed!')

class SoftBoiled(Recover):
    NAME = 'Soft-Boiled'
    MAX_PP = 16

class Reflect(Move):
    NAME = 'Reflect'
    MAX_PP = 32

    def main_effect(self, user, opponent):
        if user.reflect:
            logging.debug('But it Failed!')
        else:
            user.reflect = True
            logging.debug('{} gained armour!'.format(user.nickname))

class Struggle(Move):
    NAME = 'Struggle'
    BASE_POWER = 40
    RECOIL = True
    TYPE = 'Normal'
