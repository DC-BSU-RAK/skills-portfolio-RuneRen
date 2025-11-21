"""
*********************************

        Arithmetic Quiz

*********************************
"""

import tkinter as tk 
from tkinter import messagebox  
import random  # Import the random module for generating random numbers (for quiz questions)
import winsound  # Import the winsound module for playing system sounds 


# main window

root = tk.Tk()  # Initialize the main window (the root window) of the Tkinter application
root.title("Math Arithmetic Quiz") 
root.geometry("650x600")  
root.configure(bg="#0F0F0F")  
try:
    root.iconbitmap("mathquizicon.ico")  # icon for the window
except Exception:
    # ignore if icon missing
    pass  # If the icon file is missing or an error occurs, simply ignore it
root.resizable(True, True)  # Allow the window to be resized by the user (both width and height)

# Variables
difficulty = "easy"
score = 0
question_number = 0
attempt = 1
num1 = 0
num2 = 0
operation = "+"
score_label = None
answer_entry = None
timer_label = None
time_left = 10
timer_running = False
fullscreen = False

# Countdown bar variables
timer_bar = None
timer_bar_rect = None
bar_width = 300
bar_height = 20

glow_colors = ["#00FFAA", "#00FFFF", "#FF00FF", "#FF44CC", "#00FFAA"]
color_index = 0

title_colors = ["#00FFAA", "#00FFFF", "#FF00FF", "#FF44CC"]
title_index = 0

# Star bg variables
stars = []
num_stars = 100
starfield_canvas = None
neon_colors = ["#00FFAA", "#00FFFF", "#FF00FF", "#FF44CC", "#FFFF00", "#FF8800", "#FF4444"]

# Lives variables
initial_lives = 5
lives = initial_lives
hearts_labels = []  # list of heart Label widgets 
heart_full_char = "♥"  # pixel-style heart
heart_empty_char = "♡"


# Design functions

def scale_fonts(event=None):
    width = root.winfo_width()
    title_size = max(int(width / 25), 16)
    label_size = max(int(width / 40), 12)
    button_size = max(int(width / 60), 10)
    entry_size = max(int(width / 40), 12)
    
    for widget in root.winfo_children():
        recursive_scale(widget, title_size, label_size, button_size, entry_size)

def recursive_scale(widget, title_size, label_size, button_size, entry_size):
    if isinstance(widget, tk.Label):
        text = widget.cget("text")
        if "ARITHMETIC QUEST" in text or "GAME OVER" in text or "LIVES OVER" in text:
            widget.config(font=("Courier", title_size, "bold"))
        else:
            widget.config(font=("Courier", label_size, "bold"))
    elif isinstance(widget, tk.Button):
        widget.config(font=("Courier", button_size, "bold"))
    elif isinstance(widget, tk.Entry):
        widget.config(font=("Courier", entry_size, "bold"))
    for child in widget.winfo_children():
        recursive_scale(child, title_size, label_size, button_size, entry_size)

def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

def exit_fullscreen(event=None):
    global fullscreen
    fullscreen = False
    root.attributes("-fullscreen", False)

def play_correct_sound():
    # quick beep for correct
    try:
        winsound.Beep(800, 150)
    except Exception:
        pass

def play_wrong_sound():
    try:
        winsound.Beep(400, 300)
    except Exception:
        pass

def play_life_lost_sound():
    try:
        # Short low beep for life lost
        winsound.Beep(300, 200)
    except Exception:
        pass

def animate_border(frame):
    global color_index
    frame.config(bg=glow_colors[color_index])
    color_index = (color_index + 1) % len(glow_colors)
    root.after(250, lambda: animate_border(frame))

def animate_title(label):
    global title_index
    label.config(fg=title_colors[title_index])
    title_index = (title_index + 1) % len(title_colors)
    root.after(300, lambda: animate_title(label))

