import os
from os import listdir, chdir
from os.path import isfile, join
import json
from typing import List, Any, Dict
from scripts.txt_individuals_from_json import txt_population


def create_txt_population_foreach_json(jsons_dir_path: str) -> List[str]:
    impr_filenames: List[str] = []
    for filename in [f for f in listdir(jsons_dir_path) if isfile(join(jsons_dir_path, f))]:
        try:
            txt_population(jsons_dir_path + '/' + filename,
                           "progsys/Fizz Buzz.bnf",  # TODO grammar from csv of problems
                           jsons_dir_path.split('/')[-1] + '_' + filename.replace(".json", ''))
            impr_filenames.append(filename)
        except Exception as e:
            print(f"{filename} raises an exception: {str(e)}")
    if len(impr_filenames) == 0:
        e: str = "None of given jsons lead to a valid seed for improvement"
        raise Exception(e)
    return impr_filenames


TRAIN_DATASET_TAG: str = "<train>"
TEST_DATASET_TAG: str = "<test>"
SEED_FOLDER_TAG: str = "<seedFolder>"


def create_params_file(jsons_dir_path: str, impr_filenames: List[str]) -> str:
    cwd: str = os.getcwd()
    chdir("../PonyGE2/parameters")
    jsons_dir_name: str = jsons_dir_path.split('/')[-1]
    with open("./progimpr_base.txt", 'r') as file:
        impr_base_file: str = file.read()
    base_path: str = "./improvements/"
    if not os.path.isdir(base_path):
        os.mkdir(base_path)
    params_dir_path: str = os.path.join(base_path, jsons_dir_name)
    if not os.path.isdir(params_dir_path):
        os.mkdir(params_dir_path)
    for impr_filename in impr_filenames:
        impr_file: str = impr_base_file.replace(
            SEED_FOLDER_TAG,
            jsons_dir_name + '_' + impr_filename.replace(".json", ''))
        with open(os.path.join(jsons_dir_path, impr_filename), 'r') as read_file:
            extracted_json: Any = json.load(read_file)
        prob_name: List[Dict[str, Any]] = extracted_json["problem_name"]
        impr_file = impr_file.replace(
            TRAIN_DATASET_TAG,
            prob_name)
        impr_file = impr_file.replace(
            TEST_DATASET_TAG,
            prob_name)
        output_filepath: str = os.path.join(params_dir_path, impr_filename.replace(".json", "txt"))
        output_file = open(output_filepath, 'w')
        output_file.write(impr_file)
        output_file.close()
    chdir(cwd)
    return os.path.abspath(params_dir_path)
