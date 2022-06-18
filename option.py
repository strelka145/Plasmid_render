from argparse import ArgumentParser


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input_file',help='Path of input json file')
    argparser.add_argument('--input_json',default="[]",help='Input json text')
    argparser.add_argument('-os', '--output_svg_file',help='Path of output svg file')
    argparser.add_argument('-op', '--output_png_file',help='Path of output svg file')

    argparser.add_argument('-cp','--config_path',help='Configuration file path')
    argparser.add_argument('--margin',type=float,default=50,help='Margin size')
    argparser.add_argument('-r','--radius',type=float,default=90,\
                            help='Plasmid radius, which automatically determines the size of the image.')
    argparser.add_argument('-pw','--plasmid_width',type=float,default=2.5,\
                            help='Width of plasmid line')
    argparser.add_argument('-th','--tag_height',type=float,default=20,\
                            help='Height of tag(an annular sector)')
    argparser.add_argument('-tl','--tag_line_width',type=float,default=1,\
                            help='Tag(an annular sector) outline thickness')
    argparser.add_argument('--font',help='Font name')
    argparser.add_argument('--font_size',type=float,default=16,help='Font size')


    return argparser.parse_args()
