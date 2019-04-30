from ete3 import TextFace, faces, AttrFace, TreeStyle, NodeStyle, PhyloTree, ImgFace
from PyQt4 import QtCore
from PyQt4.QtGui import QGraphicsRectItem, QFont ,QGraphicsPolygonItem,QGraphicsTextItem,QPolygonF,QColor, QPen, QBrush
import PyQt4.QtGui

def get_example_tree():

    t = PhyloTree('partition.nxs.treefile')

    # delete nodes supported less than 70% in Bootstrap
    #for node in t.get_descendants():
        #if not node.is_leaf() and node.support <= 90:
            #node.delete()
    #set size to 0

    #list_remove = []

    #for node in t.get_descendants():
        #if node.dist>0:
            
            #list_remove.append(node.name)
    
    #str_list = [x for x in list_remove if x]
    
    #t.prune(str_list)






    #style2 = NodeStyle()
    #style2["fgcolor"] = "#000000"
    #style2["shape"] = "circle"
    #style2["size"]=0
    #for l in t.iter_leaves():
        #l.img_style = style2


    #set the box around the commmon ancestor

    #nst1 = NodeStyle()
    #nst1["bgcolor"] = "LightSteelBlue"
    #nst2 = NodeStyle()
    #nst2["bgcolor"] = "SteelBlue"
    #nst3 =NodeStyle()
    #nst3["bgcolor"] = "PaleTurquoise"
    #nst4 = NodeStyle()
    #nst4["bgcolor"] = "PowderBlue"

    #n1 = t.get_common_ancestor("CMW50197_Raffaelea_kentii_sp._nov.", "CMW49902_Raffaelea_kentii_sp._nov.")
    #n1.set_style(nst1)

    #n2 = t.get_common_ancestor("Raffaelea_sulphurea", "Raffaelea_quercivora")
    #n2.set_style(nst2)

    #n3 = t.get_common_ancestor("Raffaelea_cyclorhipidia", "Raffaelea_subalba")
    #n3.set_style(nst3)

    #n4 = t.get_common_ancestor("Raffaelea_lauricola", "Raffaelea_brunnea")
    #n4.set_style(nst4)






    # Set the path in which images are located
    #img_path = "./"
    #Raff_Ai = faces.ImgFace(img_path + "Fig2_CMW49901.png")

    # Specify the boundaries of the Image, how big do you want it
    # Raff_Ai.width = 200
    # Raff_Ai.height = 200
    # How much to the left do you want the Image
    # Raff_Ai.margin_left = 200



    ts = TreeStyle()
    ts.show_branch_length = False  # show branch length
    ts.show_branch_support = True  # show support
    ts.show_leaf_name = False
    ts.branch_vertical_margin = 1  # 1 pixels between adjacent branches
    ts.scale = 2000  # 2000 pixels per branch length unit
    ts.layout_fn = layout


    return t, ts


def scientific_name_face(node, *args, **kwargs):
    scientific_name_text = QGraphicsTextItem()
    #underscore = node.name.replace("_", " ")
    words = node.name.split("_")
    text = []
    if len(words) < 2:
        # some sort of acronym or bin name, leave it alone
        text = words
    elif len(words) > 2:
        if len(words) >= 5:
            text.extend(['<b>' + words[0] + ' <i> ' + words[1], words[2] + ' </i> '])
            text.extend(words[3:] + ['</b>'])

        elif len(words) == 3:
            text.extend([' <span style="color:grey"><i> ' + words[0], words[1] + words[2] +'  </i></span>'])

        else:
            # assume that everything after the
            # second word is strain name
            # which should not get italicized
            text.extend([' <span style="color:grey"><i> ' + words[0], words[1] + '  </i></span>'])
            text.extend(words[2:])
    else:
        text.extend([' <span style="color:grey"><i> ' + words[0], words[1] + ' </i></span> '])

    scientific_name_text.setHtml(' '.join(text))

    # below is a bit of a hack - I've found that the height of the bounding
    # box gives a bit too much padding around the name, so I just minus 10
    # from the height and recenter it. Don't know whether this is a generally
    # applicable number to use
    #myFont = QFont()
    masterItem = QGraphicsRectItem(0, 0,
                                   scientific_name_text.boundingRect().width(),
                                   scientific_name_text.boundingRect().height() - 10)

    scientific_name_text.setParentItem(masterItem)
    center = masterItem.boundingRect().center()
    scientific_name_text.setPos(masterItem.boundingRect().x(),
                                center.y() - scientific_name_text.boundingRect().height() / 2)

    # I don't want a border around the masterItem
    masterItem.setPen(QPen(QtCore.Qt.NoPen))

    return masterItem



def layout(node):
    # If node is a leaf, add the nodes name and a its scientific name
    if node.is_leaf():
        F = faces.DynamicItemFace(scientific_name_face)
        if F.node == "DAR34208_Raffaelea_kilii_sp._nov.":
            F.background = "Black"
            faces.add_face_to_node(F, node, 0, )
        F.margin_left = 10
        faces.add_face_to_node(F, node, 0, )


if __name__ == "__main__":
    t, ts = get_example_tree()
    ts.scale = 120
    t.show(tree_style=ts)
    t.render("style.png", tree_style=ts, dpi=600)

