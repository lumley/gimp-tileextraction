#!/usr/bin/env python

# =================== LICENSE =================
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Sergio R. Lumley
# 2013/03/14
# lumley256@gmail.com
# =================== LICENSE =================

# ========= What does this Script do?? =========
# This script extracts tiles specifying the offsets (vertical and horizontal)
# and places all of the tiles extracted in a single layer in the same
# order.
# For a better understanding, I will give an example:
# We have an image of 24x8 (which is 3 squares of 8x8 pixels), we want to
# get a new image of 12x4 (3 squares of 4x4 pixels) from the previous image
# extracting the center of each square, then we apply this filter with
# vertical offset set to 2 and horizontal offset set to 2.

# This tells Python to load the Gimp module 
from gimpfu import *
from array import array

# This is the function that will perform actual actions
def extract_offsetted_tiles(pImage, pDrawable, pTileColumns, pTileRows, pOffsetX, pOffsetY):
    if pTileColumns <= 0 or pTileRows <= 0 :
        gimp.pdb.gimp_message("Horizontal and vertical tiles must be bigger than 0")
        return

    # Calculate image bounds (if there was a selection, then it will
    # be probably smaller than the current pDrawable size
    thereIsSelection, x1, y1, x2, y2 = gimp.pdb.gimp_drawable_mask_bounds(pDrawable)
    
    # Numbers are integers, so no problem with this
    tileWidth = pDrawable.width/pTileColumns - pOffsetX*2
    tileHeight = pDrawable.height/pTileRows - pOffsetY*2

    if tileWidth <= 0 or tileHeight <= 0 :
        gimp.pdb.gimp_message("Specified offsets must result in a tile size bigger than 0 (You have setted offset with too high values!)")
        return

    # We group undoing so the history will show only one operation
    gimp.pdb.gimp_image_undo_group_start(pImage)
    gimp.pdb.gimp_progress_init("Extracting tiles, please wait", None)
    
    # Create the new working layer
    workingLayer = gimp.pdb.gimp_layer_new(pImage,
                                           tileWidth*pTileColumns,
                                           tileHeight*pTileRows,
                                           pDrawable.type,
                                           pDrawable.name+"_extracted_tiles",
                                           100,
                                           NORMAL_MODE)

    # Change working values and backup them to leave everything as it was
    currentForegroundColorBackup = gimp.pdb.gimp_context_get_foreground()
    gimp.pdb.gimp_context_set_foreground((0, 0, 0))

    # Change working values and backup them to leave everything as it was
    currentForegroundColorBackup = gimp.pdb.gimp_context_get_foreground()

    # Start extracting the tiles!
    for column in range(pTileColumns):
        for row in range (pTileRows):
            xPos = x1+column*(tileWidth+pOffsetX*2)+pOffsetX
            yPos = y1+row*(tileHeight+pOffsetY*2)+pOffsetY

            # drawable.get_pixel_rgn(x, y, w, h, [dirty, [shadow])
            srcPixelRegion = pDrawable.get_pixel_rgn(xPos, yPos, tileWidth, tileHeight, False, False) # Read only, lets make it efficient (no dirty, no shadows)!
            srcPixels = array("B", srcPixelRegion[:, :]) # Create a python array, B stands for Unsigned Chars

            destPixelRegion = workingLayer.get_pixel_rgn(column*tileWidth,
                                                 row*tileHeight,
                                                 tileWidth,
                                                 tileHeight,
                                                 True, True) # We want to set this pixel region as dirty and draw in shadow (performance!)
            # We copy all the values (note this is not the same as doing destPixelRegion = origPixelRegion, we are
            # copying each value independently, not changing the reference)
            destPixelRegion[:, :] = srcPixels.tostring() # Pixels are written as Strings (chars)
            
            
        gimp.pdb.gimp_progress_update(column/float(pTileColumns))
    
    #Now we finish grouping these changes
    gimp.pdb.gimp_context_set_foreground(currentForegroundColorBackup)
    gimp.pdb.gimp_image_insert_layer(pImage, workingLayer, None, -1)

    workingLayer.merge_shadow() # Note that when we were writing in the pixel regions of this layer, we used "True" in shadow pixels, so we now need to merge it
    workingLayer.update(0, 0, tileWidth*pTileColumns, tileHeight*pTileRows) # Update the dirty regions (which should be all the regions)
    workingLayer.flush() # Force show the changes on gimp UI
    gimp.displays_flush()
    gimp.pdb.gimp_image_undo_group_end(pImage)
    
    return

# This is the plugin registration function
# I have written each of its parameters on a different line 
register(
    "extract_offsetted_tiles",    
    "Extract tiles from an image",   
    "This script will extract tiles from a given image clipping the edges by the specified offset.",
    "Sergio R. Lumley", 
    "You are free to use, distribute and sell this plugin under license GPLv3", 
    "14 March 2013",
    "<Image>/Filters/Map/Extract clipped tiles", 
    "*", 
    [(PF_INT16, "tiles_x", "Number of horizontal tiles", 8, None),
     (PF_INT16, "tiles_y", "Number of vertical tiles", 8, None),
     (PF_INT16, "offset_x", "Horizontal clipping area for each tile", 8, None),
     (PF_INT16, "offset_y", "Vertical clipping area for each tile", 8, None),], 
    [],
    extract_offsetted_tiles
    )

main()
