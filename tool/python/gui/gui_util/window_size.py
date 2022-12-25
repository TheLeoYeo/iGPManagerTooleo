from configparser import ConfigParser

from util.utils import join


SIZE_FILE_DIR = join("gui","gui_util","win_size.ini", uplevel=2)

 
def update_size(height:int, width:int):
    '''Takes height and width and saves these to a config file'''
    
    config = ConfigParser()
    config.read(SIZE_FILE_DIR)
    settings = config["SETTINGS"]
    settings["height"] = height.__str__()
    settings["width"] = width.__str__()
    
    with open(SIZE_FILE_DIR, "w") as size_file:
        config.write(size_file)


def read_size():
    config = ConfigParser()
    config.read(SIZE_FILE_DIR)
    try:
        settings = config["SETTINGS"]
        width = int(settings["width"])
        height = int(settings["height"])
        return {"height":height,"width":width}
    except:
        raise ValueError("Error reading Width and/or Height from file")