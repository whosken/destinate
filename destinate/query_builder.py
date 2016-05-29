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
    
def build_from_guide(guide, regions=None, weather=None, months=None):
    must = [{
            'match':{
                'guide':{
                    'query':guide,
                    'cutoff_frequency':0.005
                    }
                }
            }
        ]
    should = []
    if regions:
        if isinstance(regions, (unicode,str)):
            regions = [regions]
        must.append({
            'match':{
                'regions':{
                    'query':regions,
                    'operator':'or'
                    }
                }
            })
    if weather:
        should += [{'term':{'weather.{}'.format(k):v}} for k,v in weather.items()]
    if months:
        should.append({'terms':{'months_ideal':months}})
    query = {'bool':{'must':must}}
    if should:
        query['bool']['should'] = should
    return query
    