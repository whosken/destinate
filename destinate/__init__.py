import storage
import query_builder
import nlp

def suggest_from_city(city_name, **options):
    seed = storage.search_cities(
        query_builder.build_from_name(city_name),
        fields=['guide','cid','name']).next()
    print 'found', seed['name'].encode('utf8'), seed['cid']
    return suggest_from_summary(nlp.summarize(seed['guide']), seed['cid'])

def suggest_from_summary(summary, ignore_cid=None, **options):
    query = query_builder.build_from_summary(summary, **options)
    valid_cid = lambda c: not ignore_cid or c['cid'] != ignore_cid
    return filter(valid_cid, storage.search_cities(query))
