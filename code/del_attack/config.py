# config.py
# generate delete instances
# Input file paths
TRAIN_ALL_FILE_PATH = '../../dataset/{}_all/{}_all.txt'
RULES_JSON_FILE_PATH = '../../data_processed/{}_del_10/{}_high_conf_rules.json'

# Output file paths
OUTPUT_INSTANCES_FILE_PATH = '../../data_processed/{}_del_10/{}_generated_del_instances.txt'

# generate delete triples
# Input file paths
TRAIN_FILE_PATH = '../../dataset/{}/train.txt'

# Output file paths
OUTPUT_TRAIN_FILE_PATH = '../../data_processed/{}_del_10/train.txt'

# Other parameters
SORT_LIMIT = 8684  # Number of top triples to sort and exclude (10% deletions)   wn18rr:8684 / fb15k237:27212

