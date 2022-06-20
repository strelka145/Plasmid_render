import json
import svg_draw
import option


#input_file=None,input_json=None,output_svg_file=None,output_png_file=None,config_path=None,picture_box=500.0,radius=180.0,plasmid_width=2.5,tag_height=20,tag_line_width=1.0,cut_line_length=20.0,cut_line_thickness=2.5,arrow_size=10.0,arrow_radius=200.0,arrow_thickness=2.0,font=None,font_size=16.0,rotation_angle=-90.0
def draw():
    args = option.get_option()
    if args.config_path!=None:
        option.option_json(args.config_path)
    if args.input_file==None:
        gene_list=json.loads(args.input_json)
    else:
        with open( args.input_file,mode="r") as f:
            gene_list = json.load(f)
    svg_text=svg_draw.head_svg()
    angle=0.0
    id=0
    flag_before_item_is_tag=False
    for gene_item in gene_list:
        if "font_color" in gene_item:
            font_color=gene_item["font_color"]
        else:
            font_color="black"
        if gene_item["type"]=="tag":
            if flag_before_item_is_tag:
                angle+=5
            svg_text+=svg_draw.annular_sector(angle,gene_item["angle"],gene_item["color"],gene_item["label"],id,font_color)
            flag_before_item_is_tag=True
            id+=1
            angle+=float(gene_item["angle"])
        elif gene_item["type"]=="line":
            svg_text+=svg_draw.point(angle,gene_item["color"],gene_item["label"],id,font_color)
            id+=1
            flag_before_item_is_tag=False
        elif gene_item["type"]=="arrow":
            svg_text+=svg_draw.arrow(angle,gene_item["angle"],gene_item["color"],gene_item["label"],id,font_color)
            id+=1
            flag_before_item_is_tag=False
        else:
            flag_before_item_is_tag=False
            angle+=float(gene_item["angle"])



    svg_text+='</g></svg>'

    if args.output_svg_file!=None:
        svg_draw.save_SVG(args.output_svg_file,svg_text)

    if args.output_png_file!=None:
        svg_draw.save_png(args.output_png_file,svg_text)


args = option.get_option()
if args.config_path!=None:
    option.option_json(args.config_path)

if __name__ == '__main__':

    draw()
