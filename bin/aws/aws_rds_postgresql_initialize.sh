#!/bin/bash -e
# You need to install the AWS Command Line Interface from http://aws.amazon.com/cli/

if [[ ! $PGUSER && ! $PGPASSWORD ]];
then
echo "Please make sure that PGUSER and PGPASSWORD are set in your shell's environment."
echo "Enter 'export PGUSER=' followed by a username you have chosen."
echo "Enter 'export PGPASSWORD=' followed by a password you have chosen."
exit 0;
fi

if [[ ! $PGUSER ]];
then
echo "Please make sure that PGUSER is set in your shell's environment by entering 'export PGUSER=' followed by a username you have chosen."
exit 0;
fi

if [[ ! $PGPASSWORD ]];
then
echo "Please make sure that PGPASSWORD is set in your shell's environment by entering 'export PGPASSWORD=' followed by a password you have chosen."
exit 0;
fi

maindir=$(pwd)

awsdir="$maindir/bin/aws"

source $awsdir/aws_ec2_param_functions.sh

#setting default parameters for the instance by calling param_functions, to override any function assign the corresponding env var

valid_ports=( 22 80 443 5432 )

sgname #sets security group or creates it and opens ports for the ip of the local machine

if [[ ! $DB_NAME ]];
then
    export DB_NAME=arlingtoncourts
fi
echo $DB_NAME

if [[ ! $DB_INSTANCEID ]];
then
    export DB_INSTANCEID=arlingtoncourts
fi
echo $DB_INSTANCEID

if [[ ! $DB_STORAGE ]];
then
    export DB_STORAGE=20
fi
echo $DB_STORAGE

if [[ ! $DB_INSTANCECLASS ]];
then
    export DB_INSTANCECLASS=db.t3.large
fi
echo $DB_INSTANCECLASS

export DB_ENGINE=postgres

if [[ $profile ]];
then
export INSTANCEID_DB=$(aws rds create-db-instance \
    --profile $profile \
    --db-name $DB_NAME \
    --vpc-security-group-ids $SGID \
    --db-instance-identifier $DB_INSTANCEID \
    --allocated-storage $DB_STORAGE \
    --db-instance-class $DB_INSTANCECLASS \
    --engine $DB_ENGINE \
    --master-username $PGUSER \
    --master-user-password $PGPASSWORD \
--query "DBInstance.DBInstanceIdentifier" --output text)
else
export INSTANCEID_DB=$(aws rds create-db-instance \
    --db-name $DB_NAME \
    --vpc-security-group-ids $SGID \
    --db-instance-identifier $DB_INSTANCEID \
    --allocated-storage $DB_STORAGE \
    --db-instance-class $DB_INSTANCECLASS \
    --engine $DB_ENGINE \
    --master-username $PGUSER \
    --master-user-password $PGPASSWORD \
--query "DBInstance.DBInstanceIdentifier" --output text)
fi

echo "waiting for $INSTANCEID_DB ..."

if [[ $profile ]];
then
aws rds wait db-instance-available --profile $profile --db-instance-identifier $INSTANCEID_DB
else
aws rds wait db-instance-available --db-instance-identifier $INSTANCEID_DB
fi

if [[ $profile ]];
then
export ENDPOINT_DB=$(aws rds describe-db-instances --profile $profile --db-instance-identifier $INSTANCEID_DB --query "DBInstances[0].Endpoint.Address" --output text)
else
export ENDPOINT_DB=$(aws rds describe-db-instances --db-instance-identifier $INSTANCEID_DB --query "DBInstances[0].Endpoint.Address" --output text)
fi

echo "$INSTANCEID_DB is available and listening on [$ENDPOINT_DB]."

export PGHOST="${ENDPOINT_DB}"

export DB_HOST=${PGHOST}

export fec_DB_HOST=${PGHOST}

export SGID="${SGID}"

echo "Type 'terminate_db' to shut down and delete the database."

function terminate_db() {
                      SNAPSHOTID=${INSTANCEID_DB}-$(date +%F-%H%M%S%Z);
                      if [[ $profile ]];
                      then
                      aws rds delete-db-instance --profile $profile --db-instance-identifier $INSTANCEID_DB --no-delete-automated-backups --no-skip-final-snapshot --final-db-snapshot-identifier $SNAPSHOTID;
                      echo "terminating $INSTANCEID_DB ...";
                      aws rds wait db-instance-deleted --profile $profile --db-instance-identifier $INSTANCEID_DB;
                      else
                      aws rds delete-db-instance --db-instance-identifier $INSTANCEID_DB --no-delete-automated-backups --no-skip-final-snapshot --final-db-snapshot-identifier $SNAPSHOTID;
                      echo "terminating $INSTANCEID_DB ...";
                      aws rds wait db-instance-deleted --db-instance-identifier $INSTANCEID_DB;
                      fi
                      echo $INSTANCEID_DB terminated
}

export -f terminate_db

exec $SHELL -i
