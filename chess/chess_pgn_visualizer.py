import chess
import chess.pgn
import chess.svg

###################################################################################
# This script is used to visualize the chess opening based on PGN file.
# Examples:
# -  The openings published at https://wang-qs.github.io
###################################################################################

# Something we need change for the input and output.
pgn_filename = "daning.pgn"
workspace = "data/cicilian-defence_argentina_lasker-pelikan-variation_bo_danning/"
svg_prefix = "cicilian-defence_argentina_"
github_img_path = "/img/chess/opening/cicilian-defence_argentina_argentina-variation_bw_danning/"


pgn = open(workspace + pgn_filename, encoding="utf-8")

markdown = open(workspace + "markdown.md", "w")

first_game = chess.pgn.read_game(pgn)
print(first_game.headers["Event"])

board = first_game.board()

index = 1
white = True

for move in first_game.mainline_moves():
    board.push(move)
    current_svg = chess.svg.board(board=board, lastmove=move, size=800)

    tempFile = ""
    turn = ""
    old_index = index
    old_white = white

    if white:
        tempFile = "step{:02d}_{}".format(index, "a_white")
        turn = "White"
        white = False # change it for next loop
    else:
        tempFile = "step{:02d}_{}".format(index, "b_black")
        turn = "Black"
        white = True # change it for next loop
        index += 1
    tempFile = svg_prefix + tempFile + ".svg"

    # create svg file.
    f = open(workspace + tempFile, "w")
    f.write(current_svg)
    f.close()

    # update markdown file.
    if old_white:
        markdown.write("## Step "+ str(old_index) + "\n\n")
    markdown.write("" + turn + "\n\n")
    img_link = "![Step {:d}, {} ]({})\n\n".format(old_index, turn, github_img_path + tempFile)
    markdown.write(img_link)

print("Final status of this PGN file.")
print(board)
