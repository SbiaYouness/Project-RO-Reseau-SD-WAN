"""
Streamlit Application for Shortest Path Visualization
Operations Research Project - Path Optimization with Dijkstra Algorithm
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from graph_algorithms import Graph

# Page configuration
st.set_page_config(
    page_title="Recherche de Chemin Optimal",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
        font-size: 1.4rem;
        font-weight: bold;
        color: #2e7d32;
        padding: 1.2rem;
        background-color: #e8f5e9;
        border-radius: 0.5rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize graph
@st.cache_resource
def load_graph():
    """Load and cache the graph object."""
    return Graph()

def get_fixed_positions():
    """
    Return fixed positions for nodes to avoid overlap.
    Casablanca (C) positioned far left as requested.
    """
    return {
        'C': (-4, 0),      # Casablanca - far left
        'R': (-2.5, 1),    # Rabat - upper left
        'M': (-2.5, -1),   # Marrakech - lower left
        'T': (-1, 2.5),    # Tanger - top
        'A': (-1, -2.5),   # Agadir - bottom
        'F': (1, 0),       # Fes - center
        'H': (3, 1.5),     # Hoceima - upper right
        'B': (2, -1.5),    # Benguerir - lower right
        'S': (0, -2.5),    # Safi - bottom center
        'O': (4.5, 0)      # Oujda - far right
    }

def create_network_graph(graph_obj, path=None):
    """
    Create a NetworkX graph visualization with fixed positions.
    
    Args:
        graph_obj: Graph object
        path: Optional path to highlight
    """
    G = nx.DiGraph()
    
    # Add edges with weights
    for source, dest, weight in graph_obj.get_edges():
        G.add_edge(source, dest, weight=weight)
    
    # Create figure with larger size
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Use fixed positions for better visualization
    pos = get_fixed_positions()
    
    # Draw nodes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if path and node in path:
            if node == path[0]:
                node_colors.append('#4CAF50')  # Green for start
                node_sizes.append(2500)
            elif node == path[-1]:
                node_colors.append('#F44336')  # Red for end
                node_sizes.append(2500)
            else:
                node_colors.append('#FFC107')  # Yellow for path
                node_sizes.append(2200)
        else:
            node_colors.append('#2196F3')  # Blue for others
            node_sizes.append(2000)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=node_sizes, alpha=0.95, ax=ax)
    
    # Draw edges with custom connection styles to avoid overlap
    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    else:
        path_edges = []
    
    # Define custom connection styles for specific edges to avoid overlap
    edge_styles = {
        ('A', 'M'): 'arc3,rad=0.25',
        ('A', 'S'): 'arc3,rad=-0.2',
        ('A', 'B'): 'arc3,rad=0.2',
        ('A', 'C'): 'arc3,rad=0.3',
        ('B', 'M'): 'arc3,rad=-0.25',
        ('B', 'S'): 'arc3,rad=0.15',
        ('B', 'F'): 'arc3,rad=-0.2',
        ('C', 'M'): 'arc3,rad=-0.35',
        ('C', 'R'): 'arc3,rad=0.15',
        ('C', 'T'): 'arc3,rad=0.25',
        ('R', 'M'): 'arc3,rad=0.3',
        ('R', 'F'): 'arc3,rad=0.15',
        ('T', 'F'): 'arc3,rad=-0.25',
        ('T', 'H'): 'arc3,rad=0.2',
        ('F', 'H'): 'arc3,rad=0.15',
        ('F', 'O'): 'arc3,rad=-0.2',
        ('H', 'O'): 'arc3,rad=0.15',
    }
    
    # Draw each edge individually with custom style
    for edge in G.edges():
        is_path = edge in path_edges
        color = '#4CAF50' if is_path else '#999999'
        width = 5 if is_path else 2
        alpha = 0.8 if is_path else 0.5
        
        connection_style = edge_styles.get(edge, 'arc3,rad=0.1')
        
        nx.draw_networkx_edges(G, pos, edgelist=[edge],
                              edge_color=color, 
                              width=width, alpha=alpha,
                              arrows=True, arrowsize=25, 
                              arrowstyle='->', ax=ax,
                              connectionstyle=connection_style)
    
    # Draw labels (city codes)
    nx.draw_networkx_labels(G, pos, font_size=16, 
                           font_weight='bold', font_color='white', ax=ax)
    
    # Draw edge labels (weights) with better positioning
    edge_labels = nx.get_edge_attributes(G, 'weight')
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, 
                                 font_size=11, font_color='#d32f2f',
                                 font_weight='bold', ax=ax,
                                 bbox=dict(boxstyle='round,pad=0.3', 
                                          facecolor='white', alpha=0.8))
    
    ax.set_title("Réseau des Villes Marocaines", fontsize=18, fontweight='bold', pad=20)
    ax.axis('off')
    ax.margins(0.15)
    plt.tight_layout()
    
    return fig

def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">🗺️ Recherche de Chemin Optimal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Trouver les routes optimales entre les villes marocaines avec l\'algorithme de Dijkstra</div>', 
                unsafe_allow_html=True)
    
    # Load graph
    graph = load_graph()
    nodes = graph.get_nodes()
    city_names = graph.get_city_names_dict()
    
    # Create two columns: sidebar (left) and main content (right)
    col_sidebar, col_main = st.columns([1, 3])
    
    with col_sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")
        
        # Source selection
        st.markdown("##### 📍 Sélection des Villes")
        
        # Create display options with full names
        display_options = [f"{city_names[code]} ({code})" for code in nodes]
        node_to_display = {code: f"{city_names[code]} ({code})" for code in nodes}
        display_to_node = {f"{city_names[code]} ({code})": code for code in nodes}
        
        source_display = st.selectbox(
            "Ville de Départ",
            options=display_options,
            index=display_options.index(node_to_display['C']),  # Default to Casablanca
            help="Choisissez le point de départ de votre itinéraire"
        )
        
        destination_display = st.selectbox(
            "Ville d'Arrivée",
            options=display_options,
            index=display_options.index(node_to_display['M']),  # Default to Marrakech
            help="Choisissez la destination de votre itinéraire"
        )
        
        # Convert back to node codes
        source = display_to_node[source_display]
        destination = display_to_node[destination_display]
        
        st.markdown("---")
        
        # Run button
        run_button = st.button("🚀 Trouver le Chemin Optimal", type="primary")
        
        st.markdown("---")
        
        # Legend
        st.markdown("##### 🎨 Légende")
        st.markdown("""
        - 🟢 **Vert**: Ville de départ
        - 🔴 **Rouge**: Ville d'arrivée
        - 🟡 **Jaune**: Villes intermédiaires
        - 🔵 **Bleu**: Autres villes
        """)
    
    with col_main:
        # Check if button is clicked or initialize
        if run_button:
            if source == destination:
                st.warning("⚠️ La ville de départ et d'arrivée sont identiques ! Veuillez sélectionner des villes différentes.")
            else:
                # Run Dijkstra
                distances, predecessors = graph.dijkstra(source)
                path = graph.reconstruct_path(predecessors, source, destination)
                
                if not path:
                    st.error(f"❌ Aucun chemin trouvé de {city_names[source]} à {city_names[destination]}")
                    # Show graph even when no path
                    st.markdown("### 🗺️ Carte du Réseau")
                    fig = create_network_graph(graph, None)
                    st.pyplot(fig)
                    plt.close()
                else:
                    # Create two columns: graph on left, results on right
                    graph_col, results_col = st.columns([2, 1])
                    
                    with graph_col:
                        st.markdown("### 🗺️ Carte du Réseau")
                        fig = create_network_graph(graph, path)
                        st.pyplot(fig)
                        plt.close()
                    
                    with results_col:
                        # Display results
                        st.success(f"✅ Chemin optimal trouvé !")
                        
                        # Metrics
                        st.metric("Latence Totale", f"{distances[destination]}", help="Latence totale du trajet")
                        st.metric("Nombre d'Étapes", len(path) - 1, help="Nombre de villes intermédiaires")
                        
                        # Path display with full names
                        path_full_names = [city_names[node] for node in path]
                        path_str = " → ".join(path_full_names)
                        st.markdown(f'<div class="path-display">{path_str}</div>', unsafe_allow_html=True)
                        
                        # Detailed route
                        with st.expander("📝 Itinéraire Détaillé", expanded=True):
                            path_details = graph.get_path_with_weights(path)
                            
                            for i, (from_node, to_node, weight) in enumerate(path_details, 1):
                                st.write(f"**Étape {i}:** {city_names[from_node]} → {city_names[to_node]} (latence: {weight})")
        
        else:
            # Default view - show instruction and full graph
            st.info("👈 Configurez votre itinéraire dans la barre latérale et cliquez sur 'Trouver le Chemin Optimal' pour commencer !")
            
            st.markdown("### 🗺️ Carte Complète du Réseau")
            fig = create_network_graph(graph)
            st.pyplot(fig)
            plt.close()
            
            # Show graph statistics
            st.markdown("---")
            st.markdown("### 📊 Statistiques du Réseau")
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            
            with stat_col1:
                st.metric("Nombre de Villes", len(graph.get_nodes()))
            
            with stat_col2:
                st.metric("Nombre de Connexions", len(graph.get_edges()))
            
            with stat_col3:
                edges = graph.get_edges()
                avg_weight = sum(w for _, _, w in edges) / len(edges) if edges else 0
                st.metric("Latence Moyenne", f"{avg_weight:.1f}")

if __name__ == "__main__":
    main()
