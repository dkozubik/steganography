import steganography

"""A successful example"""
try:
    print("1st example")
    im = steganography.ImageToImage("host.png")
    im.encode_image('Lenna_small.png', "Lenna_small_encoded.png")
except OverflowError as e:
    print(e)
    print("This image should be small enough to be encoded...")
else:
    im.open_host_image("Lenna_small_encoded.png")
    im.decode_image("Lenna_small_decoded.png")
    print("OK, let's visually verify the decoded image :)")
finally:
    del im

"""An unsuccessful example"""
try:
    print("2nd example")
    im = steganography.ImageToImage("host.png")
    im.encode_image('obr1.png', "obr1_encoded.png")
except OverflowError as e:
    print (e)
    print ("This is probably OK")
else:
    print("The image should be too large to be encoded into the host image. Verify the data after decoding.")
    print("This is probably not OK")
finally:
    del im