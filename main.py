import os
from scripts.get_data import data_orgao_deputado, data_proposicao_microdados, data_proposicao_tema, data_votacao_objeto, data_votacao_parlamentar, data_votacao
from scripts.data_processing import process_prepositions  # Import the new script

# Define the base directory to save the files
data_dir = "data/dados_abertos/"

def process_all_data():
    print("Processing orgao_deputado.csv...")
    data_orgao_deputado.process_data(os.path.join(data_dir, 'orgao_deputado.csv'))

    print("Processing proposicao_microdados.csv...")
    data_proposicao_microdados.process_data(os.path.join(data_dir, 'proposicao_microdados.csv'))

    print("Processing proposicao_tema.csv...")
    data_proposicao_tema.process_data(os.path.join(data_dir, 'proposicao_tema.csv'))

    print("Processing votacao_objeto.csv...")
    data_votacao_objeto.process_data(os.path.join(data_dir, 'votacao_objeto.csv'))

    print("Processing votacao_parlamentar.csv...")
    data_votacao_parlamentar.process_data(os.path.join(data_dir, 'votacao_parlamentar.csv'))

    print("Processing votacao.csv...")
    data_votacao.process_data(os.path.join(data_dir, 'votacao.csv'))

    print("Running prepositions analysis script...")
    process_prepositions.main()  

if __name__ == "__main__":
    process_all_data()

