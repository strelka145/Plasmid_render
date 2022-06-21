import math
import asyncio
from playwright.async_api import async_playwright
from . import option
import pathlib
import os
import json
import subprocess
import platform

def head_svg():
    size=option.arguments.picture_box/2
    svg_text='<svg width="'+str(size*2)+'" height="'+str(size*2)+'" viewBox="0, 0, '+str(size*2)+', '+str(size*2)+'" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g transform="rotate('+str(option.arguments.rotation_angle)+','+str(size)+','+str(size)+')"> <circle cx="'+str(size)+'" cy="'+str(size)+'" r="'+str(option.arguments.radius)+'" fill="none" fill-opacity="0" stroke="black" stroke-width="'+str(option.arguments.plasmid_width)+'" id="circle1"/><!-- This image was created using plasmid render. -->'
    return svg_text

def annular_sector(angle,central_angle,color,label_text,id,font_color="black"):
    center=option.arguments.picture_box/2

    angle_add=angle+float(central_angle)
    dx=math.sin(math.radians(angle_add))-math.sin(math.radians(angle))
    dy=math.cos(math.radians(angle))-math.cos(math.radians(angle_add))
    start_point_x=(option.arguments.radius+(option.arguments.tag_height/2))*math.sin(math.radians(angle))+center
    start_point_y=center-(option.arguments.radius+(option.arguments.tag_height/2))*math.cos(math.radians(angle))
    svg_code='<path d="M '+str(start_point_x)+','+str(start_point_y)+' a '+str(option.arguments.radius+(option.arguments.tag_height/2))+' '+str(option.arguments.radius+(option.arguments.tag_height/2))+' '+str(angle-90)+' 0 1 '+str(dx*(option.arguments.radius+(option.arguments.tag_height/2)))+','+str(dy*(option.arguments.radius+(option.arguments.tag_height/2)))+' l '+str(-option.arguments.tag_height*math.sin(math.radians(angle_add)))+' '+str(option.arguments.tag_height*math.cos(math.radians(angle_add)))+' a '+str(option.arguments.radius-(option.arguments.tag_height/2))+' '+str(option.arguments.radius-(option.arguments.tag_height/2))+' '+str(angle_add-90)+' 0 0 '+str(-dx*(option.arguments.radius-(option.arguments.tag_height/2)))+','+str(-dy*(option.arguments.radius-(option.arguments.tag_height/2)))+'z" fill="'+color+'" stroke="black" stroke-width="'+str(option.arguments.tag_line_width)+'"/>'

    start_point_x=option.arguments.radius*math.sin(math.radians(angle))+center
    start_point_y=center-option.arguments.radius*math.cos(math.radians(angle))
    svg_code+='<path d="M '+str(start_point_x)+','+str(start_point_y)+' a '+str(option.arguments.radius)+' '+str(option.arguments.radius)+' '+str(angle-90)+' 0 1 '+str(dx*option.arguments.radius)+','+str(dy*option.arguments.radius)+'" fill="none" id="path'+str(id)+'"/>'
    if option.arguments.font==None:
        font_style=""
    else:
        font_style='font-family="'+option.arguments.font+'"'

    svg_code+='<text font-size="'+str(option.arguments.font_size)+'" '+font_style+' dominant-baseline="central" text-anchor="middle" stroke="none" fill="'+font_color+'">'
    svg_code+='<textPath startOffset="50%" href="#path'+str(id)+'" >'+label_text+'</textPath></text>'
    return svg_code

def point(angle,color,label_text,id,font_color="black"):
    center=option.arguments.picture_box/2
    angle_add=angle
    start_point_x=(option.arguments.radius+(option.arguments.cut_line_length/2))*math.sin(math.radians(angle))+center
    start_point_y=center-(option.arguments.radius+(option.arguments.cut_line_length/2))*math.cos(math.radians(angle))
    end_point_x=(option.arguments.radius-(option.arguments.cut_line_length/2))*math.sin(math.radians(angle))+center
    end_point_y=center-(option.arguments.radius-(option.arguments.cut_line_length/2))*math.cos(math.radians(angle))
    svg_code='<path d="M'+str(start_point_x)+','+str(start_point_y)+' L '+str(end_point_x)+' '+str(end_point_y)+'" stroke-width="'+str(option.arguments.cut_line_thickness)+'" stroke="'+color+'"/>'
    start_point_x=(option.arguments.radius+(option.arguments.cut_line_length/2))*math.sin(math.radians(angle-80))+center
    start_point_y=center-(option.arguments.radius+(option.arguments.cut_line_length/2))*math.cos(math.radians(angle-80))
    end_point_x=(option.arguments.radius+(option.arguments.cut_line_length/2))*math.sin(math.radians(angle+80))+center
    end_point_y=center-(option.arguments.radius+(option.arguments.cut_line_length/2))*math.cos(math.radians(angle+80))
    svg_code+='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str((option.arguments.radius+(option.arguments.cut_line_length/2)))+' '+str((option.arguments.radius+(option.arguments.cut_line_length/2)))+' '+str(angle-90)+' 0 1 '+str(end_point_x)+','+str(end_point_y)+'" fill="none" id="path'+str(id)+'"/>'
    if option.arguments.font==None:
        font_style=""
    else:
        font_style='font-family="'+option.arguments.font+'"'
    svg_code+='<text font-size="'+str(option.arguments.font_size)+'" '+font_style+' dominant-baseline="ideographic" text-anchor="middle" stroke="none" fill="'+font_color+'">'
    svg_code+='<textPath startOffset="50%" href="#path'+str(id)+'" >'+label_text+'</textPath></text>'
    return svg_code

