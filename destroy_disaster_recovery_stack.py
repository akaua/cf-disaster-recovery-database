import boto3
import time

client_cloud_formation_dr = boto3.client('cloudformation', region_name='us-east-2')
client_cloud_formation_main = boto3.client('cloudformation', region_name='us-east-1')

def start():
    res = raw_input("Voce gostaria de destruir a stack: (Y/N) \n") 
    if res.lower()=='y': 
        print "Iniciando destruicao"
    else:
        print 'Cancelando'
        exit()

def verificar_delete_stack_main(stack_name):
    nao_finalizado = True
    while nao_finalizado:
        time.sleep(30)
        try:
            Stack = client_cloud_formation_main.describe_stacks(StackName=stack_name)['Stacks'][0]
            StackStatus = Stack['StackStatus']
            print StackStatus
            print 'Ainda nao finalizou'
        except Exception:
            nao_finalizado = False



def verificar_delete_stack_dr(stack_name):
    nao_finalizado = True
    while nao_finalizado:
        time.sleep(30)
        try:
            Stack = client_cloud_formation_dr.describe_stacks(StackName=stack_name)['Stacks'][0]
            StackStatus = Stack['StackStatus']
            print StackStatus
            print 'Ainda nao finalizou'
        except Exception:
            nao_finalizado = False

def destroy_stack_vpc_east_1():
    print '######### Iniciando destruicao de VPC Principal #########'
    stack_name = 'MainVPCRegionStack'
    response_main = client_cloud_formation_main.delete_stack(StackName=stack_name)
    print '######### Verificando se VPC principal foi destruida com sucesso #########'   
    verificar_delete_stack_main(stack_name=stack_name)
    print '######### Finalizada destruicao de VPC principal com sucesso #########'  

def destroy_stack_vpc_east_2():
    print '######### Iniciando destruicao de VPC Disaster Recovery #########'
    stack_name = 'DrVPCRegionStack'
    response_dr = client_cloud_formation_dr.delete_stack(StackName=stack_name)
    print '######### Verificando se VPC Disaster Recovery foi destruida com sucesso #########'   
    verificar_delete_stack_dr(stack_name=stack_name)
    print '######### Finalizada destruicao de VPC Disaster Recovery com sucesso #########'  

def destroy_stack_peering_connection():
    print '######### Iniciando destruicao de Peering connection cross region #########'
    stack_name='MainPeeringVPCCrossRegionStack'
    response = client_cloud_formation_main.delete_stack(StackName=stack_name)
    print '######### Verificando se Peering connection cross region foi destruido com sucesso #########'   
    verificar_delete_stack_main(stack_name=stack_name)
    print '######### Finalizada destruicao de Peering connection cross region com sucesso #########'

def destroy_stack_peering_connection_dr():
    print '######### Iniciando destruicao de Peering connection cross region #########'
    stack_name='DrPeeringVPCCrossRegionStack'
    response = client_cloud_formation_dr.delete_stack(StackName=stack_name)
    print '######### Verificando se Peering connection cross region foi destruido com sucesso #########'   
    verificar_delete_stack_dr(stack_name=stack_name)
    print '######### Finalizada destruicao de Peering connection cross region com sucesso #########'
   

def destroy_stack_rds():
    print '######### Iniciando destruicao de instancia de Disaster Recovery em outra regiao #########'          
    stack_name='DRRDSStack'
    response_dr = client_cloud_formation_dr.delete_stack(StackName='DRRDSStack')
    print '######### Finalizada destruicao da instancia de Disaster Recovery com sucesso #########' 
    
    print '######### Verificando se a instancia foi destruida com sucesso #########'                
    verificar_delete_stack_dr(stack_name=stack_name)
    print '######### Finalizada criacao da instancia Disaster Recovery com sucesso #########'  
    
    print '######### Iniciando destruicao de instancia Principal RDS #########'
    response_main = client_cloud_formation_main.delete_stack(StackName='MainRDSStack')

    print '######### Verificando se a instancia foi destruida com sucesso #########'                
    verificar_delete_stack_main(stack_name='MainRDSStack')
    print '######### Finalizada criacao da instancia principal com sucesso #########'  

start()
destroy_stack_rds()
destroy_stack_peering_connection_dr()
destroy_stack_peering_connection()
destroy_stack_vpc_east_2()
destroy_stack_vpc_east_1()



