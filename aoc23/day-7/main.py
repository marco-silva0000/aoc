from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
from structlog import get_logger


log = get_logger()

f = open("7/test.txt")
f = open("7/input2.txt")
f = open("7/input.txt")


class Card(str):
    ranks = "23456789TJQKA"

    def get_rank(self):
        return self.ranks.index(self)

    def __lt__(self, other):
        first = self.ranks.index(self)
        second = self.ranks.index(other)
        # log.debug(f"first second: {first} {second}")
        return first < second


class Card2(Card):
    ranks = "J23456789TQKA"


class Hand(str):
    part2 = False

    @property
    def n_jokers(self):
        if self.part2:
            return self.count("J")
        return 0

    @property
    def is_poker_alho(self):
        try:
            five_card = next(
                c for c in self if self.count(c) == 5 - self.n_jokers if c != "J"
            )
            log.debug(f"is_poker_alho", card=five_card)
            return True
        except StopIteration:
            if self.part2:
                return self.count("J") == 5
            return False

    @property
    def is_poker(self):
        try:
            four_card = next(
                c for c in self if self.count(c) == 4 - self.n_jokers if c != "J"
            )
            log.debug(f"is_poker", hand=self, four_card=four_card)
            return not self.is_poker_alho
        except StopIteration:
            if self.part2:
                return self.count("J") == 4
            return False

    @property
    def is_three(self):
        try:
            three_card = next(
                c for c in self if self.count(c) == 3 - self.n_jokers if c != "J"
            )
            log.debug(f"three_card: {three_card}")
            log.debug(f"part2: {self.part2}")
            return (
                not self.is_poker_alho and not self.is_poker and not self.is_full_house
            )
        except StopIteration:
            if self.part2:
                return self.count("J") == 3
            return False

    @property
    def is_pair(self):
        try:
            two_card = next(
                c for c in self if self.count(c) == 2 - self.n_jokers if c != "J"
            )
            log.debug(f"two_card: {two_card}")
            return (
                not self.is_poker_alho and not self.is_poker and not self.is_full_house
            )
        except StopIteration:
            if self.part2:
                return self.count("J") == 2
            return False

    @property
    def is_full_house(self):
        try:
            three_card = next(
                c for c in self if self.count(c) == 3 - self.n_jokers if c != "J"
            )
            two_card = next(
                c for c in self if self.count(c) == 2 if c not in [three_card, "J"]
            )
            log.debug(f"is_full_house: {three_card} {two_card}")
            return True
        except StopIteration:
            return False

    @property
    def is_two_pairs(self):
        try:
            two_card = next(
                c for c in self if self.count(c) == 2 - self.n_jokers if c != "J"
            )
            other_two_card = next(
                c for c in self if self.count(c) == 2 if c not in [two_card, "J"]
            )

            return (
                not self.is_poker_alho
                and not self.is_poker
                and not self.is_full_house
                and not self.is_three
            )
        except StopIteration:
            return False

    def get_points(self):
        if self.is_poker_alho:
            return 100
        elif self.is_poker:
            return 90
        elif self.is_full_house:
            return 80
        elif self.is_three:
            return 70
        elif self.is_two_pairs:
            return 60
        elif self.is_pair:
            return 50
        else:
            return 0

    def __lt__(self, other):
        log.debug(f"self other: {self} {other}")
        this_points = self.get_points()
        other_points = other.get_points()
        log.debug(f"this_points other_points: {this_points} {other_points}")
        if this_points == other_points:
            # if self.get_points() + other.get_points() == 0:
            for i in range(5):
                if not self.part2:
                    a_rank = Card(self[i]).get_rank()
                    b_rank = Card(other[i]).get_rank()
                else:
                    a_rank = Card2(self[i]).get_rank()
                    b_rank = Card2(other[i]).get_rank()
                    log.debug(f"a_rank b_rank: {a_rank} {b_rank}")
                if a_rank != b_rank:
                    return a_rank < b_rank

        return this_points < other_points


class Hand2(Hand):
    part2 = True


assert Card2("2") < Card2("3")
assert Card2("2") < Card2("3")
assert Card2("J") < Card2("3")
assert Card2("J") < Card2("2")
assert Hand2("22J34") < Hand2("22J35")
assert Hand2("22J33").is_full_house
assert Hand2("23J33").is_poker
assert Hand2("33J33").is_poker_alho
assert Hand2("12J34").is_pair
assert not Hand2("12345").is_pair
assert Hand2("JJJJJ").is_poker_alho
assert Hand2("2345A") < Hand2("J345A")
assert Hand2("AAAKK").is_full_house
assert Hand2("AAKKJ").is_full_house
assert Hand2("AQKKJ").is_three

# exit()


lines = f.readlines()
hands = []
for l in lines:
    l = l.strip()
    print(l)
    hand, bid = l.split()
    hand = Hand(hand)
    print(hand.is_poker_alho)
    print(hand.is_poker)
    print(hand.is_full_house)
    print(hand.is_three)
    print(hand.is_pair)
    bid = int(bid)
    hands.append((hand, bid))
    print(f"hand: {hand} bid: {bid}")

sorted_hands = sorted(hands, key=lambda x: x[0])
for i, (hand, bid) in enumerate(sorted_hands):
    print(f"{i+1}: {hand} {bid} {hand.get_points()}")
part1 = sum([(i + 1) * bid for i, (_, bid) in enumerate(sorted_hands)])
print(f"part1: {part1}")

# part2
for hand, bid in sorted_hands:
    hand.part2 = True
sorted_hands = sorted(sorted_hands, key=lambda x: x[0])

for i, (hand, bid) in enumerate(sorted_hands):
    print(f"{i+1}: {hand} {bid} {hand.get_points()}")
part2 = sum([(i + 1) * bid for i, (_, bid) in enumerate(sorted_hands)])
print(f"part2: {part2}")
