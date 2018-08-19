import string
from random import shuffle


def random_string(length=9):
    choice = list(string.ascii_uppercase + string.digits)
    shuffle(choice)
    return ''.join(choice[0:length])


def unique_id_generator(instance, generator):
    uuid = generator()
    Klass = instance.__class__
    exists = Klass.objects.filter(uuid=uuid).first()
    if exists:
        return unique_id_generator(instance, generator)
    return uuid
