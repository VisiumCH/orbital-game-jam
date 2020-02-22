#!/bin/bash/
export ZEROMQ_SOCK_TMP_DIR=/tmp/

bert-serving-start -model_dir src/models/uncased_L-24_H-1024_A-16/ -num_worker=2 -graph_tmp_dir /tmp/ -max_seq_len=64