#!/bin/bash
echo "Destroy Disaster Recovery VPC Stack"
echo "Can you destroy Disaster Recovery VPC Stack?"
read -p 'Y/N: ' accept
if [[ "$accept" == "Y" ]]; then
    echo "Destroying the Disaster Recovery VPC Stack with cloudformation."
    AWS_REGION=us-east-2 aws cloudformation delete-stack --stack-name DrVPCRegionStack 
else
    echo "Operation canceled."
fi