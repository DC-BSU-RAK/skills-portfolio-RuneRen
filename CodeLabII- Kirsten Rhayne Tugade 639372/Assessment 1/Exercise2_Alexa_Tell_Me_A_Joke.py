"""
************************************

        Alexa Tell Me A Joke

************************************
"""




import tkinter as tk
import random
import winsound


# LOAD JOKES FROM FILE

def load_jokes(filename="randomJokes.txt"):
    jokes = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline.strip()))
    except FileNotFoundError:
        jokes = [("File not found!", "Please ensure randomJokes.txt is in the folder.")]
    return jokes


# HOVER EFFECT FUNCTION

def add_hover_effect(button, color, hover_color, scale_factor=1.05):
    original_font = button["font"]
    button.bind("<Enter>", lambda e: [button.config(bg=hover_color),
                                      button.config(font=(original_font[0], int(original_font[1]*scale_factor)))])
    button.bind("<Leave>", lambda e: [button.config(bg=color),
                                      button.config(font=original_font)])


# MAIN APPLICATION CLASS

class AlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Terminal")
        self.root.geometry("540x360")
        self.root.config(bg="#0b1a2a")
        self.jokes = load_jokes()
        self.current_joke = None

        # Title Label
        self.title_label = tk.Label(
            root,
            text="🤖 ALEXA JOKE TERMINAL",
            font=("Consolas", 20, "bold"),
            bg="#0b1a2a",
            fg="#00dfff"
        )
        self.title_label.pack(pady=15)

        # Joke Frame (Card Style)
        self.joke_frame = tk.Frame(root, bg="#13263f", bd=2, relief="ridge")
        self.joke_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Joke setup label
        self.joke_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Arial", 14),
            wraplength=480,
            bg="#13263f",
            fg="#a0e7ff",
            justify="left",
            anchor="w",
            padx=10,
            pady=10
        )
        self.joke_label.pack(fill="both", expand=True)

        # Punchline label
        self.punchline_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Arial", 13, "italic"),
            wraplength=480,
            bg="#13263f",
            fg="#00ffaa",
            justify="left",
            anchor="w",
            padx=10,
            pady=10
        )
        self.punchline_label.pack(fill="both", expand=True)

        # Buttons frame
        self.button_frame = tk.Frame(root, bg="#0b1a2a")
        self.button_frame.pack(fill="x", pady=10, padx=20)

        # Buttons
        self.tell_joke_btn = tk.Button(
            self.button_frame, text="▶ Generate Joke", command=self.show_joke,
            bg="#00cfff", fg="#000", borderwidth=0, relief="flat", padx=10, pady=8
        )
        self.show_punchline_btn = tk.Button(
            self.button_frame, text="💬 Reveal Punchline", command=self.show_punchline,
            bg="#00ffaa", fg="#000", borderwidth=0, relief="flat", padx=10, pady=8
        )
        self.next_joke_btn = tk.Button(
            self.button_frame, text="⟳ Next Joke", command=self.show_joke,
            bg="#0077ff", fg="white", borderwidth=0, relief="flat", padx=10, pady=8
        )

        # Grid buttons for equal spacing
        self.tell_joke_btn.grid(row=0, column=0, padx=5, sticky="ew")
        self.show_punchline_btn.grid(row=0, column=1, padx=5, sticky="ew")
        self.next_joke_btn.grid(row=0, column=2, padx=5, sticky="ew")
        for i in range(3):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Quit button
        self.quit_btn = tk.Button(
            root, text="✖ Close", command=root.destroy,
            bg="#ff003c", fg="white", borderwidth=0, relief="flat", padx=10, pady=8
        )
        self.quit_btn.pack(pady=10)

        # Hover effects with scale
        add_hover_effect(self.tell_joke_btn, "#00cfff", "#33e6ff")
        add_hover_effect(self.show_punchline_btn, "#00ffaa", "#33ffaa")
        add_hover_effect(self.next_joke_btn, "#0077ff", "#3399ff")
        add_hover_effect(self.quit_btn, "#ff003c", "#ff3366")

    
        # SCALING LOGIC
   
        self.default_fonts = {"title": 20, "joke": 14, "punchline": 13, "button": 11, "quit": 11}
        self.default_wrap = {"joke": 480, "punchline": 480}
        self.default_paddings = {"title": 15, "buttons": 10, "quit": 10, "joke": 10, "punchline": 10}

        self.root.bind("<Configure>", self.scale_ui)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.is_fullscreen = False

    
    # FUNCTIONS

    def show_joke(self):
        self.punchline_label.config(text="")
        self.current_joke = random.choice(self.jokes)
        self.joke_label.config(text="> " + self.current_joke[0])

    def show_punchline(self):
        if self.current_joke:
            emojis = ["😂", "🤣", "😹", "😆"]
            self.punchline_label.config(text="→ " + self.current_joke[1] + " " + random.choice(emojis))
        else:
            self.punchline_label.config(text="System: Please request a joke first.")


    # FULLSCREEN FUNCTIONS
  
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.scale_ui()

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.scale_ui()


    # SCALING FUNCTION
    
    def scale_ui(self, event=None):
        base_width = 540
        scale_factor = max(self.root.winfo_width() / base_width, 1)

        # Title
        self.title_label.config(font=("Consolas", int(self.default_fonts["title"]*scale_factor), "bold"))
        self.title_label.pack_configure(pady=int(self.default_paddings["title"]*scale_factor))

        # Joke and punchline
        self.joke_label.config(font=("Arial", int(self.default_fonts["joke"]*scale_factor)),
                               wraplength=int(self.default_wrap["joke"]*scale_factor),
                               padx=int(self.default_paddings["joke"]*scale_factor),
                               pady=int(self.default_paddings["joke"]*scale_factor))
        self.punchline_label.config(font=("Arial", int(self.default_fonts["punchline"]*scale_factor), "italic"),
                                    wraplength=int(self.default_wrap["punchline"]*scale_factor),
                                    padx=int(self.default_paddings["punchline"]*scale_factor),
                                    pady=int(self.default_paddings["punchline"]*scale_factor))

        # Buttons
        for btn in [self.tell_joke_btn, self.show_punchline_btn, self.next_joke_btn]:
            btn.config(font=("Arial", int(self.default_fonts["button"]*scale_factor)))
        self.quit_btn.config(font=("Arial", int(self.default_fonts["quit"]*scale_factor)))
        self.quit_btn.pack_configure(pady=int(self.default_paddings["quit"]*scale_factor))



# RUN APPLICATION

if __name__ == "__main__":
    root = tk.Tk()
    app = AlexaJokeApp(root)
    try:
        root.iconbitmap("alexaicon.ico")
    except Exception:
        pass
    root.resizable(True, True)
    root.mainloop()
