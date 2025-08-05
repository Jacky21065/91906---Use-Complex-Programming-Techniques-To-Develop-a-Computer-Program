"""
Program Name: Python Maths Car Game
Version Name: v3_maths_car_race_with_movement
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
    # Background image 1 X position
    bg_x1 = (DISPLAY_WIDTH / 2) - (360 / 2)
    # Background image 2 X position
    bg_x2 = (DISPLAY_WIDTH / 2) - (360 / 2)
    # Background 1 starting Y position
    bg_y1 = 0
    # Background 2 starts above the screen
    bg_y2 = -600
    # Scrolling speed (how fast the player is travelling on the road)
    bg_speed = 6  
    # Initial X position of player car (centered)
    car_x = ((DISPLAY_WIDTH / 2) - (CAR_WIDTH / 2))
    # Constant Y position of player car (bottom of screen)
    car_y = (DISPLAY_HEIGHT - CAR_HEIGHT)
    # Player starts in the left lane
    # 1 = left, 2 = right
    car_lane = 1  

    # Start y-position for obstacle car
    car_starty = -600
    # Obstacle car movement speed 
    car_speed = 3
    # Score counter for tracking score
    count = 0
    # Control variable for gameloop()
    gameExit = False  

    # Left lane boundary
    road_start_x =  (DISPLAY_WIDTH / 2) - 112
    # Right lane boundary
    road_end_x = (DISPLAY_WIDTH / 2) + 112  

    # Calculate lane width used to set
    # Position 1 or position 2 for the obstacle car to appear in
    lane_width = (road_end_x - road_start_x) / 2
    # Sets the left lane for the obstacle car to reappear in
    lane1_x = road_start_x + (lane_width - CAR_WIDTH) / 2
    # Sets the right lane for the obstacle car to reappear in
    lane2_x = road_start_x + lane_width + (lane_width - CAR_WIDTH) / 2
    # Random chance of the obstacle car to reappear in the left lane or right lane
    car_startx = random.choice([lane1_x, lane2_x])

    # While Game loop
    while not gameExit:  
        # Loop through all events in the event queue
        for event in pygame.event.get(): 
            # Check if the event is closing the window
            if event.type == pygame.QUIT:  
                # Quit all Pygame modules and close the window
                pygame.quit()
                # Exit the Python program completely
                quit()  

            # If the left arrow key or right arrow key is pressed
            if event.type == pygame.KEYDOWN:
                # Check which key is being pressed, if it is the left arrow key
                # Then shift the player car to the left lane from the right lane
                if event.key == pygame.K_LEFT and car_lane == 2:
                    car_lane = 1
                # Otherwise, if the right arrow key is being pressed
                # Then shift the player car to the right lane from the left lane
                elif event.key == pygame.K_RIGHT and car_lane == 1:
                    car_lane = 2  

            # If they key is released by the user, hence "KEYUP"
            # Stop all horizontal movement of the player car
            if event.type == pygame.KEYUP:  
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0  

        # Update car's position
        if car_lane == 1:
            car_x = lane1_x
        else:
            car_x = lane2_x  

        # Crash if player leaves the road boundaries
        if car_x < road_start_x:
            crash(car_x - CAR_WIDTH, car_y)
        elif car_x > road_end_x - CAR_WIDTH:
            crash(car_x, car_y)

        # Create Rect objects for player car 
        player_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
        # Create Rect objects for obstacle car
        obstacle_rect = pygame.Rect(car_startx, car_starty, CAR_WIDTH, CAR_HEIGHT)

        # Check for collision
        if player_rect.colliderect(obstacle_rect):
            crash(car_x, car_y - CAR_HEIGHT // 2)

        # Sets the background colour beyond the road as BLUE
        gameDisplay.fill(BLUE) 

        # Draw first background
        gameDisplay.blit(bgImg, (bg_x1, bg_y1))
        # Draw second background
        gameDisplay.blit(bgImg, (bg_x2, bg_y2))  

        # Draw player car
        car(car_x, car_y)
        # Draw obstacle car
        draw_car(car_startx, car_starty, car2Img)
        # Display score
        score(count)
        # Increase the score using operations
        count += 1
        # Moves the obstacle car down as the player car moves up
        car_starty += car_speed  

        # If obstacle car moves off screen
        if car_starty > DISPLAY_HEIGHT:
            # Sets a new X position for the obstacle car
            lane_width = (road_end_x - road_start_x) / 2
            # Sets the left lane for the obstacle car to reappear in
            lane1_x = road_start_x + (lane_width - CAR_WIDTH) / 2
            # Sets the right lane for the obstacle car to reappear in
            lane2_x = road_start_x + lane_width + (lane_width - CAR_WIDTH) / 2
            # Random chance of the obstacle car to reappear in the left lane or right lane
            car_startx = random.choice([lane1_x, lane2_x])
            # Resets the Y position for the obstacle car
            car_starty = -200  
        # Scroll background 1
        bg_y1 += bg_speed
        # Scroll background 2
        bg_y2 += bg_speed 

        # Reset background loop for background 1
        if bg_y1 >= DISPLAY_HEIGHT:  
            bg_y1 = -600

        # Reset background loop for background 2
        if bg_y2 >= DISPLAY_HEIGHT:  
            bg_y2 = -600

        # Update screen
        pygame.display.update()  
        # Run at 60 frames per second
        clock.tick(60)  

# Show the introduction screen
introduction_screen()
# Start the main game loop, which encapsulates the code into a
# modular, resuable function
gameloop() 
