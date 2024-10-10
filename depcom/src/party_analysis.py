import networkx as nx
import os
import pandas as pd
import matplotlib.pyplot as plt

def load_graphs(graphs_dir='data/graphs'):
    """
    Carrega os arquivos .gml dos grafos ao longo dos anos.
    """
    graphs = {}
    for file in os.listdir(graphs_dir):
        if file.endswith('.gml'):
            year = int(file.split('_')[1])
            G = nx.read_gml(os.path.join(graphs_dir, file))
            graphs[year] = G
    return graphs

def get_party_info_by_community(G):
    """
    Extrai a quantidade de deputados por partido em cada comunidade para um grafo G.
    """
    party_community_data = []
    for node, data in G.nodes(data=True):
        partido = data.get('sigla_partido', 'Unknown')
        comunidade = data.get('community', -1)
        party_community_data.append({'sigla_partido': partido, 'community': comunidade})
    
    df = pd.DataFrame(party_community_data)
    party_count_by_community = df.groupby(['sigla_partido', 'community']).size().reset_index(name='count')
    
    return party_count_by_community

def get_party_percentages_by_year(graphs):
    """
    Gera uma tabela com o número e % de deputados de cada partido em cada comunidade ao longo dos anos.
    """
    all_years_data = []
    
    for year, G in graphs.items():
        party_data = get_party_info_by_community(G)
        
        # Calcular o total de deputados por partido em cada ano
        total_deputados_by_party = party_data.groupby('sigla_partido')['count'].sum().reset_index(name='total')
        
        # Merge para calcular percentuais
        party_data = party_data.merge(total_deputados_by_party, on='sigla_partido')
        party_data['percentual'] = (party_data['count'] / party_data['total']) * 100
        party_data['year'] = year
        all_years_data.append(party_data)
    
    return pd.concat(all_years_data)

def rank_parties_by_deputies(party_data_by_year):
    """
    Rankear partidos com base no número de deputados em cada ano.
    """
    ranking = party_data_by_year.groupby(['year', 'sigla_partido'])['count'].sum().reset_index()
    ranking = ranking.sort_values(by=['year', 'count'], ascending=[True, False])
    
    return ranking

def get_parties_by_year(party_data_by_year):
    """
    Obtém a lista de partidos que aparecem em todos os anos e no último ano.
    """
    years = party_data_by_year['year'].unique()
    last_year = max(years)
    
    # Partidos que aparecem em todos os anos
    partidos_todos_os_anos = party_data_by_year.groupby('sigla_partido')['year'].nunique()
    partidos_todos_os_anos = partidos_todos_os_anos[partidos_todos_os_anos == len(years)].index.tolist()
    
    # Partidos que aparecem no último ano
    partidos_ultimo_ano = party_data_by_year[party_data_by_year['year'] == last_year]['sigla_partido'].unique().tolist()
    
    return partidos_todos_os_anos, partidos_ultimo_ano

def get_deputados_for_retained_parties(party_data_by_year, retained_parties):
    """
    Obtém o número de deputados nas comunidades ao longo dos anos para os partidos que se mantiveram.
    """
    return party_data_by_year[party_data_by_year['sigla_partido'].isin(retained_parties)]

def get_deputados_for_current_parties(party_data_by_year, current_parties):
    """
    Obtém o número de deputados nas comunidades ao longo dos anos para os partidos que existem no último ano.
    """
    return party_data_by_year[party_data_by_year['sigla_partido'].isin(current_parties)]

def rank_parties_by_percentage_difference(party_data_by_year, current_parties):
    """
    Rankear partidos com base na diferença percentual de deputados entre comunidades ao longo dos anos.
    """
    current_parties_data = party_data_by_year[party_data_by_year['sigla_partido'].isin(current_parties)]
    
    # Calcular a diferença percentual para cada partido em cada ano
    diff_df = current_parties_data.groupby(['year', 'sigla_partido']).agg({
        'percentual': lambda x: x.max() - x.min()
    }).reset_index()
    
    # Ordenar pelo maior valor de diferença
    diff_df = diff_df.sort_values(by=['year', 'percentual'], ascending=[True, False])
    
    return diff_df

