# Weekly Menu Planner

Python script for planning a balanced weekly menu.

## How it works

The script reads from a config file written in YAML and generates a random balanced menu from it.
It's made for programming five pseudo-random meals a day: Breakfast, morning snack, lunch, afternoon snack, dinner.

## `config.yaml` file tweaks

You can change the categories I use (meat, legumes, etc) by the ones that fit your diet (e.g. carbs, proteins, etc.).
You can add as many meals per category as you want. Just make sure that **the number of meals per category is larger than the number of times the category appears per week**. The script will warn you if your *config* file does not meet the requirements.

## Usage:

```
$ python weekly-menu.py [winter/summer]
```
