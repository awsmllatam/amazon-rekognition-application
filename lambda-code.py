import json
import boto3

def lambda_handler(event, context):

    rekognition = boto3.client('rekognition')
    dynamodb = boto3.client('dynamodb')
    
    bucketName = event['Records'][0]['s3']['bucket']['name']
    imagePath = event['Records'][0]['s3']['object']['key']
    
    detectLabelsResponse = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': imagePath,
            }
        }
    )
    
    dataload = ' | '

    for labels in detectLabelsResponse['Labels']:
        dataload = dataload + labels['Name'] + ' | '
    
    dynamodb.put_item(TableName='my-table', Item={'imageName':{'S':bucketName + "/" + imagePath},'information':{'S': dataload}})

    return {
        'statusCode': 200,
        'body': json.dumps(dataload)
    }