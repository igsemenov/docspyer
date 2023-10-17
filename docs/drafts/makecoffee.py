# -*- coding: utf-8 -*-
"""Container of coffee makers.
"""

from abc import ABC, abstractmethod


def makecoffee(drink):
    maker = get_coffee_maker(drink)
    run_coffee_maker(maker)


def get_coffee_maker(drink):
    if drink == 'espresso':
        return EspressoMaker()
    if drink == 'latte':
        return LatteMaker()
    return None


def run_coffee_maker(maker):
    maker.make_coffee()


class CoffeeMaker(ABC):
    """Base class for coffee makers.
    """

    def make_coffee(self):
        self.preprocessing()
        self.run_coffee_machine()

    def preprocessing(self):
        self.fill_water_tank()
        self.add_coffee_beans()

    def fill_water_tank(self):
        pass

    def add_coffee_beans(self):
        pass

    @abstractmethod
    def run_coffee_machine(self):
        pass


class EspressoMaker(CoffeeMaker):
    """Makes a cup of espresso.
    """

    def run_coffee_machine(self):
        self.push_espresso_button()

    def push_espresso_button(self):
        pass


class LatteMaker(CoffeeMaker):
    """Makes a cup of latte.
    """

    def run_coffee_machine(self):
        self.push_latte_button()

    def push_latte_button(self):
        pass
