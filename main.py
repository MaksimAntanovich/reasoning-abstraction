import pandas as pd
from typing import List, Tuple, Dict
import os
import json

DATA_PATH = '/home/maksim/Downloads/abstraction-and-reasoning-challenge/'


def is_splittable(image: List[Tuple[int, int]], pattern: List[Tuple[int, int]]) -> bool:
    """
    checks is it possible to split given image by specified pattern

    :param image: list of cells which represents an image
    :param pattern: cells which should tile the image
    :return:if image could be tiled with pattern
    """
    image_width, image_height = rectangular_size(image)
    pattern_width, pattern_height = rectangular_size(pattern)
    if (image_width % pattern_width != 0 or image_height % pattern_height != 0):
        return False



def rectangular_size(image: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Computes size of border rectangular for pattern

    :param image: cells forming the pattern
    :return: width and height of pattern rectangular
    """
    widths = [cell[0] for cell in image]
    heights = [cell[1] for cell in image]
    return max(widths) - min(widths) + 1, max(heights) - min(heights) + 1


# load data
def load_data(path):
    tasks = pd.Series()
    for file_path in os.listdir(path):
        task_file = os.path.join(path, file_path)
        with open(task_file, 'r') as f:
            task = json.load(f)
        tasks[file_path[:-5]] = task
    return tasks


def print_sample(input_output_json):
    for input_output_sample in input_output_json:
        print('=' * 50)
        color_groups = group_by_color(input_output_sample['input'])
        for color, cells in color_groups.items():
            print(str(color) + ' : ' + str(discover_patterns(cells, False)))
        for input_line in input_output_sample['input']:
            print(input_line)
        print()
        for output_line in input_output_sample['output']:
            print(output_line)
        print()
        print()


def group_by_color(input: List[List[int]]) -> Dict[int, List[Tuple[int, int]]]:
    """
    Iterates over cells of input task, grouping them by color

    :param input: task field - colorized m x n rectangular
    :return: fields of input rectangular grouped by color
    """
    colors = dict()
    for lineidx, line in enumerate(input):
        for cellidx, cell in enumerate(line):
            if cell not in colors:
                colors[cell] = list()
            colors[cell].append((lineidx, cellidx))
    return colors


def discover_patterns(cells_original: List[Tuple[int, int]], count_diagonal: bool = True) -> List[
    List[Tuple[int, int]]]:
    """
    Simply picks adjacent cells and groups them together

    :param cells_original: list of cells with same color
    :param count_diagonal: do we count diagonal adjacency or not
    :return: list of patterns - groups of adjacent cells
    """
    cells = cells_original.copy()
    patterns = list()
    while len(cells) > 0:
        next_cell = cells.pop(0)
        pattern = [next_cell]
        for candidate in pattern:
            for lineidx in range(candidate[0] - 1, candidate[0] + 2):
                for cellidx in range(candidate[1] - 1, candidate[1] + 2):
                    neighbour = (lineidx, cellidx)
                    if neighbour in cells and (count_diagonal or lineidx == candidate[0] or cellidx == candidate[1]):
                        pattern.append(neighbour)
                        cells.remove(neighbour)
        patterns.append(pattern)
    return patterns


train = load_data(DATA_PATH + 'training/')
print(train.iloc[0])
print_sample(train.iloc[3]['train'])
