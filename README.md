# Untargeted Adversarial Attack on Knowledge Graph Embeddings
To get started, please download some necessary files related to this project from [Baidu Netdisk](https://pan.baidu.com/s/14jlWk9JFlJNI-xSYz0n3pg?pwd=car2). The folder name is `data_processed`. Place this folder in the project directory.
## Addition

`cd code/add_attack `

`python generate_neg_rules.py --dataset <dataset_name>`

`python generate_neg_triples.py --dataset <dataset_name>`

## Deletion

`cd code/del_attack `

`python generate_del_instances.py --dataset <dataset_name>`

`python genarate_del_triples.py --dataset <dataset_name>`
Acceptable values for `--dataset` are `WN18RR` or `FB15k237`.
