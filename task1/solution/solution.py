def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        var_names = func.__code__.co_varnames

        
        for i in range(len(args)):
            # is annotation for attribute exists
            required = annotations.get(var_names[i]) 
            real = type(args[i])
            if required and required != real:
                raise TypeError(f'Argument {var_names[i]} must be {required}, not {real}')
            
        res = func(*args, **kwargs)
        # is annotation for return exists
        if  (return_type :=  annotations.get('return')) and  type(res) != return_type: 
            raise TypeError(f'Return value must be {annotations["return"]}, not {type(res)}')
        
        
        return res
    return wrapper




