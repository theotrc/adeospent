import random
def generate_code():
    code = int(str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)))
    return code