def make_button(text, command, parent):
    button = tk.Button(parent, text=text, command=command,
                       fg="#00FFAA", bg="#111111",
                       activebackground="#222222",
                       activeforeground="#00FFFF",
                       width=30, relief="ridge", bd=4)
    button.bind("<Enter>", lambda e: button.config(bg="#222222", fg="#FFAA00"))
    button.bind("<Leave>", lambda e: button.config(bg="#111111", fg="#00FFAA"))
    return button

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# -------------------
# Starfield Functions
# -------------------
def create_starfield(parent):
    global starfield_canvas, stars
    # if there's already a canvas, destroy it to avoid duplicates
    if starfield_canvas is not None:
        try:
            starfield_canvas.destroy()
        except Exception:
            pass

    starfield_canvas = tk.Canvas(parent, bg="black", highlightthickness=0)
    starfield_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    width = parent.winfo_width() if parent.winfo_width() > 1 else 650
    height = parent.winfo_height() if parent.winfo_height() > 1 else 600

    stars = []
    for _ in range(num_stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        color = random.choice(neon_colors)
        speed = size * random.uniform(0.5, 1.5)  # Depth effect
        star_id = starfield_canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        stars.append({"id": star_id, "size": size, "color": color, "speed": speed})

    animate_starfield(width, height)

def animate_starfield(width, height):
    # starfield_canvas may be re-created
    global starfield_canvas, stars
    if starfield_canvas is None:
        return
    for star in stars:
        try:
            starfield_canvas.move(star["id"], 0, star["speed"])
            x1, y1, x2, y2 = starfield_canvas.coords(star["id"])
            if y1 > height:
                new_x = random.randint(0, width)
                star["color"] = random.choice(neon_colors)
                star["speed"] = star["size"] * random.uniform(0.5, 1.5)
                starfield_canvas.coords(star["id"], new_x, 0, new_x + star["size"], star["size"])
                starfield_canvas.itemconfig(star["id"], fill=star["color"])
            else:
                if random.random() < 0.1:  # Twinkle twinkle
                    starfield_canvas.itemconfig(star["id"], fill=random.choice(neon_colors))
        except Exception:
            continue
                
    if starfield_canvas is not None:
        starfield_canvas.after(50, lambda: animate_starfield(width, height))

# -------------------
# Quiz functions
# -------------------
def randomInt(level):
    if level == "easy":
        return random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99)
    elif level == "advanced":
        return random.randint(1000, 9999)

def decideOperation():
    return random.choice(["+", "-"])

def start_timer():
    global time_left, timer_running, timer_bar, timer_bar_rect
    timer_running = True
    full_time = time_left  # Save initial time for scaling

    def countdown():
        global time_left, timer_running, timer_bar, timer_bar_rect
        if not timer_running:  # Stops if user goes back to menu
            return
        if time_left > 0:
            try:
                timer_label.config(text=f"Time: {time_left}s")
            except Exception:
                pass

            remaining_width = int(bar_width * (time_left / full_time)) if full_time > 0 else 0
            try:
                timer_bar.coords(timer_bar_rect, 0, 0, remaining_width, bar_height)
            except Exception:
                pass

            percentage = time_left / full_time if full_time > 0 else 0
            if percentage > 0.5:
                color = "#00FF00"
            elif percentage > 0.2:
                color = "#FFFF00"
            else:
                color = "#FF4444"
            try:
                timer_bar.itemconfig(timer_bar_rect, fill=color)
            except Exception:
                pass

            time_left -= 1
            root.after(1000, countdown)
        else:
            # Time up -> lose a life
            timer_running = False
            try:
                timer_bar.coords(timer_bar_rect, 0, 0, 0, bar_height)
            except Exception:
                pass
            play_wrong_sound()
            lose_life(reason="TIME UP")
    countdown()

def goBackToMenu():
    global timer_running, time_left
    timer_running = False
    time_left = 0
    root.unbind("<Return>")
    displayMenu()

def displayMenu():
    clear_window()
    root.configure(bg="#0F0F0F")
    create_starfield(root)  # Add starfield behind everything

    border_frame = tk.Frame(root, bg="#00FFAA", bd=6)
    border_frame.pack(padx=30, pady=30, fill="both", expand=True)
    animate_border(border_frame)

    inner_frame = tk.Frame(border_frame, bg="#0F0F0F")
    inner_frame.pack(padx=20, pady=20, fill="both", expand=True)

    title_label = tk.Label(inner_frame, text="ARITHMETIC QUEST", fg="#00FFAA", bg="#0F0F0F")
    title_label.pack(pady=40)
    animate_title(title_label)

    tk.Label(inner_frame, text="SELECT DIFFICULTY", fg="#FF00FF", bg="#0F0F0F").pack(pady=15)

    make_button("1. EASY (1-digit)", lambda: start_quiz("easy"), inner_frame).pack(pady=10)
    make_button("2. MODERATE (2-digit)", lambda: start_quiz("moderate"), inner_frame).pack(pady=10)
    make_button("3. ADVANCED (4-digit)", lambda: start_quiz("advanced"), inner_frame).pack(pady=10)

    scale_fonts()

