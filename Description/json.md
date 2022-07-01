# Json file notation

Use json of a list of dictionary type objects.

# type  
A necessary key. The `type` key specifies the shape to be drawn.

## tag ("type":"tag")
Drawing of an annular sector.

![Example Image](/Description/images/fig1.png)

### angle ("type":"tag","angle":45)
A necessary key. Specify the angle of θ in the figure above. Angles are given in degrees, NOT in arc degrees.

### label ("type":"tag","label":"text")
A necessary key. Specify the string to be displayed. If you do not want anything to be displayed, specify an empty string (`""`).

### color ("type":"tag","color":"red")
A necessary key. Specifies the color to be filled. Colors can be specified as in Web colors.

## space

## arrow

## line
