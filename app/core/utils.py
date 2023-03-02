"""
Utility functions for core app.
"""


class NumberToWords:
    """Convert a number to English word."""
    lookup = {
        0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four",
        5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine",
        10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen",
        14: "Fourteen", 15: "Fifteen", 16: "Sixteen", 17: "Seventeen",
        18: "Eighteen", 19: "Nineteen", 20: "Twenty", 30: "Thirty",
        40: "Forty", 50: "Fifty", 60: "Sixty", 70: "Seventy",
        80: "Eighty", 90: "Ninety",
    }
    units = ["", "Thousand", "Million", "Billion"]

    @staticmethod
    def convert(number):
        if number == 0:
            return "Zero"
        res, i = [], 0
        while number:
            cur = number % 1000
            if number % 1000:
                res.append(
                    NumberToWords.threeDigits(cur, NumberToWords.units[i])
                    )
            number //= 1000
            i += 1
        return " ".join(res[::-1])

    @staticmethod
    def twoDigits(num):
        if num in NumberToWords.lookup:
            return NumberToWords.lookup[num]
        ret = NumberToWords.lookup[(num // 10) * 10]
        ret += " " + NumberToWords.lookup[num % 10]
        return ret

    @staticmethod
    def threeDigits(num, unit):
        res = []
        if num // 100:
            res = [NumberToWords.lookup[num // 100] + " " + "Hundred"]
        if num % 100:
            res.append(NumberToWords.twoDigits(num % 100))
        if unit != "":
            res.append(unit)
        return " ".join(res)
