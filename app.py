"""
Streamlit Application - Plus Court Chemin avec Simulation de Pannes
Projet Recherche Opérationnelle
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from graph_algorithms import Graph

# Page configuration
st.set_page_config(
    page_title="Plus Court Chemin - RO",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .path-display {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2e7d32;
        padding: 1rem;
        background-color: #e8f5e9;
        border-radius: 0.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_graph():
    return Graph()

def get_fixed_positions():
    """Positions optimisées des villes"""
    return {
        'C': (-5, 0), 'R': (-3, 2.5), 'M': (-3, -5), 'T': (-4, 4.5),
        'A': (1, -5), 'F': (2, 0), 'H': (3, 2.5), 'B': (3.5, -5.5),
        'S': (2, -3.5), 'O': (5, 0)
    }

def get_edge_styles():
    """Styles optimisés pour les liens"""
    return {
        ('A', 'M'): 'arc3,rad=0.1',
        ('A', 'S'): 'arc3,rad=-0.15',
        ('B', 'A'): 'arc3,rad=0',
        ('A', 'C'): 'arc3,rad=0.12',
        ('B', 'M'): 'arc3,rad=-0.12',
        ('B', 'S'): 'arc3,rad=0.12',
        ('B', 'F'): 'arc3,rad=-0.05',
        ('C', 'M'): 'arc3,rad=-0.1',
        ('C', 'R'): 'arc3,rad=0.05',
        ('C', 'T'): 'arc3,rad=0.08',
        ('R', 'M'): 'arc3,rad=0.08',
        ('R', 'F'): 'arc3,rad=0.05',
        ('T', 'F'): 'arc3,rad=-0.05',
        ('T', 'H'): 'arc3,rad=0.05',
        ('F', 'H'): 'arc3,rad=0.05',
        ('F', 'O'): 'arc3,rad=-0.05',
        ('H', 'O'): 'arc3,rad=0.05',
    }

def create_network_graph(graph_obj, path, disabled_links, disabled_cities):
    """Create graph with failures simulation."""
    G = nx.DiGraph()
    for source, dest, weight in graph_obj.get_edges():
        # Skip disabled links and cities
        if (source, dest) in disabled_links or source in disabled_cities or dest in disabled_cities:
            continue
        G.add_edge(source, dest, weight=weight)
    
    fig, ax = plt.subplots(figsize=(18, 10))
    pos = get_fixed_positions()
    edge_styles = get_edge_styles()
    
    # Include all nodes even if not in current graph
    all_nodes = list(pos.keys())
    
    # Node colors
    node_colors = []
    node_sizes = []
    for node in all_nodes:
        if node in disabled_cities:
            node_colors.append('#CCCCCC')
            node_sizes.append(2200)
        elif path and node in path:
            if node == path[0]:
                node_colors.append('#4CAF50')
                node_sizes.append(2800)
            elif node == path[-1]:
                node_colors.append('#F44336')
                node_sizes.append(2800)
            else:
                node_colors.append('#FFC107')
                node_sizes.append(2400)
        else:
            node_colors.append('#2196F3')
            node_sizes.append(2200)
    
    # Draw all nodes
    nx.draw_networkx_nodes(all_nodes, pos, node_color=node_colors, node_size=node_sizes, alpha=0.95, ax=ax)
    
    # Path edges
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)] if path else []
    
    # Draw edges
    for edge in G.edges():
        is_path = edge in path_edges
        color = '#4CAF50' if is_path else '#999999'
        width = 6 if is_path else 2.5
        alpha = 0.85 if is_path else 0.55
        
        connection_style = edge_styles.get(edge, 'arc3,rad=0.1')
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=color, 
                              width=width, alpha=alpha, arrows=True, arrowsize=28, 
                              arrowstyle='->', ax=ax, connectionstyle=connection_style)
    
    # Labels for all nodes
    nx.draw_networkx_labels(G, pos, font_size=17, font_weight='bold', font_color='white', ax=ax)
    
    # Edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12, font_color='#d32f2f',
                                 font_weight='bold', ax=ax,
                                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85))
    
    ax.set_title("Réseau de Villes - Plus Court Chemin", fontsize=20, fontweight='bold', pad=25, color='#1f77b4')
    ax.axis('off')
    ax.margins(0.18)
    plt.tight_layout()
    return fig

def main():
    st.markdown('<div class="main-header">🗺️ Plus Court Chemin</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Recherche Opérationnelle - Simulation de Pannes</div>', 
                unsafe_allow_html=True)
    
    graph = load_graph()
    nodes = graph.get_nodes()
    city_names = graph.get_city_names_dict()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        display_options = [f"{city_names[code]} ({code})" for code in nodes]
        node_to_display = {code: f"{city_names[code]} ({code})" for code in nodes}
        display_to_node = {f"{city_names[code]} ({code})": code for code in nodes}
        
        source_display = st.selectbox("🟢 Départ", options=display_options,
                                     index=display_options.index(node_to_display['C']))
        destination_display = st.selectbox("🔴 Arrivée", options=display_options,
                                          index=display_options.index(node_to_display['M']))
        
        source = display_to_node[source_display]
        destination = display_to_node[destination_display]
        
        with st.expander("⚠️ Simulation de Pannes", expanded=False):
            disabled_cities = st.multiselect(
                "Villes Hors Service",
                options=[code for code in nodes if code not in [source, destination]],
                format_func=lambda x: f"{city_names[x]} ({x})",
                key="disabled_cities"
            )
            
            all_links = []
            for src, dest, weight in graph.get_edges():
                if src not in disabled_cities and dest not in disabled_cities:
                    all_links.append((src, dest, weight))
            
            disabled_links_display = st.multiselect(
                "Liaisons en Panne",
                options=all_links,
                format_func=lambda x: f"{city_names[x[0]]}-{city_names[x[1]]} ({x[2]})",
                key="disabled_links"
            )
            disabled_links = [(src, dest) for src, dest, _ in disabled_links_display]
        
        run_button = st.button("🚀 Calculer", type="primary", use_container_width=True)
        
        with st.expander("🎨 Légende"):
            st.markdown("🟢 Départ | 🔴 Arrivée\n🟡 Intermédiaires | 🔵 Autres\n⚪ Hors service")
    
    # Main content - Always show graph
    if run_button:
        if source == destination:
            st.warning("⚠️ La ville de départ et d'arrivée sont identiques !")
            graph_col = st.container()
        else:
            # Create modified graph excluding failures
            modified_graph = Graph()
            modified_graph.graph = {node: [] for node in nodes}
            
            for src, dest, weight in graph.get_edges():
                if src not in disabled_cities and dest not in disabled_cities and (src, dest) not in disabled_links:
                    modified_graph.graph[src].append((dest, weight))
            
            distances, predecessors = modified_graph.dijkstra(source)
            path = modified_graph.reconstruct_path(predecessors, source, destination)
            
            if not path:
                col1, col2 = st.columns([3, 1])
                with col2:
                    st.error(f"❌ Aucun chemin trouvé")
                    if disabled_cities or disabled_links:
                        st.warning("⚠️ Pannes bloquent les chemins")
                graph_col = col1
            else:
                col1, col2 = st.columns([3, 1])
                with col2:
                    st.success(f"✅ Chemin optimal")
                    st.metric("Latence", f"{distances[destination]}")
                    st.metric("Étapes", len(path) - 1)
                    
                    path_full_names = [city_names[node] for node in path]
                    path_str = " → ".join(path_full_names)
                    st.markdown(f"**Trajet:**")
                    st.info(path_str)
                    
                    if disabled_cities or disabled_links:
                        st.caption(f"🔧 {len(disabled_cities)} ville(s), {len(disabled_links)} liaison(s) désactivée(s)")
                graph_col = col1
            
            # Show graph in left column
            with graph_col:
                fig = create_network_graph(graph, path, disabled_links, disabled_cities)
                st.pyplot(fig)
                plt.close()
    
    else:
        col1, col2 = st.columns([3, 1])
        with col2:
            st.info("👈 Configurez et cliquez sur **Calculer**")
        with col1:
            fig = create_network_graph(graph, None, set(), set())
            st.pyplot(fig)
            plt.close()

if __name__ == "__main__":
    main()
