class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_singleton_instance"):
            cls._singleton_instance = super().__call__(*args, **kwargs)
        return cls._singleton_instance