def get_top_parties_per_community_last_year(party_data_by_year):
    """
    Verificar o partido com mais deputados em cada comunidade no ano mais recente.
    """
    last_year = party_data_by_year['year'].max()
    last_year_data = party_data_by_year[party_data_by_year['year'] == last_year]
    
    top_parties = last_year_data.groupby('community').apply(lambda x: x.nlargest(1, 'count')).reset_index(drop=True)
    
    return top_parties

def plot_party_comparison_consistent(party_data_by_year, top_parties, partido_1="PL", partido_0="PT", output_dir='data/plots_party_comparisons', top_n=7):
    """
    Gera gráficos comparando os partidos com os maiores partidos das comunidades no ano mais recente,
    assumindo que a comunidade a qual o 'partido_1' (ex: PL) pertence será considerada comunidade 1 e
    a comunidade a qual o 'partido_0' (ex: PT) pertence será considerada comunidade 0 ao longo dos anos.

    Args:
        party_data_by_year (pd.DataFrame): DataFrame com os dados dos partidos por ano.
        top_parties (pd.DataFrame): DataFrame com os partidos que são os maiores de cada comunidade.
        partido_1 (str): Partido a ser assumido como pertencente à Comunidade 1 (ex: PL).
        partido_0 (str): Partido a ser assumido como pertencente à Comunidade 0 (ex: PT).
        output_dir (str): Diretório onde os gráficos serão salvos.
        top_n (int): Número máximo de partidos a serem mostrados nos gráficos.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Manter a relação da comunidade a qual o partido_1 (ex: PL) e partido_0 (ex: PT) pertencem a cada ano
    community_map = {}

    for year in party_data_by_year['year'].unique():
        # Verificar em qual comunidade o partido_1 (ex: PL) está nesse ano
        partido_1_data = party_data_by_year[(party_data_by_year['year'] == year) & (party_data_by_year['sigla_partido'] == partido_1)]
        partido_0_data = party_data_by_year[(party_data_by_year['year'] == year) & (party_data_by_year['sigla_partido'] == partido_0)]

        if not partido_1_data.empty:
            comunidade_1 = partido_1_data['community'].mode()[0]  # Comunidade do partido_1 (ex: PL)
        else:
            comunidade_1 = None  # Caso não haja dados do partido naquele ano

        if not partido_0_data.empty:
            comunidade_0 = partido_0_data['community'].mode()[0]  # Comunidade do partido_0 (ex: PT)
        else:
            comunidade_0 = None

        community_map[year] = {'comunidade_1': comunidade_1, 'comunidade_0': comunidade_0}

    # Agora, reclassificar as comunidades de acordo com os partidos dominantes
    party_data_by_year['community_reclass'] = party_data_by_year.apply(
        lambda row: 1 if row['community'] == community_map[row['year']]['comunidade_1'] else
                    (0 if row['community'] == community_map[row['year']]['comunidade_0'] else row['community']),
        axis=1
    )

    # Continuar o processo de plotagem considerando as comunidades reclassificadas
    for _, top_party in top_parties.iterrows():
        top_party_name = top_party['sigla_partido']
        community = top_party['community']

        # Comparar os demais partidos com o top partido
        comparison_df = party_data_by_year[(party_data_by_year['community_reclass'] == community) & 
                                           (party_data_by_year['sigla_partido'] != top_party_name)]

        # Somar o número total de deputados para cada partido ao longo dos anos
        total_deputados_by_party = comparison_df.groupby('sigla_partido')['count'].sum().reset_index()

        # Selecionar os top_n partidos com o maior número de deputados
        top_parties_to_plot = total_deputados_by_party.nlargest(top_n, 'count')['sigla_partido'].tolist()

        # Filtrar apenas os top_n partidos no DataFrame de comparação
        comparison_df = comparison_df[comparison_df['sigla_partido'].isin(top_parties_to_plot)]

        plt.figure(figsize=(10, 6))
        for partido in comparison_df['sigla_partido'].unique():
            party_data = comparison_df[comparison_df['sigla_partido'] == partido]
            plt.plot(party_data['year'], party_data['percentual'], label=partido)

        plt.title(f'Comparison with Top Party: {top_party_name} (Reclassified Community)')
        plt.xlabel('Year')
        plt.ylabel('Percentage of Deputies')
        plt.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'comparison_with_{top_party_name}_reclassified_community.png'))
        plt.close()

    print(f"Plots saved to {output_dir}")
