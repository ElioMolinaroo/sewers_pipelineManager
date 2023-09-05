from anytree import Node
from anytree.exporter import DictExporter

# Create the tree structure
root = Node('projectName')
node1 = Node('00_management', parent=root)
node2 = Node('01_external_data', parent=root)
node3 = Node('02_ressource', parent=root)
node4 = Node('03_preprod', parent=root)
node5 = Node('04_workspace', parent=root)

node6 = Node('01_scenario', parent=node4)
Node('edit', parent=node6)
Node('publish', parent=node6)

node7 = Node('02_storyboom', parent=node4)
Node('edit', parent=node7)
Node('publish', parent=node7)

node8 = Node('03_fond_forme', parent=node4)
Node('edit', parent=node8)
Node('publish', parent=node8)

node9 = Node('04_lumascript', parent=node4)
Node('edit', parent=node9)
Node('publish', parent=node9)

node10 = Node('05_colorscript', parent=node4)
Node('edit', parent=node10)
Node('publish', parent=node10)

node11 = Node('06_key_shot', parent=node4)
Node('edit', parent=node11)
Node('publish', parent=node11)

node12 = Node('07_concept_design', parent=node4)

node13 = Node('houdini', parent=node5)
Node('abc', parent=node13)
Node('audio', parent=node13)
Node('comp', parent=node13)
Node('desk', parent=node13)
Node('flip', parent=node13)
Node('geo', parent=node13)
Node('hdz', parent=node13)
Node('render', parent=node13)
Node('scripts', parent=node13)
Node('sim', parent=node13)
Node('tex', parent=node13)
Node('video', parent=node13)

node14 = Node('maya', parent=node5)
node23 = Node('cache', parent=node14)
Node('alembic', parent=node23)
Node('bifrost', parent=node23)
Node('nCache', parent=node23)
Node('particles', parent=node23)

Node('data', parent=node14)
Node('images', parent=node14)
Node('movies', parent=node14)

node27 = Node('scenes', parent=node14)
node25 = Node('edit', parent=node27)
Node('assetLayout', parent=node25)
Node('dressing', parent=node25)
Node('groom', parent=node25)
Node('lookdev', parent=node25)
Node('modeling', parent=node25)
Node('rig', parent=node25)

node26 = Node('publish', parent=node27)
Node('assetLayout', parent=node26)
Node('dressing', parent=node26)
Node('geo', parent=node26)
Node('groom', parent=node26)
Node('lightRig', parent=node26)
Node('lookdev', parent=node26)
Node('rig', parent=node26)
Node('shader', parent=node26)

Node('shot', parent=node27)


Node('sound', parent=node14)

node24 = Node('sourceimages', parent=node14)
Node('3dPaintTextures', parent=node24)
Node('environment', parent=node24)
Node('imagePlane', parent=node24)
Node('imageSequence', parent=node24)


node15 = Node('nuke', parent=node5)
Node('input', parent=node15)
Node('output', parent=node15)

node16 = Node('paint_2D', parent=node5)

node17 = Node('paint_3D', parent=node5)
Node('mari', parent=node17)
Node('substance', parent=node17)

node18 = Node('photogrammetry', parent=node5)
Node('input', parent=node18)
Node('output', parent=node18)

node19 = Node('review', parent=node5)
Node('images', parent=node19)
Node('videos', parent=node19)

node20 = Node('sculpt', parent=node5)
node22 = Node('zbrush', parent=node20)
Node('input', parent=node22)
Node('output', parent=node22)

node21 = Node('wrap', parent=node5)
Node('input', parent=node21)
Node('output', parent=node21)








# Export the tree as nested dictionaries
exporter = DictExporter()
nested_dict = exporter.export(root)

# Print the nested dictionaries
print(nested_dict)

