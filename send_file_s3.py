import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd  # Adicionei a importação do pandas para trabalhar com Excel


def get_credentials_aws():
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    return access_key_id, secret_access_key, bucket_name


def upload_to_s3_aws(
    file_name, access_key_id, secret_access_key, bucket_name, destination_path
):
    s3_client = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )
    try:
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y/%m/%d")

        # Alteração no nome do arquivo para adicionar "-2"
        upload_path = os.path.join(
            destination_path,
            formatted_date,
            os.path.basename(file_name).replace(".mp3", "-2.mp3"),
        )

        response = s3_client.upload_file(file_name, bucket_name, upload_path)

        # Definir o tempo de expiração desejado (3 anos)
        tempo_expiracao = 94608000  # em segundos (60 * 60 * 24 * 365 * 3)

        # Calcular o tempo de expiração
        expiration_time = datetime.utcnow() + timedelta(seconds=tempo_expiracao)

        # Geração do URL assinado para download
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": upload_path},
            ExpiresIn=tempo_expiracao,
        )

        print(f"URL para download do arquivo: {url}")
        return url
    except ClientError as e:
        logging.error(e)
        return None


def main():
    base_folder = "audios"
    destination_folder = "reprocessamento"
    excel_data = []

    access_key_id, secret_access_key, bucket_name = get_credentials_aws()

    if access_key_id and secret_access_key and bucket_name:
        for root, dirs, files in os.walk(base_folder):
            for file_name in files:
                if file_name.endswith(".mp3"):
                    full_path = os.path.join(root, file_name)
                    print(f"Upload para AWS S3: {full_path}")

                    # Alteração na chamada da função para incluir o novo destino
                    url = upload_to_s3_aws(
                        full_path,
                        access_key_id,
                        secret_access_key,
                        bucket_name,
                        destination_folder,
                    )

                    if url:
                        file_id = os.path.splitext(file_name)[0]
                        excel_data.append({"id": file_id, "link": url})
                else:
                    logging.warning(
                        f"Arquivo {file_name} não é um arquivo de áudio MP3."
                    )

        # Criando o DataFrame e salvando para um arquivo Excel
        df = pd.DataFrame(excel_data)
        df.to_excel("output.xlsx", index=False)
        print("Planilha Excel criada com sucesso.")
    else:
        logging.error("Credenciais AWS não configuradas corretamente")


if __name__ == "__main__":
    load_dotenv()
    main()
