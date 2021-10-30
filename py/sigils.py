


class SigilList(object):
    def __init__(self, json):
        self._sigil_list = {}
        for element in json:
            sigil = sigil_from_json(element)
            print("DEBUG: %s" % sigil)
            self._sigil_list[sigil.name] = sigil

        print("DEBUG: %d sigils loaded" % len(self._sigil_list))

    def get(self, name):
        return self._sigil_list[name.split('(')[0].strip().lower()]


class Sigil(object):
    def __init__(self,name,initials,helptext,verb=None,force=False):
        self.name = name.lower()
        self.initials = initials
        self.helptext = helptext
        self.verb = verb
        self.force = force

    def __str__(self):
        return self.name


def sigil_from_json(json):
    return Sigil(
        name=json["name"],
        initials=json["initials"],
        helptext=json.get("help",None),
        verb=json.get("verb",None),
        force=json.get("force",False)
    )
