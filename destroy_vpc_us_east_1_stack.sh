#!/bin/bash
echo "Destroy Main VPC Stack"
echo "Can you destroy Main VPC Stack?"
read -p 'Y/N: ' accept
if [[ "$accept" == "Y" ]]; then
    echo "Destroying the Main VPC Stack with cloudformation."
    AWS_REGION=us-east-1 aws cloudformation delete-stack --stack-name MainVPCRegionStack 
else
    echo "Operation canceled."
fi