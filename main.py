import json
import svg_draw
import option

def json_load(json_path):
    with open(json_path,mode="r") as f:
        d = json.load(f)
    return d

args = option.get_option()
if __name__ == '__main__':

    if args.input_file==None:
        gene_list=json.loads(args.input_json)
    else:
        gene_list=json_load(str(args.input_file))

    size=args.radius+(args.tag_height/2)+args.margin
    svg_text='<svg width="'+str(size*2)+'" height="'+str(size*2)+'" viewBox="0, 0, '+str(size*2)+', '+str(size*2)+'" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><circle cx="'+str(size)+'" cy="'+str(size)+'" r="'+str(args.radius)+'" fill="none" fill-opacity="0" stroke="black" stroke-width="'+str(args.plasmid_width)+'" id="circle1"/><!-- This image was created using plasmid render. -->'
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
