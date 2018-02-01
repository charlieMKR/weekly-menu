#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script generates a random but balanced weekly menu
Author:
	@charlieMKR
	https://makemyday.io
'''

import yaml, random, sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
Constants
'''

MAX_BREAKFAST = 2 # Max times a breakfast is repeated through the week
MAX_SNACK = 4 # Same with snacks
DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"] # Names to be displayed
MEALS = ["Desayuno", "Almuerzo", "Comida", "Merienda", "Cena"] # Names to be displayed

'''
Functions
'''

def alreadyPicked(menu, candidate):
	for day, meals in menu.iteritems():
		for meal, value in meals.iteritems():
			if value == candidate:
				return True
	return False

def noMoreThanX(menu, candidate, max_times):
	count = 0
	for day, meals in menu.iteritems():
		for meal, value in meals.iteritems():
			if value == candidate:
				count+=1
	if count == max_times:
		return True
	return False

def countTimes(menu, candidate):
	count = 0
	for day, meals in menu.iteritems():
		for meal, value in meals.iteritems():
			if value == candidate:
				count+=1
	return count

def printMenu(menu):
	for day, meals in menu.iteritems():
		print DAYS[int(day)] + ":"
		print "-" * len(DAYS[int(day)])
		for meal in MEALS:
			print meal + ": " + str(meals[meal])
		print "\n#####################\n"

def safeChecks(possible_meals, template):
	# Count how much times each category appears on template
	categorycount = {}
	for key, values in template.iteritems():
		for value in values:
			if value in categorycount:
				categorycount[value] += 1
			else:
				categorycount[value] = 1

	# Perform each check
	for key in possible_meals:

		# Enough snacks check
		if key == "Snacks" and len(possible_meals[key])*MAX_SNACK < 14:
			return "Error: Please add more snacks to config.yaml or increase MAX_SNACK"
		# Enough breakfast meals check
		elif key == "Breakfast" and len(possible_meals[key])*MAX_BREAKFAST < 7:
			return "Error: Please add more breakfast meals to config.yaml or increase MAX_BREAKFAST"
		# Enough of each meal category
		elif key != "Snacks" and key != "Breakfast" and len(possible_meals[key]) < categorycount[key]:
			return "Error: Please add more '" + key + "' meals to config.yaml or reduce the number of times it appears on the template"


	# All OK!
	return "pass"


'''
MAIN
'''

def main():
	# Parameters
	season = "All"
	for arg in sys.argv[1:]:
		if arg == "winter":
			season = "Winter"
		elif arg == "summer":
			season = "Summer"

	# Load data
	stream = open("config.yaml", "r")
	config = yaml.load(stream)
	template = config["Template"]
	# Add posible meals by category
	possible_meals = config["All year"]
	# Load seasonal meals:
	if season != "All":
		for key in possible_meals:
			if key in config[season] and config[season][key] != None:
				possible_meals[key] = possible_meals[key] + config[season][key]
	# Safe check block
	checkresult = safeChecks(possible_meals, template)
	if checkresult != "pass":
		print checkresult
		return 1 # Impossible to generate menu
	# Generate empty menu
	menu = {}
	for day in template:
		menu[day] = dict.fromkeys(MEALS)

	# Fill main meals
	for day, meals in template.iteritems():
		for i in range(2):
			candidate = random.choice(possible_meals[meals[i]])
			while alreadyPicked(menu, candidate):
				candidate = random.choice(possible_meals[meals[i]])
			if i == 0:
				menu[day][MEALS[2]] =  candidate
			else:
				menu[day][MEALS[4]] = candidate

	# Add breakfast
	for day in menu:
		# Add breakfast
		candidate = random.choice(possible_meals["Breakfast"])
		while noMoreThanX(menu, candidate, MAX_BREAKFAST):
			candidate = random.choice(possible_meals["Breakfast"])
		menu[day][MEALS[0]] = candidate

	# Add snacks
	for day in menu:
		# Add snack 1
		candidate = random.choice(possible_meals["Snacks"])
		while noMoreThanX(menu, candidate, MAX_SNACK):
			candidate = random.choice(possible_meals["Snacks"])

		menu[day][MEALS[1]] = candidate

		# Add snack 2
		candidate = random.choice(possible_meals["Snacks"])
		while noMoreThanX(menu, candidate, MAX_SNACK) or candidate == menu[day][MEALS[1]]:
			candidate = random.choice(possible_meals["Snacks"])

		menu[day][MEALS[3]] = candidate
	# Done!
	printMenu(menu)


if __name__ == "__main__":
	main()
