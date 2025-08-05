"""
Program Name: Python Maths Car Game
Version Name: v3_maths_car_race_with_time_saving
Author: Jacky
Date: Friday, 6th June 2025
Purpose/Description: Development Program 2
Language Used: Python 3.10
Files Required: Images, Music
Known Issues: Need to add a range of difficulty levels and their corresponding maths questions.
Fixed Issues: Same answer generating twice on obstacle cars.
Fixed Issues: Created the function - def generate_question_and_answer():
"""


# Purpose: Import necessary libraries
# Imports the PYGAME library for developing the code
import pygame
# Imports the TIME library for pausing and restarting
import time
# Imports the RANDOM library for generating random numbers for maths questions and random positioning of obstacle cars
import random
# Imports FRACTIONS to be generated in the maths questions
from fractions import Fraction
# Imports the TKINTER GUI library for start screen and leaderboard
import tkinter as tk
# For popup alert windows in Tkinter
from tkinter import messagebox

# Global variables for tracking game time
LAST_GAME_TIME = 0.0
start_time_global = 0.0

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
# RGB value for GREEN
GREEN = (0, 255, 0)
# RGB for RED
RED = (255, 0, 0)
# RGB for BLUE
BLUE = (0, 0, 255)

# Purpose: Set dimensions for the cars
# Height of the car
CAR_HEIGHT = 100
# Width of the car
CAR_WIDTH = 50

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


