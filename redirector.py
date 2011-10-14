import logging, unittest

def build_travel_link(place_name):
    logging.info('Flight redirect to <{0}>'.format(place_name))
    return 'http://skyscanner.net/'
    
def build_info_link(place_name):
    logging.info('Info redirect for <{0}>'.format(place_name))
    return 'http://wikitravel.org/en/' + place_name

link_builders = {
        'travel':build_travel_link,
        'info':build_info_link
    }

def build_link(target, place_name):
    return link_builders[target](place_name)
    