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
    
def build_from_guide(guide, regions=None, weathers=None, months=None, ignore_cids=None, ignore_name=None):
    must = [{
        'match':{'guide':{
            'query':guide,
            'cutoff_frequency':0.005
            }}
        }]
    should = []
    must_not = []
    if regions:
        if isinstance(regions, (unicode,str)):
            regions = [regions]
        must.append({
            'match':{'regions':{
                'query':regions,
                'operator':'or'
                }}
            })
    if weathers:
        if isinstance(weathers, dict):
            weathers = [weathers]
        should += list(yield_weather_conditions(*weathers))
    if months:
        should.append({'terms':{'months_ideal':months}})
    if ignore_cids:
        must_not.append({'terms':{'cid':ignore_cids}})
    if ignore_name:
        must_not.append(build_from_name(ignore_name))
        
    query = {'bool':{'must':must}}
    if should:
        query['bool']['should'] = should
    if must_not:
        query['bool']['must_not'] = must_not
    return query
    
def yield_weather_conditions(*weathers):
    temps = [w['temperature']['celsius'] for w in weathers if 'celsius' in w.get('temperature',{})]
    if temps:
        yield {'range':{'weather.temperature.celsius':{
            'gte':min(temps) - 3,
            'lte':max(temps) + 3
            }}}
    humidities = [w['humidity'] for w in weathers if 'humidity' in w]
    if humidities:
        yield {'range':{'weather.humidity':{
            'gte':min(humidities) - 0.1,
            'lte':max(humidities) + 0.1
            }}}
    patterns = [w['pattern'] for w in weathers if 'pattern' in w]
    if patterns:
        yield {'terms':{'weather.pattern':patterns}}
