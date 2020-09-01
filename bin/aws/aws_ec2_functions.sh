#!/bin/bash -e
# You need to install the AWS Command Line Interface from http://aws.amazon.com/cli/

if [[ ! $PEM ]];
then
echo "Please make sure that a key is set by entering 'export PEM=' followed by a path to key you have chosen."
exit 0;
fi

echo "waiting for $INSTANCEID ..."
read -r -d '' instructions <<-EOF
Type 'connect' to access the server
Type 'upload [FILEPATH]' to send a file to the server.
EOF

echo "$instructions"
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
function terminate_instance() {
                      if [[ $profile ]];
                      then
                      aws ec2 terminate-instances --profile $profile --instance-ids $INSTANCEID;
                      echo "terminating $INSTANCEID ...";
                      aws ec2 wait instance-terminated --profile $profile --instance-ids $INSTANCEID;
                      else
                      aws ec2 terminate-instances --instance-ids $INSTANCEID;
                      echo "terminating $INSTANCEID ...";
                      aws ec2 wait instance-terminated --instance-ids $INSTANCEID;
                      fi
                      if [[ $mypid ]]
                      then
                        jobs
                        fg %1 2>/dev/null
                      fi
                      echo $INSTANCEID terminated
}

export -f instructions
export -f terminate_instance
export -f upload
export -f connect
