from pathlib import Path

from . import config

class CacheHandler:

    def __init__(self):
        self.rootDir = Path(__file__).parent.absolute()
        self.cacheDir = '{root}/cache'.format(root=self.rootDir)

    def getCache(self, key):
        if key in config.CACHE: return config.CACHE[key]

        keyPath = '{cache}/{key}.txt'.format(cache=self.cacheDir, key=key)

        try:
            with open(keyPath, 'r') as f:
                value = f.readlines()[0]
            
            config.CACHE[key] = value
            return value

        except IOError:
            return None
    
    def setCache(self, key, value):
        keyPath = '{cache}/{key}.txt'.format(cache=self.cacheDir, key=key)

        try:
            with open(keyPath, 'w+') as f:
                f.write(value)
            
            config.CACHE[key] = value
            return value

        except IOError:
            return None