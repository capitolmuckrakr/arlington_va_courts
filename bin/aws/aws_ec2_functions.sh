#!/bin/bash -e
# You need to install the AWS Command Line Interface from http://aws.amazon.com/cli/

if [[ ! $PEM ]];
then
echo "Please make sure that a key is set by entering 'export PEM=' followed by a path to key you have chosen."
exit 0;
fi

read -r -d '' instructions <<-EOF
Type 'connect' to access the server
Type 'upload [FILEPATH]' to send a file to the server.
EOF

export instructions=$instructions
function instructions() {
    echo "$instructions"
}

export oldPS1=$PS1
function upload() {
    filepath=$1
    scp -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i $PEM $filepath ubuntu@${ENDPOINT}:/home/ubuntu/;
    }
function connect() {
    ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i $PEM ubuntu@${ENDPOINT}
    }
function wait_terminate_instance() {
    if [[ $profile ]];
    then
    aws ec2 wait instance-terminated --profile $profile --instance-ids $INSTANCEID;
    else
    aws ec2 wait instance-terminated --instance-ids $INSTANCEID;
    fi
    if [[ $mypid ]]
    then
        if [[ $(ps -q ${mypid} -o comm=) ]]
        then
        jobs
        fg %1 2>/dev/null
    fi
fi
echo $INSTANCEID terminated
    if [[ $terminatepid ]]
    then
        if [[ $(ps -q ${terminatepid} -o comm=) ]]
        then
        jobs
        fg %1 2>/dev/null
    fi
fi
exit
}
function terminate_instance() {
    if [[ $profile ]];
    then
    aws ec2 terminate-instances --profile $profile --instance-ids $INSTANCEID;
    else
    aws ec2 terminate-instances --instance-ids $INSTANCEID;
    fi
    echo "terminating $INSTANCEID ...";
    sleep 1;
    wait_terminate_instance & terminatepid=$!
}

export -f instructions
export -f wait_terminate_instance
export -f terminate_instance
export -f upload
export -f connect
