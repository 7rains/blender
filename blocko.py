import bpy
import json
import mathutils
from mathutils import Vector

gapSize = 0
boardSize = 8
level = '{"blocks":[{"color": "white", "coordinates": {"x": 1, "y": 1}}, {"color": "orange", "coordinates": {"x": 7, "y": 7}}], "tiles":[{"color": "blue", "coordinates": {"x": 2, "y": 2}}]}'
gd = json.loads(level)


def main():
  clearBoard()
  drawBoard()
  colorTiles(gd["tiles"])
  addBlocks(gd["blocks"])


def clearBoard():
  bpy.ops.object.select_pattern(pattern="Tile_*")
  bpy.ops.object.select_pattern(pattern="Block_*")
  bpy.ops.object.delete()


def drawBoard():
  for x in range(0, boardSize):
    for y in range(0, boardSize):
      gapX = gapSize * x
      gapY = gapSize * y
      tileObj = createCube('Tile_' + str(x) + '_' + str(y), Vector((x + gapX, y + gapY, -0.75)))
      tileObj.scale.z *= 0.5


def colorTiles(tiles):
  for t in tiles:
    coordinates = t['coordinates']
    color = t['color']
    tileObj = bpy.data.objects['Tile_'+str(coordinates['x'])+'_'+str(coordinates['y'])]
    tileObj.data.materials[0] = bpy.data.materials[color]
    

def addBlocks(blocks):
  for b in blocks:
    coordinates = b['coordinates']
    color = b['color']
    x = int(coordinates['x']) + (gapSize * int(coordinates['x']))
    y = int(coordinates['y']) + (gapSize * int(coordinates['y']))
    blockObj = createCube('Block_'+str(coordinates['x'])+'_'+str(coordinates['y']), Vector((x, y, 0)))

    # offset white tiles from white blocks and make white blocks smaller
    if color == 'white':
      color = 'light'
      blockObj.scale.z *=0.5
      blockObj.location.z -= 0.25

    blockObj.data.materials[0] = bpy.data.materials[color]
   

def createCube(name, origin):
  bpy.ops.mesh.primitive_cube_add(
    radius=0.5, 
    view_align=False, 
    enter_editmode=False, 
    location=origin, 
    rotation=(0, 0, 0))

  obj = bpy.context.object
  bevel = obj.modifiers.new('Bevel', 'BEVEL')
  bevel.width = 0.01
  obj.name = name
  obj.show_name = False
  obj.data.materials.append(bpy.data.materials['white'])
  obj.data.name = name
  return obj

 
if __name__ == '__main__':
  main()


# filename = '/Users/Steven_2/Documents/dev/blocko.py'
# exec(compile(open(filename).read(), filename, 'exec'))