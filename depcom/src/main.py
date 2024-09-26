import pandas as pd
import numpy as np
import random
from utils import data_acquisition, data_processing, optimize_polarization_interval, save_results

def main():
    # Set the fixed random state
    fixed_random_state = 42

    # Set random seeds
    random.seed(fixed_random_state)
    np.random.seed(fixed_random_state)

    # Step 1: Data Acquisition
    #data_acquisition()

    # Step 2: Data Processing
    df_filtered, num_propositions_before, df_orgao_deputado = data_processing()

    # Step 3: Prepare voting data
    df_votacao_parlamentar = pd.read_csv('data/csv/votacao_parlamentar.csv')

    # Prepare deputies information
    df_deputados = df_votacao_parlamentar[['id_deputado', 'nome', 'sigla_partido', 'sigla_uf']].drop_duplicates(subset='id_deputado')

    # Step 4: Optimize Polarization Interval and Perform Analysis
    final_results = optimize_polarization_interval(df_filtered, df_deputados, fixed_random_state)

    # Step 5: Save Final Results
    save_results(final_results)

if __name__ == "__main__":
    main()