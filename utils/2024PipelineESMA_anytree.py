from anytree import Node
from anytree.exporter import DictExporter
import pprint


'''# Templates
def assetTemplate(parent_node, asset_name):
    asset_root = Node(asset_name, parent=parent_node)
    # Asset subfolders
    houdini = Node('houdini', parent=asset_root)
    houdiniProject(houdini)
    Node('maya', parent=asset_root)
    # TODO build maya subfolders
    nuke = Node('nuke', parent=asset_root)
    inputOutput(nuke)
    Node('paint_2D', parent=asset_root)
    paint = Node('paint_3D', parent=asset_root)
    Node('mari', parent=paint)
    Node('substance', parent=paint)
    photogrammetry = Node('photogrammetry', parent=asset_root)
    inputOutput(photogrammetry)
    Node('preprod', parent=asset_root)
    Node('review', parent=asset_root)
    Node('sculpt', parent=asset_root)
    wrap = Node('wrap', parent=asset_root)
    inputOutput(wrap)'''


# Main folders
def preProd(parent_node):
    node6 = Node('01_scenario', parent=parent_node)
    Node('edit', parent=node6)
    Node('publish', parent=node6)
    node7 = Node('02_storyboard', parent=parent_node)
    Node('edit', parent=node7)
    Node('publish', parent=node7)
    node9 = Node('03_lumascript', parent=parent_node)
    Node('edit', parent=node9)
    Node('publish', parent=node9)
    node10 = Node('04_colorscript', parent=parent_node)
    Node('edit', parent=node10)
    Node('publish', parent=node10)
    node11 = Node('05_key_shot', parent=parent_node)
    Node('edit', parent=node11)
    Node('publish', parent=node11)
    node12 = Node('06_concept_design', parent=parent_node)
def Print(parent_node):
    template_print = Node('_template_print', parent=parent_node)
    mayaPrintProject(template_print)
def editing(parent_node):
    Node('input_shot', parent=parent_node)
    Node('input_sound', parent=parent_node)
    Node('output', parent=parent_node)
def asset(parent_node):
    Node('character', parent=parent_node)
    Node('FX', parent=parent_node)
    Node('item', parent=parent_node)
    Node('prop', parent=parent_node)
    Node('set', parent=parent_node)
def shot(parent_node):
    Node('_credits', parent=parent_node)
    Node('_masterCamera', parent=parent_node)
    Node('_RLO_roughLayout', parent=parent_node)
    Node('_TLO_sequenceLayout', parent=parent_node)


# Software Projects
def houdiniProject(parent_node):
    Node('abc', parent=parent_node)
    Node('audio', parent=parent_node)
    Node('comp', parent=parent_node)
    Node('desk', parent=parent_node)
    Node('flip', parent=parent_node)
    Node('geo', parent=parent_node)
    Node('hdz', parent=parent_node)
    Node('render', parent=parent_node)
    Node('scripts', parent=parent_node)
    Node('sim', parent=parent_node)
    Node('tex', parent=parent_node)
    Node('video', parent=parent_node)
def mayaProject(parent_node):
    cache = Node('cache', parent=parent_node)
    Node('bifrost', parent=cache)
    Node('nCache', parent=cache)
    Node('particles', parent=cache)
    Node('data', parent=parent_node)
    Node('images', parent=parent_node)
    Node('movies', parent=parent_node)
    Node('scenes', parent=parent_node)
    Node('sound', parent=parent_node)
    sourceimages = Node('sourceimages', parent=parent_node)
    Node('3dPaintTextures', parent=sourceimages)
    Node('environment', parent=sourceimages)
    Node('imagePlane', parent=sourceimages)
    Node('imageSequence', parent=sourceimages)


# Variants
def mayaPrintProject(parent_node):
    Node('assets', parent=parent_node)
    Node('autosave', parent=parent_node)
    cache = Node('cache', parent=parent_node)
    Node('bifrost', parent=cache)
    Node('nCache', parent=cache)
    Node('particles', parent=cache)
    Node('clips', parent=parent_node)
    Node('data', parent=parent_node)
    images = Node('images', parent=parent_node)
    Node('edits', parent=images)
    Node('movies', parent=parent_node)
    postprod = Node('postprod', parent=parent_node)
    inputOutput(postprod)
    renderData = Node('renderData', parent=parent_node)
    Node('depth', parent=renderData)
    fur = Node('fur', parent=renderData)
    Node('furAttrMap', parent=fur)
    Node('furEqualMap', parent=fur)
    Node('furFiles', parent=fur)
    Node('furImages', parent=fur)
    Node('furShadowMap', parent=fur)
    Node('iprImages', parent=renderData)
    Node('shaders', parent=renderData)
    Node('renderman', parent=parent_node)
    scenes = Node('scenes', parent=parent_node)
    Node('backup', parent=scenes)
    Node('edits', parent=scenes)
    Node('scripts', parent=parent_node)
    Node('sound', parent=parent_node)
    sourceimages = Node('sourceimages', parent=parent_node)
    Node('3dPaintTextures', parent=sourceimages)
    Node('edits', parent=sourceimages)
    Node('environment', parent=sourceimages)
    Node('imagePlane', parent=sourceimages)
    Node('imageSequence', parent=sourceimages)


# Utils
def inputOutput(parent_node):
    Node('input', parent=parent_node)
    Node('output', parent=parent_node)


# Create the tree structure
root = Node('projectName')
management = Node('00_management', parent=root)
external_data = Node('01_external_data', parent=root)
ressource = Node('02_ressource', parent=root)
preprodFolder = Node('03_preprod', parent=root)
preProd(preprodFolder)
assetFolder = Node('04_asset', parent=root)
asset(assetFolder)
shotFolder = Node('05_shot', parent=root)
shot(shotFolder)
review = Node('06_review', parent=root)
editingFolder = Node('07_editing', parent=root)
editing(editingFolder)
test = Node('08_test', parent=root)
printFolder = Node('09_print', parent=root)
Print(printFolder)
jury = Node('10_jury', parent=root)


# Export the tree as nested dictionaries
exporter = DictExporter()
nested_dict = exporter.export(root)

# Print the nested dictionaries
pprint.pprint(nested_dict)

