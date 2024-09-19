import basedosdados as bd
import os

def get_data_orgao_deputado(data_dir):
    # Load the data directly into pandas
    df = bd.read_table(dataset_id='br_camara_dados_abertos',
                       table_id='orgao_deputado',
                       billing_project_id="voting-networks")

    # Ensure the directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Full path of the file
    file_path = os.path.join(data_dir, 'orgao_deputado.csv')

    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)