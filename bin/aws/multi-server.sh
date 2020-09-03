#!/bin/bash
LIMITNUM=742
instancecount=8
panecount=8
remainingcount=$(($instancecount - $panecount))
export TMUX_SESSION="arlingtoncourts"
tmux has-session -t $TMUX_SESSION 2>/dev/null
if [[ $? != 0 ]];
then
tmux new-session -s $TMUX_SESSION -n arlingtoncourts:window1 -d
tmux setenv PEM '/home/alex/apc.pem'
tmux setenv LIMITNUM $LIMITNUM
tmux split-window -v -p 99 -t $TMUX_SESSION
tmux kill-pane -t $TMUX_SESSION:1.1
tmux split-window -h -t $TMUX_SESSION:1
tmux split-window -v -t $TMUX_SESSION:1.2
tmux split-window -v -t $TMUX_SESSION:1.1
tmux split-window -v -t $TMUX_SESSION:1.4
tmux split-window -v -t $TMUX_SESSION:1.3
tmux split-window -v -t $TMUX_SESSION:1.2
tmux split-window -v -t $TMUX_SESSION:1.1
    for i in $(seq 1 $panecount)
        do
          tmux send-keys -t $TMUX_SESSION:1.$i 'bash aws_ec2.sh' C-m
          count="$i"
          tmux send-keys -t $TMUX_SESSION:1.$i "export INSTANCECOUNT="$count C-m
    done
fi
tmux attach -t $TMUX_SESSION
