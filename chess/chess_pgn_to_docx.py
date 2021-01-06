import chess
import chess.pgn
import chess.svg
import os

from docx import Document
from docx.shared import Inches, Cm
from cairosvg import svg2png

style_black_and_white = '''
.square.light { fill: #cacaca; }
.square.dark  { fill: #898989; }
.square.light.lastmove { fill: #c3d889; }
.square.dark.lastmove { fill: #92b167; }
.check { fill: url(#check_gradient); }
.arrow { stroke: #ff5858; fill: #ff5858; }
.mark { stroke: #959fff; fill: #959fff;}
'''

style_mono_print = '''
.square.light { fill: #ffffff; }
.square.dark  { fill: #cacaca; }
.square.light.lastmove { fill: #ffffff; stroke: #000000;  stroke-width: 5;  stroke-linecap: butt;  stroke-dasharray: 0; }
.square.dark.lastmove { fill: #797979; stroke: #000000;  stroke-width: 5;  stroke-linecap: butt;  stroke-dasharray: 0; }
.check { fill: url(#check_gradient); }
.arrow { stroke: #ff5858; fill: #ff5858; }
.mark { stroke: #959fff; fill: #959fff;}
'''

def set_number_of_columns(section, cols):
    """ sets number of columns through xpath. """
    # # https://github.com/python-openxml/python-docx/issues/167
    WNS_COLS_NUM = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num"
    section._sectPr.xpath("./w:cols")[0].set(WNS_COLS_NUM, str(cols))

def set_margin(section):
    # changing the page margins => https://stackoverflow.com/questions/32914595/modify-docx-page-margins-with-python-docx
    # section.top_margin = Cm(0.5)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

def pgn_to_docx(workspace, pgn_filename, docx_filename,svg_style=None, flipped=False):
    temp_svg_file = "chess_pgn_to_docx_temp_svg.svg"
    temp_png_file = "chess_pgn_to_docx_temp_svg.png"

    document = Document()
    document.add_heading(pgn_filename, 0)
    sections = document.sections
    for section in sections:
        set_margin(section)
        set_number_of_columns(section,3)

    pgn = open(workspace + pgn_filename, encoding="utf-8")
    first_game = chess.pgn.read_game(pgn)
    print("Game Inforamtion:\n" + str(first_game) + "\n")

    comment_map = {}
    san_map = {}
    last_node = first_game.root()
    idx = 0

    while last_node.variations:
        # TODO: for variations.
        idx = idx + 1
        last_node = last_node.variations[0]
        comment_map[idx] = last_node.comment
        san_map[idx] = str(last_node.san())
        print("# " + str(idx))
        print("san: " + str(last_node.san())) #Comparing to last_node.move or last_node.uci(), we are familiar with SAN.
        print("variations: " + str(last_node.variations))
        print("comment: " + last_node.comment)
        if len(last_node.variations) > 1:
            another_node = last_node.variations[1]
            print("Other variations: " + str(another_node.variations))
        print("")


    board = first_game.board()
    index = 1
    white = True
    for move in first_game.mainline_moves():
        board.push(move)
        current_svg = chess.svg.board(board=board, lastmove=move, flipped=flipped, size=400, style=svg_style)

        turn = ""
        old_index = index
        old_white = white

        # create svg file.
        f = open(workspace + temp_svg_file, "w")
        f.write(current_svg)
        f.close()

        if white:
            turn = "White"
            white = False # change it for next loop
        else:
            turn = "Black"
            white = True # change it for next loop
            index += 1

        # update the docx file.
        if old_white:
            write_step = san_map[old_index*2 -1]
            blank_step = "-"
            if old_index * 2 in san_map:
                blank_step = san_map[old_index * 2]
            #document.add_paragraph("## Step "+ str(old_index) +": " + write_step + ", " + blank_step , style='List Number')
            p = document.add_paragraph("" , style='List Number')
            p.add_run(write_step + ", " + blank_step).bold = True
            comment = comment_map[old_index*2 -1]
        else:
            if old_index * 2 in comment_map:
                comment = comment_map[old_index * 2]
            else:
                comment = ""

        with open(workspace + temp_svg_file, 'r') as content_file:
            content = content_file.read()
            svg2png(bytestring=content, write_to=temp_png_file)
        document.add_picture(temp_png_file, width=Inches(2.2))
        if comment:
            document.add_paragraph(turn + " Comment: " + comment )


    print("Final status of this PGN file.")
    print(board)
    document.save(docx_filename)

    os.remove(temp_svg_file)
    os.remove(temp_png_file)

if __name__ == '__main__':
    workspace = "./"
    pgn_filename = "B33-42.pgn"
    docx_filename = pgn_filename.replace(".pgn","") + ".docx"

    #pgn_to_md(pgn_filename, workspace, svg_style=style_black_and_white)
    #pgn_to_docx(workspace, pgn_filename, docx_filename, svg_style=style_mono_print)
    pgn_to_docx(workspace, pgn_filename, docx_filename, svg_style=style_mono_print, flipped=True)