def displayProblem():
    global num1, num2, operation, answer_entry, score_label, timer_label, time_left, timer_running
    global timer_bar, timer_bar_rect, bar_width, bar_height, hearts_labels
    global score, question_number

    clear_window()
    root.configure(bg="#0F0F0F")
    create_starfield(root)

    border_frame = tk.Frame(root, bg="#00FFAA", bd=6)
    border_frame.pack(padx=30, pady=30, fill="both", expand=True)
    animate_border(border_frame)

    inner_frame = tk.Frame(border_frame, bg="#0F0F0F")
    inner_frame.pack(padx=20, pady=20, fill="both", expand=True)

    operation = decideOperation()
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)

    # Score display
    score_label = tk.Label(inner_frame, text=f"Score: {score}", fg="#00FF00", bg="#0F0F0F")
    score_label.pack(pady=5)

    # Lives / Hearts display
    hearts_frame = tk.Frame(inner_frame, bg="#0F0F0F")
    hearts_frame.pack(pady=5)
    hearts_labels = []
    for i in range(initial_lives):
        if i < lives:
            heart_text = heart_full_char
            fg_color = "#FF4444"
        else:
            heart_text = heart_empty_char
            fg_color = "#333333"
        lbl = tk.Label(hearts_frame, text=heart_text, fg=fg_color, bg="#0F0F0F", font=("Courier", 18, "bold"))
        lbl.pack(side="left", padx=4)
        hearts_labels.append(lbl)

    question_text = f"Q{question_number + 1}/10\n\n{num1} {operation} {num2} = ?"
    tk.Label(inner_frame, text=question_text, fg="#00FFFF", bg="#0F0F0F").pack(pady=20)

    answer_entry = tk.Entry(inner_frame, fg="#00FF00", bg="#000000",
                            justify='center', insertbackground="#00FF00", width=10)
    answer_entry.pack(pady=10)
    answer_entry.focus()

    if difficulty == "easy":
        time_left = 10
    elif difficulty == "moderate":
        time_left = 30
    elif difficulty == "advanced":
        time_left = 60

    timer_label = tk.Label(inner_frame, text=f"Time: {time_left}s", fg="#FFAA00", bg="#0F0F0F")
    timer_label.pack(pady=5)

    timer_bar = tk.Canvas(inner_frame, width=bar_width, height=bar_height, bg="#222222", highlightthickness=0)
    timer_bar.pack(pady=5)
    timer_bar_rect = timer_bar.create_rectangle(0, 0, bar_width, bar_height, fill="#00FF00")

    start_timer()
    root.bind("<Return>", enter_pressed)

    make_button("SUBMIT", checkAnswer, inner_frame).pack(pady=20)
    make_button("BACK TO MENU", goBackToMenu, inner_frame).pack(pady=10)
    scale_fonts()

def enter_pressed(event):
    checkAnswer()

def isCorrect(user_answer):
    return user_answer == (num1 + num2 if operation == "+" else num1 - num2)

def update_score_label():
    try:
        score_label.config(text=f"Score: {score}")
    except Exception:
        pass

def update_hearts_display():
    # Update hearts_labels to reflect current lives
    try:
        for i, lbl in enumerate(hearts_labels):
            if i < lives:
                lbl.config(text=heart_full_char, fg="#FF4444")
            else:
                lbl.config(text=heart_empty_char, fg="#333333")
    except Exception:
        pass

def animate_heart_loss(index):
    # Briefly make the lost heart flash / enlarge then settle as empty
    try:
        lbl = hearts_labels[index]
    except Exception:
        return

    def grow():
        try:
            lbl.config(font=("Courier", 24, "bold"))
            root.after(120, shrink)
        except Exception:
            pass

    def shrink():
        try:
            lbl.config(text=heart_empty_char, fg="#333333", font=("Courier", 18, "bold"))
        except Exception:
            pass

    grow()

def lose_life(reason=""):
    global lives, question_number, attempt, timer_running
    # Stop current timer
    timer_running = False

    # Play life lost sound
    play_life_lost_sound()

    # Deduct a life
    lives -= 1
    attempt = 1  # reset attempt for next question

    # Animate the heart that was lost (last filled heart)
    lost_index = max(0, lives)  # if lives was 5->4, lost_index=4 (0-based)
    animate_heart_loss(lost_index)
    update_hearts_display()

    if lives <= 0:
        root.unbind("<Return>")
        displayLivesOver()
        return
    else:
        nextQuestion()

