from ast import literal_eval


# At the moment, levels are described as follows:
#   w:(x1, y1), (x2, y2), ..., (xn, yn)
#       x is offset by half the screen size. left = -400; right = 400; center = 0
#           I was planning on just having a right side and a left side, nothing else, so this made sense at the time.
#       y is just y. It moves down slowly as the game progresses
#       These points make a GL_LINE_LOOP, or a wireframe polygon.
#       Feel free to add more if you want. There are only a few as a proof of concept.
#   e:(x, y)
#       Places an enemy at (x, y) coordinates. No funky offset this time.
def load_level(level_file):
    # TODO make this into a class, instead of just a dict
    obstacles = []
    with open(level_file, 'r') as file:
        for row in file:
            if row == "\n":
                continue
            data = row.split(':')
            ob_type = data[0]
            evaluated = literal_eval(data[1])
            obstacles.append({"type": ob_type, "data": evaluated})
    return obstacles
