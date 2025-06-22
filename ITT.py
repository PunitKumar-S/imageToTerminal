from PIL import Image


class ImageToASCII:
    def __init__(self, img_path, result_path="result.png", max_width=150, max_height=200):
        self.img_path = img_path
        self.result_path = result_path
        self.max_width = max_width
        self.max_height = max_height
        self.pixel_ascii = "@%#*+=-:. "  # Dark -> Light

        self.image = None  # PIL Image
        self.gray_image = None
        self.width = 0
        self.height = 0

    def resize_if_needed(self, img):
        if img.width > self.max_width or img.height > self.max_height:
            return img.resize((self.max_width, self.max_height))
        return img

    def has_transparency(self, img):
        return any(d[3] == 0 for d in img.getdata())

    def convert_to_grayscale(self):
        img = Image.open(self.img_path).convert('RGBA')
        img = self.resize_if_needed(img)

        if self.has_transparency(img):
            r, g, b, a = img.split()
            gray = Image.merge("RGB", (r, g, b)).convert('L')
            result = Image.merge('LA', (gray, a))
        else:
            result = img.convert('LA')

        result.save(self.result_path)
        self.gray_image = result
        self.width, self.height = result.size

    def grayscale_to_ascii_index(self, gray_value):
        return int((gray_value * (len(self.pixel_ascii) - 1)) / 254)

    def get_ascii_image(self):
        if self.gray_image is None:
            raise RuntimeError("Grayscale image not prepared")

        ascii_str = ""
        pixels = list(self.gray_image.getdata())

        for pixel in pixels:
            gray, alpha = pixel
            if alpha == 0:
                ascii_str += " "
            else:
                ascii_str += self.pixel_ascii[self.grayscale_to_ascii_index(gray)]
        return ascii_str

    def render_to_terminal(self):
        self.convert_to_grayscale()
        ascii_data = self.get_ascii_image()

        index = 0
        for y in range(self.height):
            line = ascii_data[index:index + self.width]
            print(line)
            index += self.width

