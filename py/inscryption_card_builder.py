import csv
import pygame.image
import pygame.font

import card

class InscryptionCardBuilder(object):
    def __init__(self, resources, inputfile):
        if not pygame.font.get_init():
            pygame.font.init()

        self._resources = resources
        self._inputfile = inputfile

        self._font = pygame.font.Font(self._resources.joinpath('font', 'GARBAGES.TTF'), 128)

    def generate_card(self, row):
        data = card.from_csv_row(row)
        print("DEBUG: Generating %s" % data)
        data.image = pygame.image.load(self._resources.joinpath('border', data.template).with_suffix(".png"))

        (NAME_WIDTH, NAME_HEIGHT) = (240, 100)
        NAME_ASPECT_RATIO = NAME_WIDTH/NAME_HEIGHT
        card_name_surface = self._font.render(data.name, True, (0,0,0))
        card_name_surface = pygame.transform.smoothscale(card_name_surface, (NAME_WIDTH,card_name_surface.get_height()/card_name_surface.get_width()*NAME_HEIGHT))
        data.image.blit(card_name_surface, (card.WIDTH/2-card_name_surface.get_width()/2,15))

        POWER_X, POWER_Y = (26, 260)
        card_power_surface = self._font.render(str(data.power), True, (0,0,0))
        card_power_surface = pygame.transform.smoothscale(card_power_surface, (40,80))
        data.image.blit(card_power_surface, (POWER_X, POWER_Y))

        TOUGH_X, TOUGH_Y = (250, 260)
        card_power_surface = self._font.render(str(data.tough), True, (0,0,0))
        card_power_surface = pygame.transform.smoothscale(card_power_surface, (40,80))
        data.image.blit(card_power_surface, (TOUGH_X, TOUGH_Y))



        return data

    def write_card(self, card, outdir):
        print("DEBUG: Writing %s" % card)
        pygame.image.save(card.image, outdir.joinpath(card.name).with_suffix(".png"))

    def write(self, outdir):
        """
        Write completed cards out to a directory
        """
        outdir.mkdir(parents=True, exist_ok=True)
        with open(self._inputfile) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                card = self.generate_card(row)
                self.write_card(card, outdir)
        
