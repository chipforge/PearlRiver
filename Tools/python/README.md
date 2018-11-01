# Tools

These are scripts we use to generate GDS two masks and structures from images and so on

## ASCI 2 Magic

First you need a monochrome JPEG

convert -monochrome apple.gif apple_monochrome.jpeg

Then run jp2a (zypper install jp2a)

jp2a --size=240x240 --background=light --chars=" *********" apple_monochrome.jpeg > apple_big.txt

Then you've got to edit the script asci2magic.py in order to match your input and output file names.
