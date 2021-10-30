import json
import itertools
import re

import pygame.image
import pygame.font


class Template(object):
    def __init__(self, resources_path, template_path):
        with open(template_path) as template_file:
            template_json = json.load(template_file)
        
        self.border = pygame.image.load(
            template_path.parents[0].joinpath(
                template_json["border"]
            )
        )

        self.width = self.border.get_width()
        self.height = self.border.get_height()

        self.font = resources_path.joinpath('font', template_json["font"])
        self.cost_loc = template_json["cost_loc"]
        self.name_box = template_json["name_box"]
        self.name_loc = template_json["name_location"]
        self.power_loc = template_json["power_location"]
        self.toughness_loc = template_json["toughness_location"]
        self.sigil_layouts = template_json["sigil_layouts"]
        self.helptext_loc = template_json["helptext_location"]
        self.text_color = template_json["text_color"]
        self.helptext_color = template_json["helptext_color"]
    
    def get_border(self):
        return self.border.copy()

    def render_card_name(self, surface, name):
        font = pygame.font.Font(self.font, 48)
        (width,height) = self.name_box
        aspect_ratio = width/height
        name_surface = font.render(name, True, self.text_color)
        if name_surface.get_width() > width:
            name_surface = pygame.transform.smoothscale(
                name_surface,
                (
                    width,
                    width/name_surface.get_width()*name_surface.get_height()
                )
            )
        
        surface.blit(name_surface, (
            self.name_loc[0]-name_surface.get_width()/2,
            self.name_loc[1]-name_surface.get_height()/2
            )
        )

    def render_cost(self, surface, cost):
        data = cost.split(' ')
        print("DEBUG: %s" % data)
        if data[0].lower() == "blood":
            # Placeholder for blood symbol
            cost_surface = pygame.font.Font(self.font, 48).render(data[1], True, (120,0,0))
            surface.blit(cost_surface, self.cost_loc)
        elif data[0].lower() == "bone":
            # Placeholder for bone symbol
            cost_surface = pygame.font.Font(self.font, 48).render(data[1], True, (255,255,255))
            surface.blit(cost_surface, self.cost_loc)
        elif data[0].lower() == "energy":
            # Placeholder for energy symbol
            cost_surface = pygame.font.Font(self.font, 48).render(data[1], True, (255,255,255))
            surface.blit(cost_surface, self.cost_loc)
        elif data[0].lower() == "gem":
            # Placeholder for gem symbols
            cost = ''.join([word[0] for word in data[1:]])
            cost_surface = pygame.font.Font(self.font, 48).render(cost, True,(0,0,120))
            surface.blit(cost_surface, self.cost_loc)
            print("DEBUG: %s" % cost)

    def render_stats(self, surface, power, tough):
        font = pygame.font.Font(self.font, 96)
        power_surface = font.render(str(power), True, self.text_color)
        surface.blit(power_surface, self.power_loc)
        tough_surface = font.render(str(tough), True, self.text_color)
        surface.blit(tough_surface, self.toughness_loc)

    def render_sigils(self, surface, sigil_list, sigils):
        font = pygame.font.Font(self.font, 96)
        for (sigil, i) in zip(sigils, itertools.count(0)):
            # Placeholder for sigil symbol
            sigil_surface = font.render(sigil_list.get(sigil).initials, True, self.text_color)
            (x,y) = self.sigil_layouts[len(sigils)-1][i]
            if len(sigils) > 1:
                sigil_surface = pygame.transform.smoothscale(
                    sigil_surface,
                    (sigil_surface.get_width()*3/5, sigil_surface.get_height()*3/5)
                )
            surface.blit(sigil_surface, (x-sigil_surface.get_width()/2, y-sigil_surface.get_height()/2))

    def _render_multiline(self, surface, font, loc, color, multiline):
        if not isinstance(multiline, list):
            multiline = multiline.split('|')
        for (line, i) in zip(multiline, itertools.count(0)):
            text_surface = font.render(line, True, color)
            surface.blit(text_surface,(
                    loc[0]-text_surface.get_width()/2,
                    loc[1] + text_surface.get_height()*i - text_surface.get_height()/2
            ))

    def render_text(self, surface, trigger, sigil_list, sigils):
        if trigger is not None:
            font = pygame.font.Font(self.font, 18)
            self._render_multiline(surface, font, self.helptext_loc, self.text_color, trigger)
        elif len([sigil for sigil in sigils if len(sigil.split('(')) > 1]) > 0:
            sigil = [sigil for sigil in sigils if len(sigil.split('('))>1][0]
            font = pygame.font.Font(self.font, 18)
            text = "%s %s" % (sigil_list.get(sigil).verb, re.split('[\(\)]', sigil)[1])
            self._render_multiline(surface, font, self.helptext_loc, self.text_color, text)
        elif len(sigils) == 1:
            font = pygame.font.Font(self.font, 16)
            self._render_multiline(surface, font, self.helptext_loc, self.helptext_color, sigil_list.get(sigils[0]).helptext)
        else:
            forced = [sigil for sigil in sigils if sigil_list.get(sigil).force]
            if len(forced) > 0:
                font = pygame.font.Font(self.font, 16)
                self._render_multiline(surface,font,self.helptext_loc, self.helptext_color, sigil_list.get(forced[0]).helptext)
            




