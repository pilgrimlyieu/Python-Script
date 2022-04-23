from itertools import product

def SmallSet(input):
    length = len(input)
    return [list(input[start:end]) for start in range(0, length - 2) for end in range(start + 3, length + 1)]

def ForAll(balls):
    ValidArrangeList = []

    for Arrange in product((-1, 1), repeat = balls):
        BreakorNot = 0
        for smallset in SmallSet(Arrange):
            if not -2 <= sum(smallset) <= 2:
                BreakorNot = 1
                break
        if BreakorNot:
            continue
        ValidArrangeList.append(list(Arrange))

    return ValidArrangeList

# From https://oeis.org/A027383
def Formula(balls):
    return 2 ** (balls // 2 + 2) - 2 if balls % 2 else 3 * 2 ** (balls // 2) - 2