import sys
import os
from graphbuilder import makeGraph

if __name__ == "__main__":
    
    from genericpath import exists
    import sys

    if not exists(sys.argv[1]):
        print("Please pass a path to a md file to embed your graph")

    i = 0
    outFile = sys.argv[2]
    while exists(outFile) and not "-force" in sys.argv:
        outFile = f"""{".".join(sys.argv[2].split(".")[:-1])} {i} .md"""
        i+=1
    else:
        if i > 0:
            print(f"Creating new file {outFile} because passed name exists to override pass -force")

    Gname = 0
    with open(sys.argv[1], 'r') as fin:
        try:
            with open(outFile, 'w') as fout:
                for line in fin:
                    if "<g>\n" == line:
                        graphFileName = os.path.join("Generated", ".".join(outFile.split(".")[:-1]), f"Graph{Gname}")
                        fout.write(f"""![graph]({graphFileName}.svg)\n<details>\n<summary> Graph body </summary>\n\n""")
                        graphDesc = ""
                        line = line.replace("<g>", "")
                        while "</g>\n" != line and line:
                            graphDesc += line + "\n"
                            line = fin.readline()                        
                        graphDesc += line.replace("</g>", "")
                        makeGraph(graphDesc, filename=graphFileName).render()
                        fout.write(graphDesc)
                        fout.write("""\n</details>\n""")
                        Gname+=1

                    else:
                        fout.writelines((line))
        except OSError as e:
            print("")
            raise e
