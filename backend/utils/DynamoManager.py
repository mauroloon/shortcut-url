import os
from datetime import datetime
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

load_dotenv()


REGION_AWS = os.getenv('REGION')


class DynamoManager:

    @staticmethod
    def save_url(
        url: str,
        short_url: str,
    ) -> None:
        """
        Guarda la url original y la url corta en DynamoDB.

        Args:
            url (str): Url original.
            short_url (str): Url corta.

        Returns:
            None

        Created:
            - 11/07/2024
        """
        dynamodb = boto3.resource('dynamodb', region_name=REGION_AWS)
        table = dynamodb.Table('short_urls')

        # Subir el token a DynamoDB
        table.put_item(
            Item={
                'id': short_url,
                'url': url,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'last_date_click': '',
                'count_clicks': 0,
            }
        )

    def update_clicks(
        short_url: str,
    ) -> None:
        """
        Actualiza el contador de clicks de una url corta.

        Args:
            short_url (str): Url corta.

        Returns:
            None

        Created:
            - 11/07/2024
        """
        dynamodb = boto3.resource('dynamodb', region_name=REGION_AWS)
        table = dynamodb.Table('short_urls')
        try:
            response = table.get_item(
                Key={
                    'id': short_url
                }
            )
        except Exception as e:
            print(e)
            return

        item = response['Item']
        # NOTE: Al traer 'count_clicks' lo trae como string por lo que no sirve
        # hacer item['count_clicks'] += 1
        item['count_clicks'] = int(item['count_clicks']) + 1
        item['last_date_click'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        table.put_item(Item=item)
        return item['url']
