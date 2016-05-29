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
    
def build_from_guide(guide, regions=None, weather=None, months=None, ignore_cid=None, ignore_name=None):
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
    must_not = []
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
    if ignore_cid:
        must_not.append({'term':{'cid':ignore_cid}})
    if ignore_name:
        must_not.append(build_from_name(ignore_name))
        
    query = {'bool':{'must':must}}
    if should:
        query['bool']['should'] = should
    if must_not:
        query['bool']['must_not'] = must_not
    return query
    