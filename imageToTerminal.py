from PIL import Image


## Constants
IMG_PATH = "img.jpg"
PIXELS_ASCII = "@%#*+=-:. "
RESULT_IMG_PATH = 'result.png'

#
MAX_WIDTH = 150
MAX_HEIGHT = 200

##
def resizeIfExceedRange(max_width, max_height, img):
    if img.width > max_width or img.height > max_height:
        return img.resize((max_width, max_height))

def checkForTransparency(img):
    data = img.getdata()
    has_transparency = any(d[3] == 0 for d in data)
    return data

def getGrayscalledImage(img_path):
    # Opening the image
    img = Image.open(img_path).convert('RGBA')
    img = resizeIfExceedRange(MAX_WIDTH, MAX_HEIGHT, img)

    ##
    has_transparency = checkForTransparency(img)
    if has_transparency:
        r,g,b,a = img.split()
        gray = Image.merge("RGB", (r,g,b)).convert('L')
        result = Image.merge('LA', (gray, a))
    else:
        result = img.convert('LA')
    
    # saving
    result.save(RESULT_IMG_PATH)

def getImagePixelsFromGray(img):
    return list(img.getdata())

def getPixelIndexFromGrayscale(value, p_ascii_len):
    return int((value * (p_ascii_len - 1))/254)

def makeImage():
    image = "" # render Image

    img = Image.open(RESULT_IMG_PATH)
    WIDTH = img.width
    HEIGHT = img.height

    pixels = getImagePixelsFromGray(img)

    ## Making the Image
    for pixel in pixels:
        index = getPixelIndexFromGrayscale(pixel[0], len(PIXELS_ASCII))
        if pixel[1] == 0:
            image += " "
        else:   
            image += PIXELS_ASCII[index]
    return image, WIDTH, HEIGHT

##
def render_row(image, width, height):
    index = -1
    row = ""
    for y in range(height):
        for x in range(width):
            index += 1 
            row += image[index]
        print(row) # printing each row
        row = "" # reseting row

def render(img_path):
    # steps
    getGrayscalledImage(img_path)
    image, WIDTH, HEIGHT = makeImage()
    render_row(image, WIDTH, HEIGHT)


render(IMG_PATH)

