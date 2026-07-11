def get(self, key, defaultValue=None):
        """Get the configured value for some key, or return a default otherwise."""
        if defaultValue is None:   # Py4J doesn't call the right get() if we pass None
            if self._jconf is not None:
                if not self._jconf.contains(key):
                    return None
                return self._jconf.get(key)
            else:
                if key not in self._conf:
                    return None
                return self._conf[key]
        else:
            if self._jconf is not None:
                return self._jconf.get(key, defaultValue)
            else:
                return self._conf.get(key, defaultValue)