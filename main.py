import json
import svg_draw
import option

def drow():
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

        if gene_item["type"]=="tag":
            if flag_before_item_is_tag:
                angle+=5
            svg_text+=svg_draw.annular_sector(angle,gene_item["angle"],gene_item["color"],gene_item["label"],id)
            flag_before_item_is_tag=True
            id+=1
        else:
            flag_before_item_is_tag=False

        angle+=float(gene_item["angle"])


    svg_text+='</svg>'

    if args.output_svg_file!=None:
        svg_draw.save_SVG(args.output_svg_file,svg_text)

    if args.output_png_file!=None:
        svg_draw.save_png(args.output_png_file,svg_text)


args = option.get_option()
if args.config_path!=None:
    option.option_json(args.config_path)

if __name__ == '__main__':
    drow()
