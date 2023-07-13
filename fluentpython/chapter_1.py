# @File  : chapter_1.py
# @Author: LiuXingsheng
# @Date  : 2021/2/20
# @Desc  :
import collections
import random

Card = collections.namedtuple('Card', ['rank', 'suit'])
card1 = Card('7', 'diamonds')
print(card1, type(card1))


class FrechDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JKQA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)


deck = FrechDeck()
print(len(deck))
print(random.choice(deck))

numlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(numlist[2::2])
for num in numlist[::-2]:
    print(num)

suit_value = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrechDeck.ranks.index(card.rank)
    return rank_value * len(suit_value) + suit_value[card.suit]


print('---', len(suit_value))

for card in sorted(deck, key=spades_high):
    print(card)

atuple = (1, 2)


def add_m(a, b):
    return a + b


print(add_m(*atuple))

City = collections.namedtuple('City', ['name', 'country', 'population', 'coordinates'])
tokyo = City('Tokyo', 'JP', 36.933, (35.68, 139.695))
print(tokyo)

beijing = City(name='Beijing', country='China', population=12, coordinates=(1, 2))
print(beijing.name)
print(beijing.country)
print(beijing.population)
print(City._fields)
dlphi = ('Delhi', 'IN', 21.95, (12, 23))
delh = City(*dlphi)
print(delh._asdict())
for key, value in delh._asdict().items():
    print(key + ':', value)

numlist = [1,2,3]
numlist.__delitem__(0)
print(numlist)
numlist.extend((4,3))
print(numlist)
numlistnew = numlist.__add__([4,3])
print(numlist,numlistnew)
numlist.__iadd__([4,3])
print(numlist)
nu = [1,2,3]
newnu = nu.__mul__(10)
print(newnu)
touchnumlist = [1,2,3,4,5,6,7]
print(touchnumlist[:3])
print(type(touchnumlist[0:5:2]))
header = slice(0,2)
footer = slice(4,6)
print(touchnumlist[header],touchnumlist[footer])
testlist =  [['-'] * 3 for i in range(3)]
print(testlist)