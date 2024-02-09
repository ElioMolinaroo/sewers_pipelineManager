from anytree import Node
from anytree.exporter import DictExporter

import pprint

# Utils
def inputOutput(parent_node):
    Node('input', parent=parent_node)
    Node('output', parent=parent_node)


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
    Node('workFiles', parent=parent_node)


def mayaProject(parent_node):
    cache = Node('cache', parent=parent_node)
    Node('alembic', parent=cache)
    Node('bifrost', parent=cache)
    Node('nCache', parent=cache)
    Node('particles', parent=cache)
    Node('data', parent=parent_node)
    Node('images', parent=parent_node)
    Node('movies', parent=parent_node)
    scenes = Node('scenes', parent=parent_node)

    edit = Node('edit', parent=scenes)
    Node('assetLayout', parent=edit)
    Node('cloth', parent=edit)
    Node('dressing', parent=edit)
    Node('groom', parent=edit)
    Node('lookdev', parent=edit)
    Node('modeling', parent=edit)
    Node('rig', parent=edit)

    publish = Node('publish', parent=scenes)
    Node('assetLayout', parent=publish)
    Node('cloth', parent=publish)
    Node('dressing', parent=publish)
    Node('groom', parent=publish)
    Node('lightRig', parent=publish)
    Node('lookdev', parent=publish)
    Node('modeling', parent=publish)
    Node('rig', parent=publish)
    Node('shader', parent=publish)

    Node('sound', parent=parent_node)
    sourceimages = Node('sourceimages', parent=parent_node)
    Node('3dPaintTextures', parent=sourceimages)
    Node('environment', parent=sourceimages)
    Node('imagePlane', parent=sourceimages)
    Node('imageSequence', parent=sourceimages)


root = Node('assetName')
# Asset subfolders
houdini = Node('houdini', parent=root)
houdiniProject(houdini)
maya = Node('maya', parent=root)
mayaProject(maya)
nuke = Node('nuke', parent=root)
inputOutput(nuke)
paint2d = Node('paint_2D', parent=root)
Node('photoshop', parent=paint2d)
Node('procreate', parent=paint2d)
paint3d = Node('paint_3D', parent=root)
Node('mari', parent=paint3d)
Node('substance', parent=paint3d)
Node('preprod', parent=root)
Node('review', parent=root)
Node('sculpt', parent=root)


# Export the tree as nested dictionaries
exporter = DictExporter()
nested_dict = exporter.export(root)

# Print the nested dictionaries
pprint.pprint(nested_dict)

