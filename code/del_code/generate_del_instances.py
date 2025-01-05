import json
from config import (
    TRAIN_ALL_FILE_PATH,
    RULES_JSON_FILE_PATH,
    OUTPUT_INSTANCES_FILE_PATH
)


def generate_predicate_dict(file_path):
    """
    Generate a dictionary of predicates mapping to their subject-object pairs.

    Args:
        file_path (str): Path to the triples file.

    Returns:
        dict: A dictionary where keys are predicates and values are lists of [subject, object] pairs.
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


def generate_head_and_tail_dicts(predicate_dict):
    """
    Generate head and tail dictionaries from the predicate dictionary.

    Args:
        predicate_dict (dict): A dictionary where keys are predicates, and values are [subject, object] pairs.

    Returns:
        tuple: Two dictionaries - head_dict and tail_dict.
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


def generate_instances(rules, predicate_dict, head_dict, tail_dict):
    """
    Generate instances for the given rules.

    Args:
        rules (list): A list of rules loaded from the JSON file.
        predicate_dict (dict): Predicate dictionary mapping predicates to subject-object pairs.
        head_dict (dict): Head dictionary mapping predicates to their head entities.
        tail_dict (dict): Tail dictionary mapping predicates to their tail entities.

    Returns:
        list: A list of generated instances with confidence, head triples, and body triples.
    """
    generated_instances = []
    rule_counter = 0

    for example in rules:
        rule_counter += 1
        print(f"Processing rule: {rule_counter} / {len(rules)}")

        rule_body = example.get("Rule Body", [])  # List of predicates in the rule body
        rule_head = example.get("Rule Head", [])[0]  # Rule head predicate

        # Only process rules with two predicates in the body
        if len(rule_body) == 2:
            if rule_body[0] in tail_dict:
                for j in range(len(tail_dict[rule_body[0]])):
                    tail1 = tail_dict[rule_body[0]][j]

                    if rule_body[1] in head_dict:
                        for k in range(len(head_dict[rule_body[1]])):
                            head_entity = head_dict[rule_body[1]][k]

                            if tail1 == head_entity:  # Match tail of first predicate to head of second predicate
                                head1 = head_dict[rule_body[0]][j]
                                tail_entity = tail_dict[rule_body[1]][k]

                                # Check if the head triple exists in the predicate dictionary
                                if rule_head in predicate_dict:
                                    if [head1, tail_entity] in predicate_dict[rule_head]:
                                        body_triple1 = f"{head1}\t{rule_body[0]}\t{tail1}"
                                        body_triple2 = f"{head_entity}\t{rule_body[1]}\t{tail_entity}"
                                        head_triple = f"{head1}\t{rule_head}\t{tail_entity}"
                                        generated_instances.append([
                                            str(example.get("conf", [])),
                                            head_triple,
                                            [body_triple1, body_triple2]
                                        ])

    return generated_instances


def save_instances_to_file(instances, output_path):
    """
    Save generated instances to a file.

    Args:
        instances (list): A list of generated instances.
        output_path (str): Path to the output file.
    """
    #body
    with open(output_path, 'w') as f:
        for instance in instances:
            f.write(instance[0] + '\t' + str(instance[2]) + '\n')
    #head
    # with open(output_path, 'w') as f:
    #     for instance in instances:
    #         f.write(instance[0] + '\t' + str(instance[1]) + '\n')


def main():
    # Step 1: Generate the predicate dictionary
    predicate_dict = generate_predicate_dict(TRAIN_ALL_FILE_PATH)

    # Step 2: Generate head and tail dictionaries
    head_dict, tail_dict = generate_head_and_tail_dicts(predicate_dict)

    # Step 3: Load rules from the JSON file
    with open(RULES_JSON_FILE_PATH, "r") as json_file:
        rules = json.load(json_file)

    # Step 4: Generate instances
    generated_instances = generate_instances(rules, predicate_dict, head_dict, tail_dict)

    print(f"The number of generated instances: {len(generated_instances)}")

    # Step 5: Save the generated instances to the output file
    save_instances_to_file(generated_instances, OUTPUT_INSTANCES_FILE_PATH)


if __name__ == "__main__":
    main()