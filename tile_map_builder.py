import sys
import json

# Use this to convert exported tilesets from tiled to python tilesets for the tilemap builder

tilejson = open(sys.argv[1], 'r')
tileset = json.load(tilejson)
tilejson.close()

out = open(sys.argv[1].replace('json', 'py'), 'w')

out.write('import pygame\n\ntile_images = {\n')

for tile in tileset['tiles']:
    out.write(f"    {tile['id']} : pygame.image.load(\"{tile['image']}\"),\n")

out.write('}')