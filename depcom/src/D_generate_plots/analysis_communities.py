import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ternary  # Biblioteca para gráficos ternários
from collections import defaultdict

# Definir um mapeamento fixo de cores para partidos
PARTY_COLORS = {
    "PT": "red",
    "PSDB": "blue",
    "MDB": "green",
    "PSOL": "purple",
    "PL": "orange",
    "DEM": "cyan",
    "PP": "brown",
    "PSB": "pink",
    "PDT": "yellow",
    "NOVO": "gray",
    # Adicione mais partidos conforme necessário
}

def load_graph(year, graphs_dir='data/graphs'):
    """
    Carrega o grafo para um determinado ano a partir do arquivo .gml.
    """
    filename = f"graph_{year}_communities.gml"
    filepath = os.path.join(graphs_dir, filename)
    if not os.path.exists(filepath):
        print(f"Graph file {filepath} not found.")
        return None
    try:
        G = nx.read_gml(filepath)
        print(f"Graph for year {year} loaded successfully.")
        return G
    except Exception as e:
        print(f"Error loading graph for year {year}: {e}")
        return None

def compute_party_inclination(G):
    """
    Computa a inclinação de cada partido em relação às comunidades no grafo.

    Args:
        G (nx.Graph): Grafo com atributos 'sigla_partido' e 'community'.

    Returns:
        pd.DataFrame: DataFrame com 'sigla_partido', percentual de deputados em cada comunidade e total de deputados por partido.
    """
    if G is None:
        return None

    # Extrair dados dos nós
    data = []
    for node, attrs in G.nodes(data=True):
        partido = attrs.get('sigla_partido', 'Unknown')
        comunidade = attrs.get('community', -1)
        data.append({'sigla_partido': partido, 'community': comunidade})

    df = pd.DataFrame(data)

    # Contar deputados por partido
    total_deputados = df.groupby('sigla_partido').size().reset_index(name='total_deputados')

    # Contar deputados por partido e comunidade
    count = df.groupby(['sigla_partido', 'community']).size().reset_index(name='count')

    # Merge com total_deputados
    count = count.merge(total_deputados, on='sigla_partido')

    # Calcular percentual de deputados em cada comunidade
    count['percentual'] = (count['count'] / count['total_deputados']) * 100

    # Pivotar os dados para ter colunas de comunidades
    df_pivot = count.pivot(index='sigla_partido', columns='community', values='percentual').fillna(0)

    # Resetar o index para trazer 'sigla_partido' de volta como coluna
    df_pivot = df_pivot.reset_index()

    # Adicionar a coluna 'total_deputados'
    df_pivot = df_pivot.merge(total_deputados, on='sigla_partido')

    # Renomear as colunas das comunidades para 'Community X (%)'
    df_pivot.columns = ['sigla_partido'] + [f'Community {int(col)} (%)' for col in df_pivot.columns[1:-1]] + ['total_deputados']

    # Debug: Verifique se a coluna total_deputados foi criada corretamente
    print(df_pivot.head())  # Verifique a saída para confirmar a existência da coluna

    return df_pivot


def analyze_community_groups(df_party_inclination):
    """
    Analisa os partidos predominantes em cada comunidade e renomeia as comunidades para serem consistentes ao longo dos anos.
    
    Args:
        df_party_inclination (pd.DataFrame): DataFrame com os percentuais dos partidos em cada comunidade.
    
    Returns:
        df_renamed (pd.DataFrame): DataFrame com as comunidades renomeadas como 'Community A', 'Community B', e 'Community C'.
    """
    # Encontrar a comunidade onde cada partido tem maior representação
    community_max = df_party_inclination.set_index('sigla_partido').idxmax(axis=1)

    # Contar quantos partidos têm a maioria em cada comunidade
    community_counts = community_max.value_counts()

    # Mapear as comunidades para Community A, B e C de acordo com o tamanho
    communities_order = {}
    
    try:
        # A maior comunidade será Community A
        communities_order[community_counts.index[0]] = 'Community A (%)'

        # A segunda maior será Community B
        communities_order[community_counts.index[1]] = 'Community B (%)'

        # Se houver uma terceira comunidade, será Community C
        if len(community_counts) > 2:
            communities_order[community_counts.index[2]] = 'Community C (%)'
    except IndexError:
        print("Error analyzing community groups: not enough communities detected.")

    # Renomear as colunas do DataFrame para corresponder à análise
    df_renamed = df_party_inclination.rename(columns=communities_order)

    return df_renamed

