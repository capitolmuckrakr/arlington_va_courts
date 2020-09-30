#!/bin/bash
panecount=2
dotsdir="$HOME/scripts/arlington_va_courts/dots"
oldfile="$dotsdir/.env"
cp -f $dotsdir/env.template $dotsdir/.env
EXENDPNT='export ENDPOINT_DB='"${ENDPOINT_DB}"
sed -i 's/ENDPOINTDB/'"$(echo ${EXENDPNT})"'/' $oldfile
EPGUSER='export PGUSER='"${PGUSER}"
EPGPASSWORD='export PGPASSWORD='"${PGPASSWORD}"
EPGDATABASE='export DB_NAME='"${DB_NAME}"
sed -i 's/PGUSERNAME/'"$(echo ${EPGUSER})"'/' $oldfile
sed -i 's/PGPSWD/'"$(echo ${EPGPASSWORD})"'/' $oldfile
sed -i 's/PGDB/'"$(echo ${EPGDATABASE})"'/' $oldfile
export TMUX_SESSION="remotetmuxtest"
tmux has-session -t $TMUX_SESSION 2>/dev/null
if [[ $? != 0 ]];
then
    tmux new-session -s $TMUX_SESSION -n default -d
    tmux setenv PEM '/home/alex/apc.pem'
    tmux split-window -v -p 99 -t $TMUX_SESSION
    tmux kill-pane -t $TMUX_SESSION:1.1
    tmux split-window -h -t $TMUX_SESSION:1
    tmux send-keys -t $TMUX_SESSION:1.2 'export startserver=$(date); echo $startserver; bash aws_ec2.sh' C-m
    tmux send-keys -t $TMUX_SESSION:1.2 'ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i $PEM ubuntu@$ENDPOINT -t "tmux new -s default -d"' C-m
    tmux send-keys -t $TMUX_SESSION:1.2 'ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i $PEM -t ubuntu@$ENDPOINT -t "tmux send-keys -t $TMUX_SESSION:1 scraperenv C-m"'
fi
tmux attach -t $TMUX_SESSION:1.2
