# config.py
# generate delete instances
# Input file paths
TRAIN_ALL_FILE_PATH = '../../dataset/wn18rr_all/wn18rr_all.txt'
RULES_JSON_FILE_PATH = '../../data_processed/WN18RR_del_10/WN18RR_1_50_2.json'

# Output file paths
OUTPUT_INSTANCES_FILE_PATH = '../../data_processed/WN18RR_del_10/wn18rr_generated_del_instances_50_2_conf_body.txt'

# generate delete triples
# Input file paths
TRAIN_FILE_PATH = '../../dataset/wn18rr/train.txt'

# Output file paths
OUTPUT_TRAIN_FILE_PATH = '../../data_processed/WN18RR_del_10/train.txt'

# Other parameters
SORT_LIMIT = 8684  # Number of top triples to sort and exclude (10% deletions)

