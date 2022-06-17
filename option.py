from argparse import ArgumentParser


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input_file',help='Path of input json file')
    argparser.add_argument('--input_json',default="[]",help='Input json text')
    argparser.add_argument('-o', '--output_file',default="./out.svg",help='Path of output svg file')

    argparser.add_argument('-cp','--config_path',help='Configuration file path')
    argparser.add_argument('--radius',type=float,default=90,\
                            help='Plasmid radius, which automatically determines the size of the image.')
    argparser.add_argument('-pw','--plasmid_width',type=float,default=2.5,\
                            help='Width of plasmid line')
    argparser.add_argument('-th','--tag_height',type=float,default=20,\
                            help='Height of tag(an annular sector)')
    argparser.add_argument('-tl','--tag_line_width',type=float,default=1,\
                            help='Tag(an annular sector) outline thickness')
    argparser.add_argument('--font',help='Font name')


    return argparser.parse_args()
