# sensesGraphBuilder
This is a tool that translates text to graphs with [graphviz](https://graphviz.readthedocs.io/en/stable/) and regex

# Use
run the script with the only argument being the path to a text file containing a graph definition. This will generate an svg of the same name.

# Format

A node is denoted `<Label>:<TYPE>:<NUM>`  

An edge is denoted either `<NODE><Connector><NODE>`  
    where nodes can be either `<TYPE>:<NUM>` or `<Label>`  
    Connectors can be one of -/<-> for bidirectional -> for forwards or <- for backwards  

An example graph is:  

\<g>  (Tag for makeGrapsInMD)
![graph](Generated\ReadME_E\Graph0.svg)
<details>
<summary> Graph body </summary>



`Physical Phenomenon:PP:1->Energy Translation:ET:1`  

`Energy Translation->Processing result:PR:1`  

`PR:1->Dependent Processing result:PR:2`  

`PR:2->ET:1 #comment`  

`PR:2->OM:1`  

`inline comment can be made wherever`  

`OM:1->Processing result Dependent on all others:PR:3`  

`PR:3->OM:2`



</details>
\</g>

This gets turned into :  
![Example graph](README.svg)

by running `python graphbuilder.py README.md` it's beautiful all the stuff that isn't a graph is simply ignored.

# Make graphs in MD

This lets you embed a graph in md (contained within \<g> tags).
See ReadME_E.md for an example it was generated with `python makeGraphsInMD.py README.md ReadME_E.md`