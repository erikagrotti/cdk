import uuid
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tab_custom_cdk')  

def get_user_id_from_event(event):
    logger.info("Evento recebido na função get_user_id_from_event: %s", event)
    try:
        authorization_header = event['headers'].get('Authorization', event['headers'].get('authorization', None))
        if not authorization_header:
            raise KeyError("Token JWT não encontrado no cabeçalho 'Authorization/authorization'")

        logger.info("Cabeçalho de autorização: %s", authorization_header)
        token = authorization_header.split('Bearer ')[1]
        logger.info("Token JWT recebido: %s", token)

        cognito_client = boto3.client('cognito-idp')
        response = cognito_client.get_user(AccessToken=token)
        user_id = response['Username']
        logger.info("User ID extraído: %s", user_id)
        return user_id

    except ClientError as e:
        logger.exception("Erro de cliente Boto3 durante a autenticação:")
        raise Exception("Erro ao autenticar usuário: " + str(e))
    except KeyError as e:
        logger.exception("Chave ausente no evento durante a autenticação:")
        raise Exception(f"Erro ao autenticar usuário: Chave ausente - {e}")
    except IndexError as e:
        logger.exception("Erro de índice ao processar o token:")
        raise Exception("Formato inválido do token JWT no cabeçalho 'Authorization': " + str(e))
    except Exception as e:
        logger.exception("Erro genérico durante a autenticação:")
        raise Exception("Erro ao autenticar usuário: " + str(e))

