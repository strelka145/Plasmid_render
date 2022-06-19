import math
from playwright.sync_api import sync_playwright
import main
import pathlib
import os
import json
import subprocess

def head_svg():
    size=main.args.radius+(main.args.tag_height/2)+main.args.margin
    svg_text='<svg width="'+str(size*2)+'" height="'+str(size*2)+'" viewBox="0, 0, '+str(size*2)+', '+str(size*2)+'" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><circle cx="'+str(size)+'" cy="'+str(size)+'" r="'+str(main.args.radius)+'" fill="none" fill-opacity="0" stroke="black" stroke-width="'+str(main.args.plasmid_width)+'" id="circle1"/><!-- This image was created using plasmid render. -->'
    return svg_text

def annular_sector(angle,central_angle,color,label_text,id):
    max_r=(main.args.radius+(main.args.tag_height/2))
    center=max_r+main.args.margin

    angle_add=angle+float(central_angle)
    dx=math.sin(math.radians(angle_add))-math.sin(math.radians(angle))
    dy=math.cos(math.radians(angle))-math.cos(math.radians(angle_add))
    start_point_x=(main.args.radius+(main.args.tag_height/2))*math.sin(math.radians(angle))+center
    start_point_y=center-(main.args.radius+(main.args.tag_height/2))*math.cos(math.radians(angle))
    svg_code='<path d="M '+str(start_point_x)+','+str(start_point_y)+' a '+str(main.args.radius+(main.args.tag_height/2))+' '+str(main.args.radius+(main.args.tag_height/2))+' '+str(angle-90)+' 0 1 '+str(dx*(main.args.radius+(main.args.tag_height/2)))+','+str(dy*(main.args.radius+(main.args.tag_height/2)))+' l '+str(-main.args.tag_height*math.sin(math.radians(angle_add)))+' '+str(main.args.tag_height*math.cos(math.radians(angle_add)))+' a '+str(main.args.radius-(main.args.tag_height/2))+' '+str(main.args.radius-(main.args.tag_height/2))+' '+str(angle_add-90)+' 0 0 '+str(-dx*(main.args.radius-(main.args.tag_height/2)))+','+str(-dy*(main.args.radius-(main.args.tag_height/2)))+'z" fill="'+color+'" stroke="black" stroke-width="'+str(main.args.tag_line_width)+'"/>'

    start_point_x=main.args.radius*math.sin(math.radians(angle))+center
    start_point_y=center-main.args.radius*math.cos(math.radians(angle))
    svg_code+='<path d="M '+str(start_point_x)+','+str(start_point_y)+' a '+str(main.args.radius)+' '+str(main.args.radius)+' '+str(angle-90)+' 0 1 '+str(dx*main.args.radius)+','+str(dy*main.args.radius)+'" fill="none" id="path'+str(id)+'"/>'
    if main.args.font==None:
        font_style=""
    else:
        font_style='font-family="'+main.args.font+'"'

    svg_code+='<text font-size="'+str(main.args.font_size)+'" '+font_style+' dominant-baseline="central" text-anchor="middle">'
    svg_code+='<textPath startOffset="50%" href="#path'+str(id)+'" >'+label_text+'</textPath></text>'
    return svg_code

def point(angle,color,label_text,id):
    max_r=(main.args.radius+(main.args.tag_height/2))
    center=max_r+main.args.margin
    angle_add=angle
    start_point_x=(main.args.radius+(main.args.cut_line_length/2))*math.sin(math.radians(angle))+center
    start_point_y=center-(main.args.radius+(main.args.cut_line_length/2))*math.cos(math.radians(angle))
    end_point_x=(main.args.radius-(main.args.cut_line_length/2))*math.sin(math.radians(angle))+center
    end_point_y=center-(main.args.radius-(main.args.cut_line_length/2))*math.cos(math.radians(angle))
    svg_code='<path d="M'+str(start_point_x)+','+str(start_point_y)+' L '+str(end_point_x)+' '+str(end_point_y)+'" stroke-width="'+str(main.args.cut_line_thickness)+'" stroke="'+color+'"/>'
    start_point_x=(main.args.radius+(main.args.cut_line_length/2))*math.sin(math.radians(angle-80))+center
    start_point_y=center-(main.args.radius+(main.args.cut_line_length/2))*math.cos(math.radians(angle-80))
    end_point_x=(main.args.radius+(main.args.cut_line_length/2))*math.sin(math.radians(angle+80))+center
    end_point_y=center-(main.args.radius+(main.args.cut_line_length/2))*math.cos(math.radians(angle+80))
    svg_code+='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str((main.args.radius+(main.args.cut_line_length/2)))+' '+str((main.args.radius+(main.args.cut_line_length/2)))+' '+str(angle-90)+' 0 1 '+str(end_point_x)+','+str(end_point_y)+'" fill="none" id="path'+str(id)+'"/>'
    if main.args.font==None:
        font_style=""
    else:
        font_style='font-family="'+main.args.font+'"'
    svg_code+='<text font-size="'+str(main.args.font_size)+'" '+font_style+' dominant-baseline="ideographic" text-anchor="middle">'
    svg_code+='<textPath startOffset="50%" href="#path'+str(id)+'" >'+label_text+'</textPath></text>'
    return svg_code

