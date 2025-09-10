def is_allowed_target(target):
    from config import lab_scope
    return target in lab_scope['allowed_targets']

def require_scope(func):
    def wrapper(*args, **kwargs):
        target = kwargs.get('target') or (args[0] if args else None)
        if not is_allowed_target(target):
            raise PermissionError("Target not allowed")
        return func(*args, **kwargs)
    return wrapper
