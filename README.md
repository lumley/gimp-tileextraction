# Gimp plugin - Extract tiles from an image

This script extracts tiles specifying the offsets (vertical and horizontal) and places all of the tiles extracted in a single layer in the same order.

For a better understanding, I will give an example:
 * We have an image of 24x8 (which is 3 squares of 8x8 pixels), we want to get a new image of 12x4 (3 squares of 4x4 pixels) from the previous image extracting the center of each square, then we apply this filter with vertical offset set to 2 and horizontal offset set to 2.

This plugin is written to be really fast and efficient, but it still has some issues (it does not work on selected regions). It has been tested in Gimp2.8.

## Requirements
This plugin requires the following:
 * [`The Gimp GNU Image Manipulation Program`][URI_TheGimp] The GIMP program (Available on Linux, Windows and Mac)
 * Python GIMP-extension (usually installed by default)

## Installation
Installation of this plugin goes like any other Python-fu plugin. Just download the file and move it to your GIMP plug-ins folder (by default, "%USERPROFILE%\\.gimp-2.8\plug-ins\" in Windows and "~/.gimp-2.8/plug-ins/" in Linux).

Once installed you will find the plugin in Gimp menu: Filters -> Map -> Extract tiles from an image

## Collaborate
Want to improve this plugin? You could start by making it work on a selected region (not only on whole layers).
Want to make your own plugins? You can find some information on how to start on the next link:
 * [`Frederic Jaume - Python-Fu introduction`][URI_GimpTutorial1]


[URI_TheGimp]: http://www.gimp.org/
[URI_GimpTutorial1]: http://www.exp-media.com/content/extending-gimp-python-python-fu-plugins-part-1