def arrow(angle,central_angle,color,label_text,id):
    max_r=(main.args.radius+(main.args.tag_height/2))
    center=max_r+main.args.margin
    start_point_x=(main.args.arrow_radius)*math.sin(math.radians(angle))+center
    start_point_y=center-(main.args.arrow_radius)*math.cos(math.radians(angle))
    end_point_x=(main.args.arrow_radius)*math.sin(math.radians(angle+float(central_angle)))+center
    end_point_y=center-(main.args.arrow_radius)*math.cos(math.radians(angle+float(central_angle)))
    if abs(float(central_angle))<180:
        f1='0'
    else:
        f1='1'
    if float(central_angle)>0:
        f2='1'
        svg_code='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(main.args.arrow_radius)+' '+str(main.args.arrow_radius)+' '+str(angle-90)+' '+f1+' '+f2+' '+str(end_point_x)+','+str(end_point_y)+' l '+str(main.args.arrow_size*math.cos(math.radians(135-(angle+float(central_angle)))))+' '+str(-main.args.arrow_size*math.sin(math.radians(135-(angle+float(central_angle)))))+'" stroke-width="'+str(main.args.arrow_thickness)+'" fill="none" stroke="'+color+'"/>'
        #svg_code+='<path d="M'+str(end_point_x)+','+str(end_point_y)+' l '+str(-main.args.arrow_size*math.sin(225-(angle+float(central_angle))))+' '+str(main.args.arrow_size*math.cos(225-(angle+float(central_angle))))+'" stroke-width="'+str(main.args.arrow_thickness)+'" stroke="'+color+'"/>'
    else:
        f2='0'
        svg_code='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(main.args.arrow_radius)+' '+str(main.args.arrow_radius)+' '+str(angle-90)+' '+f1+' '+f2+' '+str(end_point_x)+','+str(end_point_y)+' l '+str(main.args.arrow_size*math.cos(math.radians(45-(angle+float(central_angle)))))+' '+str(-main.args.arrow_size*math.sin(math.radians(45-(angle+float(central_angle)))))+'" stroke-width="'+str(main.args.arrow_thickness)+'" fill="none" stroke="'+color+'"/>'
    #svg_code+='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(main.args.arrow_radius)+' '+str(main.args.arrow_radius)+' '+str(angle-90)+' '+f1+' '+f2+' '+str(end_point_x)+','+str(end_point_y)+'" stroke-width="'+str(main.args.arrow_thickness)+'" fill="none" stroke="'+color+'" />'
    start_point_x=(main.args.arrow_radius+(main.args.arrow_size*math.sin(45)))*math.sin(math.radians((angle+(float(central_angle)/2))-80))+center
    start_point_y=center-(main.args.arrow_radius+(main.args.arrow_size*math.sin(45)))*math.cos(math.radians((angle+(float(central_angle)/2))-80))
    end_point_x=(main.args.arrow_radius+(main.args.arrow_size*math.sin(45)))*math.sin(math.radians((angle+(float(central_angle)/2))+80))+center
    end_point_y=center-(main.args.arrow_radius+(main.args.arrow_size*math.sin(45)))*math.cos(math.radians((angle+(float(central_angle)/2))+80))
    svg_code+='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(main.args.arrow_radius+(main.args.arrow_size*math.sin(45)))+' '+str(main.args.arrow_radius+(main.args.arrow_size*math.sin(45)))+' '+str((angle+(float(central_angle)/2))-80-90)+' '+'0'+' '+'1'+' '+str(end_point_x)+','+str(end_point_y)+'" fill="none" id="path'+str(id)+ '"/>'

    if main.args.font==None:
        font_style=""
    else:
        font_style='font-family="'+main.args.font+'"'
    svg_code+='<text font-size="'+str(main.args.font_size)+'" '+font_style+' dominant-baseline="ideographic" text-anchor="middle">'
    svg_code+='<textPath startOffset="50%" href="#path'+str(id)+'" >'+label_text+'</textPath></text>'
    return svg_code


def save_png(output_path,svg_code):
    subprocess.call(["playwright" ,"install"], shell=True)
    with open("./temp.svg", mode='w',encoding="utf_8") as f:
        f.write(svg_code)
    with sync_playwright() as p:
        browser = p.firefox.launch()
        p = pathlib.Path('./temp.svg')
        page = browser.new_page()
        page.goto('file:'+str(p.resolve()))
        page.locator("svg").screenshot(path=output_path)
        browser.close()

def save_SVG(output_path,svg_code):
    with open(output_path, mode='w',encoding="utf_8") as f:
        f.write(svg_code)
