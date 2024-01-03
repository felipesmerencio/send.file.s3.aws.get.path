# Install dependencias

```
pip install mysql.connector boto3
```

# Variables

```
export CF_DB_HOST=seu_host
export CF_DB_USER=seu_usuario
export CF_DB_PASSWORD=sua_senha
```

# Criação de estrutura de tabela

```
CREATE TABLE `setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `days_to_keep` int(11) NOT NULL,
  `recording_location` varchar(50) DEFAULT 'aws',
  `updated` datetime(3) NOT NULL DEFAULT current_timestamp(3),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE callface.recording_settings (
    description VARCHAR(20) PRIMARY KEY,
    aws_access_key_id VARCHAR(50),
    aws_secret_access_key VARCHAR(50),
    bucket_name VARCHAR(50),
    google_credentials JSON,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Informativo

Na tabela setting especificar para o cloud que esta sendo utilizando para o envio da gravação. Que pode ser aws ou google
