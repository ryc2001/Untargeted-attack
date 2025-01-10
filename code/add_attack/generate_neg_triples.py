import json
import random
import argparse
from config import (
    TRAIN_FILE_PATH,
    VALID_FILE_PATH,
    TEST_FILE_PATH,
    OUTPUT_NEGATIVE_RULES_PATH,
    OUTPUT_TP_FILE_PATH,
    SORT_LIMIT,
    OUTPUT_SEL_TP_FILE_PATH,
    ORIGINAL_TRAIN_PATH,
    OUTPUT_TRAIN_FILE_PATH
)


def generate_predicate_dict(file_path):
    """
    Generate a dictionary for predicates with their head and tail entities.

    Args:
        file_path (str): Path to the triples file.

    Returns:
        dict: A dictionary where keys are predicates and values are lists of [head, tail] pairs.
    """
    predicate_dict = {}
    with open(file_path, 'r') as file:
        triples = file.readlines()

    for triple in triples:
        subject, predicate, obj = triple.strip().split('\t')

        if predicate in predicate_dict:
            predicate_dict[predicate].append([subject, obj])
        else:
            predicate_dict[predicate] = [[subject, obj]]

    return predicate_dict


def generate_head_tail_dicts(predicate_dict):
    """
    Generate dictionaries storing head and tail entities for each predicate.

    Args:
        predicate_dict (dict): A dictionary where keys are predicates and values are lists of [head, tail] pairs.

    Returns:
        tuple: Two dictionaries - one for head entities and one for tail entities.
    """
    head_dict = {}
    tail_dict = {}

    for predicate, entities in predicate_dict.items():
        head_entities = []
        tail_entities = []
        for entity_pair in entities:
            if len(entity_pair) == 2:
                head_entities.append(entity_pair[0])
                tail_entities.append(entity_pair[1])

        head_dict[predicate] = head_entities
        tail_dict[predicate] = tail_entities

    return head_dict, tail_dict


def generate_triples(rules, predicate_dict, head_dict, tail_dict, predicate_dict_val, predicate_dict_test):
    """
    Generate triples based on the rules and predicate dictionaries.

    Args:
        rules (list): List of rules loaded from the JSON file.
        predicate_dict (dict): Predicate dictionary for training data.
        head_dict (dict): Dictionary of head entities for each predicate.
        tail_dict (dict): Dictionary of tail entities for each predicate.
        predicate_dict_val (dict): Predicate dictionary for validation data.
        predicate_dict_test (dict): Predicate dictionary for test data.

    Returns:
        list: List of generated triples.
    """
    tp = []
    rule_counter = 0

    for example in rules:
        rule_counter += 1
        print("Processing rule:", rule_counter, "/", len(rules))
        rule_body = example.get("Rule Body", [])
        rule_head = example.get("Rule Head", [])[0]

        # Case where the rule body has only one predicate
        if len(rule_body) == 1:
            for j in range(len(head_dict[rule_body[0]])):
                head_entity = head_dict[rule_body[0]][j]
                tail1 = tail_dict[rule_body[0]][j]
                head_triple = f"{tail1}\t{rule_head}\t{head_entity}"

                if [tail1, head_entity] not in predicate_dict.get(rule_head, []):
                    if (rule_head not in predicate_dict_val or [tail1, head_entity] not in predicate_dict_val.get(rule_head, [])):
                        if (rule_head not in predicate_dict_test or [tail1, head_entity] not in predicate_dict_test.get(rule_head, [])):
                            tp.append(head_triple)

        # Case where the rule body has two predicates
        if len(rule_body) == 2:
            for j in range(len(tail_dict[rule_body[0]])):
                tail1 = tail_dict[rule_body[0]][j]
                for k in range(len(head_dict[rule_body[1]])):
                    head_entity = head_dict[rule_body[1]][k]
                    if tail1 == head_entity:
                        head1 = head_dict[rule_body[0]][j]
                        tail_entity = tail_dict[rule_body[1]][k]
                        head_triple = f"{head1}\t{rule_head}\t{tail_entity}"

                        if [head1, tail_entity] not in predicate_dict.get(rule_head, []):
                            if (rule_head not in predicate_dict_val or [head1, tail_entity] not in predicate_dict_val.get(rule_head, [])):
                                if (rule_head not in predicate_dict_test or [head1, tail_entity] not in predicate_dict_test.get(rule_head, [])):
                                    tp.append(head_triple)

    return tp


def process_triples(tp):
    """
    Post-process triples to handle inverted relations and remove duplicates.

    Args:
        tp (list): List of generated triples.

    Returns:
        list: List of unique, processed triples.
    """
    new_tp = []

    for line in tp:
        parts = line.strip().split("\t")
        subject = parts[0]
        relation = parts[1]
        obj = parts[2]

        if relation.startswith("inv_"):
            # Remove "inv_" and swap subject and object
            relation = relation[4:]
            new_line = f"{obj}\t{relation}\t{subject}"
            new_tp.append(new_line)
        else:
            new_tp.append(line)

    # Remove duplicates
    unique_lines = set(new_tp)
    return list(unique_lines)


def save_triples(triples, output_file_path, sel_output_file_path, original_train, final_train_path):
    """
    Save triples to a file.

    Args:
        triples (list): List of triples to save.
        output_file_path (str): Path to the output file.
    """
    with open(output_file_path, 'w') as f2:
        for line in triples:
            f2.write(line + '\n')
    sel_tp = random.sample(triples, SORT_LIMIT)
    with open(sel_output_file_path, 'w') as f2:
        for line in sel_tp:
            f2.write(line + '\n')
    final_train =set()
    with open(original_train, 'r') as f3:
        for line in f3:
            final_train.add(line.strip())
    final_train = final_train.union(set(sel_tp))
    with open(final_train_path, 'w') as f4:
        for line in final_train:
            f4.write(line + '\n')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, choices=['WN18RR', 'FB15k237'])

    args = parser.parse_args()
    # Generate predicate dictionaries
    predicate_dict = generate_predicate_dict(TRAIN_FILE_PATH.format(args.dataset, args.dataset))
    predicate_dict_val = generate_predicate_dict(VALID_FILE_PATH.format(args.dataset))
    predicate_dict_test = generate_predicate_dict(TEST_FILE_PATH.format(args.dataset))

    # Generate head and tail dictionaries
    head_dict, tail_dict = generate_head_tail_dicts(predicate_dict)

    # Load rules from JSON file
    with open(OUTPUT_NEGATIVE_RULES_PATH.format(args.dataset, args.dataset), "r") as json_file:
        rules = json.load(json_file)

    # Generate triples
    tp = generate_triples(rules, predicate_dict, head_dict, tail_dict, predicate_dict_val, predicate_dict_test)

    # Post-process triples
    processed_triples = process_triples(tp)

    # Save the triples to a file
    save_triples(processed_triples, OUTPUT_TP_FILE_PATH.format(args.dataset, args.dataset), OUTPUT_SEL_TP_FILE_PATH.format(args.dataset, args.dataset), ORIGINAL_TRAIN_PATH.format(args.dataset), OUTPUT_TRAIN_FILE_PATH.format(args.dataset))

    print(f"Number of unique triples: {len(processed_triples)}")


if __name__ == "__main__":
    main()