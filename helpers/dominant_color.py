from PIL import Image, ImageDraw

def dominant_color(im, exclude):
    colors = {}
    colors_list = []

    if exclude == "default":
        exclude = [
            "247253255",
            "250243221",
            "255255255",
            "000000000"
        ]

    im = im.resize((16, 16), Image.NEAREST).convert("RGBA")

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            color = str(im.getpixel((i,j))[0]).zfill(3) + str(im.getpixel((i,j))[1]).zfill(3) + str(im.getpixel((i,j))[2]).zfill(3)
            if not color in exclude:
                if not color in colors:
                    colors[color] = 1
                else:
                    colors[color] = colors[color] + 1

    keys = list(colors.keys())
    values = list(colors.values())

    for x in zip(keys,values):
        colors_list.append({"color": x[0], "count": x[1]})

    colors_list.sort(key=lambda x: 1 / x["count"])

    return colors_list

def domimant_to_rgb(color):
    red = int(color[0:3])
    gre = int(color[3:6])
    blu = int(color[6:9])
    rgb = 65536 * red + 256 * gre + blu
    return rgb

def domimant_to_hex(color):
    red = int(color[0:3])
    gre = int(color[3:6])
    blu = int(color[6:9])
    return '#%02x%02x%02x' % (red,gre,blu)