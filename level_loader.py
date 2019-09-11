from ast import literal_eval


def load_level(level_file):
    obstacles = []
    with open(level_file, 'r') as file:
        for row in file:
            data = row.split(':')
            ob_type = data[0]
            evaluated = literal_eval(data[1])
            obstacles.append({"type":ob_type, "data":evaluated})
    return obstacles
