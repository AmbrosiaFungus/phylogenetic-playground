from ete3 import TextFace, faces, AttrFace, TreeStyle, NodeStyle, PhyloTree, ImgFace
from PyQt4 import QtCore
from PyQt4.QtGui import QGraphicsRectItem, QGraphicsSimpleTextItem, \
QGraphicsPolygonItem, QGraphicsTextItem, QPolygonF, \
     QColor, QPen, QBrush, QFont


def get_example_tree():

    t = PhyloTree('partition.nxs.treefile')

    # delete nodes supported less than 70% in Bootstrap
    for node in t.get_descendants():
        if not node.is_leaf() and node.support <= 70:
            node.delete()
    #set size to 0

    style2 = NodeStyle()
    style2["fgcolor"] = "#000000"
    style2["shape"] = "circle"
    style2["size"]=0
    for l in t.iter_leaves():
        l.img_style = style2


    #set the box around the commmon ancestor

    nst1 = NodeStyle()
    nst1["bgcolor"] = "LightSteelBlue"
    nst2 = NodeStyle()
    nst2["bgcolor"] = "SteelBlue"
    nst3 =NodeStyle()
    nst3["bgcolor"] = "PaleTurquoise"
    nst4 = NodeStyle()
    nst4["bgcolor"] = "PowderBlue"

    n1 = t.get_common_ancestor("CMW50197_Raffaelea_kentii_sp._nov.", "CMW49902_Raffaelea_kentii_sp._nov.")
    n1.set_style(nst1)

    n2 = t.get_common_ancestor("Raffaelea_sulphurea", "Raffaelea_quercivora")
    n2.set_style(nst2)

    n3 = t.get_common_ancestor("Raffaelea_cyclorhipidia", "Raffaelea_subalba")
    n3.set_style(nst3)

    n4 = t.get_common_ancestor("Raffaelea_lauricola", "Raffaelea_brunnea")
    n4.set_style(nst4)


    #TextFace for Raffaelea sulphurea

    Raff_Sulphurea_complex = TextFace("Raffaelea sulphurea")
    Raff_Sulphurea_complex.margin_left = 100
    Raff_Sulphurea_complex.margin_bottom = 20
    Raff_Sulphurea_complex.fsize = 15
    Raff_Sulphurea_complex.fstyle = "italic"

    complex_text = TextFace("complex")
    complex_text.fsize = 15
    complex_text.margin_left = 15
    complex_text.margin_bottom = 20

    #Textface for Raffaelea lauricola

    Raff_Lauri_complex = TextFace("Raffaelea lauricola")
    Raff_Lauri_complex.margin_left = 200
    Raff_Lauri_complex.margin_top = 20
    Raff_Lauri_complex.fsize = 15
    Raff_Lauri_complex.fstyle = "italic"

    complex_text_l = TextFace("complex")
    complex_text_l.fsize = 15
    complex_text_l.margin_left = 15
    complex_text_l.margin_top = 20

    # Textface for Raffaelea lauricola

    Raff_Aus = TextFace("Raffaelea")
    Raff_Aus.margin_left = 5
    Raff_Aus.fsize = 15
    Raff_Aus.fstyle = "italic"


    Aus = TextFace("Australian Clade of ")
    Aus.fsize = 15
    Aus.margin_left = 100



    # Where are the different Raffaelea complex
    sulphurea = t & ("Raffaelea_sulphurea")
    sulphurea.add_face(complex_text, column=2, position="branch-right")
    sulphurea.add_face(Raff_Sulphurea_complex,column=1, position="branch-right")
    #sulphurea.add_face(Raff_Ai, column=1, position = "branch-right")

    lauricola = t & ("Raffaelea_lauricola")
    lauricola.add_face(Raff_Lauri_complex, column=1, position = "branch-right")
    lauricola.add_face(complex_text_l, column=2, position = "branch-right")

    Raff_kentii = t & ("CMW50200_Raffaelea_kentii_sp._nov")
    Raff_kentii.add_face(Aus, column=1, position = "branch-right")
    Raff_kentii.add_face(Raff_Aus, column=2, position = "branch-right")





    # Set the path in which images are located
    img_path = "./"
    # Raff_Ai = faces.ImgFace(img_path + "Fig2_CMW49901.png")

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
    underscore = node.name.replace("_", " ")
    words = underscore.split()
    text = []
    if len(words) < 2:
        # some sort of acronym or bin name, leave it alone
        text = words
    elif len(words) > 2:
        if len(words) >= 5:
            text.extend([words[0] + ' <i> ' + words[1], words[2] + ' </i> '])
            text.extend(words[3:])

        else:
            # assume that everything after the
            # second word is strain name
            # which should not get italicized
            text.extend([' <i> ' + words[0], words[1] + ' </i> '])
            text.extend(words[2:])
    else:
        text.extend([' <i> ' + words[0], words[1] + ' </i> '])

    scientific_name_text.setHtml(' '.join(text))

    # below is a bit of a hack - I've found that the height of the bounding
    # box gives a bit too much padding around the name, so I just minus 10
    # from the height and recenter it. Don't know whether this is a generally
    # applicable number to use
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
        #temp = node.name.split('_')
        #sp = temp[0] + ' ' + temp[1]
        #faces.add_face_to_node(TextFace(sp, fsize=18, fstyle='italic'),node, column=0)
        #faces.add_face_to_node(AttrFace("name", fstyle="italic"), node, column=0, )
        F = faces.DynamicItemFace(scientific_name_face)
        F.margin_left = 10
        faces.add_face_to_node(F, node, 0)


if __name__ == "__main__":
    t, ts = get_example_tree()
    #t.show(tree_style=ts)
    t.render("style.png", tree_style=ts, dpi=600)

