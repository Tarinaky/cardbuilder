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

# Attribution
Art assets provided by:
 * [Beverwitch](https://twitter.com/baublebeverage)

With thanks to [Daniel Mullins](https://twitter.com/DMullinsGames) for creating Inscryption
