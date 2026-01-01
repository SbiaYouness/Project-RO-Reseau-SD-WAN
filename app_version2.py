"""
VERSION 2: Selective High Curves - Focus on problematic left side only
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from graph_algorithms import Graph

st.set_page_config(page_title="Version 2 - Selective Curves", page_icon="🗺️", layout="wide")

st.markdown("""<style>
.main-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center; margin-bottom: 0.5rem; }
.sub-header { font-size: 1.05rem; color: #666; text-align: center; margin-bottom: 2rem; }
.path-display { font-size: 1.4rem; font-weight: bold; color: #2e7d32; padding: 1.2rem; background-color: #e8f5e9; border-radius: 0.5rem; text-align: center; margin: 1.5rem 0; }
.stButton>button { width: 100%; background-color: #1f77b4; color: white; font-weight: bold; padding: 0.75rem; border-radius: 0.5rem; font-size: 1.1rem; }
</style>""", unsafe_allow_html=True)

@st.cache_resource
def load_graph():
    return Graph()

def get_fixed_positions():
    return {
        'C': (-4, 0), 'R': (-2.5, 1), 'M': (-2.5, -1), 'T': (-1, 2.5),
        'A': (-1, -2.5), 'F': (1, 0), 'H': (3, 1.5), 'B': (2, -1.5),
        'S': (0, -2.5), 'O': (4.5, 0)
    }

def create_network_graph(graph_obj, path=None):
    G = nx.DiGraph()
    for source, dest, weight in graph_obj.get_edges():
        G.add_edge(source, dest, weight=weight)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    pos = get_fixed_positions()
    
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if path and node in path:
            if node == path[0]:
                node_colors.append('#4CAF50')
                node_sizes.append(2500)
            elif node == path[-1]:
                node_colors.append('#F44336')
                node_sizes.append(2500)
            else:
                node_colors.append('#FFC107')
                node_sizes.append(2200)
        else:
            node_colors.append('#2196F3')
            node_sizes.append(2000)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.95, ax=ax)
    
    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    else:
        path_edges = []
    
    # VERSION 2: FOCUS ON LEFT SIDE (C, R, M, A, S, B connections)
    edge_styles = {
        # Left side problem area - high curves
        ('A', 'M'): 'arc3,rad=0.5',      # Extra curve
        ('A', 'S'): 'arc3,rad=-0.4',     # Strong opposite curve
        ('A', 'B'): 'arc3,rad=0.35',
        ('A', 'C'): 'arc3,rad=0.6',      # Maximum
        ('B', 'M'): 'arc3,rad=-0.5',     # Extra curve opposite
        ('B', 'S'): 'arc3,rad=0.3',
        ('B', 'F'): 'arc3,rad=-0.25',    # Moderate
        ('C', 'M'): 'arc3,rad=-0.55',    # Extra strong
        ('C', 'R'): 'arc3,rad=0.3',
        ('C', 'T'): 'arc3,rad=0.4',
        ('R', 'M'): 'arc3,rad=0.5',      # Extra curve
        ('R', 'F'): 'arc3,rad=0.15',     # Gentle on right side
        # Right side - keep moderate
        ('T', 'F'): 'arc3,rad=-0.2',
        ('T', 'H'): 'arc3,rad=0.15',
        ('F', 'H'): 'arc3,rad=0.15',
        ('F', 'O'): 'arc3,rad=-0.15',
        ('H', 'O'): 'arc3,rad=0.15',
    }
    
    for edge in G.edges():
        is_path = edge in path_edges
        color = '#4CAF50' if is_path else '#999999'
        width = 5 if is_path else 2
        alpha = 0.8 if is_path else 0.5
        
        connection_style = edge_styles.get(edge, 'arc3,rad=0.1')
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=color, 
                              width=width, alpha=alpha, arrows=True, arrowsize=25, 
                              arrowstyle='->', ax=ax, connectionstyle=connection_style)
    
    nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold', font_color='white', ax=ax)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=11, font_color='#d32f2f',
                                 font_weight='bold', ax=ax,
                                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax.set_title("VERSION 2: Courbures Sélectives (Focus Gauche)", fontsize=18, fontweight='bold', pad=20)
    ax.axis('off')
    ax.margins(0.15)
    plt.tight_layout()
    return fig

def main():
    st.markdown('<div class="main-header">🗺️ Version 2: Courbures Sélectives</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Focus sur le côté gauche problématique</div>', unsafe_allow_html=True)
    
    graph = load_graph()
    nodes = graph.get_nodes()
    city_names = graph.get_city_names_dict()
    
    col_sidebar, col_main = st.columns([1, 3])
    
    with col_sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")
        st.markdown("##### 📍 Sélection des Villes")
        
        display_options = [f"{city_names[code]} ({code})" for code in nodes]
        node_to_display = {code: f"{city_names[code]} ({code})" for code in nodes}
        display_to_node = {f"{city_names[code]} ({code})": code for code in nodes}
        
        source_display = st.selectbox("Ville de Départ", options=display_options,
                                     index=display_options.index(node_to_display['C']))
        destination_display = st.selectbox("Ville d'Arrivée", options=display_options,
                                          index=display_options.index(node_to_display['M']))
        
        source = display_to_node[source_display]
        destination = display_to_node[destination_display]
        
        st.markdown("---")
        run_button = st.button("🚀 Trouver le Chemin Optimal", type="primary")
        st.markdown("---")
        st.markdown("##### 🎨 Légende")
        st.markdown("- 🟢 **Vert**: Ville de départ\n- 🔴 **Rouge**: Ville d'arrivée\n- 🟡 **Jaune**: Villes intermédiaires\n- 🔵 **Bleu**: Autres villes")
    
    with col_main:
        if run_button:
            if source == destination:
                st.warning("⚠️ La ville de départ et d'arrivée sont identiques !")
            else:
                distances, predecessors = graph.dijkstra(source)
                path = graph.reconstruct_path(predecessors, source, destination)
                
                if not path:
                    st.error(f"❌ Aucun chemin trouvé")
                    st.markdown("### 🗺️ Carte du Réseau")
                    fig = create_network_graph(graph, None)
                    st.pyplot(fig)
                    plt.close()
                else:
                    graph_col, results_col = st.columns([2, 1])
                    
                    with graph_col:
                        st.markdown("### 🗺️ Carte du Réseau")
                        fig = create_network_graph(graph, path)
                        st.pyplot(fig)
                        plt.close()
                    
                    with results_col:
                        st.success(f"✅ Chemin optimal trouvé !")
                        st.metric("Latence Totale", f"{distances[destination]}")
                        st.metric("Nombre d'Étapes", len(path) - 1)
                        path_full_names = [city_names[node] for node in path]
                        path_str = " → ".join(path_full_names)
                        st.markdown(f'<div class="path-display">{path_str}</div>', unsafe_allow_html=True)
                        
                        with st.expander("📝 Itinéraire Détaillé", expanded=True):
                            path_details = graph.get_path_with_weights(path)
                            for i, (from_node, to_node, weight) in enumerate(path_details, 1):
                                st.write(f"**Étape {i}:** {city_names[from_node]} → {city_names[to_node]} (latence: {weight})")
        else:
            st.info("👈 Configurez votre itinéraire et testez cette version !")
            st.markdown("### 🗺️ Carte Complète du Réseau")
            fig = create_network_graph(graph)
            st.pyplot(fig)
            plt.close()

if __name__ == "__main__":
    main()
