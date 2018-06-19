from ete3 import TextFace, faces, AttrFace, TreeStyle, NodeStyle, PhyloTree, ImgFace

def layout(node):
    # If node is a leaf, add the nodes name and a its scientific name
    if node.is_leaf():
        faces.add_face_to_node(AttrFace("name"), node, column=0)

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

    # Set the path in which images are located
    img_path = "./"
    Raff_Ai = faces.ImgFace(img_path + "Fig2_CMW49901.png")



    #set the box around the commmon ancestor

    nst1 = NodeStyle()
    nst1["bgcolor"] = "LightSteelBlue"
    nst2 = NodeStyle()
    nst2["bgcolor"] = "SteelBlue"
    nst3 =NodeStyle()
    nst3["bgcolor"] = "PaleTurquoise"
    nst4 = NodeStyle()
    nst4["bgcolor"] = "PowderBlue"

    n1 = t.get_common_ancestor("CMW_50197__Raffaelea_kentii_sp._nov.", "CMW_49902__Raffaelea_kentii_sp._nov.")
    n1.set_style(nst1)

    n2 = t.get_common_ancestor("Raffaelea_sulphurea", "Raffaelea_quercivora")
    n2.set_style(nst2)

    Raff_complex = TextFace("Raffaelea sulphurea complex")
    Raff_complex.margin_left = 100
    Raff_complex.margin_bottom =20
    Raff_complex.fsize = 20

    # # Set the path in which images are located
    # img_path = "./"
    # Raff_Ai = faces.ImgFace(img_path + "Fig2_CMW49901.png")
    #
    # #Specify the boundaries of the Image, how big do you want it
    # Raff_Ai.width = 200
    # Raff_Ai.height = 200
    # # How much to the left do you want the Image
    # Raff_Ai.margin_left = 200


    sulphurea = t & ("Raffaelea_sulphurea")
    sulphurea.add_face(Raff_complex ,column=1, position="branch-right")
    #sulphurea.add_face(Raff_Ai, column=1, position = "branch-right")


    n3 = t.get_common_ancestor("Raffaelea_cyclorhipidia", "Raffaelea_subalba")
    n3.set_style(nst3)

    n4 = t.get_common_ancestor("Raffaelea_lauricola", "Raffaelea_brunnea")
    n4.set_style(nst4)







    ts = TreeStyle()
    ts.show_branch_length = False  # show branch length
    ts.show_branch_support = True  # show support
    ts.show_leaf_name = False
    ts.branch_vertical_margin = 1  # 10 pixels between adjacent branches
    ts.scale = 2000  # 120 pixels per branch length unit
    ts.layout_fn = layout

    return t, ts

if __name__ == "__main__":
    t, ts = get_example_tree()
    #t.show(tree_style=ts)
    t.render("node_style.png", tree_style=ts, dpi=600)
