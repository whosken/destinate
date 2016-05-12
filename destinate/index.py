import storage
import nomadlist
import wikivoyage

def build():
    cities = nomadlist.list_cities()
    storage.store_cities(cities)
    for city in cities:
        wiki = wikivoyage.find_city(city['name'])
        guide = create_guide(city, wiki)
        storage.store_city(guide)

def create_guide(city, wiki=None):
    pass
