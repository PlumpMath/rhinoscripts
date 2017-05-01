import rhinoscriptsyntax as rs

# this pulls in all of rhino's native commands into python,
# so from here on out we can just say rs.[whatever] to access rhino's stuff
# a list of rhino python commands is here: http://www.rhino3d.com/5/ironpython/index.html
# first, we need some information from the user:
numberOfPoints = rs.GetInteger("how many data points?") # do the same for the number of data points
radius = rs.GetReal("what's the radius of your sun-sphere?") # get a radius for the sphere the sun's going to rotate around

rs.AddLayer("sun sphere", [0,0,255]) # make a new layer for the sphere itself, and color it blue
rs.AddLayer("sun rays", [255,0,0]) # make a new layer for the rays shooting inwards from the sun, color it red
rs.CurrentLayer("sun sphere") # go to the sun sphere layer

sunSphere = rs.AddSphere([0,0,0], radius) # draw the sun sphere at the origin with a radius of whatever is in the variable "radius" (and store it in a variable called sunSphere)



# saying if(something) is a boolean test - checks to see whether the statements are true.
# it just checks to see whether there's anything positive in these variables
if ((numberOfPoints > 0) and (radius > 0)):

    dayName = rs.GetString("which day is this? (no spaces!)") # ask for a label (text blocks are called 'strings') for the eventual curve object
    print "current day = ", dayName # print it to the command line, just to make sure it worked
    rs.AddLayer(dayName, [255,255,255]) # make a new layer for each day - make everything on them white, just to distinguish
    # (you can change [255,255,255] to any color, or delete that part)
    rs.CurrentLayer(dayName) # go to that layer
    
    listOfPoints = [] # setup a list (empty at this point) to hold all the points for the curve
    rs.AddPoint([0,radius,0]) # put down one point at x=0, y= the radius of the sun-sphere, z=0
    starterPt = rs.FirstObject() # FirstObject grabs the last thing created, in this case that point we just made - let's name that 'starterPt'
    
    # this next thing is called a 'for loop' - it basically says:
    # - make a variable called 'i' which starts at 0
    # - as long as i is less than numberOfPoints, run the indented block of code.
    # - when you're done with the block of code, add 1 to i, and do it again
    # so a for loop is a great way to do something repeatedly a specific number of times
    # (i.e. until i is no longer less than numberOfPoints)
    
    # so: cycle through each day, and each time, do the following
    for i in range (numberOfPoints):
        elevation = rs.GetReal("what's the elevation angle?") # ask for an elevation angle, just like up top
        azimuth = rs.GetReal("what's the azimuth angle?") # ask for an azimuth angle
    
        azimuth *= -1 # flip the azimuth - because by default, rhino rotates things CCW, and compasses go CW
        # rotate that first point to the elevation angle
        # rotate works like this: RotateObject( object_to_rotate, center_point, angle_to_rotate, rotation_axis, copy_yes/no )
        rs.RotateObject(starterPt, [0,0,0], elevation, axis=[1,0,0], copy=True)
        rs.RotateObject(rs.FirstObject(), [0,0,0], azimuth, axis=[0,0,1], copy=False) # do the same thing for the azimuth
        listOfPoints.append(rs.FirstObject()) # once we have the final location, add that point to our listOfPoints list

        rs.CurrentLayer("sun rays") # switch to the sun rays layer
        sunRay = rs.AddLine([0,0,0],rs.FirstObject()) # on that layer, draw a line for the ray
        rs.CurrentLayer(dayName) # switch back to the current day (for the next loop)
        
        #this is the end of the "for loop" - note how the next "if" statement isn't indented as much
            
    if(listOfPoints): # check whether listOfPoints has anything in it
         sunpath = rs.AddInterpCurve(listOfPoints) # add an interpolated curve (one that goes THROUGH the points)
         newsunpath = rs.PullCurve(sunSphere, sunpath, False) # pull that curve to the sphere
         rs.ObjectName(newsunpath, dayName) # name it using the 'dayName' variable from earlier - fyi, object names show up if you type 'properties' in rhino
         rs.DeleteObject(sunpath) # delete the old (non-pulled) curve
         crvstojoin = rs.ObjectsByName(dayName, True) # sometimes pulling breaks up a curve, so we have to gather all those pieces
         if (len(crvstojoin) > 1): # if, in fact, there are multiple curves
             crvstojoin = rs.JoinCurves(crvstojoin, True) # join them
         rs.ObjectName(crvstojoin, dayName) # for some reason joining things kills their names - so if you want, rename the final curve
         
         rs.DeleteObject(starterPt) # finally, delete that original point that we copied and rotated around
         rs.DeleteObject(sunSphere) # and delete the sphere.
         
else: # if we didn't successfully get points or radius
    print "please enter positive values!" # explain why nothing happened