def arrow(angle,central_angle,color,label_text,id,font_color="black"):
    center=option.arguments.picture_box/2
    start_point_x=(option.arguments.arrow_radius)*math.sin(math.radians(angle))+center
    start_point_y=center-(option.arguments.arrow_radius)*math.cos(math.radians(angle))
    end_point_x=(option.arguments.arrow_radius)*math.sin(math.radians(angle+float(central_angle)))+center
    end_point_y=center-(option.arguments.arrow_radius)*math.cos(math.radians(angle+float(central_angle)))
    if abs(float(central_angle))<180:
        f1='0'
    else:
        f1='1'
    if float(central_angle)>0:
        f2='1'
        svg_code='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(option.arguments.arrow_radius)+' '+str(option.arguments.arrow_radius)+' '+str(angle-90)+' '+f1+' '+f2+' '+str(end_point_x)+','+str(end_point_y)+' l '+str(option.arguments.arrow_size*math.cos(math.radians(135-(angle+float(central_angle)))))+' '+str(-option.arguments.arrow_size*math.sin(math.radians(135-(angle+float(central_angle)))))+'" stroke-width="'+str(option.arguments.arrow_thickness)+'" fill="none" stroke="'+color+'"/>'
        #svg_code+='<path d="M'+str(end_point_x)+','+str(end_point_y)+' l '+str(-option.arguments.arrow_size*math.sin(225-(angle+float(central_angle))))+' '+str(option.arguments.arrow_size*math.cos(225-(angle+float(central_angle))))+'" stroke-width="'+str(option.arguments.arrow_thickness)+'" stroke="'+color+'"/>'
    else:
        f2='0'
        svg_code='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(option.arguments.arrow_radius)+' '+str(option.arguments.arrow_radius)+' '+str(angle-90)+' '+f1+' '+f2+' '+str(end_point_x)+','+str(end_point_y)+' l '+str(option.arguments.arrow_size*math.cos(math.radians(45-(angle+float(central_angle)))))+' '+str(-option.arguments.arrow_size*math.sin(math.radians(45-(angle+float(central_angle)))))+'" stroke-width="'+str(option.arguments.arrow_thickness)+'" fill="none" stroke="'+color+'"/>'
    #svg_code+='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(option.arguments.arrow_radius)+' '+str(option.arguments.arrow_radius)+' '+str(angle-90)+' '+f1+' '+f2+' '+str(end_point_x)+','+str(end_point_y)+'" stroke-width="'+str(option.arguments.arrow_thickness)+'" fill="none" stroke="'+color+'" />'
    start_point_x=(option.arguments.arrow_radius+(option.arguments.arrow_size*math.sin(45)))*math.sin(math.radians((angle+(float(central_angle)/2))-80))+center
    start_point_y=center-(option.arguments.arrow_radius+(option.arguments.arrow_size*math.sin(45)))*math.cos(math.radians((angle+(float(central_angle)/2))-80))
    end_point_x=(option.arguments.arrow_radius+(option.arguments.arrow_size*math.sin(45)))*math.sin(math.radians((angle+(float(central_angle)/2))+80))+center
    end_point_y=center-(option.arguments.arrow_radius+(option.arguments.arrow_size*math.sin(45)))*math.cos(math.radians((angle+(float(central_angle)/2))+80))
    svg_code+='<path d="M'+str(start_point_x)+','+str(start_point_y)+' A '+str(option.arguments.arrow_radius+(option.arguments.arrow_size*math.sin(45)))+' '+str(option.arguments.arrow_radius+(option.arguments.arrow_size*math.sin(45)))+' '+str((angle+(float(central_angle)/2))-80-90)+' '+'0'+' '+'1'+' '+str(end_point_x)+','+str(end_point_y)+'" fill="none" id="path'+str(id)+ '"/>'

    if option.arguments.font==None:
        font_style=""
    else:
        font_style='font-family="'+option.arguments.font+'"'
    svg_code+='<text font-size="'+str(option.arguments.font_size)+'" '+font_style+' dominant-baseline="ideographic" text-anchor="middle" stroke="none" fill="'+font_color+'">'
    svg_code+='<textPath startOffset="50%" href="#path'+str(id)+'" >'+label_text+'</textPath></text>'
    return svg_code


async def save_png(output_path,svg_code):
    if platform.system()=="Windows":
        shell=True
    else:
        shell=False
    subprocess.run(["playwright" ,"install","firefox"], shell=shell)
    with open("./temp.svg", mode='w',encoding="utf_8") as f:
        f.write(svg_code)
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        path_svg = pathlib.Path('./temp.svg')
        page = await browser.new_page()
        await page.goto('file:'+str(path_svg.resolve()))
        await page.locator("svg").screenshot(path=output_path)
        await browser.close()

def save_SVG(output_path,svg_code):
    with open(output_path, mode='w',encoding="utf_8") as f:
        f.write(svg_code)
