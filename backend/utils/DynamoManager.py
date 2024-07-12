import os
from datetime import datetime
from uuid import uuid4

import boto3
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
                'id': str(uuid4()),
                'url': url,
                'short_url': short_url,
                'date': datetime.now().strftime('%Y-%m-%d'),
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
                    'short_url': short_url
                }
            )
        except Exception as e:
            print(e)
            return

        if 'Item' in response:
            item = response['Item']
            print("Item retrieved successfully:")
            print(item)
        else:
            print("Item not found")

        item = response['Item']
        item['count_clicks'] += 1

        table.put_item(Item=item)
