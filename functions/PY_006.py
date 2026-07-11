def setExecutorEnv(self, key=None, value=None, pairs=None):
        """Set an environment variable to be passed to executors."""
        if (key is not None and pairs is not None) or (key is None and pairs is None):
            raise Exception("Either pass one key-value pair or a list of pairs")
        elif key is not None:
            self.set("spark.executorEnv." + key, value)
        elif pairs is not None:
            for (k, v) in pairs:
                self.set("spark.executorEnv." + k, v)
        return self