import pandas as pd
import os
from data_fetching import fetch_all_datasets
from data_processing import (
    rename_columns,
    filter_votacoes,
    calculate_yes_vote_percentage,
    filter_polarized_votacoes
)
from graph_generation import generate_graph, save_graph
from community_detection import (
    analyze_pruning,
    plot_results,
    prune_graph,
    detect_communities
)
from utils import determine_optimal_pruning
import networkx as nx

def main():
    # Step 1: Data Acquisition
    #fetch_all_datasets()

    # Step 2: Data Processing
    # Load datasets
    df_proposicao_microdados = pd.read_csv('data/csv/proposicao_microdados.csv')
    df_proposicao_tema = pd.read_csv('data/csv/proposicao_tema.csv')
    df_votacao_objeto = pd.read_csv('data/csv/votacao_objeto.csv')
    df_votacao = pd.read_csv('data/csv/votacao.csv')
    df_orgao_deputado = pd.read_csv('data/csv/orgao_deputado.csv')

    # Rename columns for consistency
    df_proposicao_microdados = rename_columns(df_proposicao_microdados, {'data': 'proposition_date', 'ano': 'proposition_year'})
    df_votacao_objeto = rename_columns(df_votacao_objeto, {'data': 'voting_date'})

    # Merge datasets step by step using appropriate keys
    # Merge proposicao_microdados and proposicao_tema on 'id_proposicao'
    df_proposicao = pd.merge(
        df_proposicao_microdados[['id_proposicao', 'proposition_year', 'proposition_date', 'sigla', 'tipo']],
        df_proposicao_tema[['id_proposicao', 'tema']],
        on='id_proposicao',
        how='left'
    )

    # Merge the result with votacao_objeto on 'id_proposicao'
    df_proposicao_votacao = pd.merge(
        df_proposicao,
        df_votacao_objeto[['id_proposicao', 'id_votacao', 'voting_date']],
        on='id_proposicao',
        how='left'
    )

    # Now merge with votacao on 'id_votacao'
    df_merged = pd.merge(
        df_proposicao_votacao,
        df_votacao[['id_votacao', 'sigla_orgao', 'aprovacao', 'voto_sim', 'voto_nao', 'voto_outro']],
        on='id_votacao',
        how='left'
    )

    # Filter out votacoes with null 'aprovacao'
    df_filtered = filter_votacoes(df_merged)

    # Calculate yes vote percentage
    df_filtered = calculate_yes_vote_percentage(df_filtered)

    # Number of propositions before the polarization filter
    num_propositions_before = df_filtered['id_proposicao'].nunique()

    # Filter polarized votacoes (40%-60% 'Sim' votes)
    df_polarized = filter_polarized_votacoes(df_filtered)

    # Number of propositions after the polarization filter
    num_propositions_after = df_polarized['id_proposicao'].nunique()

    print(f"Number of propositions before polarization filter: {num_propositions_before}")
    print(f"Number of propositions after polarization filter: {num_propositions_after}")

    # Step 3: Graph Generation
    df_votacao_parlamentar = pd.read_csv('data/csv/votacao_parlamentar.csv')

    # Convert 'data' column to datetime and extract 'ano_votacao'
    df_votacao_parlamentar['data'] = pd.to_datetime(df_votacao_parlamentar['data'])
    df_votacao_parlamentar['ano_votacao'] = df_votacao_parlamentar['data'].dt.year

    # Keep only votes from selected votacoes
    df_votes = df_votacao_parlamentar[df_votacao_parlamentar['id_votacao'].isin(df_polarized['id_votacao'])]

    # Prepare deputies information
    df_deputados = df_votacao_parlamentar[['id_deputado', 'nome', 'sigla_partido', 'sigla_uf']].drop_duplicates(subset='id_deputado')

    # Divide votes by year
    years = df_votes['ano_votacao'].unique()
    for year in years:
        print(f"\nProcessing year: {year}")
        G = generate_graph(df_votes, year)
        graph_path = f"data/graphs/graph_{year}.gpickle"
        os.makedirs(os.path.dirname(graph_path), exist_ok=True)
        save_graph(G, graph_path)

        # Step 4: Community Detection
        pruning_percentages = list(range(0, 101, 2))
        results = analyze_pruning(G, pruning_percentages)
        plot_results(results)

        # Automatically determine the optimal pruning percentage
        optimal_pruning_percentage = determine_optimal_pruning(results)

        if optimal_pruning_percentage is None:
            print(f"No optimal pruning percentage found for year {year}. Skipping community assignment.")
            continue  # Proceed to next year

        # Prune the graph at the optimal pruning percentage
        G_optimal = prune_graph(G.copy(), optimal_pruning_percentage)

        # Detect communities on the pruned graph
        communities, modularity = detect_communities(G_optimal)

        # Assign communities to nodes
        community_dict = {}
        for node in G_optimal.nodes():
            community_dict[node] = communities[node]

        nx.set_node_attributes(G_optimal, community_dict, 'community')

        # Assign additional node attributes
        party_orientation = {
            "PT": "esquerda",
            "PSOL": "esquerda",
            "PCdoB": "esquerda",
            "PL": "direita",
            "PP": "direita",
            "REPUBLICANOS": "centro-direita",
            "MDB": "centro",
            "PSB": "centro-esquerda",
            "PSD": "centro",
            "AGIR": "direita",
            "CIDADANIA": "centro-esquerda",
            "DC": "direita",
            "NOVO": "direita",
            "PCB": "esquerda",
            "PCO": "esquerda",
            "PDT": "centro-esquerda",
            "PMB": "direita",
            "PMN": "esquerda",
            "PODE": "centro-direita",
            "PRTB": "direita",
            "PSDB": "centro",
            "PV": "esquerda",
            "REDE": "esquerda",
            "SOLIDARIEDADE": "centro",
            "PSL": "centro-direita",
            "PR": "direita",
            "PTN": "direita",
            "AVANTE": "centro",
            "PMDB": "centro",
            "PRB": "direita",
            "PSC": "direita",
            "PTB": "direita",
            "PFL": "centro-direita",
            "DEM": "centro-direita",
            "UNIÃO": "centro-direita",
            "PPS": "esquerda",
            "PROS": "centro",
            "PATRIOTA": "direita"
        }

        for node in G_optimal.nodes():
            # Get deputy info
            deputado_info = df_deputados[df_deputados['id_deputado'] == node]
            if not deputado_info.empty:
                nome = deputado_info.iloc[0]['nome']
                sigla_partido = deputado_info.iloc[0]['sigla_partido']
                sigla_uf = deputado_info.iloc[0]['sigla_uf']
                orientation = party_orientation.get(sigla_partido, 'unknown')

                # Assign attributes
                G_optimal.nodes[node]['nome'] = nome
                G_optimal.nodes[node]['sigla_partido'] = sigla_partido
                G_optimal.nodes[node]['sigla_uf'] = sigla_uf
                G_optimal.nodes[node]['orientation'] = orientation
            else:
                print(f"Deputy info not found for id_deputado: {node}")
                G_optimal.nodes[node]['nome'] = 'Unknown'
                G_optimal.nodes[node]['sigla_partido'] = 'Unknown'
                G_optimal.nodes[node]['sigla_uf'] = 'Unknown'
                G_optimal.nodes[node]['orientation'] = 'unknown'

        # Step 5: Final Results
        # Save the graph with complete information
        graph_path_with_communities = f"data/graphs/graph_{year}_communities.gml"
        save_graph(G_optimal, graph_path_with_communities)
        print(f"Graph with communities saved to {graph_path_with_communities}")


    # Output the final information
    print("\n=== Final Results ===")
    print(f"Number of propositions before polarization filter: {num_propositions_before}")
    print(f"Number of propositions after polarization filter: {num_propositions_after}")
    print("Processing completed successfully.")

if __name__ == "__main__":
    main()
