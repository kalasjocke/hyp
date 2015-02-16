from collections import defaultdict

class Collector(object):

    def __init__(self):
        self.linked = defaultdict(dict)
        self.links = defaultdict(set)

    def add_linked(self, type, id, resource):
        # Added to a dict to strip duplicates and sort results.
        self.linked[type][id] = resource

    def include_link(self, responder, key):
        # Flag each entry as they are used, final structure will
        # be built at the end.
        self.links[responder].add(key)

    def get_linked_dict(self):
        # Convert the defaultdict(dict) structure to a dict(list) structure
        return dict([(k, list(items.values())) for k, items in self.linked.items()])

    def get_links_dict(self):
        # Build the links structure for the links that have been used
        rv = {}

        for responder, keys in self.links.items():
            for key in keys:
                link = responder.LINKS[key]
                association = "%s.%s" % (responder.TYPE, key)

                rv[association] = {'type': link['responder'].TYPE}
                if 'href' in link:
                    rv[association]['href'] = link['href']

        return rv
