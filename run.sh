#!/bin/bash

#是否存在对应的进程
declare -a processes
PROGRAM_NAME="${PWD}/run_detail.py"
processes=($(ps aux | grep "python3 ${PROGRAM_NAME}" | grep -v "grep" | cut -d ' ' -f 1))

echo ${processes}
echo ${PWD}
#不存在对应的程序，则执行
declare -i count
count=${#processes[*]}

echo "${count}"
if [ "${count}" == "0" ]; then
  echo "${PROGRAM_NAME} is not running"
  echo "${PROGRAM_NAME} will start"
  python3 "${PROGRAM_NAME}"
else
  echo "${PROGRAM_NAME} has been running"
fi
