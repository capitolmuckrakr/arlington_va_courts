#!/bin/bash -e
LIMITNUM=742
instancecount=8
panecount=8
remainingcount=$(($instancecount - $panecount))

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
              tmux send-keys -t $TMUX_SESSION:1.$i "export INSTANCECOUNT="$i C-m
              tmux send-keys -t $TMUX_SESSION:1.$i "export LIMITNUM" C-m
              tmux send-keys -t $TMUX_SESSION:1.$i "export ENDPOINT_DB" C-m
              tmux send-keys -t $TMUX_SESSION:1.$i "export PGUSER" C-m
              tmux send-keys -t $TMUX_SESSION:1.$i "export PGPASSWORD" C-m
              tmux send-keys -t $TMUX_SESSION:1.$i "export DB_NAME" C-m
              tmux send-keys -t $TMUX_SESSION:1.$i 'export startserver=$(date); echo $startserver; bash aws_ec2.sh' C-m
              tmux send-keys -t $TMUX_SESSION:1.$i 'echo "$INSTANCECOUNT, $ENDPOINT, $startserver" >>/home/alex/scripts/arlington_va_courts/data/sessions.txt' C-m
              tmux send-keys -t $TMUX_SESSION:1.$i 'ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i $PEM -t ubuntu@$ENDPOINT "tmux new -s scraper -d"' C-m
    #          tmux send-keys -t $TMUX_SESSION:1.$i 'ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i $PEM -t ubuntu@$ENDPOINT "~/phrasecount.sh $INSTANCECOUNT"' C-m
    #          tmux send-keys -t $TMUX_SESSION:1.$i 'export sourcefilename="/home/ubuntu/$INSTANCECOUNT.txt"' C-m
    #          tmux send-keys -t $TMUX_SESSION:1.$i 'export destinationfilename="/home/alex/$INSTANCECOUNT.txt"' C-m
    #          tmux send-keys -t $TMUX_SESSION:1.$i 'scp -v -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i $PEM ubuntu@$ENDPOINT:$sourcefilename $destinationfilename' C-m
        done
fi
tmux attach -t $TMUX_SESSION:1.1