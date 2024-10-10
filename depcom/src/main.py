import pandas as pd
import numpy as np
import random
from utils import data_acquisition, data_processing, optimize_polarization_interval, save_results
import os
from analysis import generate_all_plots  # Importando a função para gerar os gráficos
from analysis_communities import generate_all_party_inclination_plots  # Importando a função para gerar os gráficos de inclinação
from party_analysis import (
    load_graphs, 
    get_party_percentages_by_year, 
    rank_parties_by_deputies, 
    get_parties_by_year, 
    get_deputados_for_retained_parties, 
    get_deputados_for_current_parties, 
    rank_parties_by_percentage_difference, 
    get_top_parties_per_community_last_year, 
    plot_party_comparison_consistent
)

def main():
    # Set the fixed random state
    fixed_random_state = 42

    # Set random seeds
    random.seed(fixed_random_state)
    np.random.seed(fixed_random_state)

    # Step 1: Data Acquisition
    #data_acquisition()

    # Step 2: Data Processing
    #df_filtered, num_propositions_before, df_orgao_deputado = data_processing()
    #if df_filtered is None:
    #    print("Erro no processamento de dados. Encerrando o script.")
    #    return

    # Step 3: Prepare voting data
    #df_votacao_parlamentar = pd.read_csv('data/csv/votacao_parlamentar.csv')

    # Prepare deputies information
    #df_deputados = df_votacao_parlamentar[['id_deputado', 'nome', 'sigla_partido', 'sigla_uf']].drop_duplicates(subset='id_deputado')

    # Step 4: Optimize Polarization Interval and Perform Analysis
    #final_summary_results, detailed_results = optimize_polarization_interval(df_filtered, df_deputados, fixed_random_state)


    # Step 5: Save Final Results
    #save_results(final_summary_results, detailed_results)

    # Passo 6: Gerar Gráficos de Análise
    #detailed_results_path = 'data/detailed_results.csv'
    #plots_output_dir = 'data/plots'

    # Salvar os dados resumidos para análise (já foi salvo pela função save_results)
    # Gerar todos os gráficos
    #generate_all_plots(detailed_results_path, plots_output_dir)

    graphs_dir = 'data/graphs'
    #generate_all_party_inclination_plots(graphs_dir, plots_output_dir)

    # Carregar os grafos
    graphs = load_graphs(graphs_dir)
    
    # Extrair os dados dos partidos e comunidades ao longo dos anos
    party_data_by_year = get_party_percentages_by_year(graphs)
    
    # Rankear partidos com maior número de deputados
    party_ranking = rank_parties_by_deputies(party_data_by_year)
    
    # Listar partidos que aparecem em todos os anos e no último ano
    retained_parties, current_parties = get_parties_by_year(party_data_by_year)
    
    # Deputados por comunidade para os partidos que se mantiveram
    retained_parties_data = get_deputados_for_retained_parties(party_data_by_year, retained_parties)
    
    # Deputados por comunidade para os partidos atuais
    current_parties_data = get_deputados_for_current_parties(party_data_by_year, current_parties)
    
    # Rankear partidos baseados na diferença percentual de deputados entre comunidades
    percentage_diff_ranking = rank_parties_by_percentage_difference(party_data_by_year, current_parties)
    
    # Verificar o top partido de cada comunidade no ano mais recente
    top_parties_last_year = get_top_parties_per_community_last_year(party_data_by_year)
    
    # Plotar comparações dos partidos com os maiores partidos de cada comunidade (apenas top 7)
    plot_party_comparison_consistent(party_data_by_year, top_parties_last_year, partido_1="PL", partido_0="PT", top_n=7)

if __name__ == "__main__":
    main()