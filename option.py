from argparse import ArgumentParser


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input_file',help='Path of input json file')
    argparser.add_argument('--input_json',default="[]",help='Input json text')
    argparser.add_argument('-o', '--output_file',default="./out.svg",help='Path of output svg file')

    return argparser.parse_args()
