#!/bin/bash
script_dir="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd $script_dir/..
$script_dir/run_docker.sh run -v $script_dir/workdir:/kb/module/work -v /homes/chicago/seaver/genomes:/kb/module/genomes -e "SDK_CALLBACK_URL=$1" test/genomefileutil:latest test
