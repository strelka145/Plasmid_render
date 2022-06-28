# Plasmid_render
CLI tool to illustrate plasmids with a structure described by json.

![Example Image](/test/SVG.svg)

This program is a CLI tool that can describe the plasmid structure in json and output it as an image in SVG format.  

The output is in vector format, so there is no possibility of poor quality images being output.

## Usage

### Prerequisites
- Python3

### Install
Install using pip.

```
pip install plasmidrender
```

### Json file notation

![Example Image](/test/SVG.svg)

If you want to draw a plasmid like the one shown in the figure, you can write a json like this.

```json
[
  {"type":"arrow","angle":10,"label":"primer","color":"black"},
  {"type":"space","angle":10},
  {"type":"tag","angle":45,"label":"EGFP","color":"green"},
  {"type":"space","angle":10},
  {"type":"arrow","angle":-10,"label":"primer","color":"black"},
  {"type":"space","angle":20},
  {"type":"tag","angle":60,"label":"RFP","color":"red"},
  {"type":"tag","angle":60,"label":"BFP","color":"#1E90FF"},
  {"type":"space","angle":30},
  {"type":"line","angle":45,"label":"BamHI","color":"black"}
]
```
[For a detailed explanation, please click here.](/Description/json.md "Writing json")

### Using from the command line

#### Output from a json file

SVG

```
plasmidrender -i (Path of input json file) --output_svg_file (Path of output a svg file)
```

png

```
plasmidrender -i (Path of input json file) --output_png_file (Path of output a png file)
```

#### Output from json string

SVG

```
plasmidrender --input_json (Path of input json file) --output_svg_file (Path of output svg file)
```

png

```
plasmidrender --input_json (Path of input json string) --output_png_file (Path of output a png file)
```

### Using as a Python module

```python
import plasmidrender

plasmidrender.draw(input_json="/path/to/input.json",output_svg_file="/path/to/output.svg")
```

```python
import plasmidrender

jsoncode=(
  '  ['
  '{"type":"arrow","angle":10,"label":"primer","color":"black"},'
  '{"type":"space","angle":10},'
  '{"type":"tag","angle":45,"label":"EGFP","color":"green"},'
  '{"type":"space","angle":10},'
  '{"type":"arrow","angle":-10,"label":"primer","color":"black"},'
  '{"type":"space","angle":20},'
  '{"type":"tag","angle":60,"label":"RFP","color":"red"},'
  '{"type":"tag","angle":60,"label":"BFP","color":"#1E90FF"},'
  '{"type":"space","angle":30},'
  '{"type":"line","angle":45,"label":"BamHI","color":"black"}'
']'
)
plasmidrender.draw(input_file=jsoncode,output_png_file="output.png")
```

### Output as png format

```
python3 main.py -i (Path of input json file) --output_png_file (Path of output png file)
```


### Future
- To be able to change the text style
- Allow the hight of a annular sector to be changed
- Allow adjustable line thickness

### More future
- Restriction Enzyme Indication
- Show primer
- Show translation direction
