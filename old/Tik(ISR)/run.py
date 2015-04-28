from pylab import *
import os
# set the interactive mode of pylab to ON
ion()
# opens a new figure to plot into
fig_hndl = figure()
# make an empty list into which we'll append
# the filenames of the PNGs that compose each
# frame.
files=[]    
# filename for the name of the resulting movie
filename = 'animation'
number_of_frames = 100
for t in range(number_of_frames):
    # draw the frame
    imshow(rand(100,100))
    # form a filename
    fname = '_tmp%03d.png'%t
    # save the frame
    savefig(fname)
    # append the filename to the list
    files.append(fname)
# call mencoder 
os.system("mencoder 'mf://_tmp*.png' -mf type=png:fps=10 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o " + filename + ".mpg")
# cleanup
for fname in files: os.remove(fname)
