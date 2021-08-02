import json
import tkinter as tk
from game import BouncingBall


class Window:
    def __init__(self):
        """
        Initialising tkinter window attributes.
        """
        self.window = tk.Tk()
        self.width = 685
        self.height = 200
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.title('Set the timer.')
        self.will_tkinter_run = True
        self.time = tk.IntVar()

        # Getting the time previously entered:
        with open('time.json') as time_file:
            self.time.set(json.load(time_file))

        self.label = tk.Label(text='Enter the time for which you want to play in secs:- ', font='bold 15').grid()
        self.entry = tk.Entry(textvariable=self.time).grid(row=0, column=1)
        self.btn = tk.Button(self.window, text='Set the timer', bd='5', command=self.stop_tkinter, bg='blue',
                             fg='white').grid()

    def stop_tkinter(self):
        """
        Stop the tkinter window, call the run function.
        :return: None
        """
        # Save the time :-
        with open('time.json', 'w') as time_file:
            json.dump(self.time.get(), time_file)
        self.window.destroy()
        self.will_tkinter_run = False
        self.run()

    def run(self):
        """
        Run the game and the tkinter window.
        :return: None
        """
        if self.will_tkinter_run:
            # Run the tkinter window.
            tk.mainloop()
        else:
            # Run the game :-
            game = BouncingBall()
            game.settings.time_in_seconds = self.time.get()
            game.run()


w = Window()
w.run()
