"""
Django command to add default arithmetical concepts to database.
"""
from core.models import (
    NumberModel,
    ArithmeticalConceptModel,
)

from django.core.management.base import BaseCommand


def get_mult_of_arth(number):
    return {
        'name': f"Multiples of {number}",
        'description': f"All numbers which are divisible by {number}.",
        'numbers': [i for i in range(1, 101) if i % number == 0],
    }


def get_ends_with_arth(number):
    return {
        'name': f"Ends with {number}",
        'description': f"All numbers ends with {number}.",
        'numbers': [i for i in range(1, 101) if i % 10 == number],
    }


def get_power_of_arth(number, offset=0):
    ret = {
        'name': f"Power of {number}",
        'description': f"All numbers which are power of {number}",
        'numbers': [offset + number**i for i in range(0, 101)
                    if offset+number**i < 101 and offset+number**i >= 1],
    }
    sign = " + "
    if offset < 0:
        sign = " - "
    if offset:
        ret['name'] += sign
        ret['name'] += f"{abs(offset)}"
        ret['description'] += f", with offset = {offset}"

    return ret


ARITH_CONCEPTS = [
    {
        'name': "Even Numbers",
        'description': "All numbers which are divisible by 2.",
        'numbers': [i for i in range(2, 101) if i % 2 == 0],
    },
    {
        'name': "Odd Numbers",
        'description': "All numbers which are not divisible by 2.",
        'numbers': [i for i in range(2, 101) if i % 2 == 1],
    },
    {
        'name': "Squares Numbers",
        'description': "All numbers which are\
                        the product of a number multiplied by itself.",
        'numbers': [i*i for i in range(1, 11)],
    },
    {
        'name': "All Numbers",
        'description': "All numbers.",
        'numbers': [i for i in range(1, 101)],
    }
]


class Command(BaseCommand):
    """Django command to add default arithmetical concepts to database"""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        NumberModel.objects.all().delete()
        for i in range(1, 101):
            NumberModel.objects.create(value=i)

        for i in range(3, 11):
            ARITH_CONCEPTS.append(get_mult_of_arth(i))

        for i in range(1, 10):
            ARITH_CONCEPTS.append(get_ends_with_arth(i))
        for i in range(2, 11):
            ARITH_CONCEPTS.append(get_power_of_arth(i))

        ARITH_CONCEPTS.append(get_power_of_arth(2, 37))
        ARITH_CONCEPTS.append(get_power_of_arth(2, -32))

        ArithmeticalConceptModel.objects.all().delete()
        for arth in ARITH_CONCEPTS:
            ac = ArithmeticalConceptModel.objects.create(
                name=arth['name'],
                description=arth['description'],
            )
            for number in arth['numbers']:
                ac.add_number(NumberModel.objects.get(value=number))
            ac.save()