# Function to determine what happens in the event the user crashes
# into the correct car
def crash(x, y):
    # Calculate how long the game lasted
    global LAST_GAME_TIME, start_time_global
    LAST_GAME_TIME = time.time() - start_time_global 
    # Show crash image and restart the game
    # Display crash image at specified position X and position Y
    gameDisplay.blit(crash_img, (x, y))
    # Show crash text
    message_display("You Crashed", 115, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    # Refresh screen
    pygame.display.update()
    # Pause Pygame to allow the crash screen to display properly
    # Short delay to show crash message
    pygame.time.delay(1000)  
    # Stop Pygame loop  
    pygame.quit()
    # Launch Tkinter end screen
    show_end_screen() 

def generate_question():
    operation = random.choice(['+', '-', '*', '/', 'frac_add', 'frac_sub', 'frac_mul', 'frac_div'])
    
    if operation in ['+', '-', '*', '/']:
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        if operation == '+':
            question = f"{a} + {b} = ?"
            answer = a + b
        elif operation == '-':
            a, b = max(a, b), min(a, b)
            question = f"{a} - {b} = ?"
            answer = a - b
        elif operation == '*':
            question = f"{a} × {b} = ?"
            answer = a * b
        else:  # division
            answer = random.randint(1, 12)
            b = random.randint(1, 12)
            a = answer * b
            question = f"{a} ÷ {b} = ?"
    else:
        frac1 = Fraction(random.randint(1, 9), random.randint(2, 9)).limit_denominator()
        frac2 = Fraction(random.randint(1, 9), random.randint(2, 9)).limit_denominator()
        if operation == 'frac_add':
            question = f"{frac1} + {frac2} = ?"
            answer = frac1 + frac2
        elif operation == 'frac_sub':
            if frac1 < frac2:
                frac1, frac2 = frac2, frac1
            question = f"{frac1} - {frac2} = ?"
            answer = frac1 - frac2
        elif operation == 'frac_mul':
            question = f"{frac1} × {frac2} = ?"
            answer = frac1 * frac2
        else:  # frac_div
            question = f"{frac1} ÷ {frac2} = ?"
            answer = frac1 / frac2

    if answer.denominator == 1:
        answer = answer.numerator
    else:
        answer = str(answer)
    
    return question, answer

def make_wrong_answer(correct):
    if isinstance(correct, Fraction):
        numerator = correct.numerator + random.choice([-3, -2, -1, 1, 2, 3])
        denominator = correct.denominator + random.choice([-2, -1, 1, 2])
        # Avoid zero or negative denominators
        denominator = max(1, denominator)  
        wrong = Fraction(numerator, denominator)
    elif isinstance(correct, int):
        wrong = correct + random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    else:
        wrong = random.randint(1, 20)
    
    return wrong

    answers = [correct_answer] + [make_wrong_answer(correct_answer) for _ in range(2)]
    random.shuffle(answers)

    answer_lane_map = {
        lane1_x: answers[0],
        lane2_x: answers[1],
        lane3_x: answers[2]
                }


def generate_question_and_answer(lane1_x, lane2_x, lane3_x):
    current_question, correct_answer = generate_question()

    # Start with the correct answer
    answers = [correct_answer]

    # Generate two unique wrong answers
    while len(answers) < 3:
        wrong = make_wrong_answer(correct_answer)
        if wrong not in answers:
            answers.append(wrong)


    # Shuffle and assign to lanes
    random.shuffle(answers)
    answer_lane_map = {
        lane1_x: answers[0],
        lane2_x: answers[1],
        lane3_x: answers[2]
    }

    return current_question, correct_answer, answer_lane_map

# Function to display the previously created text
# To be used for displaying the answers on the obstacle cars, in white
def message_display(text, size, x, y, color=(255,255,255)):
    font = pygame.font.Font("freesansbold.ttf", size)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    gameDisplay.blit(text_surface, text_rect)
    
def setup_pygame():
    global gameDisplay, clock, carImg, car2Img, bgImg, crash_img, START_MUSIC
    # Purpose: Initialise Pygame
    # Start Pygame modules
    pygame.init()  
    
    # Purpose: Set up visuals of the game
    # Set display dimensions of the game window using
    # previously defined dimensions above
    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    # Set the window title on the game window
    pygame.display.set_caption("Maths Car Game")
    # Create the clock object to manage frame rate
    clock = pygame.time.Clock() 
    
    # Purpose: Load images for the game
    # Load image of the player's car
    carImg = pygame.image.load("player_car.png")
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
        print("Error: Background music file not found. To fix this error, make sure \"background_music.mp3\" is inside this program's folder.")

# Function of the main game loop which handles game logic,
# events, updates and rendering"""
def gameloop():
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
  
    # Create a semi-transparent black box surface for the question display
    question_box_height = 80
    question_box_width = lane_width * 3
    question_box_surface = pygame.Surface((question_box_width, question_box_height))
    # semi-transparent
    question_box_surface.set_alpha(230)  
    question_box_surface.fill(BLACK)

    # Generate initial question and answers
    current_question, correct_answer, answer_lane_map = generate_question_and_answer(lane1_x, lane2_x, lane3_x)

    car_starty = 80

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
            crash(car_x, car_y)

        player_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
        collision_happened = False

        for lane_x, answer in answer_lane_map.items():
            obstacle_rect = pygame.Rect(lane_x, car_starty, CAR_WIDTH, CAR_HEIGHT)
            if player_rect.colliderect(obstacle_rect):
                collision_happened = True
                if answer == correct_answer:
                    count += 1
                else:
                    crash(car_x, car_y - CAR_HEIGHT // 2)

                # Reset for new question
                car_starty = 80
                current_question, correct_answer, answer_lane_map = generate_question_and_answer(lane1_x, lane2_x, lane3_x)
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

        # Blit the black semi-transparent box behind the question
        gameDisplay.blit(question_box_surface, (road_start_x, 10))

        # Display the question text centered inside the box (vertically approx center at y=50)
        message_display(current_question, 50, road_start_x + question_box_width // 2, 50, WHITE)

        car(car_x, car_y)

        for lane_x, answer in answer_lane_map.items():
            draw_car(lane_x, car_starty, car2Img)
            message_display(str(answer), 40, lane_x + CAR_WIDTH // 2, car_starty + CAR_HEIGHT // 2, WHITE)

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

    # Close Tkinter window and start game
    root.destroy()

    # Start game
    setup_pygame()
    gameloop()

# Create Tkinter window
# Create the initial launcher window
root = tk.Tk()
root.title("Maths Car Game")
root.geometry("800x600")
root.configure(bg="skyblue")

def start_clicked():
    # Hide menu buttons and show username entry
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Enter Username", font=("SegoeUI", 20), bg="skyblue").pack(pady=10)

    username_frame = tk.Frame(root, bg="skyblue")
    username_frame.pack(pady=5)

    tk.Label(username_frame, text="Username:", font=("SegoeUI", 14), bg="skyblue").pack(side=tk.LEFT)
    global username_entry
    username_entry = tk.Entry(username_frame, font=("SegoeUI", 14))
    username_entry.pack(side=tk.LEFT)

    tk.Button(root, text="Continue", font=("SegoeUI", 12), command=launch_game).pack(pady=10)

def show_instructions():
    messagebox.showinfo("Instructions",
                        """Welcome to Maths Car Race!
You are the blue player car. Navigate through the 3 lanes to answer maths questions.

Keys: Use the left and right arrow keys to move the blue player car across the 3 lanes.
Hold SPACE to boost speed.

Answer the math questions and score points by driving into the red car with the correct answer.""")

def show_leaderboard():
    messagebox.showinfo("Leaderboard", "Placeholder")

# Logo/title
tk.Label(root, text="MATHS CAR GAME", font=("SegoeUI", 36, "bold"), bg="skyblue").pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="skyblue")
btn_frame.pack(pady=30)

tk.Button(btn_frame, text="Start", font=("SegoeUI", 14), width=16, command=start_clicked).pack(pady=10)
tk.Button(btn_frame, text="Instructions", font=("SegoeUI", 14), width=16, command=show_instructions).pack(pady=10)
tk.Button(btn_frame, text="Leaderboard", font=("SegoeUI", 14), width=16, command=show_leaderboard).pack(pady=10)
tk.Button(btn_frame, text="Exit", font=("SegoeUI", 14), width=16, command=root.destroy).pack(pady=10)

def show_end_screen():
    # Create a new Tkinter window for the end screen
    end_root = tk.Tk()
    end_root.title("Game Over - Maths Car Game")
    end_root.geometry("800x600")
    end_root.configure(bg="skyblue")

    tk.Label(end_root, text="You Crashed!", font=("SegoeUI", 24, "bold"), bg="skyblue").pack(pady=30)

    # Display elapsed time from the last game run
    global LAST_GAME_TIME
    if 'LAST_GAME_TIME' in globals():
        time_text = f"Time Survived: {LAST_GAME_TIME:.2f} seconds"
    else:
        time_text = "Time Survived: N/A"

    tk.Label(end_root, text=time_text, font=("SegoeUI", 16), bg="skyblue").pack(pady=10)
    # Restart button — closes this window and restarts Pygame game loop
    def restart_game():
        end_root.destroy()
        setup_pygame()
        gameloop()

    # Mistakes button — work on next iteration
    def show_mistakes():
        messagebox.showinfo("Mistakes", "mistakes")

    # Leaderboard button — work on next iteration
    def show_leaderboard_screen():
        messagebox.showinfo("Leaderboard", "leaderboard")

    # Quit button — closes the whole app
    def quit_game():
        end_root.destroy()
        quit()

    # Buttons
    tk.Button(end_root, text="Restart", font=("SegoeUI", 16), width=15, command=restart_game).pack(pady=10)
    tk.Button(end_root, text="Mistakes", font=("SegoeUI", 16), width=15, command=show_mistakes).pack(pady=10)
    tk.Button(end_root, text="Leaderboard", font=("SegoeUI", 16), width=15, command=show_leaderboard_screen).pack(pady=10)
    tk.Button(end_root, text="Quit", font=("SegoeUI", 16), width=15, command=quit_game).pack(pady=10)

    end_root.mainloop()

if __name__ == "__main__":
    root.mainloop()
