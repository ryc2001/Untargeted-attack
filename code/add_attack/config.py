# config.py
# generate neg rules
# Paths for input files
RELATION_MATRIX_PATH = "../../data_processed/{}_add_10/{}_relation_score_matrix.csv"
RELATION_TO_NUMBER_PATH = "../../data_processed/{}_add_10/{}_relation_to_number.json"
TOP1_RELATIONS_DICT_PATH = "../../data_processed/{}_add_10/{}_top1_relations_dict.json"
LOW_CONF_RULES_PATH = "../../data_processed/{}_add_10/{}_low_conf_rules.json"
INDICES_PATH = "../../data_processed/{}_add_10/{}_replace_rel_indices.txt"
HIGH_CONF_RULES_PATH = "../../data_processed/{}_add_10/{}_high_conf_rules.json"

# Paths for output files
OUTPUT_TOP1_RELATIONS_DICT_PATH = "../../data_processed/{}_add_10/{}_top1_relations_dict.json"
OUTPUT_NEGATIVE_RULES_PATH = "../../data_processed/{}_add_10/{}_negative_rules.json"

# generate neg triples
# Paths for input files
TRAIN_FILE_PATH = "../../dataset/{}_all/{}_all.txt"
VALID_FILE_PATH = "../../dataset/{}_all/valid_all.txt"
TEST_FILE_PATH = "../../dataset/{}_all/test_all.txt"
ORIGINAL_TRAIN_PATH = '../../dataset/{}/train.txt'

# Paths for output files
OUTPUT_TP_FILE_PATH = "../../data_processed/{}_add_10/{}_negative_tp_not_in_dataset.txt"
OUTPUT_SEL_TP_FILE_PATH = '../../data_processed/{}_add_10/{}_negative_tp_not_in_dataset_sel_10.txt'
OUTPUT_TRAIN_FILE_PATH = '../../data_processed/{}_add_10/train.txt'

SORT_LIMIT = 27212  # Number of top triples to sort and exclude (10% deletions)     wn18rr:8684 / fb15k237:27212