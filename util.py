import os, re
import logging, unittest
import yaml
from functools import wraps

config = {}
def load_yaml(path):
    logging.info('Reading yaml from <{0}>'.format(path))
    with open(path) as file:
        raw_yaml = file.read()
    return yaml.load(raw_yaml)

def load_db_config(db_type):
    if db_type == 'couchdb':
        env_url = os.environ.get('CLOUDANT_URL',None)
        logging.debug('loaded cloudant url is <{0}>'.format(env_url))
        if not env_url: return {'server':'http://127.0.0.1:5984'}
        
        parsed = re.search(r'https://(.*):(.*)@(.*)', env_url)
        config = {
                'server': 'https://'+parsed.group(3),
                'username': parsed.group(1),
                'password': parsed.group(2)
            }
        logging.debug('parsed cloudant config is <{0}>'.format(config))
        return config
    
def load_config():
    global config
    if not config:
        path = os.path.join(os.getcwd(), 'config.yaml')
        config = load_yaml(path)
    return config
    
def iter_txt(file_name):
    path = os.path.join(os.getcwd(),file_name)
    logging.info('Reading txt from <{0}>'.format(path))
    with open(path) as file:
        for line in file:
            try:
                yield line.decode('utf-8')
            except:
                yield line
    
def write_line(file_name, line):
    path = os.path.join(os.getcwd(),file_name)
    with open(path, 'a') as file:
        file.write('\n'+line)
        
def cached(cache, timeout=60 ** 2, ignore_first_arg=False):
    def decorator(func):
        @wraps(func)
        def cached_func(*args, **kwargs):
            str_args = str(args) if not ignore_first_arg else str(args[1:])
            keys = [func.__name__, str_args, str(kwargs.values())]
            cache_key = ';'.join(keys)
            cached = cache.get(cache_key)
            if cached: return cached
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            return result
        return cached_func
    return decorator
    
class UtilTests(unittest.TestCase):
    def test_load_yaml(self):
        test_var = 'variable'
        test_value = 'value'
        config = load_yaml('test.yaml')
        self.assertIn(test_var, config)
        self.assertEqual(config[test_var], test_value)
    
    def test_cached(self):
        from werkzeug.contrib.cache import SimpleCache
        cache = SimpleCache()
        func = lambda : True
        cached_func = cached(cache)(func)
        
        self.assertTrue(cached_func())
        func = lambda : False
        self.assertTrue(cached_func())
        
    def test_cached_ignore_first_arg(self):
        from werkzeug.contrib.cache import SimpleCache
        cache = SimpleCache()
        func = lambda x: x or False
        cached_func = cached(cache, ignore_first_arg=True)(func)
        
        self.assertTrue(cached_func(True))
        self.assertTrue(cached_func(False))
        
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilTests))
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())