
WIDTH=321
HEIGHT=400

class Card(object):
    def __init__(self, name, template, cost, power, tough, sigils, trigger=None):
        self.name = name
        self.template = template
        self.cost = cost
        self.power = int(power)
        self.tough = int(tough)
        self.sigils = [a for a in sigils.split(',') if a != '']
        self.trigger = trigger
        self.image = None

    def __str__(self):
        return "%s (cost %s): %d/%d: %s)" % (
                self.name,
                self.cost if self.cost!="" else "free",
                self.power,
                self.tough,
                self.sigils if self.sigils!=[] else ["none"]
        )

def from_csv_row(row):
    if len(row) > 6:
        trigger = row[6]
        if trigger == "":
            trigger = None
    else:
        trigger = None
    return Card(
        name=row[0],
        template=row[1],
        cost=row[2],
        power=row[3],
        tough=row[4],
        sigils=row[5],
        trigger=trigger
    )

