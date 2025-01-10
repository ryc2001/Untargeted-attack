import json
import copy
import csv
import argparse
from config import (  # Import all the paths from config.py
    RELATION_MATRIX_PATH,
    RELATION_TO_NUMBER_PATH,
    TOP1_RELATIONS_DICT_PATH,
    LOW_CONF_RULES_PATH,
    INDICES_PATH,
    HIGH_CONF_RULES_PATH,
    OUTPUT_TOP1_RELATIONS_DICT_PATH,
    OUTPUT_NEGATIVE_RULES_PATH,
)


def load_relation_matrix(file_path):
    """
    Load the relation matrix and remove diagonal elements.

    Args:
        file_path (str): Path to the relation matrix file.

    Returns:
        list: The processed relation matrix.
    """
    relation_matrix = []
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            relation_matrix.append([float(x) for x in row])

    # Remove diagonal elements
    for i in range(len(relation_matrix)):
        relation_matrix[i][i] = 0.0  # Set diagonal elements to 0

    return relation_matrix


def load_relation_mappings(file_path):
    """
    Load the mapping from relation IDs to relation names.

    Args:
        file_path (str): Path to the mapping file.

    Returns:
        tuple: A dictionary mapping relation IDs to names and vice versa.
    """
    with open(file_path, "r") as relation_file:
        relation_to_number = json.load(relation_file)

    number_to_relation = {v: k for k, v in relation_to_number.items()}
    return relation_to_number, number_to_relation


def generate_top_relations(relation_matrix, number_to_relation, top_n=1):
    """
    Generate the top N related relations for each relation.

    Args:
        relation_matrix (list): The relation matrix.
        number_to_relation (dict): Mapping from relation IDs to names.
        top_n (int): The number of top relations to select.

    Returns:
        dict: A dictionary of top N related relations for each relation.
    """
    top_relations_dict = {}
    for i, row in enumerate(relation_matrix):
        top_indices = sorted(range(len(row)), key=lambda x: -row[x])[:top_n]
        top_relations = [number_to_relation[idx + 1] for idx in top_indices]
        top_relations_dict[number_to_relation[i + 1]] = top_relations
    return top_relations_dict


def save_json(data, file_path):
    """
    Save data to a JSON file.

    Args:
        data (dict or list): The data to save.
        file_path (str): The file path to save the JSON.
    """
    with open(file_path, "w") as output_file:
        json.dump(data, output_file, indent=4)


def load_json(file_path):
    """
    Load data from a JSON file.

    Args:
        file_path (str): The file path to load the JSON from.

    Returns:
        dict or list: The loaded JSON data.
    """
    with open(file_path, "r", encoding="utf-8") as json_file:  # Ensure utf-8 encoding
        return json.load(json_file)
def load_txt(file_path):
    """
    Load data from a TXT file.

    """
    output = []
    with open(file_path, "r", encoding="utf-8") as file:  # Ensure utf-8 encoding
        for line in file:
            output.append(line.strip())
        return output

def generate_new_rules(json_data, indices, top_relations_dict):
    """
    Generate new rules by replacing relations using top N related relations.

    Args:
        json_data (list): The original rules data.
        indices (list): The list of indices to replace.
        top_relations_dict (dict): A dictionary of top N related relations.

    Returns:
        list: A list of newly generated rules.
    """
    new_rules = []
    a = 0
    for rule in json_data:
        index = int(indices[a])
        a += 1
        rule_body = rule["Rule Body"]
        selected_relation = rule_body[index]

        # If the selected relation is in the top relations dictionary, replace it with top N relations
        if selected_relation in top_relations_dict:
            top_replacements = top_relations_dict[selected_relation]
            for replacement in top_replacements:
                new_rule = copy.deepcopy(rule)
                new_rule["Rule Body"][index] = replacement
                new_rules.append(new_rule)

    return new_rules


def filter_existing_rules(new_rules, existing_data):
    """
    Filter out rules that already exist in the existing dataset.

    Args:
        new_rules (list): The list of newly generated rules.
        existing_data (list): The list of existing rules.

    Returns:
        list: A list of filtered rules that are not in the existing dataset.
    """
    return [rule for rule in new_rules if rule not in existing_data]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, choices=['WN18RR','FB15k237'])

    args = parser.parse_args()
    # Load the relation matrix
    relation_matrix = load_relation_matrix(RELATION_MATRIX_PATH.format(args.dataset, args.dataset))

    # Load the relation mappings
    relation_to_number, number_to_relation = load_relation_mappings(RELATION_TO_NUMBER_PATH.format(args.dataset, args.dataset))

    # Generate the top1 related relations dictionary
    top_relations_dict = generate_top_relations(relation_matrix, number_to_relation, top_n=1)
    save_json(top_relations_dict, OUTPUT_TOP1_RELATIONS_DICT_PATH.format(args.dataset, args.dataset))

    # Load data
    top_relations_dict = load_json(TOP1_RELATIONS_DICT_PATH.format(args.dataset, args.dataset))
    json_data = load_json(LOW_CONF_RULES_PATH.format(args.dataset, args.dataset))
    indices = load_txt(INDICES_PATH.format(args.dataset, args.dataset))

    # Generate new rules
    new_rules = generate_new_rules(json_data, indices, top_relations_dict)

    # Load existing rules
    existing_data = load_json(HIGH_CONF_RULES_PATH.format(args.dataset, args.dataset))

    # Filter out existing rules
    filtered_rules = filter_existing_rules(new_rules, existing_data)
    # Save the final rules
    save_json(filtered_rules, OUTPUT_NEGATIVE_RULES_PATH.format(args.dataset, args.dataset))


if __name__ == "__main__":
    main()