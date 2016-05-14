import storage
import nomadlist
import wikivoyage

def build(cities=None):
    index_guides(cities or index_cities())
    return True
    
def index_cities():
    cities = nomadlist.list_cities()
    storage.upsert_cities(cities)
    return cities
    
def index_guides(cities):
    city_docs = map(build_guide, cities)
    storage.upsert_cities(city_docs)
    return True
    
def build_guide(city):
    guide = wikivoyage.find_city(city['name'])
    return dict(city.items() + guide.items())
    