def build_from_name(city_name):
    return {
        'match':{
            'name':{
                'query':city_name,
                'operator':'and',
                'fuzziness':'AUTO'
                }
            }
        }
    
def build_from_summary(summary, regions=None):
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
    