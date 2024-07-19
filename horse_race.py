#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Module: Trot Race Simulation

Description:
    This module simulates a trot race with multiple horses. It allows users to select the type of race (Tiercé, Quarté,
    or Quinté), specify the number of horses, and run the race by simulating the horses' movements based on dice rolls.
    The program displays the current standings and the results once the race is complete.

Author(s):
    [Name]
    [Email]

Date:
    [Date]

License:
    This software is licensed under the [License Name] License. See the LICENSE file for details.

Usage:
    Run this script to start the trot race simulation. Follow the prompts to choose the type of race, enter the number
    of horses, and advance through the race. Press 'Enter' to simulate each round of the race.

Dependencies:
    - random
    - unicodedata
"""

import random
import unicodedata

# Table for speed changes based on dice roll and current speed
SPEED_CHANGE = {
    0: {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2},
    1: {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2},
    2: {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2},
    3: {1: -1, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1},
    4: {1: -1, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1},
    5: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: 1},
    6: {1: -2, 2: -1, 3: 0, 4: 0, 5: 0, 6: 'DQ'}
}

# Table for distance covered based on speed
DISTANCE_BY_SPEED = {
    0: 0,
    1: 23,
    2: 46,
    3: 69,
    4: 92,
    5: 115,
    6: 138
}

# Table for horses names to be randomly used
HORSES_NAMES = {

}


def get_race_type():
    """
    Prompt the user to select the type of race (1 for Tiercé, 2 for Quarté, 3 for Quinté).

    Returns:
        str: The race type selected by the user.
    """
    race_type_map = {
        '1': 'tiercé',
        '2': 'quarté',
        '3': 'quinté'
    }

    while True:
        race_choice = input("Choisissez le type de la course (1 pour Tiercé, 2 pour Quarté, 3 pour Quinté): ").strip()
        normalized_choice = normalize_string(race_choice)
        if normalized_choice in race_type_map:
            return race_type_map[normalized_choice]
        print("Choix invalide. Veuillez entrer '1' pour Tiercé, '2' pour Quarté, ou '3' pour Quinté.")


def get_number_of_horses():
    """
    Prompt the user to enter the number of horses.

    Returns:
        int: The number of horses selected by the user.
    """
    while True:
        try:
            number = int(input("Entrez le nombre de chevaux (entre 12 et 20): "))
            if 12 <= number <= 20:
                return number
            print("Nombre invalide. Veuillez entrer un nombre entre 12 et 20.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")


def display_ranking(horses, race_type):
    """
    Display the ranking of horses based on their distance covered.

    Args:
        horses (list): The list of Horse objects.
        race_type (str): The type of race to determine the number of winners to display.
    """
    sorted_horses = sorted([horse for horse in horses if not horse.disqualified], key=lambda x: x.distance_covered,
                           reverse=True)
    num_winners = {'tiercé': 3, 'quarté': 4, 'quinté': 5}.get(race_type, 0)
    print("\nClassement actuel:")
    for horse in sorted_horses[:num_winners]:
        print(horse)
    print()


class Horse:
    def __init__(self, name):
        """
        Initialize a Horse instance.

        Args:
            name (str): The name of the horse.
        """
        self.name = name
        self.speed = 0
        self.distance_covered = 0
        self.disqualified = False

    def roll_dice(self):
        """
        Simulate rolling a 6-sided dice.

        Returns:
            int: The result of the dice roll (between 1 and 6).
        """
        return random.randint(1, 6)

    def update_speed(self):
        """
        Update the horse's speed based on the dice roll and current speed.
        The horse may get disqualified if its speed becomes 'DQ'.
        """
        if not self.disqualified:
            dice_roll = self.roll_dice()
            speed_change = SPEED_CHANGE.get(self.speed, {}).get(dice_roll, 0)
            if speed_change == 'DQ':
                self.disqualified = True
                self.speed = 'DQ'
            else:
                self.speed = max(0, self.speed + speed_change)

    def advance(self):
        """
        Advance the horse based on its current speed.
        """
        if not self.disqualified:
            self.distance_covered += DISTANCE_BY_SPEED.get(self.speed, 0)

    def __str__(self):
        """
        Return a string representation of the horse.

        Returns:
            str: Description of the horse's current status.
        """
        if self.disqualified:
            return f"{self.name} (DQ)"
        return f"{self.name}: Speed {self.speed}, Distance {self.distance_covered}"


def normalize_string(s):
    """
    Normalize a string by converting it to lowercase and removing accents.

    Args:
        s (str): The string to normalize.

    Returns:
        str: The normalized string.
    """
    s = s.lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s


def main():
    """
    Main function to run the trot race simulation.
    """
    print("Bienvenue au simulateur de course de trot attelé!")

    num_horses = get_number_of_horses()
    race_type = get_race_type()

    horses = [Horse(f"Cheval {i + 1}") for i in range(num_horses)]

    time_elapsed = 0
    finish_line = 2400

    while True:
        input("Appuyez sur n'importe quelle touche pour avancer d'un tour...")

        for horse in horses:
            horse.update_speed()
            horse.advance()

        time_elapsed += 10
        print(f"\nTemps écoulé: {time_elapsed // 60}m {time_elapsed % 60}s")

        display_ranking(horses, race_type)

        if any(horse.distance_covered >= finish_line and not horse.disqualified for horse in horses):
            break

    print("\nLa course est terminée!")
    display_ranking(horses, race_type)


if __name__ == "__main__":
    main()
