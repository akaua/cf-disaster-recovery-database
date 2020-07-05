#!/bin/bash
echo "Destroy Main VPC Peering Cross Region Stack"
echo "Can you destroy Main VPC Peering Cross Region Stack?"
read -p 'Y/N: ' accept
if [[ "$accept" == "Y" ]]; then
    echo "Destroying the Main VPC Peering Cross Region Stack with cloudformation."
    AWS_REGION=us-east-1 aws cloudformation delete-stack --stack-name MainPeeringVPCCrossRegionStack 
else
    echo "Operation canceled."
fi