import storage
import nlp

def suggest_from_city(city_name, **options):
    seed = get_city_guide(city_name)
    query = build_query_from_guide(seed['guide'], **options)
    return [c for c in storage.search_cities(query) if c['cid'] != seed['cid']]
    
def get_city_guide(city_name):
    return storage.search_cities(
        build_name_query(city_name),
        fields=['guide','cid']).next()
    
def build_name_query(city_name):
    return {
        'match':{
            'name':{
                'query':city_name,
                'operator':'and'
                }
            }
        }
    
def build_query_from_guide(guide, regions=None):
    summary = nlp.summarize(guide, max_sentence_count=30)
    query = {
        'bool':{
            'must':[{
                'match':{
                    'guide':{
                        'query':summary,
                        'cutoff_frequency':0.005
                        }
                    }
                }
            ]}
        }
    if regions:
        if isinstance(regions, (unicode,str)):
            regions = [regions]
        query['bool']['must'].append({
            'match':{
                'regions':{
                    'query':regions,
                    'operator':'or'
                    }
                }
            })
    return query

def suggest_from_collaborative_filter(user):
    pass
