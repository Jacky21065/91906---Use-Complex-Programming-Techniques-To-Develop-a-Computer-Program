"""
Program Name: Python Maths Car Game
Version Name: Version_2_Blue
Author: Jacky
Date: Sunday 13th July, 2025
Purpose/Description: Blue Car
Language Used: Python 3.10
Files Required: Images, Music
"""

# Purpose: Import necessary libraries
# Imports the PYGAME library for developing the code
import pygame
# Imports the TIME library for pausing and restarting
import time
# Imports the RANDOM library for generating random numbers for maths questions and random positioning of obstacle cars
import random
# Imports the SYMPY library for can generate questions for derivatives, integrals, algebra and number theory
import sympy as sp
# Imports the save file in Json format
import json
# Imports the OS module to allow the system to write to a save file
import os
# Imports FRACTIONS to be generated in the maths questions
from fractions import Fraction
# Imports the TKINTER GUI library for start screen and leaderboard
import tkinter as tk
# For popup alert windows in Tkinter
from tkinter import messagebox


# Global variables for tracking game time
total_game_time = 0.0
start_time_global = 0.0
avg_answer_time = 0.0
# Time taken per question
answer_times = []
# When current question appeared
question_start_time = 0
# Global variables for difficulty selection
selected_difficulty = None

# Mistakes feature
MISTAKES_FILE = "mistakes.json"  # --- MISTAKES FEATURE ---

# Purpose: Define dimensions for the game window
# Width of the game window
DISPLAY_WIDTH = 800
# Height of the game window
DISPLAY_HEIGHT = 600  

# Purpose: Define color shades using RGB values
# RGB value for BLACK
BLACK = (0, 0, 0)
# RGB value for WHITE
WHITE = (255, 255, 255)
# RGB for BLUE
BLUE = (0, 0, 255)

# Purpose: Set dimensions for the cars
# Height of the car
CAR_HEIGHT = 100
# Width of the car
CAR_WIDTH = 50

# Only calculate average if at least one answer recorded
if answer_times:
    avg_answer_time = sum(answer_times) / len(answer_times)
else:
    avg_answer_time = 0.0

# Function to count the score and display it to the player
def score(count):
    # Display the current score
    # Set the font size and font style for displaying the current score
    font = pygame.font.SysFont(None, 70)
    # Render and create score text
    text = font.render("Score : " + str(count), True, BLACK)
    # Display the score to the player 
    gameDisplay.blit(text, (0, 0))  

# Function to draw cars at specified X positions and Y positions
def draw_car(carx, cary, car):
    # Display obstacle car
    # Draw car image at given X position and Y position
    gameDisplay.blit(car, (carx, cary))  

# Function to draw car
def car(x, y):
    # Display player's car
    # Draw car at specified X position and Y position
    gameDisplay.blit(carImg, (x, y))  

# Function to create text to go with the rectangle
def text_objects(text, font):
    # Create text surface and return surface with its rectangle
    # Render and create the text
    textSurface = font.render(text, True, BLACK)
    # Return rendered surface and rectangle
    return textSurface, textSurface.get_rect()  

# Function to display the previously created text
# To be used for displaying the current score
def message_display(text, size, x, y):
    # Display a message on the screen
    # Set the font size and font style for displaying the current score
    font = pygame.font.Font("freesansbold.ttf", size)
    # Get text and rectangle
    text_surface, text_rectangle = text_objects(text, font)
    # Set message at specified X position and Y position
    text_rectangle.center = (x, y)  
    # Display text on top rectangle on top of screen
    gameDisplay.blit(text_surface, text_rectangle)
    # Show current difficulty on screen
    diff_surface = font.render(f"Difficulty: {selected_difficulty}", True, (0, 0, 0))
    screen.blit(diff_surface, (10, 40))  

