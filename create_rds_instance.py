import boto3
import json
import time

client_cloud_formation_main = boto3.client('cloudformation', region_name='us-east-1')
client_cloud_formation_dr = boto3.client('cloudformation', region_name='us-east-2')

def create_stack():
    
    print '######### Iniciando criacao de instancia Principal RDS #########'
    with open('./templates/rds_main_instance.yaml', 'r') as cf_file:
        cft_template = cf_file.read()
        with open('./parameters/rds_main_instance.json', 'r') as param_file:
            cft_param = json.loads(param_file.read())
            response_main = client_cloud_formation_main.create_stack(
                        StackName='MainRDSStack',
                        TemplateBody=cft_template,
                        Parameters=cft_param,
                        Capabilities=[
                            'CAPABILITY_IAM'
                        ],
                        OnFailure='ROLLBACK'
                    )
    
    print '######### Verificando se a instancia foi criado com sucesso #########'                
    nao_finalizado = True
    while nao_finalizado:
        time.sleep(30)
        MainRDSStack = client_cloud_formation_main.describe_stacks(StackName='MainRDSStack')['Stacks'][0]
        MainRDSStackStatus = MainRDSStack['StackStatus']
        print MainRDSStackStatus
        if MainRDSStackStatus == 'CREATE_COMPLETE':
            nao_finalizado = False
        else:
            print 'Ainda nao finalizou'

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

create_stack()