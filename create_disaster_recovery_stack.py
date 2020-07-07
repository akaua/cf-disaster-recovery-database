import boto3
import json
import time

client_cloud_formation_dr = boto3.client('cloudformation', region_name='us-east-2')
client_cloud_formation_main = boto3.client('cloudformation', region_name='us-east-1')

def start():
    res = raw_input("Voce gostaria de criar a stack: (Y/N) \n") 
    if res.lower()=='y': 
        print "Iniciando Criacao"
    else:
        print 'Cancelando'
        exit()


def verificar_criacao_stack_main(stack_name):
    nao_finalizado = True
    while nao_finalizado:
        time.sleep(30)
        Stack = client_cloud_formation_main.describe_stacks(StackName=stack_name)['Stacks'][0]
        StackStatus = Stack['StackStatus']
        print StackStatus
        if StackStatus == 'CREATE_COMPLETE':
            nao_finalizado = False
        else:
            print 'Ainda nao finalizou'

def verificar_criacao_stack_dr(stack_name):
    nao_finalizado = True
    while nao_finalizado:
        time.sleep(30)
        Stack = client_cloud_formation_dr.describe_stacks(StackName=stack_name)['Stacks'][0]
        StackStatus = Stack['StackStatus']
        print StackStatus
        if StackStatus == 'CREATE_COMPLETE':
            nao_finalizado = False
        else:
            print 'Ainda nao finalizou'

def create_stack_vpc_east_1():
    print '######### Iniciando criacao de VPC Principal #########'
    stack_name = 'MainVPCRegionStack'
    with open('./templates/vpc_us_east_1.yaml', 'r') as cf_main_vpc_file:
        cft_main_vpc_template = cf_main_vpc_file.read()
        with open('./parameters/vpc_us_east_1.json', 'r') as param_main_vpc_file:
            cft_main_vpc_param = json.loads(param_main_vpc_file.read())
            response_dr = client_cloud_formation_main.create_stack(
                        StackName=stack_name,
                        TemplateBody=cft_main_vpc_template,
                        Parameters=cft_main_vpc_param,
                        Capabilities=[
                            'CAPABILITY_IAM'
                        ],
                        OnFailure='ROLLBACK'
                    )
    print '######### Verificando se VPC principal foi criada com sucesso #########'   
    verificar_criacao_stack_main(stack_name=stack_name)
    print '######### Finalizada criacao de VPC principal com sucesso #########'  

def create_stack_vpc_east_2():
    print '######### Iniciando criacao de VPC Disaster Recovery #########'
    stack_name = 'DrVPCRegionStack'
    with open('./templates/vpc_us_east_2.yaml', 'r') as cf_main_vpc_file:
        cft_main_vpc_template = cf_main_vpc_file.read()
        with open('./parameters/vpc_us_east_2.json', 'r') as param_main_vpc_file:
            cft_main_vpc_param = json.loads(param_main_vpc_file.read())
            response_dr = client_cloud_formation_dr.create_stack(
                        StackName=stack_name,
                        TemplateBody=cft_main_vpc_template,
                        Parameters=cft_main_vpc_param,
                        Capabilities=[
                            'CAPABILITY_IAM'
                        ],
                        OnFailure='ROLLBACK'
                    )
    print '######### Verificando se VPC Disaster Recovery foi criada com sucesso #########'   
    verificar_criacao_stack_dr(stack_name=stack_name)
    print '######### Finalizada criacao de VPC Disaster Recovery com sucesso #########'  

def create_stack_peering_connection():
    print '######### Buscando Informacoes das VPC para conectar #########'
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
    print '######### Iniciando criacao de Peering connection cross region #########'
    stack_name='MainPeeringVPCCrossRegionStack'
    with open('./templates/vpc_peering_cross_region.yaml', 'r') as cf_file:
        cft_template = cf_file.read()
        response = client_cloud_formation_main.create_stack(
                    StackName=stack_name,
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
    
    print '######### Verificando se Peering connection cross region foi criada com sucesso #########'   
    verificar_criacao_stack_main(stack_name=stack_name)
    print '######### Finalizada criacao de Peering connection cross region com sucesso #########'  

def create_stack_rds():
    stack_name='MainRDSStack'
    print '######### Iniciando criacao de instancia Principal RDS #########'
    with open('./templates/rds_main_instance.yaml', 'r') as cf_file:
        cft_template = cf_file.read()
        with open('./parameters/rds_main_instance.json', 'r') as param_file:
            cft_param = json.loads(param_file.read())
            response_main = client_cloud_formation_main.create_stack(
                        StackName=stack_name,
                        TemplateBody=cft_template,
                        Parameters=cft_param,
                        Capabilities=[
                            'CAPABILITY_IAM'
                        ],
                        OnFailure='ROLLBACK'
                    )
    
    print '######### Verificando se a instancia foi criado com sucesso #########'                
    verificar_criacao_stack_main(stack_name=stack_name)
    print '######### Finalizada criacao da instancia principal com sucesso #########'  

    print '######### Iniciando criacao de instancia de Disaster Recovery em outra regiao #########'          
    with open('./templates/rds_dr_instance.yaml', 'r') as cf_dr_file:
        cft_dr_template = cf_dr_file.read()
        with open('./parameters/rds_dr_instance.json', 'r') as param_dr_file:
            cft_dr_param = json.loads(param_dr_file.read())
            response_dr = client_cloud_formation_dr.create_stack(
                        StackName='DRRDSStack',
                        TemplateBody=cft_dr_template,
                        Parameters=cft_dr_param,
                        Capabilities=[
                            'CAPABILITY_IAM'
                        ],
                        OnFailure='ROLLBACK'
                    )
    print '######### Finalizada criacao da instancia de Disaster Recovery com sucesso #########' 
 

start()
create_stack_vpc_east_1()
create_stack_vpc_east_2()
create_stack_peering_connection()
create_stack_rds()