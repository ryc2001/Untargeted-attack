# config.py
# generate neg rules
# Paths for input files
RELATION_MATRIX_PATH = "../../../../PycharmProjects/KGEvaluator/generation/FB15k237_relation_score_matrix.csv"
RELATION_TO_NUMBER_PATH = "../../../../PycharmProjects/KGEvaluator/generation/FB15K237_relation_to_number.json"
TOP1_RELATIONS_DICT_PATH = "../../data_processed/FB15k-237_add_10/FB15k-237_top1_relations_dict.json"
JSON_DATA_PATH = "../../data_processed/FB15k-237_add_10/fb15k-237_201-210_2.json"
INDICES_PATH = "../../data_processed/FB15k-237_add_10/fb15k237_replace_rel_indices_201-210_2.txt"
EXISTING_RULES_PATH = "../../data_processed/FB15k-237_add_10/fb15k-237_200_2.json"

# Paths for output files
OUTPUT_TOP1_RELATIONS_DICT_PATH = "../../data_processed/FB15k-237_add_10/FB15K237_top1_relations_dict.json"
OUTPUT_NEGATIVE_RULES_PATH = "../../data_processed/FB15k-237_add_10/fb15k-237_negative_rules_201-210_stat_2.json"

# generate neg triples
# Paths for input files
TRAIN_FILE_PATH = "../../dataset/FB15k-237_all/fb15k237_all.txt"
VALID_FILE_PATH = "../../dataset/FB15k-237_all/valid_all.txt"
TEST_FILE_PATH = "../../dataset/FB15k-237_all/test_all.txt"
ORIGINAL_TRAIN_PATH = '../../dataset/FB15k-237/train.txt'

# Paths for output files
OUTPUT_TP_FILE_PATH = "../../data_processed/FB15k-237_add_10/fb15k237_negative_tp_not_in_dataset_201-210_2.txt"
OUTPUT_SEL_TP_FILE_PATH = '../../data_processed/FB15k-237_add_10/fb15k237_negative_tp_not_in_dataset_201-210_2_sel_10.txt'
OUTPUT_TRAIN_FILE_PATH = '../../data_processed/FB15k-237_add_10/train.txt'
SORT_LIMIT = 27212  # Number of top triples to sort and exclude (10% deletions) wn18rr:8684/fb15k237:27212