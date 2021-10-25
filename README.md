# cardbuilder
Script for building tcg cards from csv description and png templates

# How to Run
This program comes with a Dockerfile for setting up a docker container containing the Pygame/SDL dependencies needed because managing those dependencies is outside the scope of what virtualenv is capable of.

Build the container with:
	`docker build -t cardbuilder .`

Assuming you have your png resources and input csv all within the same directory, Run the container with:
	`docker run -v "<path to your data>":/data cardbuilder -r /data/<resources> -i /data/<csvfile> -o /data/out`

e.g.:
	`docker run -v "c:\dev\card_builder":/data cardbuilder -r /data/resources -i /data/test.csv -o /data/out`

# ToDo
 * [x] Read all Part 2 Leshy cards from CSV
 * [ ] Read all Part 2 Grimoria cards from CSV
 * [ ] Read all Part 2 Po3 cards from CSV
 * [ ] Read all Part 2 Magnificus cards from CSV
 * [x] Display Trigger text
 * [x] Display helper text on cards with only 1 sigil
 * [ ] JSON definitions for all Sigils
 * [ ] Use Sigil symbols instead of placeholders
 * [ ] Use Blood symbols for blood costs
 * [ ] Use Bone symbols for blood costs
 * [ ] Use Gem symbols for blood costs
 * [ ] Use Energy symbols for blood costs
 * [ ] Read Template data (colour, font, etc...) from JSON files
 * [x] Support Beast template
 * [ ] Support Crypt template
 * [ ] Support Tech template
 * [ ] Support Magic template

# Attribution
Art assets provided by:
 * [Beverwitch](https://twitter.com/baublebeverage)

With thanks to [Daniel Mullins](https://twitter.com/DMullinsGames) for creating Inscryption
