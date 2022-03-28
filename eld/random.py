import random
def generate():
    rd = ""
    while len(rd) != 6:
        rd += str(random.randint(1,9))
    return rd


