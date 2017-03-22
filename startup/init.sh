#!/bin/bash


SCRIPT_DIR=..
SCRIPT_NAME="$SCRIPT_DIR/twitter_stream.py"
PID_DIR=./PID_DIR
cd "$(dirname "$0")"
#Start the data mining, specify the filter(s) as arguments. OBS Twitter seems to be using some throtteling.
#I could only get 2 filters running at the same time. We need to implement user authentication to get more running.
start() {
  #Check that argument exists
  if [ ! -f $1 ]; then
    for i in $@
    do
        echo 'Starting service for ' + ${i}
        (python3 ${SCRIPT_NAME} ${i} &
        PID_FILE=${PID_DIR}'/'${i}'.PID'
        echo $! > ${PID_FILE});
        echo 'Service started twitter_stream '${i}
     done
  else
    echo 'Please specify at least 1 filter'
    exit 1
  fi
}

#Stops running streaming process and cleans up PID_DIR from all files. It is also possible to specify which filters
#to stop using arguments. DO NOT MANUALLY REMOVE THE PID_DIR FOLDER SINCE THEN THE PROCESS WONT STOP!!
stop() {
  if [ ! -f $1 ]; then
    for i in $@
    do
      echo 'Stopping service twitter-geo '${i}
      PID_FILE=${PID_DIR}'/'${i}'.PID'
      kill -9 $(cat "$PID_FILE") && rm -f "$PID_FILE"
      echo 'Service stopped'
    done
  else
    PID_FILES=${PID_DIR}'/*'
    for f in ${PID_FILES};
     do
        echo "Stopping $f";
        (kill -9 $(cat ${f})
        rm -f ${f});
     done
    exit 1
  fi
}

#Check which filters are running
status() {
    echo 'The following filters are running:'
    PID_FILES=${PID_DIR}'/*'
    for f in ${PID_FILES};
     do
        PID=($(cat ${f}))
        if  [ -n "$(ps -p ${PID} -o pid=)"  ]; then
            echo "The following processes are running "${f}
        fi
     done

}

case "$1" in
  start)
    start ${@:2}
    ;;
  stop)
    echo 'running stop'
    stop ${@:2}
    ;;
  restart)
    echo 'Running restart'
    stop
    start ${@:2}
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|uninstall}"
esac

