import shutil
import os
import math
from PIL import Image, ImageOps, ImageDraw, ImageFont
import glob

def normalize(file, page_format):   
    try:
        pieces = Image.open(file).convert("RGBA")
    except FileNotFoundError:
        print("The pieces file could not be found! Make sure the path is correct")
        raise SystemExit(1)        

    try:
        dpi = int(pieces.info.get("dpi", (None, None))[0])
    except TypeError:
        print("Image has no set DPI!")
        raise SystemExit(1)
    
    os.makedirs("temp", exist_ok=True)
    
    pieces = ImageOps.expand(pieces, 5, "white")
    pieces_wpx, pieces_hpx = pieces.size
    
    if pieces_wpx > pieces_hpx:
        pieces = pieces.rotate(90, expand=True)
        pieces_wpx, pieces_hpx = pieces.size
    
    margin_float = (10 * dpi) / 25.4
    half_margin = math.ceil(margin_float)
    margin = half_margin * 2
    
    if page_format == "us_letter":
        cont_hpx = int(((279.4 * dpi) / 25.4) - margin) #980 96 dpi
        cont_wpx = int(((215.9 * dpi) / 25.4) - margin) #740 96 dpi
    elif page_format == "a4":
        cont_hpx = math.ceil(((297 * dpi) / 25.4)) - margin # 1123 96 dpi
        cont_wpx = math.ceil(((210 * dpi) / 25.4)) - margin #794 96 dpi
    
    target_h = ((pieces_hpx + cont_hpx - 1) // cont_hpx) * cont_hpx
    target_w = ((pieces_wpx + cont_wpx - 1) // cont_wpx) * cont_wpx
    
    norm_pieces = Image.new("RGB", (target_w, target_h), "white")
    norm_pieces.paste(pieces, (1, 1), pieces)
                                    
    norm_pieces.save("temp/normalized_pieces.png")
    
    return half_margin, cont_wpx, cont_hpx

def tile_normal(measures):
    
    margin, cont_w, cont_h = measures
 
    norm_pieces = Image.open("temp/normalized_pieces.png")
    npieces_w, npieces_h = norm_pieces.size
     
    num_cols = npieces_w // cont_w
    num_rows = npieces_h // cont_h
     
    for row in range(num_rows):
        for col in range(num_cols):
            left = col * cont_w
            top = row * cont_h
            right = left + cont_w
            bottom = top + cont_h
            box = (left, top, right, bottom)
            cropped_tile = norm_pieces.crop(box)
            
            page = ImageOps.expand(cropped_tile, (margin, margin), "white")
            
            row_letter = chr(ord("a") + row)
            
            page.save(f"temp/{row_letter}{col+1}.png")
            
    return margin

def draw_guides(margin):
    
    font = ImageFont.truetype("res/trim.ttf", 16)
    
    for filename in os.listdir("temp/"):
        if not filename.lower().endswith(".png"):
            continue
        
        cut_icon = Image.open("res/scissor.png")
        icon_w, icon_h = cut_icon.size
        
        tile_path = os.path.join("temp/", filename)
        tile_coord = os.path.splitext(filename)[0].lower()
        
        with Image.open(tile_path) as tile:
            draw = ImageDraw.Draw(tile)
            tile_w, tile_h = tile.size
            
            b_margin = margin - 1
            x1 = b_margin
            y1 = b_margin
            x2 = tile_w - b_margin - 1
            y2 = tile_h - b_margin - 1
            
            is_top_row = tile_coord.startswith("a")
            is_not_a1 = not tile_coord == "a1"
            is_not_first_col = not tile_coord[-1] == "1"
            
            cut_top = not is_top_row
            cut_left = (is_top_row and is_not_a1) or is_not_first_col
            
            draw.line([(x2, y1), (x2, y2)], fill="black", width=1)
            draw.line([(x1, y2), (x2, y2)], fill="black", width=1)
            
            if cut_top:
                tile.paste(cut_icon, (x2 - icon_w//2, y1 - icon_h//2), cut_icon)
                
                for x in range(x1, x2, 8):
                    draw.line([(x, y1), (min(x+5, x2), y1)], fill="black", width=1)
            else:
                draw.line([(x1, y1), (x2, y1)], fill="black", width=1)
                
            if cut_left:
                cut_icon = cut_icon.rotate(270, expand=True)
                tile.paste(cut_icon, (x1 - icon_w//2, y2 - icon_h//2), cut_icon)
                
                for y in range(y1, y2, 8):
                    draw.line([(x1, y), (x1, min(y+5, y2))], fill="black", width=1)
            else:
                draw.line([(x1, y1), (x1, y2)], fill="black", width=1)
            
            coord_label = tile_coord.upper()
            label_width = draw.textlength(coord_label, font=font)
            label_x = (tile_w - label_width) // 2
            label_y = tile_h - margin + 5
            
            draw.text((label_x, label_y), coord_label, fill="black",font=font)
            
            tile.save(tile_path)
            
    os.remove("temp/normalized_pieces.png")

def pdf(file, page_format):
    
    orig_pieces_name = os.path.splitext(file)[0].lower() + "_" + page_format + "_tiled.pdf"
    
    pieces = Image.open(file)
    dpi = int(pieces.info.get("dpi", (None, None))[0])
    
    pngs = sorted(glob.glob("temp/*.png"))
    
    if page_format == "us_letter":
        page_size = (8.5*72, 11*72)
    elif page_format == "a4":
        page_size = (595, 842)
    
    tiles = [Image.open(f).convert("RGB") for f in pngs]

    tiles[0].save(
       orig_pieces_name,
       save_all=True,
       format="PDF",
       append_images=tiles[1:],
       resolution=dpi,
       quality=100,
       paper_size=page_size
    )
    shutil.rmtree("temp")
    print("Tiled PDF has been created succesfully!")
    print(f"{orig_pieces_name}")

print("This script will take exported pattern pieces from Seamly2D \nand convert them into a tiled PDF in either US Letter o A4 format. \nIt will work with patterns exported from other software \nif the DPI/resolution of the image is set correctly. \n ")

input_image = input("Pieces file location (Example: C:\\Users\\Username\\Pictures\\basic_block.png): ")
input_pformat = input("Set page format (1 for US Letter, 2 for A4): ")

if input_pformat == "1":
    page_format = "us_letter"
elif input_pformat == "2":
    page_format = "a4"
else:
    print(f"{input_pformat} is not 1 or 2...")
    raise SystemExit(1)

draw_guides(tile_normal(normalize(input_image, page_format)))
pdf(input_image, page_format)