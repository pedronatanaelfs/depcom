import os
import sys
print("Script Python executable:", sys.executable)
print("Script sys.path:", sys.path)

# Add the 'get_data' directory to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
get_data_dir = os.path.join(script_dir, 'depucom', 'src', 'get_data')
sys.path.append(get_data_dir)

# Import functions from the scripts
from data_orgao_deputado import get_data_orgao_deputado
from data_proposicao_microdados import get_data_proposicao_microdados
from data_proposicao_tema import get_data_proposicao_tema
from data_votacao_objeto import get_data_votacao_objeto
from data_votacao_parlamentar import get_data_votacao_parlamentar
from data_votacao import get_data_votacao

def main():
    # Define the data directory
    data_dir = 'data/processed'

    # Ensure the directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Call the functions from the scripts
    get_data_orgao_deputado(data_dir)
    get_data_proposicao_microdados(data_dir)
    get_data_proposicao_tema(data_dir)
    get_data_votacao_objeto(data_dir)
    get_data_votacao_parlamentar(data_dir)
    get_data_votacao(data_dir)

if __name__ == '__main__':
    main()
