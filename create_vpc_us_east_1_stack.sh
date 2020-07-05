#!/bin/bash
echo "Create Main VPC Stack"
echo "Can you create Main VPC Stack?"
read -p 'Y/N: ' accept
if [[ "$accept" == "Y" ]]; then
    echo "Creating the Main VPC Stack with cloudformation."
    AWS_REGION=us-east-1 aws cloudformation create-stack --stack-name MainVPCRegionStack  --template-body file://./templates/vpc_us_east_1.yaml --parameters file://./parameters/vpc_us_east_1.json --capabilities CAPABILITY_IAM
else
    echo "Operation canceled."
fi