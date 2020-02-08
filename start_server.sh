#!/bin/bash/
export ZEROMQ_SOCK_TMP_DIR=/tmp/

bert-serving-start -model_dir bert/uncased_L-24_H-1024_A-16/ -num_worker=4 -graph_tmp_dir /tmp/