def lambda_handler(event, context):
    logger.info("Evento Recebido: %s", event)
    body = {}
    statusCode = 200
    headers = {
        "Content-Type": "application/json",
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }

    try:
        method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']
        user_id = get_user_id_from_event(event)

        if method == "POST" and path == "/items":
            if 'body' not in event:
                raise ValueError("O corpo da requisição está ausente")

            requestJSON = json.loads(event['body'])
            list_id = str(uuid.uuid4())  
            list_sk = f"LIST#{list_id}"  

            try:
               
                table.put_item(Item={
                    'PK': f"USER#{user_id}",
                    'SK': f"{list_sk}#TASK#T000",
                    'taskID': 'T000',
                    'title': requestJSON.get('title', 'Nova Lista'),
                    'status': 'pendente',
                    'listID': list_id
                })

                
                tasks = requestJSON.get('tasks', [])
                for index, task in enumerate(tasks, start=1):
                    task_id = f'T{index:03}'
                    table.put_item(Item={
                        'PK': f"USER#{user_id}",
                        'SK': f"{list_sk}#TASK#{task_id}",
                        'taskID': task_id,
                        'title': task.get('title'),
                        'status': task.get('status', 'pendente')
                    })

                body = {'message': f'Lista criada com sucesso com listID {list_id}'}
                statusCode = 201 

            except Exception as e:
                statusCode = 500
                body = {'error': str(e)}
                logger.exception("Erro ao criar lista de tarefas:")

            return {
                "statusCode": statusCode,
                "headers": headers,
                "body": json.dumps(body)
            }

        elif method == "GET" and path == "/items":
            try:
                response = table.query(
                    KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(f"USER#{user_id}") &
                                         boto3.dynamodb.conditions.Key('SK').begins_with("LIST#")
                )
                items = response.get('Items', [])
                body = items
                statusCode = 200

            except Exception as e:
                statusCode = 500
                body = {'error': str(e)}
                logger.exception("Erro ao obter listas de tarefas:")

            return {
                "statusCode": statusCode,
                "headers": headers,
                "body": json.dumps(body)
            }

        elif method == "GET" and path.startswith("/items/"):
            list_id = path.split("/")[2]  
            list_sk = f"LIST#{list_id}"
            
            try:
               
                response = table.query(
                    KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(f"USER#{user_id}") &
                                         boto3.dynamodb.conditions.Key('SK').begins_with(list_sk)
                )
                items = response.get('Items', [])
                body = items
                statusCode = 200

            except Exception as e:
                statusCode = 500
                body = {'error': str(e)}
                logger.exception("Erro ao obter a lista de tarefas:")

            return {
                "statusCode": statusCode,
                "headers": headers,
                "body": json.dumps(body)
            }

        elif method == "PATCH" and path.startswith("/items/") and path.endswith("/status"):
            list_id = path.split("/")[2] 
            task_id = path.split("/")[3]
            requestJSON = json.loads(event['body'])

            try:
                new_status = requestJSON.get('status')
                if not new_status:
                    raise ValueError('status é obrigatório para atualização.')

                table.update_item(
                    Key={
                        'PK': f"USER#{user_id}",
                        'SK': f"LIST#{list_id}#TASK#{task_id}"
                    },
                    UpdateExpression="SET #s = :s",
                    ExpressionAttributeNames={
                        '#s': 'status'
                    },
                    ExpressionAttributeValues={
                        ':s': new_status
                    }
                )
                body = {'message': f'Status atualizado com sucesso para taskID {task_id}'}
                statusCode = 200

            except Exception as e:
                statusCode = 500
                body = {'error': str(e)}
                logger.exception(f"Erro ao atualizar status da lista {list_id}:")

            return {
                "statusCode": statusCode,
                "headers": headers,
                "body": json.dumps(body)
            }

        elif method == "PATCH" and path.startswith("/items/"):
            list_id = path.split("/")[2]  
            requestJSON = json.loads(event['body'])
            list_sk = f"LIST#{list_id}"

            try:
                
                if 'title' in requestJSON:
                    table.update_item(
                        Key={
                            'PK': f"USER#{user_id}",
                            'SK': f"{list_sk}#TASK#T000"
                        },
                        UpdateExpression="SET #t = :t",
                        ExpressionAttributeNames={'#t': 'title'},
                        ExpressionAttributeValues={':t': requestJSON['title']}
                    )

                
                for task in requestJSON.get('tasks', []):
                    task_id = task['taskID']
                    table.put_item(Item={
                        'PK': f"USER#{user_id}",
                        'SK': f"{list_sk}#TASK#{task_id}",
                        'taskID': task_id,
                        'title': task.get('title'),
                        'status': task.get('status', 'pendente')
                    })

                body = {'message': f'Lista atualizada com sucesso para listID {list_id}'}
                statusCode = 200

            except Exception as e:
                statusCode = 500
                body = {'error': str(e)}
                logger.exception(f"Erro ao atualizar a lista {list_id}:")

            return {
                "statusCode": statusCode,
                "headers": headers,
                "body": json.dumps(body)
            }

        elif method == "DELETE" and path.startswith("/items/"):
            parts = path.split("/")
            if len(parts) == 4:  
                list_id = parts[2]
                task_id = parts[3]
                task_sk = f"LIST#{list_id}#TASK#{task_id}"

                try:
                    table.delete_item(
                        Key={
                            'PK': f"USER#{user_id}",
                            'SK': task_sk
                        }
                    )

                    body = {'message': f'Tarefa {task_id} da lista {list_id} deletada com sucesso'}
                    statusCode = 200  

                except Exception as e:
                    statusCode = 500
                    body = {'error': str(e)}
                    logger.exception(f"Erro ao deletar tarefa {task_id} da lista {list_id}:")

            elif len(parts) == 3:  
                list_id = parts[2]
                list_sk = f"LIST#{list_id}"

                try:
                   
                    response = table.query(
                        KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(f"USER#{user_id}") &
                                             boto3.dynamodb.conditions.Key('SK').begins_with(list_sk)
                    )
                    items = response.get('Items', [])
                    with table.batch_writer() as batch:
                        for item in items:
                            batch.delete_item(
                                Key={
                                    'PK': item['PK'],
                                    'SK': item['SK']
                                }
                            )

                    body = {'message': f'Lista {list_id} deletada com sucesso'}
                    statusCode = 200  

                except Exception as e:
                    statusCode = 500
                    body = {'error': str(e)}
                    logger.exception("Erro ao deletar lista de tarefas:")

            else:
                statusCode = 404
                body = {'message': 'Rota não encontrada'}

        else:
            statusCode = 405
            body = {'message': 'Método não permitido'}

    except Exception as e:
        statusCode = 500
        body = {'error': str(e)}
        logger.exception("Erro no manipulador Lambda:")

    return {
        "statusCode": statusCode,
        "headers": headers,
        "body": json.dumps(body)
    }
