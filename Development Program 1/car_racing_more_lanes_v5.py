"""
Program Name: Python Maths Car Game
Version Name: v4_maths_car_race_with_movement
Author: Jacky
Date: Friday, 9th May 2025
Purpose/Description: Concept Program 3
Language Used: Python 3.10
Files Required: Images
Known Issues: Need to add Maths Questions for version 4.
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

# Purpose: Initialise Pygame
# Start Pygame modules
pygame.init()  

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
# Width of the car
CAR_WIDTH = 50
# Height of the car
CAR_HEIGHT = 100  

# Purpose: Load and play the background music using a mp3 file
try:
    # Load the mp3 file containing the Background Music
    START_MUSIC = pygame.mixer.Sound("background_music.mp3")
    # Play the mp3 file containing the Background Music
    START_MUSIC.play()
    # In case the music file is missing show an error message
    # to prevent entire program from malfunctioning
except pygame.error:
    print("Error: Background music file not found. To fix this error, make sure \"background_music.mp3\" is inside this program's folder.")
except FileNotFoundError:
    print("Error: Background music file not found. To fix this error, make sure \"background_music.mp3\" is inside this program's folder.")
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

# Function to display the introduction screen
def introduction_screen():
    # Control variable for the introduction screen loop
    intro = True
    # X position for the "Start" button
    menu1_x = 200
    # Y position for the "Start" button
    menu1_y = 400
    # X position for the "Exit" button
    menu2_x = 500
    # Y position for the "Exit" button
    menu2_y = 400
    # Width of both buttons
    menu_width = 100
    # Height of both buttons
    menu_height = 50  

    # While loop to keep the introduction screen running
    while intro:
        # Loop through all events in the event queue
        for event in pygame.event.get(): 
            # Check if the event is closing the window
            if event.type == pygame.QUIT:  
                # Quit all Pygame modules and close the window
                pygame.quit()
                # Exit the Python program completely
                quit()  

        # Set game window icon to car image
        pygame.display.set_icon(carImg)  

        # Purpose: Draw BLACK button outlines
        # Forms a BLACK border around the "Start" button 
        pygame.draw.rect(gameDisplay, BLACK, (200, 400, 100, 50))
        # Forms a BLACK border around the "Exit" button
        pygame.draw.rect(gameDisplay, BLACK, (500, 400, 100, 50))  

        # Fill introduction screen with BLUE
        gameDisplay.fill(BLUE)
        # Display title on the introduction screen
        message_display("MATHS CAR GAME", 80, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)  

        # Fill the "Start" and "Exit" buttons with GREEN and RED
        # GREEN "Start" button
        pygame.draw.rect(gameDisplay, GREEN, (200, 400, 100, 50))
        # RED "Exit" button
        pygame.draw.rect(gameDisplay, RED, (500, 400, 100, 50))  

        # Get mouse cursor position
        mouse = pygame.mouse.get_pos()
        # Check mouse click states
        click = pygame.mouse.get_pressed()  

        # If mouse is hovering over "Start" button
        if menu1_x < mouse[0] < menu1_x + menu_width and menu1_y < mouse[1] < menu1_y + menu_height:
            # Highlight "Start" button in BLACK
            pygame.draw.rect(gameDisplay, BLACK, (200, 400, 100, 50))
            # If left mouse button clicked
            if click[0] == 1:
                # Exit introduction screen
                intro = False  

        # If mouse is hovering over "Exit" button
        if menu2_x < mouse[0] < menu2_x + menu_width and menu2_y < mouse[1] < menu2_y + menu_height:
            # Highlight "Exit" button in BLACK
            pygame.draw.rect(gameDisplay, BLACK, (500, 400, 100, 50))
            # If left mouse button clicked
            if click[0] == 1:
                # Quit all Pygame modules and close the window
                pygame.quit()
                # Exit the Python program completely
                quit()  

        # Display button labels
        # Start label
        message_display("Go", 40, menu1_x + menu_width / 2, menu1_y + menu_height / 2)
        # Exit label
        message_display("Exit", 40, menu2_x + menu_width / 2, menu2_y + menu_height / 2)  

        # Refresh the screen
        pygame.display.update()
        # Run at 60 frames per second
        clock.tick(60)  


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


# Function to display the previosuly created text
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
    # Show crash image and restart the game
    # Display crash image at specified position X and position Y
    gameDisplay.blit(crash_img, (x, y))
    # Show crash text
    message_display("You Crashed", 115, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    # Refresh screen
    pygame.display.update()
     # Wait 2 seconds
    time.sleep(2)
    # Restart the gameloop()
    gameloop()  

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

def message_display(text, size, x, y, color=(255,255,255)):
    font = pygame.font.Font("freesansbold.ttf", size)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    gameDisplay.blit(text_surface, text_rect)

# Function of the main game loop which handles game logic,
# events, updates and rendering"""
def gameloop():
    bg_x1 = (DISPLAY_WIDTH / 2) - (360 / 2)
    bg_x2 = (DISPLAY_WIDTH / 2) - (360 / 2)
    bg_y1 = 0
    bg_y2 = -600
    bg_speed = 3
    car_y = (DISPLAY_HEIGHT - CAR_HEIGHT)
    car_lane = 1
    car_speed = 0.5
    count = 0
    gameExit = False
    boost_active = False
    # Speed doubles while spacebar held
    boost_multiplier = 3

    road_start_x = (DISPLAY_WIDTH / 2) - 112
    road_end_x = (DISPLAY_WIDTH / 2) + 112

    lane_width = (road_end_x - road_start_x) / 4
    lane1_x = road_start_x + (lane_width - CAR_WIDTH) / 2
    lane2_x = road_start_x + lane_width + (lane_width - CAR_WIDTH) / 2
    lane3_x = road_start_x + 2 * lane_width + (lane_width - CAR_WIDTH) / 2
    lane4_x = road_start_x + 3 * lane_width + (lane_width - CAR_WIDTH) / 2
    lane_positions = [lane1_x, lane2_x, lane3_x, lane4_x]


    # Create a semi-transparent black box surface for the question display
    question_box_height = 80
    question_box_width = lane_width * 2
    question_box_surface = pygame.Surface((question_box_width, question_box_height))
    question_box_surface.set_alpha(255)  # semi-transparent
    question_box_surface.fill(BLACK)

    # Generate initial question and answers
    current_question, correct_answer = generate_question()

    def make_wrong_answer(correct):
        wrong = correct
        while wrong == correct or (isinstance(wrong, int) and wrong < 0):
            if isinstance(correct, int):
                wrong = correct + random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            else:
                wrong = random.randint(1, 20)
        return wrong

    wrong_answer = make_wrong_answer(correct_answer)
    answers = [correct_answer, wrong_answer]
    random.shuffle(answers)

    answer_lane_map = {
        lane1_x: answers[0],
        lane2_x: answers[1]
    }

    car_starty = 80

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and car_lane > 1:
                    car_lane -= 1
                elif event.key == pygame.K_RIGHT and car_lane < 4:
                    car_lane += 1
                elif event.key == pygame.K_SPACE:
                    boost_active = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    boost_active = False
    
        car_x = lane_positions[car_lane - 1]

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
                car_starty = 80
                current_question, correct_answer = generate_question()
                wrong_answer = make_wrong_answer(correct_answer)
                answers = [correct_answer, wrong_answer]
                random.shuffle(answers)
                answer_lane_map = {
                    lane1_x: answers[0],
                    lane2_x: answers[1]
                }
                break

            if not collision_happened:
                car_starty += car_speed * (boost_multiplier if boost_active else 1)

        if car_starty > DISPLAY_HEIGHT:
            car_starty = 80
            current_question, correct_answer = generate_question()
            wrong_answer = make_wrong_answer(correct_answer)
            answers = [correct_answer, wrong_answer]
            random.shuffle(answers)
            answer_lane_indices = random.sample(range(4), k=2)
            answer_lane_map = {
            lane_positions[answer_lane_indices[0]]: answers[0],
            lane_positions[answer_lane_indices[1]]: answers[1]
                              }

        gameDisplay.fill(BLUE)
        gameDisplay.blit(bgImg, (bg_x1, bg_y1))
        gameDisplay.blit(bgImg, (bg_x2, bg_y2))

        # Blit the black semi-transparent box behind the question
        gameDisplay.blit(question_box_surface, (road_start_x, 10))

        # Display the question text centered inside the box (vertically approx center at y=50)
        message_display(current_question, 50, road_start_x + question_box_width // 2, 50, WHITE)

        car(car_x, car_y)
        car_start_lane = random.randint(0, 3)
        car_startx = lane_positions[car_start_lane]

    for lane_x, answer in answer_lane_map.items():
        draw_car(lane_x, car_starty, car2Img)
        message_display(str(answer), 40, lane_x + CAR_WIDTH // 2, car_starty + CAR_HEIGHT // 2, WHITE)

        score(count)

        scroll_speed = bg_speed * (boost_multiplier if boost_active else 1)
        bg_y1 += scroll_speed
        bg_y2 += scroll_speed

        if bg_y1 >= DISPLAY_HEIGHT:
            bg_y1 = -600
        if bg_y2 >= DISPLAY_HEIGHT:
            bg_y2 = -600

        pygame.display.update()
        clock.tick(60)
        
# Show the introduction screen
introduction_screen()
# Start the main game loop, which encapsulates the code into a
# modular, resuable function
gameloop() 
