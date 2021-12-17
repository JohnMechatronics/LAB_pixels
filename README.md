# LAB_pixels
This code takes any png as input and separates each colour into individual layers

Each colour pixel is saved in a seperat file (as black pixels). The layers are named using their equivenal LAB value

The RGB to LAB convertion uses code found here: https://web.archive.org/web/20120502065620/http://cookbooks.adobe.com/post_Useful_color_equations__RGB_to_LAB_converter-14227.html

Code requirs the Pillow - Python Imaging Library - https://python-pillow.org/

Best used with indexed png images to reduce the number of colour layers.
