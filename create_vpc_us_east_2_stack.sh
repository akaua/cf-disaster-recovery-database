#!/bin/bash
echo "Create Disaster Recovery VPC Stack"
echo "Can you create Disaster Recovery VPC Stack?"
read -p 'Y/N: ' accept
if [[ "$accept" == "Y" ]]; then
    echo "Creating the Disaster Recovery VPC Stack with cloudformation."
    AWS_REGION=us-east-2 aws cloudformation create-stack --stack-name DrVPCRegionStack  --template-body file://./templates/vpc_us_east_2.yaml --parameters file://./parameters/vpc_us_east_2.json --capabilities CAPABILITY_IAM
else
    echo "Operation canceled."
fi