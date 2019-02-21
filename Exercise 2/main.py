import cardlib

cards = [(1, 's'), (2, 'h'), (1, 'h')]
def count(l, value):
    val = 0
    for i in l:
        if i.count(value):
            print(i.count(value))
            val += 1
    return val

print(cards.count(cards, 'h'))