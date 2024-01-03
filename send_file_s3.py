import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
from dotenv import load_dotenv  # pip3 install python-dotenv

def get_credentials_aws():
    access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    return access_key_id, secret_access_key, bucket_name

def upload_to_s3_aws(file_name, access_key_id, secret_access_key, bucket_name):
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
            # Gerar o URL assinado para download
            url = s3_client.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket_name, 'Key': upload_path},
                                            )
        
            print(f"URL para download do arquivo: {url}")
            return True
        except Exception as e:
            print(f"Erro ao gerar URL assinado: {e}") 
            return False              
    except ClientError as e:
        logging.error(e)
        return False

def main():
    file_name = '132.mp3'
    
    access_key_id, secret_access_key, bucket_name = get_credentials_aws()
        
    if access_key_id and secret_access_key and bucket_name:
        # Adicionando a verificação de se o arquivo realmente existe
        if os.path.isfile(file_name):
            print(f"Upload para AWS S3: {file_name}")
            upload_to_s3_aws(file_name, access_key_id, secret_access_key, bucket_name)
        else:
            logging.error(f"O arquivo {file_name} não existe.")
    else:
        logging.error("Credenciais AWS não configuradas corretamente")

if __name__ == "__main__":
    load_dotenv()  # Certifique-se de carregar as variáveis de ambiente do arquivo .env
    main()