def checkAnswer():
    global score, attempt, timer_running

    # Stop timer while checking
    timer_running = False

    try:
        user_answer = int(answer_entry.get())
    except Exception:
        messagebox.showwarning("INVALID", "Enter a valid number!")
        # resume timer
        timer_running = True
        start_timer()
        return

    if isCorrect(user_answer):
        play_correct_sound()
        if attempt == 1:
            score += 10
            messagebox.showinfo("CORRECT", "Perfect! +10 points")
        else:
            score += 5
            messagebox.showinfo("CORRECT", "Second try! +5 points")
        update_score_label()
        nextQuestion()
    else:
        play_wrong_sound()
        if attempt == 1:
            attempt += 1
            messagebox.showinfo("TRY AGAIN", "Incorrect! One more try...")
            timer_running = True
            start_timer()
        else:
            correct = num1 + num2 if operation == "+" else num1 - num2
            messagebox.showinfo("WRONG", f"Wrong again!\nAnswer was {correct}")
            # Losing a life on second wrongl
            lose_life(reason="WRONG ANSWER")

def nextQuestion():
    global question_number, attempt, lives
    # If lives depleted, show lives over
    if lives <= 0:
        displayLivesOver()
        return

    question_number += 1
    attempt = 1
    if question_number < 10:
        displayProblem()
    else:
        displayResults()

def displayResults():
    clear_window()
    root.unbind("<Return>")

    border_frame = tk.Frame(root, bg="#00FFAA", bd=6)
    border_frame.pack(padx=30, pady=30, fill="both", expand=True)
    animate_border(border_frame)

    inner_frame = tk.Frame(border_frame, bg="#0F0F0F")
    inner_frame.pack(padx=20, pady=20, fill="both", expand=True)

    if score >= 90:
        grade, color = "A+", "#00FF00"
    elif score >= 80:
        grade, color = "A", "#99FF00"
    elif score >= 70:
        grade, color = "B", "#FFFF00"
    elif score >= 60:
        grade, color = "C", "#FF8800"
    elif score >= 50:
        grade, color = "D", "#FF4444"
    else:
        grade, color = "F", "#FF0000"

    tk.Label(inner_frame, text="GAME OVER", fg="#FF00FF", bg="#0F0F0F").pack(pady=20)
    tk.Label(inner_frame, text=f"SCORE: {score}/100", fg="#00FFFF", bg="#0F0F0F").pack(pady=10)
    tk.Label(inner_frame, text=f"GRADE: {grade}", fg=color, bg="#0F0F0F").pack(pady=20)

    make_button("PLAY AGAIN", displayMenu, inner_frame).pack(pady=10)
    make_button("EXIT", root.destroy, inner_frame).pack(pady=5)
    make_button("BACK TO MENU", goBackToMenu, inner_frame).pack(pady=10)
    scale_fonts()

def displayLivesOver():
    clear_window()
    root.unbind("<Return>")

    border_frame = tk.Frame(root, bg="#FF0000", bd=6)
    border_frame.pack(padx=30, pady=30, fill="both", expand=True)
    animate_border(border_frame)

    inner_frame = tk.Frame(border_frame, bg="#0F0F0F")
    inner_frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(inner_frame, text="LIVES OVER!", fg="#FF4444", bg="#0F0F0F",
             font=("Courier", 28, "bold")).pack(pady=20)

    tk.Label(inner_frame, text=f"Final Score: {score}", fg="#00FFFF", bg="#0F0F0F",
             font=("Courier", 18, "bold")).pack(pady=10)

    # Try again restarts with same difficulty and resets lives
    make_button("TRY AGAIN", lambda: start_quiz(difficulty), inner_frame).pack(pady=10)
    make_button("BACK TO MENU", displayMenu, inner_frame).pack(pady=10) 
    scale_fonts()

def start_quiz(level):
    global difficulty, score, question_number, attempt, lives
    difficulty = level
    score = 0
    question_number = 0
    attempt = 1
    lives = initial_lives
    displayProblem()

# Bind resize font scaling and fullscreen keys
root.bind("<Configure>", scale_fonts)
root.bind("<F11>", lambda e: toggle_fullscreen())
root.bind("<Escape>", lambda e: exit_fullscreen())

displayMenu()
root.mainloop()
