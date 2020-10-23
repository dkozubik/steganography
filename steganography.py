from PIL import Image


class ImageToImage:

    """Class for encoding and decoding images into/from larger images."""

    def __init__(self, host_image_file_name=None):
        """Constructor
        :param host_image_file_name: the name of the host image
        """
        self.host_image_file_name = host_image_file_name

    def open_host_image(self, host_image_file_name):
        """Method opens the host image file using PIL.Image.open()
        :param host_image_file_name:
        """
        return Image.open(host_image_file_name).convert("RGB")

    def encode_image(self, image_file_name, new_file_name):
        """Method encodes the "image_file_name" into the host image creating a
        new file "new_file_name"
        :param image_file_name: the filename of the encoded image
        :param new_file_name: the filename of the result image
        """
        im1 = self.open_host_image(self.host_image_file_name)
        im2 = Image.open(image_file_name).convert("RGB")
        if not self.is_fitting(im2):
            raise OverflowError("The image is too large to be stored in the "
                                "host image.")
        new_image = Image.new("RGB", im1.size)
        pixles_im2 = im2.load()
        all_pixels_im2 = []
        for i in range(im2.size[0]):
            for j in range(im2.size[1]):
                all_pixels_im2.append(self.int_to_binary(pixles_im2[i, j]))
        tmp1, tmp2, tmp3 = 0, 0, 0
        for i in range(im1.size[0]):
            for j in range(im1.size[1]):
                rgb = self.int_to_binary(im1.getpixel((i, j)))
                # Saving 1 bit on every 8 bits of <host_image>
                if tmp1 < len(all_pixels_im2):
                    rgb_final_0 = rgb[0][:7] + all_pixels_im2[tmp1][tmp2][tmp3]
                    tmp3 += 1
                    if tmp3 == 8:
                        tmp3 = 0
                        tmp2 += 1
                    if tmp2 == 3:
                        tmp2 = 0
                        tmp1 += 1

                    rgb_final_1 = rgb[1][:7] + all_pixels_im2[tmp1][tmp2][tmp3]
                    tmp3 += 1
                    if tmp3 == 8:
                        tmp3 = 0
                        tmp2 += 1
                    if tmp2 == 3:
                        tmp2 = 0
                        tmp1 += 1

                    rgb_final_2 = rgb[2][:7] + all_pixels_im2[tmp1][tmp2][tmp3]
                    tmp3 += 1
                    if tmp3 == 8:
                        tmp3 = 0
                        tmp2 += 1
                    if tmp2 == 3:
                        tmp2 = 0
                        tmp1 += 1

                    rgb_final_all = (rgb_final_0, rgb_final_1, rgb_final_2)
                    new_image.putpixel((i, j),
                                       self.binary_to_int(rgb_final_all))

                else:
                    new_image.putpixel((i, j), self.binary_to_int(rgb))

        new_image.save(new_file_name)
        self.to_be_encoded_width = im2.size[0]
        self.to_be_encoded_height = im2.size[1]
        self.encodedd_name = new_file_name

    def decode_image(self, new_file_name):
        """Method decodes encoded image from the host image.
        :param new_file_name: the filename of the result
        """
        encoded_image = Image.open(self.encodedd_name).convert("RGB")
        new_image = Image.new("RGB", encoded_image.size)
        last_bites = []

        # Last bit of each pixel of decoded image is stored into <last_bites>
        for i in range(encoded_image.size[0]):
            for j in range(encoded_image.size[1]):
                rgb = self.int_to_binary(encoded_image.getpixel((i, j)))
                last_bites.append(rgb[0][-1])
                last_bites.append(rgb[1][-1])
                last_bites.append(rgb[2][-1])
        tmp = 0
        # Transforming bits from <last_bites> into RGB
        for i in range(self.to_be_encoded_width):
            for j in range(self.to_be_encoded_height):
                new_image.putpixel((i, j),
                                   self.binary_to_int(
                                       (''.join(last_bites[tmp:8 + tmp]),
                                        ''.join(last_bites[8 + tmp:16 + tmp]),
                                        ''.join(last_bites[16 + tmp:24 + tmp])))
                                   )
                tmp += 24

        area = (0, 0, self.to_be_encoded_width, self.to_be_encoded_height)
        new_image.crop(area).save(new_file_name)

    def is_fitting(self, image):
        """Method checks if the image can be encoded into the host image
        :param image: instance of PIL.Image
        :return: Bool (True if it is OK, False otherwise)
        """
        im = self.open_host_image(self.host_image_file_name)
        return ((im.size[0] * im.size[1]) // 8) >= image.size[0] * image.size[1]

    def int_to_binary(self, rgb):
        r, g, b = rgb
        return (bin(r)[2:].zfill(8),
                bin(g)[2:].zfill(8),
                bin(b)[2:].zfill(8))

    def binary_to_int(self, rgb):
        r, g, b = rgb
        return (int(r, base=2),
                int(g, base=2),
                int(b, base=2))
