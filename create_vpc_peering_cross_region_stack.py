import boto3
# import json

client_cloud_formation_dr = boto3.client('cloudformation', region_name='us-east-2')
client_cloud_formation_main = boto3.client('cloudformation', region_name='us-east-1')

def create_stack():
    response_dr = client_cloud_formation_dr.list_exports()
    response_main = client_cloud_formation_main.list_exports()
    
    main_VPC = None
    main_route_table = None

    for export in response_main['Exports']:
        if export['Name'] == "MainVPCRegionStack:VPCID":
            main_VPC = export['Value']

        elif export['Name'] == "MainVPCRegionStack:PrivateRouteTable":
            main_route_table = export['Value']

    DR_VPC = None
    DR_Route_Table = None

    for export in response_dr['Exports']:
        if export['Name'] == "DrVPCRegionStack:VPCID":
            DR_VPC = export['Value']

        elif export['Name'] == "DrVPCRegionStack:PrivateRouteTable":
            DR_Route_Table = export['Value']

    with open('./templates/vpc_peering_cross_region.yaml', 'r') as cf_file:
        cft_template = cf_file.read()
        response = client_cloud_formation_main.create_stack(
                    StackName='MainPeeringVPCCrossRegionStack',
                    TemplateBody=cft_template,
                    Parameters=[
                        {
                            'ParameterKey': 'MainVPCID',
                            'ParameterValue': main_VPC
                        },
                        {
                            'ParameterKey': 'DRVPCID',
                            'ParameterValue': DR_VPC
                        },
                        {
                            'ParameterKey': 'MainPrivateRouteTable',
                            'ParameterValue': main_route_table
                        },
                        {
                            'ParameterKey': 'DRPrivateRouteTable',
                            'ParameterValue': DR_Route_Table
                        },
                        {
                            'ParameterKey': 'DRAcceptRegion',
                            'ParameterValue': 'us-east-2'
                        },
                    ],
                    Capabilities=[
                        'CAPABILITY_IAM'
                    ],
                    OnFailure='ROLLBACK'
                )
        print response

create_stack()