def plot_party_inclination(year, df_party_inclination, output_dir='data/plots_communities'):
    """
    Plota a inclinação dos partidos em relação às comunidades para um determinado ano, com consistência nas cores e grupos.
    
    Args:
        year (int): Ano do gráfico.
        df_party_inclination (pd.DataFrame): DataFrame com as inclinações dos partidos e as comunidades renomeadas.
        output_dir (str): Diretório onde o gráfico será salvo.
    """
    if df_party_inclination.empty:
        print(f"No data to plot for year {year}.")
        return

    # Verificar se as colunas 'Community A (%)' e 'Community B (%)' existem
    if 'Community A (%)' in df_party_inclination.columns and 'Community B (%)' in df_party_inclination.columns:
        # Gráfico Unidimensional com as barras
        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        # Adicionar a linha pontilhada no 50% para indicar o meio
        ax.axvline(x=50, color='gray', linestyle='--', lw=2)

        # Ordenar partidos pela porcentagem na Community A
        df_party_inclination = df_party_inclination.sort_values('Community A (%)')

        partidos = df_party_inclination['sigla_partido']
        percentual_comunidade_a = df_party_inclination['Community A (%)']
        percentual_comunidade_b = df_party_inclination['Community B (%)']
        total_deputados = df_party_inclination['total_deputados']  # Usaremos a coluna total de deputados para a altura da barra

        # Adicionar as barras de cada partido
        bar_width = 0.4
        for i, partido in enumerate(partidos):
            # Altura da barra será proporcional ao total de deputados
            altura = total_deputados.iloc[i]
            color = PARTY_COLORS.get(partido, 'black')  # Cor consistente do partido
            
            # Plotar barras para Comunidade A e B lado a lado
            ax.barh(i - bar_width / 2, percentual_comunidade_a.iloc[i], height=bar_width, color=color, label=partido)
            ax.barh(i + bar_width / 2, percentual_comunidade_b.iloc[i], height=bar_width, color=color, alpha=0.6)

            # Adicionar o nome do partido no gráfico
            ax.text(percentual_comunidade_a.iloc[i] + 1, i - bar_width / 2, partido, va='center', ha='left', fontsize=9)
            ax.text(percentual_comunidade_b.iloc[i] + 1, i + bar_width / 2, partido, va='center', ha='left', fontsize=9)

        # Limitar a posição X para 0 a 100%
        ax.set_xlim(0, 100)
        ax.set_xlabel('Percentage in Community (%)')
        ax.set_title(f'Party Inclination in Communities - {year}', fontsize=16)

        # Legenda para os partidos
        plt.tight_layout()
        # Salvar o gráfico
        plt.savefig(os.path.join(output_dir, f"party_inclination_{year}.png"), dpi=300)
        plt.close()
        print(f"Graph for year {year} saved in {output_dir}.")
    else:
        print(f"Required community columns not found in year {year}. Skipping plot.")


def generate_all_party_inclination_plots(graphs_dir='data/graphs', plots_output_dir='data/plots_communities'):
    """
    Gera gráficos de inclinação dos partidos para todos os anos disponíveis, garantindo a consistência
    nas cores dos partidos e a renomeação correta das comunidades para cada ano.
    
    Args:
        graphs_dir (str, optional): Diretório onde os arquivos de grafo estão armazenados.
        plots_output_dir (str, optional): Diretório onde os gráficos serão salvos.
    """
    # Listar todos os arquivos .gml na pasta
    graph_files = [f for f in os.listdir(graphs_dir) if f.endswith('.gml')]

    # Extrair anos a partir dos nomes dos arquivos
    anos = []
    for f in graph_files:
        try:
            year_part = f.split('_')[1]  # Extrair o ano a partir do nome do arquivo
            year = int(year_part)
            anos.append(year)
        except (IndexError, ValueError):
            print(f"Filename {f} does not follow the pattern 'graph_<year>_communities.gml'. Skipping.")
            continue

    # Remover anos duplicados e ordenar
    anos = sorted(list(set(anos)))

    # Processar cada ano
    for ano in anos:
        print(f"\nProcessing year: {ano}")
        
        # Carregar o grafo
        G = load_graph(ano, graphs_dir)
        if G is None:
            continue
        
        # Computar a inclinação dos partidos para este ano
        df_party_inclination = compute_party_inclination(G)
        if df_party_inclination is None or df_party_inclination.empty:
            print(f"No inclination data for year {ano}. Skipping.")
            continue

        # Analisar os partidos predominantes e renomear comunidades para manter a consistência
        df_party_inclination_renamed = analyze_community_groups(df_party_inclination)

        # Garantir que o diretório de saída para os gráficos exista
        os.makedirs(plots_output_dir, exist_ok=True)

        # Plotar a inclinação dos partidos com as comunidades renomeadas
        plot_party_inclination(ano, df_party_inclination_renamed, output_dir=plots_output_dir)

    print("All party inclination plots have been generated.")