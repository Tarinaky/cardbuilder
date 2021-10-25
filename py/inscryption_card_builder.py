import csv
import json
import re
import itertools
import pygame.image
import pygame.font

import card
import sigils

class InscryptionCardBuilder(object):
    def __init__(self, resources, inputfile, **args):
        if not pygame.font.get_init():
            pygame.font.init()

        self._resources = resources
        self._inputfile = inputfile


        with open(self._resources.joinpath('sigils.json')) as sigil_file:
            self._sigil_list = sigils.SigilList(json.load(sigil_file))


    def generate_card(self, row):
        data = card.from_csv_row(row)
        print("DEBUG: Generating %s" % data)
        name_font = pygame.font.Font(self._resources.joinpath('font', 'GARBAGES.TTF'), 48)
        data.image = pygame.image.load(self._resources.joinpath('border', data.template).with_suffix(".png"))
        help_font = pygame.font.Font(self._resources.joinpath('font', 'GARBAGES.TTF'),16)
        extra_font = pygame.font.Font(self._resources.joinpath('font', 'GARBAGES.TTF'),18)

        (NAME_WIDTH, NAME_HEIGHT) = (240, 100)
        NAME_ASPECT_RATIO = NAME_WIDTH/NAME_HEIGHT
        card_name_surface = name_font.render(data.name, True, (0,0,0))
        print("DEBUG: Text width %s" % card_name_surface.get_width())
        if card_name_surface.get_width() > NAME_WIDTH:
            card_name_surface = pygame.transform.smoothscale(
                card_name_surface, 
                (
                    NAME_WIDTH,
                    NAME_WIDTH/card_name_surface.get_width()*card_name_surface.get_height()
                )
            )

        # card_name_surface = pygame.transform.smoothscale(card_name_surface, (NAME_WIDTH,card_name_surface.get_height()/card_name_surface.get_width()*NAME_HEIGHT))
        data.image.blit(card_name_surface, (card.WIDTH/2-card_name_surface.get_width()/2,50-card_name_surface.get_height()/2))

        number_font = pygame.font.Font(self._resources.joinpath('font', 'GARBAGES.TTF'), 96)
        POWER_X, POWER_Y = (26, 260)
        card_power_surface = number_font.render(str(data.power), True, (0,0,0))
        #card_power_surface = pygame.transform.smoothscale(card_power_surface, (40,80))
        data.image.blit(card_power_surface, (POWER_X, POWER_Y))

        TOUGH_X, TOUGH_Y = (250, 260)
        card_power_surface = number_font.render(str(data.tough), True, (0,0,0))
        #card_power_surface = pygame.transform.smoothscale(card_power_surface, (40,80))
        data.image.blit(card_power_surface, (TOUGH_X, TOUGH_Y))

        SIGIL_LAYOUTS = [
                [(160, 300)], # One sigil
                [(120, 300), (200, 300)], # Two sigils
                #[(140,290), (180,290), (160, 330)], # Three sigils
                #[(140,290), (180,290), (140, 330), (180, 330)] # Four sigils
        ]
        extra_text = None
        forced_description = None

        for (sigil,i) in zip(data.sigils, itertools.count(0)):
            if self._sigil_list.get(sigil).force == True:
                forced_description = sigil
            print("DEBUG: sigil %s" % sigil)
            print("DEBUG: len(data.sigils) = %d" % len(data.sigils))
            sigil_surface = number_font.render(self._sigil_list.get(sigil).initials, True, (0,0,0))
            (sigil_x, sigil_y) = SIGIL_LAYOUTS[len(data.sigils)-1][i]
            if len(data.sigils) > 1:
                sigil_surface = pygame.transform.smoothscale(sigil_surface, (sigil_surface.get_width()*3/5, sigil_surface.get_height()*3/5))
            data.image.blit(sigil_surface, (sigil_x-sigil_surface.get_width()/2, sigil_y-sigil_surface.get_height()/2))
            if len(sigil.split('(')) > 1:
                extra_text = "%s %s" % (self._sigil_list.get(sigil).verb, re.split('[\(\)]', sigil)[1])

        if data.trigger is not None:
            extra_text = data.trigger
        HELP_LOCATION_X, HELP_LOCATION_Y = (190, 345)
        if extra_text is not None:
            for (line, i) in zip(extra_text.split('|'), itertools.count(0)):
                text_surface = extra_font.render(line, True, (0,0,0))
                data.image.blit(text_surface, (HELP_LOCATION_X-text_surface.get_width()/2, HELP_LOCATION_Y-text_surface.get_height()/2+text_surface.get_height()*i))
        elif len(data.sigils) == 1:
            for (line,i) in zip(self._sigil_list.get(data.sigils[0]).helptext, itertools.count(0)):
                help_surface = help_font.render(line, True, (255/6, 255/6, 255/6))
                data.image.blit(help_surface, (HELP_LOCATION_X-help_surface.get_width()/2, HELP_LOCATION_Y-help_surface.get_height()/2+help_surface.get_height()*i))
        elif forced_description is not None:
            for (line,i) in zip(self._sigil_list.get(forced_description).helptext, itertools.count(0)):
                help_surface = help_font.render(line, True, (255/6, 255/6, 255/6))
                data.image.blit(help_surface, (HELP_LOCATION_X-help_surface.get_width()/2, HELP_LOCATION_Y-help_surface.get_height()/2+help_surface.get_height()*i))


        return data

    def write_card(self, card, outdir):
        print("DEBUG: Writing %s" % card)
        pygame.image.save(card.image, outdir.joinpath(card.name).with_suffix(".png"))

    def write(self, outdir, args):
        """
        Write completed cards out to a directory
        """
        outdir.mkdir(parents=True, exist_ok=True)
        with open(self._inputfile) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                card = self.generate_card(row)
                if args.card is None or args.card == card.name:
                    self.write_card(card, outdir)
                    if args.card is not None:
                        return
        
