# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
	If you ever have the questions "What does this Pokémon look like Shiny?" and "How rare is it in Pokémon GO?" then
	this is the program for you.

	1. This program will first prompt the user for a Pokémon to search.
	2. The odds of finding the "Shiny" version of that Pokémon in the mobile application "Pokémon GO" are then scraped.
	3. A web page will open with an image of the "Shiny" version of that Pokémon.
	4. The odds that were previously scraped are displayed.

	After and the Pokémon is given by the user and this program is executed, the user should then be able to see what the "Shiny"
	version of that Pokémon looks like and the chances of encountering it in Pokémon GO.

	IMPORTANT: "PATH" variable must be changed to the location of the chromedriver on your machine!
	You must have chromedriver installed for this script to work.
"""

# Copyright (c) 2024 Aaron Galentine
# All rights reserved.

# This is free software; you can redistribute it and/or modify it under the terms of the AGPL-3.0 License.
# This software is distributed "as is", without any guarantees of any kind, express or implied.


import tkinter as tk

from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Gives us access to enter key, escape key, etc
from selenium.webdriver.common.by import By # For explicit wait
from selenium.webdriver.support.wait import WebDriverWait # For explicit wait
from selenium.webdriver.support import expected_conditions as EC # For explicit wait

from tkinter import *
from tkinter import Tk # Used to take input from user
from tkinter.simpledialog import askstring # Used to take input from user
from tkinter import font # Used to alter font on GUI

# Configures appropriate chromedriver
PATH = 'C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe' # <--- CHANGE THIS VARIABLE
driver = webdriver.Chrome(PATH) # Makes it so that Chrome will open the next website as the set driver

root = tk.Tk() # Creates main window of tkinter
root.title("shinyinfo") # Sets title of tkinter window
custom_font = font.Font(family="Helvetica", size=24, weight="bold") # Create a custom font object
root.withdraw() # Hides the window
 
try:
	pokemon = askstring("shinyinfo", 'Enter a Pokémon to search for: ') # Generate popup asking user for Pokémon name
	pokemon = pokemon.title() # Auto-capitalizes user input

	# Opens website to scrape odds of Shiny Pokémon in Pokémon GO
	driver.get("https://shinyrates.com/")

	# We need to have the program quit as soon as it knows no Pokémon by that name is present
	element = WebDriverWait(driver, 2).until(
		EC.presence_of_element_located((By.XPATH, "//*[text()='" + pokemon + "']/following-sibling::td[1]"))
	)

	# Look for the row with the name of the Pokémon and set the rate to the value of the next cell in the table
	odds = driver.find_element(By.XPATH, "//*[text()='" + pokemon + "']/following-sibling::td[1]").text

	print("Odds: " + odds)

	# Navigates to the image for that particular Pokémon's "Shiny" form in Pokémon GO
	driver.get("https://img.pokemondb.net/sprites/go/shiny/" + pokemon.lower() + ".png")

	root.geometry("300x150") # Sets the resolution of the window
	root.deiconify() # Unhides main window of tkinter

	label = tk.Label(root, text="Odds: " + odds, font=custom_font) # Creates a Label to display the odds in a custom font
	label.pack(pady=30) # Adds vertical padding to Label

	root.mainloop() # Runs root, which is the tkinter window

except:
	print("An exception occurred.")

	root.geometry("400x150") # Sets the resolution of the window
	root.deiconify() # Unhides main window of tkinter

	error_label = tk.Label(root, text="Pokémon not found!\nTry again?", font=custom_font) # Creates an error Label in a custom font
	error_label.pack(pady=20) # Adds vertical padding to Label

	root.mainloop()

	driver.quit() # Closes entire browser