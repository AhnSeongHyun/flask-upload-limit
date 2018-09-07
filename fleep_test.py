
from utils import get_python_version
py_version = get_python_version()
if py_version >=31:
    import fleep
else:
    import fleep27 as fleep

with open("test.jpg", "rb") as file:
    info = fleep.get(file.read(128))
    print(info.type)  # prints ['raster-image']
    print(info.extension)  # prints ['png']
    print(info.mime)  # prints ['image/png']

    print(info.type_matches("raster-image"))  # prints True
    print(info.extension_matches("gif"))  # prints False
    print(info.mime_matches("image/png"))  # prints True
    print(mg.supported_types())
    print(mg.supported_extensions())
    print(mg.supported_mimes())
