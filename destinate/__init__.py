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
        weather=seed['weather'],
        ignore_cid=seed['cid'],
        **options
        )

def suggest_from_guide(guide, **options):
    query = query_builder.build_from_guide(guide, **options)
    return storage.search_cities(query)
