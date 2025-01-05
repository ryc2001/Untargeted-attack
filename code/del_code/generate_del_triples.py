import json
from config import (
    OUTPUT_INSTANCES_FILE_PATH,
    TRAIN_FILE_PATH,
    OUTPUT_TRAIN_FILE_PATH,
    SORT_LIMIT
)


def load_rules_with_confidence(file_path):
    """
    Load rules from a file and calculate cumulative confidence for each triple.

    Args:
        file_path (str): Path to the rules file.

    Returns:
        dict: A dictionary where keys are triples and values are cumulative confidence scores.
    """
    conf_count = {}

    with open(file_path, 'r') as input_file:
        lines = input_file.readlines()

    for line in lines:
        line = line.strip()
        if line:
            parts = line.split("\t")
            if len(parts) == 2:
                conf = float(parts[0])
                body = parts[1]
                relations = body[2:-2].split("', '")  # Remove brackets and split relations
                for subpart1 in relations:
                    parts = subpart1.strip().split("\\t")
                    subject = parts[0]
                    relation = parts[1]
                    obj = parts[2]

                    # Process relationships
                    subpart1 = f"{subject}\t{relation}\t{obj}"
                    if relation.startswith("inv_"):
                        # Remove "inv_" and swap subject and object
                        relation = relation[4:]
                        subpart1 = f"{obj}\t{relation}\t{subject}"

                    # Update cumulative confidence
                    if subpart1 not in conf_count:
                        conf_count[subpart1] = conf
                    else:
                        conf_count[subpart1] += conf

    return conf_count


def load_confidence_from_json(json_path):
    """
    Load confidence data from a JSON file.

    Args:
        json_path (str): Path to the JSON file.

    Returns:
        dict: A dictionary of triples and their confidence scores.
    """
    with open(json_path, 'r') as json_file:
        return json.load(json_file)


def exclude_top_triples(train_file_path, conf_count, limit):
    """
    Exclude the top triples based on confidence scores from the training file.

    Args:
        train_file_path (str): Path to the training file.
        conf_count (dict): A dictionary of triples and their confidence scores.
        limit (int): Number of top triples to exclude.

    Returns:
        set: A set of remaining lines after exclusion.
    """
    sorted_lines = sorted(conf_count.items(), key=lambda x: x[1], reverse=True)
    top_triples = {triple for triple, _ in sorted_lines[:limit]}

    with open(train_file_path, 'r') as file:
        remaining_lines = {line.strip() for line in file if line.strip() not in top_triples}

    return remaining_lines


def save_remaining_lines(remaining_lines, output_path):
    """
    Save the remaining lines to a file after excluding top triples.

    Args:
        remaining_lines (set): A set of remaining lines.
        output_path (str): Path to the output file.
    """
    with open(output_path, 'w') as output_file:
        for line in remaining_lines:
            output_file.write(f"{line}\n")


def main():
    # Step 1: Load rules and compute cumulative confidence
    conf_count = load_rules_with_confidence(OUTPUT_INSTANCES_FILE_PATH)

    # Step 3: Exclude top triples from the training file
    remaining_lines = exclude_top_triples(TRAIN_FILE_PATH, conf_count, SORT_LIMIT)

    # Step 4: Save remaining lines to the output file
    save_remaining_lines(remaining_lines, OUTPUT_TRAIN_FILE_PATH)

    print(f"Number of remaining triples: {len(remaining_lines)}")


if __name__ == "__main__":
    main()