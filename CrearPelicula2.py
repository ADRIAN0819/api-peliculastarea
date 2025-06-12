import boto3
import uuid
import os
import json
import traceback

def lambda_handler(event, context):
    try:
        # Si viene como string, parseamos el JSON
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})

        # Log de entrada (INFO)
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido",
                "body": body
            }
        }))

        # Extracción de datos
        tenant_id = body['tenant_id']
        pelicula_datos = body['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Preparación del ítem DynamoDB
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

        # Log de éxito (INFO)
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
        # Captura y log de error (ERROR)
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
