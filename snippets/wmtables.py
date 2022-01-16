import wikitextparser as wtp
from pathlib import Path

path = Path("/Users/kraemer/Dropbox/Teaching/TTM4115/website/tables/week3.mw")
with open(path, "r", encoding="utf-8", errors="surrogateescape") as file:
    string = file.read()
    t = wtp.Table(string)

    print(t.cells(span=False))

    def get_colspan(cell):
        if "colspan" in cell.attrs:
            return 'colspan="{}" '.format(cell.attrs["colspan"])
        return ""

    def get_rowspan(cell):
        if "rowspan" in cell.attrs:
            return 'rowspan="{}" '.format(cell.attrs["rowspan"])
        return ""

    for row in t.cells(span=False):
        print("-----")
        for cell in row:

            if cell is not None:

                # if "colspan" in cell.attrs:
                #    print(" col:   {}".format(cell.attrs["colspan"]))
                # if "rowspan" in cell.attrs:
                #    print(" row:   {}".format(cell.attrs["rowspan"]))
                # print(cell)
                print(cell.value)
