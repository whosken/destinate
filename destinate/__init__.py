import storage
import query_builder
import nlp

def suggest_from_city(city_name, **options):
    seed = storage.search_cities(
        query_builder.build_from_name(city_name),
        fields=['guide','cid','name','weather']).next()
    print 'found', seed['name'].encode('utf8'), seed['cid']
    return suggest_from_summary(nlp.summarize(
        seed['guide']),
        ignore_cid=seed['cid'],
        weather=seed['weather'],
        **options
        )

def suggest_from_guide(guide, ignore_cid=None, **options):
    query = query_builder.build_from_guide(guide, **options)
    valid_cid = lambda c: not ignore_cid or c['cid'] != ignore_cid
    return filter(valid_cid, storage.search_cities(query))
