import inspect


def param(prmhlpr_multi_key_mode_: bool = False, **kwargs):
    # Get the caller's frame and function name
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name

    # Retrieve argument names and current values from the caller
    args, _, _, values = inspect.getargvalues(caller_frame)

    # Determine whether the caller is a class method or a regular function
    if self := values.get("self"):
        class_ = self.__class__
        func = getattr(class_, caller_name, None)
        caller_signatures = inspect.signature(func)
    else:
        # Try to find the function in local or global scope
        func = caller_frame.f_locals.get(caller_name, None)
        if not func:
            func = caller_frame.f_globals.get(caller_name, None)
        caller_signatures = inspect.signature(func)

    # Get parameter metadata from the function signature
    caller_signatures = caller_signatures.parameters

    previous_function_args = {}
    for arg in args:
        if arg == "self":
            continue
        signature = caller_signatures[arg]
        annotation = signature.annotation
        value = values[arg]
        if value is None:
            continue

        # If the parameter has no type annotation
        if annotation == inspect._empty:
            default = signature.default
            if default != inspect._empty:
                # Use the type of the default value to cast current value
                default = type(default)
                if default is not type(None):
                    previous_function_args[arg] = default(value)
                else:
                    previous_function_args[arg] = value
            else:
                previous_function_args[arg] = value
        else:
            # Convert value according to type annotation (safe fallback)
            try:
                previous_function_args[arg] = annotation(value)
            except Exception:
                previous_function_args[arg] = value

    # Merge with any explicitly passed keyword arguments
    previous_function_args.update(kwargs)

    # Added logic for __ph_multi_key_mode
    if prmhlpr_multi_key_mode_:
        result = []
        for key, val in previous_function_args.items():
            # If the value is a list or tuple, expand into multiple (key, value) pairs
            if isinstance(val, (list, tuple)):
                result.extend((key, item) for item in val)
            else:
                result.append((key, val))
        return result

    # Default behavior: return dict
    return previous_function_args
