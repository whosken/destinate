import storage
import query_builder

def suggest_from_city(city_name, **options):
    seed = storage.search_cities(
        query_builder.build_from_name(city_name),
        fields=['guide','cid','name']).next()
    print 'found', seed['name'].encode('utf8'), seed['cid']
    query = query_builder.build_from_guide(seed['guide'], **options)
    return [c for c in storage.search_cities(query) if c['cid'] != seed['cid']]

def suggest_from_collaborative_filter(user):
    pass
