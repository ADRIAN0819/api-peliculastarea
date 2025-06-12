import boto3
import uuid
import os
import json
import traceback

def lambda_handler(event, context):
    try:
        # Log de entrada
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido",
                "event": event
            }
        }))

        # Parseo de datos de entrada
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Preparación del ítem a insertar
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        # Inserción en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de éxito
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada exitosamente",
                "pelicula": pelicula
            }
        }))

        return {
            'statusCode': 200,
            'body': json.dumps({
                'pelicula': pelicula,
                'response': response
            })
        }

    except Exception as e:
        # Captura y log del error
        error_trace = traceback.format_exc()
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": str(e),
                "traceback": error_trace
            }
        }))

        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
