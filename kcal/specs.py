from imagekit.specs import ImageSpec 
from imagekit import processors 

# now we define a display size resize processor
class ResizeKcal(processors.Resize):
    width = 360

# first we define our thumbnail resize processor 
class ResizeThumb(processors.Resize): 
    width = 100
    height = 75 
    crop = True

# now lets create an adjustment processor to enhance the image at small sizes 
class EnhanceThumb(processors.Adjustment): 
    contrast = 1.2 
    sharpness = 1.1 

# now we can define our thumbnail spec 
class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = True 
    processors = [ResizeThumb, EnhanceThumb] 

# now we can define our thumbnail spec 
class Kcal(ImageSpec): 
    access_as = 'kcal_image' 
    pre_cache = True 
    processors = [ResizeKcal] 

# and our display spec
class Display(ImageSpec):
    increment_count = True
    processors = [ResizeKcal]
