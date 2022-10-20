from os import path


def join(*dirs, uplevel:int=1):
    new_path = path.join(par_dir(uplevel=uplevel), *dirs)
    return new_path


def par_dir(dir:str=__file__, uplevel:int=1):
    if uplevel <= 1:
        return path.dirname(dir)
    
    else:
        return path.dirname(par_dir(dir, uplevel - 1))