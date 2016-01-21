import math

radius = 6.371E6 #Earth radius in meters.
p1 = [37.424928, -122.176934, 0];
p2 = [37.424157, -122.177866, 0];
     #Lat      , Long,      ,Alt
def getNodeAngle(p1,p2):
    #Returns an Azimuth angle for this node. 
    #from math notes: u is my position, w is the north dot, and v = you.
    sign = True;
    if(p1[1]>p2[1]): sign = False;
    delta = [p1[0]-p2[0], p1[1]- p2[1]]

    uw = delta[1]
    vw = delta[0]

    uv = math.acos( math.cos(delta[0])*math.cos(delta[1]))
    C = math.acos((math.cos(vw)-math.cos(uv)*math.cos(uw)  )/(  math.sin(uv)*math.sin(uw)))
    if(sign): C= -1*C;
    return C


p1 = [37.424928, -122.176934];
p2 = [37.424157, -122.177866];
print(translateInternalAngles(p2,p1)/3.14159*180);
