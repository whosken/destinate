import os
import logging, unittest
import yaml

config = {}
def load_yaml(path):
    logging.info('Reading yaml from <{0}>'.format(path))
    with open(path) as file:
        raw_config = file.read()
    return yaml.load(raw_config)

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
            yield line.decode('utf-8')
    
def write_line(file_name, line):
    path = os.path.join(os.getcwd(),file_name)
    with open(path, 'a') as file:
        file.write('\n'+line)
    
class UtilTests(unittest.TestCase):
    def test_load_yaml(self):
        test_var = 'variable'
        test_value = 'value'
        config = load_yaml('test.yaml')
        self.assertIn(test_var, config)
        self.assertEqual(config[test_var], test_value)
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilTests))
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())