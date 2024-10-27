import pandas as pd
import networkx as nx
from C_optimize_polarization import disparity_filter  # Assumindo que há um módulo que implementa o filtro de disparidade

def data_processing():
    """
    Carrega e processa os datasets necessários.
    
    Retorna:
        pd.DataFrame: DataFrame processado.
    """
    df_proposicao_microdados = pd.read_csv('data/csv/proposicao_microdados.csv')
    df_proposicao_tema = pd.read_csv('data/csv/proposicao_tema.csv')
    df_votacao_objeto = pd.read_csv('data/csv/votacao_objeto.csv')
    df_votacao = pd.read_csv('data/csv/votacao.csv')
    df_orgao_deputado = pd.read_csv('data/csv/orgao_deputado.csv')

    # Renomear e mesclar os datasets
    df_proposicao_microdados.rename(columns={'data': 'proposition_date', 'ano': 'proposition_year'}, inplace=True)
    df_votacao_objeto.rename(columns={'data': 'voting_date'}, inplace=True)
    df_votacao_objeto['voting_date'] = pd.to_datetime(df_votacao_objeto['voting_date'])
    df_votacao_objeto['voting_year'] = df_votacao_objeto['voting_date'].dt.year

    df_proposicao = pd.merge(
        df_proposicao_microdados[['id_proposicao', 'proposition_year', 'proposition_date', 'sigla', 'tipo']],
        df_proposicao_tema[['id_proposicao', 'tema']],
        on='id_proposicao',
        how='left'
    )

    df_proposicao_votacao = pd.merge(
        df_proposicao,
        df_votacao_objeto[['id_proposicao', 'id_votacao', 'voting_date', 'voting_year']],
        on='id_proposicao',
        how='left'
    )

    df_merged = pd.merge(
        df_proposicao_votacao,
        df_votacao[['id_votacao', 'sigla_orgao', 'aprovacao', 'voto_sim', 'voto_nao', 'voto_outro']],
        on='id_votacao',
        how='left'
    )

    return df_merged, df_orgao_deputado

def analyze_voting_network(df_votes, year):
    """
    Gera e analisa o grafo de votação para um ano específico.

    Args:
        df_votes (pd.DataFrame): DataFrame com as votações do ano.
        year (int): Ano sendo analisado.

    Retorna:
        dict: Resultados de modularidade e comunidades.
    """
    # Criar o grafo
    G = nx.Graph()
    for _, row in df_votes.iterrows():
        G.add_edge(row['id_deputado_1'], row['id_deputado_2'], weight=row['peso_votacao'])

    # Aplicar o "backbone extraction"
    G_backbone = disparity_filter(G)

    # Detectar comunidades usando o método Leiden
    communities = nx.community.leiden_communities(G_backbone)
    modularity = nx.algorithms.community.quality.modularity(G_backbone, communities)

    # Contar deputados por partido em cada comunidade
    community_party_count = {}
    for i, community in enumerate(communities):
        party_count = {}
        for node in community:
            party = G.nodes[node].get('sigla_partido', 'Unknown')
            party_count[party] = party_count.get(party, 0) + 1
        community_party_count[f'Community_{i+1}'] = party_count

    return {
        'Year': year,
        'Modularity': modularity,
        'Num_Communities': len(communities),
        'Community_Party_Count': community_party_count
    }
