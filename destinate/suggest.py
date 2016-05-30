import storage
import query_builder
import nlp

def from_city(city_name, **options):
    seed = storage.search_cities(
        query_builder.build_from_name(city_name),
        fields=['guide','cid','name','weather']).next()
    print 'found', seed['name'].encode('utf8'), seed['cid']
    return from_guide(
        nlp.summarize(seed['guide']),
        weather=seed['weather'],
        ignore_cid=seed['cid'],
        **options
        )

def from_guide(guide, **options):
    paging_options = {p:options.pop(p) for p in storage.PAGING_OPTIONS if p in options}
    query = query_builder.build_from_guide(guide, **options)
    return storage.search_cities(query, **paging_options)