# Function to determine what happens in the event the user crashes
# into the correct car
def crash(x, y, count):
    global total_game_time, start_time_global, avg_answer_time
    total_game_time = time.time() - start_time_global

    # Save to leaderboard BEFORE quitting and showing end screen
    import csv
    if answer_times:
        avg_answer_time = sum(answer_times) / len(answer_times)
    else:
        avg_answer_time = 0.0

    save_leaderboard_entry(USERNAME, count, total_game_time, avg_answer_time)

    # Display crash image and message
    gameDisplay.blit(crash_img, (x, y))
    message_display("You Crashed", 115, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    pygame.display.update()
    pygame.time.delay(1000)

    pygame.quit()
    show_end_screen()


def generate_question_and_answer(lane1_x, lane2_x, lane3_x):
    current_question, correct_answer = generate_question()

    answers = [correct_answer]

    while len(answers) < 3:
        wrong = make_wrong_answer(correct_answer)
        if wrong not in answers:
            answers.append(wrong)

    random.shuffle(answers)

    answer_lane_map = {
        lane1_x: answers[0],
        lane2_x: answers[1],
        lane3_x: answers[2]
    }

    return current_question, correct_answer, answer_lane_map


def generate_calculus_question(mode=None):
    x = sp.Symbol('x')

    if mode not in ["diff", "int"]:
        mode = random.choice(["diff", "int"])

    coeff = random.randint(1, 5)
    power = random.randint(1, 5)
    poly = coeff * x**power

    if mode == "diff":
        result = sp.diff(poly, x)
        question = f"d/dx of {coeff}x^{power}"
    else:
        result = sp.integrate(poly, x)
        question = f"∫ {coeff}x^{power} dx"

    # Format result as clean string
    result_str = str(result).replace('**', '^').replace('*', '')
    
    return question, result_str


def generate_basic_question():
    op = random.choice(["+", "-", "*", "/"])
    if op == "/":
        b = random.randint(1, 12)
        a = b * random.randint(1, 12)
        question = f"{a} / {b}"
        answer = a // b
    else:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        question = f"{a} {op} {b}"
        answer = eval(question)
    return question, answer


def generate_question():
    global selected_difficulty

    if selected_difficulty == "Beginner":
        return generate_basic_question()

    elif selected_difficulty == "Easy":
        mode = random.choice(["basic", "fraction", "exponent"])

        if mode == "basic":
            return generate_basic_question()

        elif mode == "fraction":
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
            question = f"{a}/{b}"
            return question, a // b

        elif mode == "exponent":
            base, exp = random.randint(1, 5), random.randint(2, 3)
            question = f"{base}^{exp}"
            return question, base ** exp

    elif selected_difficulty == "Medium":
        x = sp.Symbol('x')
        a = random.randint(1, 10)
        sol = random.randint(-10, 10)
        b = random.randint(-10, 10)
        c = a * sol + b
        question = f"Solve: {a}x + {b} = {c}"
        return question, sol

    elif selected_difficulty == "Hard":
        return generate_calculus_question("diff")

    elif selected_difficulty == "Advanced":
        return generate_calculus_question(random.choice(["diff", "int"]))

    return "2+2", 4


def make_wrong_answer(correct):
    try:
        correct = int(correct)
    except:
        return str(correct) + random.choice(["+1", "-1", "+2"])

    if isinstance(correct, int):
        return correct + random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    elif isinstance(correct, Fraction):
        numerator = correct.numerator + random.choice([-2, -1, 1, 2])
        denominator = max(1, correct.denominator + random.choice([-1, 1]))
        return Fraction(numerator, denominator)
    else:
        return str(correct) + random.choice(["1", "2", "3"])


# Function to display the previously created text
# To be used for displaying the answers on the obstacle cars, in white
def message_display(text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont("DejaVu Sans", 25, bold=True)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    gameDisplay.blit(text_surface, text_rect)
    
def setup_pygame():
    global gameDisplay, clock, carImg, car2Img, bgImg, crash_img, START_MUSIC, screen
    # Purpose: Initialise Pygame
    # Start Pygame modules
    pygame.init()  
    
    # Purpose: Set up visuals of the game
    # Set display dimensions of the game window using
    # previously defined dimensions above
    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    screen = gameDisplay  # for message_display usage
    # Set the window title on the game window
    pygame.display.set_caption("Maths Car Game")
    # Create the clock object to manage frame rate
    clock = pygame.time.Clock() 
    
    # Purpose: Load images for the game
    # Load image of the player's car
    carImg = pygame.image.load("blue.png")
    # Load image of the obstacle's car
    car2Img = pygame.image.load("obstacle_car.png")
    # Load image of the background for the game to scroll through
    bgImg = pygame.image.load("background.png")
    # Load image of a crash which only appears on collision
    crash_img = pygame.image.load("appear_on_collision.png")

    # Set game window icon to car image
    pygame.display.set_icon(carImg)  

    # Refresh the screen
    pygame.display.update()
    # Run at 60 frames per second
    clock.tick(60)  

    # Purpose: Load and play the background music using a mp3 file
    try:
        # Load the mp3 file containing the Background Music
        START_MUSIC = pygame.mixer.Sound("background_music.mp3")
        # Play the mp3 file containing the Background Music
        START_MUSIC.play()
        # In case the music file is missing show an error message
        # to prevent entire program from malfunctioning
    except (pygame.error, FileNotFoundError):
        # Show a warning popup window on Tkinter (not the console) if the music file is missing
        messagebox.showwarning(
            "Missing Music File",
            """ERROR: Background music file not found.
    To fix this error, place 'background_music.mp3' in the program's folder."

    NOTE: The game will still run without music."""
        )   


def save_mistake_entry(username, question, correct_answer, player_answer, difficulty):
    try:
        if os.path.exists(MISTAKES_FILE):
            with open(MISTAKES_FILE, "r") as file:
                mistakes = json.load(file)
        else:
            mistakes = []

        mistakes.append({
            "Username": username,
            "Question": question,
            "Correct_Answer": str(correct_answer),
            "Player_Answer": str(player_answer),
            "Difficulty": difficulty
        })

        with open(MISTAKES_FILE, "w") as file:
            json.dump(mistakes, file, indent=4)

    except Exception as e:
        print("Error saving mistake entry:", e)

def load_mistakes():
    if os.path.exists(MISTAKES_FILE):
        with open(MISTAKES_FILE, "r") as file:
            try:
                return json.load(file)
            except:
                return []
    return []

# Function of the main game loop which handles game logic,
# events, updates and rendering"""
def gameloop():
    global answer_times
    answer_times = []
    global start_time_global
    start_time_global = time.time()
    bg_height = bgImg.get_height()
    bg_y1 = 0
    bg_y2 = -bg_height
    bg_x = (DISPLAY_WIDTH / 2) - (360 / 2)
    bg_speed = 3
    car_y = (DISPLAY_HEIGHT - CAR_HEIGHT)
    car_speed = 0.5
    count = 0
    gameExit = False
    boost_active = False
    # Speed doubles while spacebar held
    boost_multiplier = 4
    
    # Centered 3-lane road based on new background
    road_start_x = (DISPLAY_WIDTH / 2) - 168  
    road_end_x = (DISPLAY_WIDTH / 2) + 168

    lane_width = (road_end_x - road_start_x) / 3
    lane1_x = road_start_x + (lane_width - CAR_WIDTH) / 2
    lane2_x = road_start_x + lane_width + (lane_width - CAR_WIDTH) / 2
    lane3_x = road_start_x + 2 * lane_width + (lane_width - CAR_WIDTH) / 2

    # Start in center
    car_lane = 2 

    # Create a black box surface for the question display
    question_box_height = 80
    question_box_width = lane_width * 3
    question_box_surface = pygame.Surface((question_box_width, question_box_height))
    question_box_surface.fill(BLACK)

    # Generate initial question and answers
    current_question, correct_answer, answer_lane_map = generate_question_and_answer(lane1_x, lane2_x, lane3_x)
    car_starty = 80

    question_start_time = time.time()

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and car_lane > 1:
                    car_lane -= 1
                elif event.key == pygame.K_RIGHT and car_lane < 3:
                    car_lane += 1
                # Support keyboard letters
                elif event.key == pygame.K_a and car_lane > 1:
                    car_lane -= 1
                elif event.key == pygame.K_d and car_lane < 3:
                    car_lane += 1
                elif event.key == pygame.K_SPACE:
                    boost_active = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    boost_active = False

        if car_lane == 1:
            car_x = lane1_x
        elif car_lane == 2:
            car_x = lane2_x
        else:
            car_x = lane3_x

        if car_x < road_start_x or car_x > road_end_x - CAR_WIDTH:
            crash(car_x, car_y, count)

        player_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
        collision_happened = False

        for lane_x, answer in answer_lane_map.items():
            obstacle_rect = pygame.Rect(lane_x, car_starty, CAR_WIDTH, CAR_HEIGHT)
            if player_rect.colliderect(obstacle_rect):
                collision_happened = True
                elapsed = time.time() - question_start_time
                answer_times.append(elapsed)
                if answer == correct_answer:
                    count += 1
                else:
                    save_mistake_entry(USERNAME, current_question, correct_answer, answer, selected_difficulty)
                    crash(car_x, car_y - CAR_HEIGHT // 2, count)

                # Reset for new question
                car_starty = 80
                current_question, correct_answer, answer_lane_map = generate_question_and_answer(lane1_x, lane2_x, lane3_x)
                question_start_time = time.time()
                # Only one collision can happen
                break  

        # Only move and reset if no collision occurred
        if not collision_happened:
            car_starty += car_speed * (boost_multiplier if boost_active else 1)

            if car_starty > DISPLAY_HEIGHT:
                car_starty = 80
                current_question, correct_answer, answer_lane_map = generate_question_and_answer(lane1_x, lane2_x, lane3_x)

        gameDisplay.fill(BLUE)
        gameDisplay.blit(bgImg, (bg_x, bg_y1))
        gameDisplay.blit(bgImg, (bg_x, bg_y2))

        # Blit the black box behind the question
        gameDisplay.blit(question_box_surface, (road_start_x, 10))

        # Display the question text centered inside the box 
        message_display(current_question, 100, road_start_x + question_box_width // 2, 50, WHITE)

        car(car_x, car_y)

        for lane_x, answer in answer_lane_map.items():
            draw_car(lane_x, car_starty, car2Img)
            message_display(str(answer), 2, lane_x + CAR_WIDTH // 2, car_starty + CAR_HEIGHT // 2, WHITE)

        score(count)

        scroll_speed = bg_speed * (boost_multiplier if boost_active else 1)
        bg_y1 += scroll_speed
        bg_y2 += scroll_speed

        if bg_y1 >= DISPLAY_HEIGHT:
            bg_y1 = bg_y2 - bg_height
        if bg_y2 >= DISPLAY_HEIGHT:
            bg_y2 = bg_y1 - bg_height

        pygame.display.update()
        clock.tick(60)
        
# Global to hold username
USERNAME = ""

def launch_game():
    global USERNAME
    USERNAME = username_entry.get().strip()

    if not USERNAME:
        messagebox.showwarning("Missing Username", "Please enter a username before starting.")
        return

    if len(USERNAME) > 12:
        messagebox.showwarning("Username Too Long", "Please enter a username with 12 characters or less.")
        return

    # Proceed to difficulty selection 
    show_difficulty_screen()

# Create Tkinter window
# Create the initial launcher window
def main_menu():
    global root
    root = tk.Tk()
    root.title("Maths Car Game")
    root.geometry("800x600")
    root.configure(bg="skyblue")
    root.resizable(False, False)

    # Load logo image
    logo_img = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo_img, bg="skyblue")
    logo_label.image = logo_img  
    logo_label.pack(pady=(3,3))

    # Title
    tk.Label(root, text="Maths Car Game", font=("Arial", 24, "bold"), bg="skyblue").pack(pady=10)

    # Buttons frame
    btn_frame = tk.Frame(root, bg="skyblue")
    btn_frame.pack(pady=30)

    tk.Button(btn_frame, text="Start", font=("Arial", 14), width=16, command=start_clicked).pack(pady=10)
    tk.Button(btn_frame, text="Instructions", font=("Arial", 14), width=16, command=show_instructions).pack(pady=10)
    tk.Button(btn_frame, text="Leaderboard", font=("Arial", 14), width=16, command=show_leaderboard_screen).pack(pady=10)
    tk.Button(btn_frame, text="Mistakes", font=("Arial", 14), width=16, command=show_mistakes_screen).pack(pady=10)
    tk.Button(btn_frame, text="Exit", font=("Arial", 14), width=16, command=root.destroy).pack(pady=10)

    root.mainloop()

def start_clicked():
    # Hide menu buttons and show username entry
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Enter Username", font=("Arial", 20), bg="skyblue").pack(pady=10)

    username_frame = tk.Frame(root, bg="skyblue")
    username_frame.pack(pady=5)

    tk.Label(username_frame, text="Username:", font=("Arial", 14), bg="skyblue").pack(side=tk.LEFT)
    global username_entry
    username_entry = tk.Entry(username_frame, font=("Arial", 14))
    username_entry.pack(side=tk.LEFT)

    tk.Button(root, text="Continue", font=("Arial", 12), command=launch_game).pack(pady=10)

def show_instructions():
    messagebox.showinfo("Instructions",
                        """Welcome to Maths Car Race!
You are the blue player car. Navigate through the 3 lanes to answer maths questions.

HOW TO PLAY:
Answer the maths questions and score points by driving into the red car with the correct answer.

CONTROLS:

Move the blue player car across the 3 lanes
*Use the Left and Right arrow keys
*OR the "A" key and "D" key

Boost speed of the blue player car
*Hold SPACEBAR

""")

LEADERBOARD_FILE = "leaderboard.json"

# Save a new score entry
def save_leaderboard_entry(username, count, total_time, avg_answer_time):
    try:
        # Load existing data
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as file:
                leaderboard = json.load(file)
        else:
            leaderboard = []

        # Append the new entry
        leaderboard.append({
            "Username": username,
            "Score": int(count),
            "Total_Time": round(float(total_time), 2),
            "Avg_Answer_Time": round(float(avg_answer_time), 2)
        })

        # Save it back
        with open(LEADERBOARD_FILE, "w") as file:
            json.dump(leaderboard, file, indent=4)

    except Exception as e:
        print("Error saving leaderboard:", e)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            try:
                return json.load(file)
            except:
                return []
    return []

def show_leaderboard_screen():
    leaderboard = load_leaderboard()

    if not leaderboard:
        messagebox.showinfo("Leaderboard", "No leaderboard data found.")
        return

    # Sort leaderboard by score descending
    leaderboard.sort(key=lambda x: x.get("Score", 0), reverse=True)

    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("800x600")
    leaderboard_window.configure(bg="cornflowerblue")
    leaderboard_window.resizable(False, False)

    # Title
    tk.Label(leaderboard_window, text="Leaderboard - Top 10", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

    # Text area
    text_frame = tk.Frame(leaderboard_window, bg="white")
    text_frame.pack(padx=70, pady=20, fill="both", expand=True)

    # Header
    header = f"{'Username':<15} {'Score':<7} {'Game Time (s)':<18} {'Average Answer Time (s)':<15}"
    tk.Label(text_frame, text=header, font=("Courier New", 13, "bold"), bg="white").pack(anchor='w')

    # Entries
    for entry in leaderboard[:10]:
        username = entry.get("Username", "N/A")
        score = entry.get("Score", 0)
        total_time = entry.get("Total_Time", 0)
        avg_time = entry.get("Avg_Answer_Time", 0)

        line = f"{username:<15} {score:<7} {total_time:<18.2f} {avg_time:<15.2f}"
        tk.Label(text_frame, text=line, font=("Courier New", 12), bg="white").pack(anchor='w')

    # Close button
    tk.Button(leaderboard_window, text="Close", command=leaderboard_window.destroy).pack(pady=10)


# Mistakes button
def show_mistakes_screen():
    mistakes = load_mistakes()

    if not mistakes:
        messagebox.showinfo("Mistakes", "No mistakes yet.")
        return

    mistakes_window = tk.Toplevel()
    mistakes_window.title("Mistakes")
    mistakes_window.geometry("1000x800")
    mistakes_window.configure(bg="cornflowerblue")
    mistakes_window.resizable(False, False)

    tk.Label(mistakes_window, text="Mistakes Log", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

    text_frame = tk.Frame(mistakes_window, bg="white")
    text_frame.pack(padx=20, pady=10, fill="both", expand=True)

    mono_font = ("Courier New", 11)

    # Header
    header = f"{'Username':<15} {'Difficulty':<12} {'Question':<32} {'Correct Answer':<20} {'Player Answer':<20}"
    tk.Label(text_frame, text=header, font=("Courier New", 12, "bold"), bg="white", anchor='w').pack(fill='x')
    
    # Divider
    divider = "-" * 120
    tk.Label(text_frame, text=divider, font=mono_font, bg="white", anchor='w').pack(fill='x')

    for entry in mistakes[-50:]:
        username = entry.get("Username", "N/A")[:14]
        diff = entry.get("Difficulty", "N/A")[:11]
        question = entry.get("Question", "N/A")[:31]
        correct_ans = entry.get("Correct_Answer", "N/A")[:19]
        player_ans = entry.get("Player_Answer", "N/A")[:19]

        line = f"{username:<15} {diff:<12} {question:<32} {correct_ans:<20} {player_ans:<20}"
        tk.Label(text_frame, text=line, font=mono_font, bg="white", anchor='w').pack(fill='x')

    # Close button
    tk.Button(mistakes_window, text="Close", command=mistakes_window.destroy).pack(pady=10)

    
def show_difficulty_screen():
    # Create a window to select difficulty after username is entered
    difficulty_window = tk.Toplevel()
    difficulty_window.title("Select Difficulty")
    difficulty_window.geometry("600x400")
    difficulty_window.configure(bg="skyblue")
    difficulty_window.resizable(False, False)

    tk.Label(difficulty_window, text="Choose Difficulty:", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

    # Create buttons for each difficulty level
    difficulties = ["Beginner", "Easy", "Medium", "Hard", "Advanced"]
    for diff in difficulties:
        tk.Button(difficulty_window, text=diff, font=("Arial", 14),
                  width=20, pady=10, bg="#e0e0e0", command=lambda d=diff: start_game_with_difficulty(d, difficulty_window)).pack(pady=5)

def start_game_with_difficulty(difficulty, window):
    global selected_difficulty
     # Store selected difficulty globally
    selected_difficulty = difficulty
    # Close difficulty window
    window.destroy()
    root.destroy()
    # Proceed to the game window
    setup_pygame()
    gameloop()

def show_end_screen():
    # Create a new Tkinter window for the end screen
    end_root = tk.Tk()
    end_root.title("Game Over - Maths Car Game")
    end_root.geometry("800x600")
    end_root.configure(bg="skyblue")
    end_root.resizable(False, False)

    # Load logo image
    logo_img = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(end_root, image=logo_img, bg="skyblue")
    logo_label.image = logo_img  
    logo_label.pack(pady=(3,3))

    tk.Label(end_root, text="You Crashed!", font=("Arial", 24, "bold"), bg="skyblue").pack(pady=10)

    # Display elapsed time from the last game run
    global total_game_time
    if 'total_game_time' in globals():
        time_text = f"Time Survived: {total_game_time:.2f} seconds"
    else:
        time_text = "Time Survived: N/A"
        
    tk.Label(end_root, text=f"Average Answer Time: {avg_answer_time:.2f} seconds", font=("Arial", 16), bg="skyblue").pack(pady=10)
    tk.Label(end_root, text=time_text, font=("Arial", 16), bg="skyblue").pack(pady=10)

    # Restart game
    def restart_game():
        global USERNAME, selected_difficulty, root

        # Clear game state
        USERNAME = ""
        selected_difficulty = ""

        # Destroy end screen window
        end_root.destroy()

        # Recreate the launcher screen
        main_menu()
        
    # Quit button 
    def quit_game():
        end_root.destroy()
        quit()

    # Buttons
    tk.Button(end_root, text="Restart", font=("Arial", 16), width=15, command=restart_game).pack(pady=10)
    tk.Button(end_root, text="Mistakes", font=("Arial", 16), width=15, command=show_mistakes_screen).pack(pady=10)
    tk.Button(end_root, text="Leaderboard", font=("Arial", 16), width=15, command=show_leaderboard_screen).pack(pady=10)
    tk.Button(end_root, text="Quit", font=("Arial", 16), width=15, command=quit_game).pack(pady=10)

    end_root.mainloop()

if __name__ == "__main__":
    main_menu()
