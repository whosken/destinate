import storage
import nomadlist
import wikivoyage

def build(cities=None):
    if not cities:
        cities = nomadlist.list_cities()
        storage.store_cities(cities)
    city_docs = map(build_guide, cities)
    storage.index_cities(city_docs)
    return True
    
def build_guide(city):
    guide = wikivoyage.find_city(city['name'])
    return dict(city.items() + guide.items())
    