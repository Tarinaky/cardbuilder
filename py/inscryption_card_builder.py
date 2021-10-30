import csv
import json
import re
import itertools
import pygame.image
import pygame.font

import card
import sigils
import template


class InscryptionCardBuilder(object):
    def __init__(self, resources, inputfile, **args):
        if not pygame.font.get_init():
            pygame.font.init()

        self._resources = resources
        self._inputfile = inputfile

        with open(self._resources.joinpath("sigils.json")) as sigil_file:
            self._sigil_list = sigils.SigilList(json.load(sigil_file))

    def generate_card(self, row):
        data = card.from_csv_row(row)
        print("DEBUG: Generating %s" % data)

        card_template = template.Template(
            self._resources,
            self._resources.joinpath("border", data.template).with_suffix(".json"),
        )
        data.image = card_template.get_border()
        card_template.render_card_name(data.image, data.name)

        card_template.render_cost(data.image, data.cost)

        card_template.render_stats(data.image, data.power, data.tough)

        card_template.render_sigils(data.image, self._sigil_list, data.sigils)

        card_template.render_text(
            data.image, data.trigger, self._sigil_list, data.sigils
        )

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
                try:
                    card = self.generate_card(row)
                    if args.card is None or args.card == card.name:
                        self.write_card(card, outdir)
                        if args.card is not None:
                            return
                except Exception as e:
                    print(e)
