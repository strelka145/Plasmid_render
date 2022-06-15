import json
import svg_draw
import option

def json_load(json_path):
    with open(json_path,mode="r") as f:
        d = json.load(f)
    return d

if __name__ == '__main__':

    args = option.get_option()
    if args.input_file==None:
        gene_list=json.loads(args.input_json)
    else:
        gene_list=json_load(str(args.input_file))

    svg_text='<svg width="300" height="300" viewBox="0, 0, 300, 300" xmlns="http://www.w3.org/2000/svg"><circle cx="150" cy="150" r="90" fill="#000000" fill-opacity="0" stroke="black" stroke-width="2.5" id="circle1"/><!-- This image was created using plasmid render. -->'
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

    with open(args.output_json, mode='w',encoding="utf_8") as f:
        f.write(svg_text)
