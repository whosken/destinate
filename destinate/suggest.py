import storage
import query_builder
import nlp

def from_cities(*names, **options):
    seeds = filter(None,map(find_city_by_name, names))
    guide = nlp.summarize(
        '\n'.join(s['guide'] for s in seeds),
        max_sentence_count=5)
    options['weathers'] = options.get('weathers') or [s['weather'] for s in seeds]
    options['ignore_cids'] = options.get('ignore_cids',[]) + [s['cid'] for s in seeds]
    return from_guide(guide, **options)

def from_guide(guide, **options):
    paging_options = {p:options.pop(p) for p in storage.PAGING_OPTIONS if p in options}
    query = query_builder.build_from_guide(guide, **options)
    return storage.search_cities(query, **paging_options)

def find_city_by_name(name):
    try:
        city = storage.search_cities(
            query_builder.build_from_name(name),
            fields=['guide','cid','name','weather'])[0]
    except IndexError:
        return
    print 'found', city['name'].encode('utf8'), city['cid']
    return city
    