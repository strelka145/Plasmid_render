import math
from playwright.sync_api import sync_playwright
import main
import pathlib
import os
import subprocess


def annular_sector(angle,central_angle,color,label_text,id):
    max_r=(main.args.radius+(main.args.tag_height/2))
    center=max_r+main.args.margin

    angle_add=angle+float(central_angle)
    dx=math.sin(math.radians(angle_add))-math.sin(math.radians(angle))
    dy=math.cos(math.radians(angle))-math.cos(math.radians(angle_add))
    start_point_x=(main.args.radius+(main.args.tag_height/2))*math.sin(math.radians(angle))+center
    start_point_y=center-(main.args.radius+(main.args.tag_height/2))*math.cos(math.radians(angle))
    svg_code='<path d="M '+str(start_point_x)+','+str(start_point_y)+' a '+str(main.args.radius+(main.args.tag_height/2))+' '+str(main.args.radius+(main.args.tag_height/2))+' '+str(angle-90)+' 0 1 '+str(dx*(main.args.radius+(main.args.tag_height/2)))+','+str(dy*(main.args.radius+(main.args.tag_height/2)))+' l '+str(-20*math.sin(math.radians(angle_add)))+' '+str(20*math.cos(math.radians(angle_add)))+' a '+str(main.args.radius-(main.args.tag_height/2))+' '+str(main.args.radius-(main.args.tag_height/2))+' '+str(angle_add-90)+' 0 0 '+str(-dx*(main.args.radius-(main.args.tag_height/2)))+','+str(-dy*(main.args.radius-(main.args.tag_height/2)))+'z" fill="'+color+'" stroke="black" stroke-width="'+str(main.args.tag_line_width)+'"/>'

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

def save_png(output_path,svg_code):
    subprocess.check_output('playwright install', shell=True)
    with open("./temp.svg", mode='w',encoding="utf_8") as f:
        f.write(svg_code)
    with sync_playwright() as p:
        browser = p.firefox.launch()
        p = pathlib.Path('./temp.svg')
        page.goto('file:'+str(p.resolve()))
        page.locator("svg").screenshot(path=output_path)
        browser.close()

def save_SVG(output_path,svg_code):
    with open(output_path, mode='w',encoding="utf_8") as f:
        f.write(svg_code)
