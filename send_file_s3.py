import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
from dotenv import load_dotenv # pip3 install python-dotenv

def get_credentials_aws():
    cloud_type = os.getenv('AccessKey')
    access_key_id = os.getenv('SecretKey')
    secret_access_key = os.getenv('BucketName')
    return cloud_type, access_key_id, secret_access_key    

def upload_to_s3_aws(file_name, cloud_type, access_key_id, secret_access_key, bucket_name):
    if cloud_type == 'aws':
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        try:
            # Obter a data atual
            current_date = datetime.now()
            
            # Formatar a data no formato YYYY/MM/DD
            formatted_date = current_date.strftime('%Y/%m/%d')
            
            # Montar o caminho completo para o upload
            upload_path = os.path.join(formatted_date, os.path.basename(file_name))
            
            response = s3_client.upload_file(file_name, bucket_name, upload_path)
            
            # Check if the file was uploaded successfully
            try:
                s3_client.head_object(Bucket=bucket_name, Key=upload_path)
                print(f"Arquivo {upload_path} enviado com sucesso para o bucket {bucket_name}")
                return True
            except ClientError as e:
                logging.error(f"Erro ao verificar objeto no bucket: {e}")
                return False   
        except ClientError as e:
            logging.error(e)
            return False
    elif cloud_type == 'google':
        send_google(file_name)
        return True
    else:
        logging.error("Invalid cloud type")
        return False

def main():
    file_name = '132.mp3'
    
    cloud_type, access_key_id, secret_access_key = get_credentials_aws()
        
    if cloud_type:
        print(cloud_type)
        #upload_to_s3_aws(file_name, cloud_type, access_key_id, secret_access_key, 'test-s3-callface2')
    else:
        logging.error("Invalid cloud type in database")

if __name__ == "__main__":
    main()
