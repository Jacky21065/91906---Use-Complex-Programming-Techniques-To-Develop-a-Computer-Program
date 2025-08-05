"""
Program Name: Python Maths Car Game
Version Name: v4_maths_car_race_with_movement
Author: Jacky
Date: Friday, 9th May 2025
Purpose/Description: Concept Program 3
Language Used: Python 3.10
Files Required: Images, Music
Known Issues:
"""


# Purpose: Import necessary libraries
# Imports the PYGAME library for developing the code
import pygame
# Imports the TIME library for pausing and restarting
import time
# Imports the RANDOM library for generating random numbers for maths questions and random positioning of obstacle cars
import random  

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

# Add this function to generate math questions and correct answers
def generate_question():
    operations = ["+", "-", "*", "/"]
    op = random.choice(operations)
    
    if op == "+":
        a, b = random.randint(1, 20), random.randint(1, 20)
        correct = a + b
    elif op == "-":
        a, b = random.randint(10, 20), random.randint(1, 10)
        correct = a - b
    elif op == "*":
        a, b = random.randint(1, 10), random.randint(1, 10)
        correct = a * b
    else:  # division
        b = random.randint(1, 10)
        correct = random.randint(1, 10)
        a = correct * b  # ensures exact division
    question = f"{a} {op} {b}"
    return question, correct

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
            # Highlight "Start" button in WHITE
            pygame.draw.rect(gameDisplay, WHITE, (200, 400, 100, 50))
            # If left mouse button clicked
            if click[0] == 1:
                # Exit introduction screen
                intro = False  

        # If mouse is hovering over "Exit" button
        if menu2_x < mouse[0] < menu2_x + menu_width and menu2_y < mouse[1] < menu2_y + menu_height:
            # Highlight "Exit" button in WHITE
            pygame.draw.rect(gameDisplay, WHITE, (500, 400, 100, 50))
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


# Function of the main game loop which handles game logic,
# events, updates and rendering"""
def gameloop():
    bg_x1 = (DISPLAY_WIDTH / 2) - (360 / 2)
    bg_x2 = (DISPLAY_WIDTH / 2) - (360 / 2)
    bg_y1 = 0
    bg_y2 = -600
    bg_speed = 6  
    car_x = ((DISPLAY_WIDTH / 2) - (CAR_WIDTH / 2))
    car_y = (DISPLAY_HEIGHT - CAR_HEIGHT)
    car_lane = 1  

    car_starty = -600
    car_speed = 3
    count = 0
    gameExit = False  

    road_start_x =  (DISPLAY_WIDTH / 2) - 112
    road_end_x = (DISPLAY_WIDTH / 2) + 112  

    lane_width = (road_end_x - road_start_x) / 2
    lane1_x = road_start_x + (lane_width - CAR_WIDTH) / 2
    lane2_x = road_start_x + lane_width + (lane_width - CAR_WIDTH) / 2

    # For single obstacle car, randomly pick lane each time
    def new_obstacle():
        # Generate new math question and correct answer
        q, correct = generate_question()
        # Randomly choose lane for obstacle car
        lane_x = random.choice([lane1_x, lane2_x])

        # Decide if the answer on car is correct or wrong
        # 70% chance to show correct answer, 30% wrong (adjustable)
        if random.random() < 0.7:
            answer = correct
            is_correct = True
        else:
            # generate a wrong answer (different and positive)
            wrong = correct + random.choice([-3, -2, -1, 1, 2, 3])
            if wrong == correct or wrong < 0:
                wrong = correct + 4
            answer = wrong
            is_correct = False
        return q, correct, lane_x, answer, is_correct

    # Initialize first obstacle
    current_question, correct_answer, car_startx, car_answer, answer_is_correct = new_obstacle()

    while not gameExit:  
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                pygame.quit()
                quit()  

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and car_lane == 2:
                    car_lane = 1
                elif event.key == pygame.K_RIGHT and car_lane == 1:
                    car_lane = 2  
                elif event.key == pygame.K_a and car_lane == 2:
                    car_lane = 1
                elif event.key == pygame.K_d and car_lane == 1:
                    car_lane = 2  

        # Update player car X position according to lane
        if car_lane == 1:
            car_x = lane1_x
        else:
            car_x = lane2_x  

        # Crash if player leaves the road boundaries (optional)
        if car_x < road_start_x:
            crash(car_x - CAR_WIDTH, car_y)
        elif car_x > road_end_x - CAR_WIDTH:
            crash(car_x, car_y)

        player_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
        obstacle_rect = pygame.Rect(car_startx, car_starty, CAR_WIDTH, CAR_HEIGHT)

        # Check collision
        if player_rect.colliderect(obstacle_rect):
            if answer_is_correct:
                # Player hits correct answer = increase score
                count += 1
                # Reset obstacle for next question
                car_starty = -200
                current_question, correct_answer, car_startx, car_answer, answer_is_correct = new_obstacle()
            else:
                # Player hits wrong answer = crash
                crash(car_x, car_y - CAR_HEIGHT // 2)

        # Move obstacle car down
        car_starty += car_speed  

        # If obstacle car moves off screen without collision (player dodged)
        if car_starty > DISPLAY_HEIGHT:
            # If the player dodged the correct answer, crash
            if answer_is_correct:
                crash(car_x, car_y - CAR_HEIGHT // 2)
            # Reset obstacle for next question
            car_starty = -200
            current_question, correct_answer, car_startx, car_answer, answer_is_correct = new_obstacle()

        # Drawing and display code
        gameDisplay.fill(BLUE) 

        gameDisplay.blit(bgImg, (bg_x1, bg_y1))
        gameDisplay.blit(bgImg, (bg_x2, bg_y2))  

        # Display math question at the top, in WHITE for clarity
        font = pygame.font.Font("freesansbold.ttf", 50)
        question_surface = font.render(current_question, True, WHITE)
        question_rect = question_surface.get_rect(center=(DISPLAY_WIDTH // 2, 50))
        gameDisplay.blit(question_surface, question_rect)

        # Draw player car
        car(car_x, car_y)
        # Draw obstacle car
        draw_car(car_startx, car_starty, car2Img)

        # Display answer on obstacle car in WHITE and centered
        answer_surface = font.render(str(car_answer), True, WHITE)
        answer_rect = answer_surface.get_rect(center=(car_startx + CAR_WIDTH // 2, car_starty + CAR_HEIGHT // 2))
        gameDisplay.blit(answer_surface, answer_rect)

        score(count)

        bg_y1 += bg_speed
        bg_y2 += bg_speed 

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
