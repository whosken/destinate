import mwclient
import mwparserfromhell

HOST = 'en.wikivoyage.org'

def find_city(city_name):
    return fetch(city_name)

def fetch(page_name):
    page = site.Pages[page_name]
    retun {
        'guide': build_guide(page.text()),
        'images': format_image(page.images())
        }
        
def format_image(image):
    return {
        'url': image['url'],
        'height': image['height'],
        'width': image['width'],
        }
    
def build_guide(code):
    wikicode = mwparserfromhell.parse(code)
    wikicode = filter_sections(wikicode)
    return wikicode.strip_code()
    
should_ignore_sections = lambda h: h.lower() in ('get in', 'get around', 'go next', 'learn')
def filter_sections(code):
    try:
        invalid_sections = code.get_sections(
            levels=[1,2],
            matches=should_ignore_sections,
            include_lead=True,
            include_headings=True
            )
        for section in invalid_sections:
            code.remove(section)
    except IndexError:
        pass
    return code

class LazyClient(object):
    _site = False
    
    def __getattr__(self, name):
        if not LazyClient._site:
            LazyClient._site = mwclient.Site(HOST)
        return getattr(LazyClient._site, name)

site = LazyClient()
