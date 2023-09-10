import tkinter as tk
import random
import collections
class Game:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = tk.Canvas(parent)
        self.status = tk.Label(parent)
        self.draw_board()
    def draw_board(self, event=None):
        self.canvas.destroy()
        self.status.destroy()
        self.canvas = tk.Canvas(self.parent, width=1027, height=400,background="#EADDCA")
        self.canvas.pack()
        self.bag = {'r':self.canvas.create_oval(960, 20, 1027, 70, fill='#D22B2B', outline='#D22B2B'),
                    'o':self.canvas.create_oval(960, 74, 1027, 120, fill='#F28C28', outline='#F28C28'),
                    'y':self.canvas.create_oval(960, 124, 1027, 170, fill='#FDDA0D', outline='#FDDA0D'),
                    'g':self.canvas.create_oval(960, 174, 1027, 220, fill='#097969', outline='#097969'),
                    'b':self.canvas.create_oval(960, 224, 1027, 270, fill='#0047AB', outline='#0047AB'),
                    'p':self.canvas.create_oval(960, 274, 1027, 320, fill='#722F37', outline='#722F37')
                   }
        self.ids = {v:k for k,v in self.bag.items()}
        self.colors = {'r':'#D22B2B', 'o':'#F28C28', 'y':'#FDDA0D',
                       'g':'#097969', 'b':'#0047AB', 'p':'#722F37'}
        self.guesses = ['']
        self.status = tk.Label(self.parent)
        self.status.pack()
        self.canvas.bind('<1>', self.check)
        self.parent.bind('<Control-n>', self.draw_board)
        self.parent.bind('<Control-N>', self.draw_board)
        self.pattern = [random.choice('roygbp') for _ in range(4)]
        self.counted = collections.Counter(self.pattern)
    def check(self, event=None):
        id = self.canvas.find_withtag("current")[0]
        guess = self.ids[id]
        self.guesses[-1] += guess
        y_offset = (len(self.guesses[-1]) - 1) * 60
        x_offset = (len(self.guesses) - 1) * 60
        self.canvas.create_oval(10+x_offset, 10+y_offset,
                                x_offset+60, y_offset+60,
                                fill=self.colors[guess],
                                outline=self.colors[guess])
        if len(self.guesses[-1]) < 4:
            return
        guess_count = collections.Counter(self.guesses[-1])
        close = sum(min(self.counted[k], guess_count[k]) for k in self.counted)
        exact = sum(a==b for a,b in zip(self.pattern, self.guesses[-1]))
        close -= exact
        colors = exact*['black'] + close*['white']
        key_coordinates = [(10+x_offset, 310, x_offset+30, 340), 
                           (10+x_offset, 340, x_offset+30, 370), 
                           (x_offset+30,310,x_offset+50,340), 
                           (x_offset+30, 340, x_offset+50, 370)]
        for color, coord in zip(colors, key_coordinates):
            self.canvas.create_oval(coord, fill=color, outline=color)
        if exact == 4:
            self.status.config(text='You win!')
            self.canvas.unbind('<1>')
        elif len(self.guesses) > 11:
            self.status.config(
                               text='Out of guesses. The correct answer is:   {}.'.format(
                                ' '.join(self.pattern).upper()))
            self.canvas.unbind('<1>')
        else:
            self.guesses.append('')
        
root = tk.Tk()
root.title("MASTERMIND")
game = Game(root)
root.mainloop()
