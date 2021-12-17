#########################################
#
# This code takes any png as input and separates each colour into seperal layers
# Each colour pixel is saved in a seperat file (as black pixels)The layers are named using their equivenal LAB value
#
# The RGB to LAB convertion uses code found here: https://web.archive.org/web/20120502065620/http://cookbooks.adobe.com/post_Useful_color_equations__RGB_to_LAB_converter-14227.html
#
# More info: John.wild@network.rca.ac.uk
#
#########################################

from PIL import Image

# - Function to convert to LAB

def rgb2lab ( inputColor ) :

    num = 0
    RGB = [0, 0, 0]

    for value in inputColor :
        value = float(value) / 255

        if value > 0.04045 :
            value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
        else :
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0,]

    X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
    Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
    Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
    XYZ[ 0 ] = round( X, 4 )
    XYZ[ 1 ] = round( Y, 4 )
    XYZ[ 2 ] = round( Z, 4 )

    XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
    XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ :

        if value > 0.008856 :
            value = value ** ( 0.3333333333333333 )
        else :
            value = ( 7.787 * value ) + ( 16 / 116 )

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = ( 116 * XYZ[ 1 ] ) - 16
    a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
    b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

    Lab [ 0 ] = round( L, 4 )
    Lab [ 1 ] = round( a, 4 )
    Lab [ 2 ] = round( b, 4 )

    return Lab


#+++++++++++++++ MAIN PROGRAM ++++++++++++++++++++++++++++++

original_img = Image.open("index10.png")

# Check image mode and convert to RGB
mode = original_img.mode
if (mode != "RGB"):
    img = original_img.convert("RGB")
else:
    img = original_img

# Get image height and width
width = img.size[0] 
height = img.size[1]

# Get all pixels from the image and store them in a list
pixel_list = []
pixel_list.append(img.getpixel((0,0)))
pixel_present = False
for i in range(0,width):# process all pixels
    for j in range(0,height):
        pixal = img.getpixel((i,j)) # get pixel colour
        
        #Check if the colour is already in the list
        pixel_list_len = len(pixel_list)
        pixel_present = False
        for x in range(pixel_list_len):
            if pixal == pixel_list[x]:
                pixel_present = True
        #If pixel not present add it to the list
        if pixel_present == False:
                pixel_list.append(pixal)

# Create a seperat layer for each colour
layer_count = 0                
for rgb_val in pixel_list:
    lab = rgb2lab(rgb_val) #Convert RGB value to lab and make it the layer name
    layer_name = str(lab[0]) + "|" + str(lab[1]) + "|" + str(lab[2]) + ".png"
    layer_count +=1
    layer = Image.new(mode="RGB", size=(width, height))
    # process all pixels in the image setting curent rgb to black and all rest to white
    for i in range(0,width):
        for j in range(0,height):
            data = img.getpixel((i,j))
            if (data[0]==rgb_val[0] and data[1]==rgb_val[1] and data[2]==rgb_val[2]):
                layer.putpixel((i,j),(0, 0, 0))
            else:
                layer.putpixel((i,j),(255, 255, 255))
                
    layer.save(layer_name) # Save the layer using its LAB value as its name
    print (layer_name)
                 
pixel_list_len = len(pixel_list)
print("Process complete")
print(pixel_list_len, " - files created")
        

