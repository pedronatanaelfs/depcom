import pandas as pd
import numpy as np
import random
from utils import data_acquisition, data_processing, optimize_polarization_interval, save_results
import os
from D_generate_plots import (
    generate_all_plots, 
    generate_all_party_inclination_plots,
    load_graphs, 
    get_party_percentages_by_year, 
    rank_parties_by_deputies, 
    get_parties_by_year, 
    get_deputados_for_retained_parties, 
    get_deputados_for_current_parties, 
    rank_parties_by_percentage_difference, 
    get_top_parties_per_community_last_year, 
    plot_party_comparison_consistent,
    export_party_community_table, 
    clean_dataframe, 
    adjust_community_labels, 
    sort_columns, 
    get_last_year, 
    export_dataframe_to_csv,
    plot_community_graphs,
    get_min_community_generalized,
    merge_min_community_with_suffix_change)

def main():
    # Set the fixed random state
    fixed_random_state = 42

    # Set random seeds
    random.seed(fixed_random_state)
    np.random.seed(fixed_random_state)

    #Prepare voting data
    df_votacao_parlamentar = pd.read_csv('data/csv/votacao_parlamentar.csv')

    # Prepare deputies information
    df_deputados = df_votacao_parlamentar[['id_deputado', 'nome', 'sigla_partido', 'sigla_uf']].drop_duplicates(subset='id_deputado')

    # Step 1: Data Acquisition
    #data_acquisition()

    # Step 2: Data Processing
    df_filtered, num_propositions_before, df_orgao_deputado = data_processing()
    if df_filtered is None:
        print("Erro no processamento de dados. Encerrando o script.")
        return

    # Step 3: Optimize Polarization Interval and Perform Analysis
    final_summary_results, detailed_results = optimize_polarization_interval(df_filtered, df_deputados, fixed_random_state)

    #Save Final Results
    save_results(final_summary_results, detailed_results)

    # Step 4: Generate Plots
    detailed_results_path = 'data/detailed_results.csv'
    plots_output_dir = 'data/plots'

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
    #party_ranking = rank_parties_by_deputies(party_data_by_year)
    
    # Listar partidos que aparecem em todos os anos e no último ano
    #retained_parties, current_parties = get_parties_by_year(party_data_by_year)
    
    # Deputados por comunidade para os partidos que se mantiveram
    #retained_parties_data = get_deputados_for_retained_parties(party_data_by_year, retained_parties)
    
    # Deputados por comunidade para os partidos atuais
    #current_parties_data = get_deputados_for_current_parties(party_data_by_year, current_parties)
    
    # Rankear partidos baseados na diferença percentual de deputados entre comunidades
    #percentage_diff_ranking = rank_parties_by_percentage_difference(party_data_by_year, current_parties)
    
    # Verificar o top partido de cada comunidade no ano mais recente
    #top_parties_last_year = get_top_parties_per_community_last_year(party_data_by_year)
    
    # Plotar comparações dos partidos com os maiores partidos de cada comunidade (apenas top 7)
    #plot_party_comparison_consistent(party_data_by_year, top_parties_last_year, partido_1="PL", partido_0="PT", top_n=7)

    # Exportar a tabela com a quantidade de deputados por partido em cada comunidade ao longo dos anos
    export_party_community_table(party_data_by_year, output_file='data/party_community_table.csv')

    df = clean_dataframe(pd.read_csv('data/party_community_table.csv'))

    df_min = get_min_community_generalized(df)

    # Specify the reference year
    reference_year = get_last_year(df)

    # Adjust community labels
    adjusted_df = adjust_community_labels(df, reference_year)

    adjusted_df = merge_min_community_with_suffix_change(adjusted_df, df_min)

    # Sort columns from the earliest year to the latest year
    sorted_df = sort_columns(adjusted_df)

    export_dataframe_to_csv(sorted_df, 'data/party_community_table_adjusted.csv')

    #plot_community_graphs('data/party_community_table_adjusted.csv')

if __name__ == "__main__":
    main()