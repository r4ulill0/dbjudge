class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "singleton_instance"):
            cls.singleton_instance = super().__call__(*args, **kwargs)
        return cls.singleton_instance
