import math

def annular_sector(angle,central_angle,color,label_text,id):
    angle_add=angle+float(central_angle)
    dx=math.sin(math.radians(angle_add))-math.sin(math.radians(angle))
    dy=math.cos(math.radians(angle))-math.cos(math.radians(angle_add))
    start_point_x=100*math.sin(math.radians(angle))+150
    start_point_y=150-100*math.cos(math.radians(angle))
    svg_code='<path d="M '+str(start_point_x)+','+str(start_point_y)+' a 100 100 '+str(angle-90)+' 0 1 '+str(dx*100)+','+str(dy*100)+' l '+str(-20*math.sin(math.radians(angle_add)))+' '+str(20*math.cos(math.radians(angle_add)))+' a 80 80 '+str(angle_add-90)+' 0 0 '+str(-dx*80)+','+str(-dy*80)+'z" fill="'+color+'" stroke="black"/>'

    start_point_x=90*math.sin(math.radians(angle))+150
    start_point_y=150-90*math.cos(math.radians(angle))
    svg_code+='<path d="M '+str(start_point_x)+','+str(start_point_y)+' a 90 90 '+str(angle-90)+' 0 1 '+str(dx*90)+','+str(dy*90)+'" fill="none" id="path'+str(id)+'"/>'
    svg_code+='<text dominant-baseline="central" text-anchor="middle">'
    svg_code+='<textPath startOffset="50%" href="#path'+str(id)+'" >'+label_text+'</textPath></text>'
    return svg_code
