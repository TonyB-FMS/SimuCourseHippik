import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import unicodedata

"""
Module: Trot Race Simulation with Tkinter

Description:
    This module simulates a trot race with multiple horses using Tkinter for GUI. It allows users to select 
    the type of race (1 for Tiercé, 2 for Quarté, 3 for Quinté), specify the number of horses, 
    and run the race by simulating the horses' movements based on dice rolls. 
    The program displays the current standings and the results once the race is complete.

Author(s):
    [Your Name]
    [Your Email]

Date:
    [Date]

License:
    This software is licensed under the [License Name] License. See the LICENSE file for details.

Usage:
    Run this script to start the trot race simulation with a graphical interface. Follow the prompts to choose 
    the type of race, enter the number of horses, and advance through the race. Press the "Next Round" button 
    to simulate each round of the race.

Dependencies:
    - tkinter
    - random
    - unicodedata
"""

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

HORSE_NAMES = [
    "Alezan", "Blaze", "Clover", "Duchess", "Eclipse", "Fury", "Ginger", "Hurricane", "Ivy", "Jasmine",
    "Knight", "Lucky", "Majesty", "Noble", "Orion", "Pepper", "Quicksilver", "Ruby", "Starlight", "Thunder",
    "Uno", "Victory", "Whirlwind", "Xena", "Yankee", "Zephyr", "Arrow", "Bandit", "Champion", "Dancer",
    "Electra", "Falcon", "Galaxy", "Hero", "Inferno", "Jupiter", "King", "Legend", "Mystery", "Neptune"
]


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
        return f"{self.name}: Distance {self.distance_covered} m"


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


class RaceApp:
    def __init__(self, root):
        """
        Initialize the Tkinter application for the trot race simulation.

        Args:
            root (tk.Tk): The main Tkinter window.
        """
        self.root = root
        self.root.title("Simulation de Course Hippique")

        # Initialize UI elements
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='lightgreen')
        self.canvas.pack()

        self.title = tk.Label(self.root, text="Simulation de Course Hippique", font=('Arial', 18))
        self.title.pack(pady=10)

        self.next_round_button = tk.Button(self.root, text="Avancer au tour suivant", command=self.next_round,
                                           state=tk.DISABLED)
        self.next_round_button.pack(pady=10)

        self.info_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.info_label.pack(pady=10)

        # Initialize instance attributes
        self.race_type = None
        self.horses = []
        self.horses_instances = []
        self.horses_positions = []
        self.horse_labels = []
        self.horses_status = []
        self.winners = []

        # Show race type selection dialog
        self.show_race_type_dialog()

    def show_race_type_dialog(self):
        """
        Show a dialog to choose the race type.
        """
        race_type = simpledialog.askstring("Type de course",
                                           "Choisissez le type de la course:\n1 pour Tiercé\n2 "
                                           "pour Quarté\n3 pour Quinté")
        if race_type is None or normalize_string(race_type) not in {'1', '2', '3'}:
            messagebox.showerror("Erreur", "Veuillez entrer '1', '2' ou '3'.")
            self.show_race_type_dialog()
            return

        self.race_type = {'1': 'tiercé', '2': 'quarté', '3': 'quinté'}[normalize_string(race_type)]
        self.start_game()

    def start_game(self):
        """
        Start the race simulation by resetting the game and enabling the 'Next Round' button.
        """
        self.reset_game()
        self.next_round_button.config(state=tk.NORMAL)
        self.info_label.config(text="Appuyez sur 'Avancer au tour suivant' pour simuler chaque tour.")

    def reset_game(self):
        """
        Reset the game by initializing all necessary attributes and UI elements.
        """
        self.horses_positions = []
        self.horse_labels = []
        self.canvas.delete("all")
        self.canvas.create_line(700, 50, 700, 550, fill='red', width=2)  # Recreate finish line

        num_horses = random.randint(12, 20)  # Random number of horses
        self.num_horses = num_horses

        self.horses = random.sample(HORSE_NAMES, num_horses)

        self.horses_instances = [Horse(name) for name in self.horses]
        self.horses_distances = [0] * num_horses
        self.horses_status = ['En course'] * num_horses
        self.winners = []

        for i, horse in enumerate(self.horses):
            y = 50 + i * (500 / num_horses)
            label = tk.Label(self.root, text=f"{horse}: 0 m", font=('Arial', 12))
            label.place(x=10, y=y)
            self.horse_labels.append(label)

            self.horses_positions.append(self.canvas.create_rectangle(50, y - 10, 100, y + 10, fill="blue"))

    def next_round(self):
        """
        Advance the race by one round.
        """
        for horse in self.horses_instances:
            if horse not in self.winners:
                horse.update_speed()
                horse.advance()

        self.update_ui()
        if len(self.winners) >= {'tiercé': 3, 'quarté': 4, 'quinté': 5}[self.race_type]:
            self.display_results()

    def update_ui(self):
        """
        Update the UI with the current positions and statuses of the horses.
        """
        for i, horse in enumerate(self.horses_instances):
            if horse.distance_covered >= 2400 and horse not in self.winners:
                self.winners.append(horse)

            x = 50 + horse.distance_covered * (600 / 2400)
            y = 50 + i * (500 / self.num_horses)
            self.canvas.coords(self.horses_positions[self.horses_instances.index(horse)], x, y - 10, x + 50, y + 10)
            self.horse_labels[self.horses_instances.index(horse)].config(
                text=f"{horse.name}: {horse.distance_covered} m")

    def display_results(self):
        """
        Display the results of the race and prompt the user to replay or exit.
        """
        results = "Classement des gagnants :\n" + "\n".join(
            f"{i + 1}. {winner.name}: {winner.distance_covered} mètres" for i, winner in enumerate(self.winners))
        messagebox.showinfo("Fin de la course", results)
        self.info_label.config(text="La course est terminée!")

        if messagebox.askyesno("Rejouer", "Souhaitez-vous rejouer ?"):
            self.show_race_type_dialog()
        else:
            self.root.quit()


def main():
    root = tk.Tk()
    app = RaceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
