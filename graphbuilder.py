from genericpath import exists
import graphviz
import re
import sys

NodeMatch = re.compile(r"((?P<label>[\w ]+):)?(?P<type>PP|PR|ET|OM):(?P<num>[0-9]+)", flags=re.MULTILINE)
EdgeMatch = re.compile(r"""(?P<name1>[\w :]+)(?P<connector><?->?)(?P<name2>[\w :]+)\s*(?P<comment>#[\w ]*)?""", flags=re.MULTILINE)


def addNodes(g: graphviz.Graph, txt: str, nickNames = {}):

    nodes = {}
    for node in re.finditer(NodeMatch, txt):
        nodeKwargs = {}

        nodeName = f"""{node.group("type")}{node.group("num")}"""

        if (nodeLabel := node.group("label")) is None:
            nodeLabel = f"""{node.group("type")}:{node.group("num")}"""
        else:
            nickNames[nodeLabel] = nodeName
            nodeKwargs["xlabel"] = f"""{node.group("type")}:{node.group("num")}"""

        nodeKwargs["label"] = nodeLabel

        if nodeName in nodes:
            if "label" in nodes[nodeName]:
                if node.group("label") is not None and node.group("label") != nodes[nodeName]["label"]:
                    raise NameError(f"""Node {nodeName} is defined with two labels {node.group("label")} {nodes[nodeName]["label"]}""")
                continue
            nodes[nodeName].update(node.groupdict())
        else:
            nodes.update({nodeName: node.groupdict()})

        nodeType = node.group("type")

        if nodeType == "PP":
            nodeKwargs["shape"] = "octagon"
        elif nodeType == "PR":
            nodeKwargs["shape"] = "ellipse"
        elif nodeType == "ET":
            nodeKwargs["shape"] = "invtrapezium"
        elif nodeType == "OM":
            nodeKwargs["shape"] = "plaintext"
            nodeKwargs["label"] = f"""<<TABLE BORDER="0" CELLBORDER="1" CELLPADDING="4" WIDTH="100"><TR><TD SIDES="TB" WIDTH="100">{nodeLabel}</TD></TR></TABLE>>"""

        g.node(nodeName, **nodeKwargs)

    return g, nickNames


def addEdges(g: graphviz.Graph, txt: str, nickNames = {}):

    for edge in re.finditer(EdgeMatch, txt):

        edgeKwargs = {}
        nodeNames = [None]*2

        for i, node in enumerate(edge.group("name1", "name2")):
            if node in nickNames:
                nodeNames[i] = nickNames[node]
            else:
                nodeDetails = re.match(NodeMatch, node)
                if not nodeDetails:
                    print(f"""Node {node} is invalid skipping the edge {edge}""")
                    continue
                nodeNames[i] = f"""{nodeDetails.group("type")}{nodeDetails.group("num")}"""

        if None in nodeNames:
            continue

        connection: str = edge.group("connector")
        if connection in ("<->", "-"):
            edgeKwargs["dir"] = "both"
        elif connection == "<-":
            edgeKwargs["dir"] = "back"
        elif connection == "->":
            edgeKwargs["dir"] = "forward"

        if (comment := edge.group("comment")) is not None:
            edgeKwargs["label"] = comment[1:]

        g.edge(nodeNames[0], nodeNames[1], **edgeKwargs)
    return g


if __name__ == "__main__":

    import os
    
    if not exists(sys.argv[1]):
        print("Please pass a path to a text file describing your graph as the only argument to this script")

    with open(sys.argv[1], "r") as f:
        graphDescr = f.read()

    g = graphviz.Digraph('G', filename=".".join(sys.argv[1].split(".")[:-1]), format="svg", engine="dot")
    #g.graph_attr["rankdir"] = "BT"

    g, nickNames = addNodes(g, graphDescr)
    g = addEdges(g, graphDescr, nickNames)

    g.render()
