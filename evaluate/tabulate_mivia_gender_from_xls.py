import argparse
from xls_models_tools import mean_dict, extract_results_by_corruption
import matplotlib.pyplot as plt
import os
import numpy as np
from collections import defaultdict, OrderedDict
from tabulate import tabulate
from matplotlib.lines import Line2D

parser = argparse.ArgumentParser(description='corruption error calculation')
parser.add_argument('--uncorrupted', dest='uncorrupted', type=str, help='original experiment results (.xls)')
args = parser.parse_args()

LATEX_TAB = False

official_model = {
    "vgg16": "VGG-16",
    "senet50": "SE-ResNet-50",
    "densenet121bc": "DenseNet-121",
    "mobilenet224": "MobileNet v2-A",
    "mobilenet96": "MobileNet v2-B",
    "mobilenet64": "MobileNet v2-C",
    "shufflenet224": "ShuffleNet",
    "squeezenet": "SqueezeNet",
    "xception71": "XceptionNet",
}


def nine_models_order(data, rename=True):
    if rename:
        data = {official_model[k]: v for k, v in data.items()}
    keyorder = {k: v for v, k in enumerate(official_model.values() if rename else official_model.keys())}
    return OrderedDict(sorted(data.items(), key=lambda i: keyorder.get(i[0])))


def table_chart(uncorrupted_exp, filepath):
    """
    # uncorrupted_exp = {
    #   sample_label : {
    #       model : value,
    #       ... : ...
    #       }
    #   }
    """

    # insert in list head uncorrupted experiment results
    uncorr_data = next(iter(uncorrupted_exp.values()))
    uncorr_data = nine_models_order(uncorr_data)

    ##### SMALL TABULATE TO FILE #####
    col_labels = ['Method', 'MIVIA-GENDER']
    row_labels = [m for m in uncorr_data.keys()]
    table_vals = [v for v in uncorr_data.values()]
    table_vals = [[r, round(v, 3)] for r, v in zip(row_labels, table_vals)]
    tab_1 = tabulate(table_vals, headers=col_labels, tablefmt="latex" if LATEX_TAB else "grid")

    print(tab_1)
    with open(os.path.splitext(filepath)[0] + "_tab1.txt", 'w') as f:
        f.write(tab_1)


if __name__ == '__main__':
    uncorrupted_results = extract_results_by_corruption(args.uncorrupted)
    table_chart(uncorrupted_results, args.uncorrupted)

