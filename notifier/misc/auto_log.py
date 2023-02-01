from functools import wraps


def log_save_update(logger_call: callable = None):
    """
    Decorator for .save method of django model to logging changes
    """

    def decorator(func: callable):
        @wraps(func)
        def decorated_function(self, *args, **kwargs):
            action = "updated" if self.id else "created"
            result = func(self, *args, **kwargs)
            logger_call(f"{self.__class__.__name__} is {action}: {self}")
            return result
        return decorated_function

    return decorator


def log_delete(logger_call: callable = None):
    """
    Decorator for .delete method of django model to logging trashing
    """
    def decorator(func: callable):
        @wraps(func)
        def decorated_function(self, *args, **kwargs):
            action = "deleted"
            self_str = str(self)
            result = func(self, *args, **kwargs)
            logger_call(f"{self.__class__.__name__} is {action}: {self_str}")
            return result
        return decorated_function

    return decorator
