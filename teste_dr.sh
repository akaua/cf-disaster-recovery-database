#!/bin/bash
echo "Create Main VPC Stack"
echo "Can you create Main VPC Stack?"
read -p 'Y/N: ' accept
if [[ "$accept" == "Y" ]]; then
    echo "Creating the Main VPC Stack with cloudformation."
    AWS_REGION=us-east-2 aws cloudformation create-stack --stack-name DRInstanceRDS  --template-body file://./templates/rds_dr_instance.yaml --parameters file://./parameters/rds_dr_instance.json --capabilities CAPABILITY_IAM
else
    echo "Operation canceled."
fi