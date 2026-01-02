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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with mobile support
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, minimum-scale=1.0, user-scalable=yes">
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
    .legend-box {
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 10px 12px;
        margin-top: 12px;
    }
    .legend-item {
        font-size: 0.875rem;
        line-height: 1.8;
        color: #333333;
        display: block;
        margin: 2px 0;
        padding: 0;
    }
    div.stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #1565c0;
        border: none;
    }
    .red-x {
        color: #dc3545;
        font-weight: bold;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def load_graph():
    """Load the graph (cache removed to ensure latest version is used)"""
    return Graph()

def get_fixed_positions():
    """Positions optimisées des villes"""
    return {
        'C': (-5, 0), 'R': (-3, 2.5), 'M': (-3, -5.5), 'T': (-4, 4.5),
        'A': (1, -5), 'F': (2, 0), 'H': (3, 2.5), 'B': (3.5, -6.2),
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
    """Create graph with failures simulation - keeping disabled elements visible but grayed out."""
    G = nx.Graph()
    seen_edges = set()
    
    # Add ALL edges (including disabled ones)
    for source, dest, weight in graph_obj.get_edges():
        edge_pair = tuple(sorted([source, dest]))
        if edge_pair not in seen_edges:
            seen_edges.add(edge_pair)
            # Mark if edge is disabled
            is_disabled = (source, dest) in disabled_links or (dest, source) in disabled_links or source in disabled_cities or dest in disabled_cities
            G.add_edge(source, dest, weight=weight, disabled=is_disabled)
    
    fig, ax = plt.subplots(figsize=(18, 10))
    pos = get_fixed_positions()
    edge_styles = get_edge_styles()
    
    # All nodes
    all_nodes = list(pos.keys())
    
    # Node colors
    node_colors = []
    node_sizes = []
    for node in all_nodes:
        if node in disabled_cities:
            node_colors.append('#CCCCCC')  # Gray for disabled
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
    
    # Draw edges - separate active and disabled
    active_edges = []
    disabled_edges = []
    
    for edge in G.edges(data=True):
        if edge[2].get('disabled', False):
            disabled_edges.append((edge[0], edge[1]))
        else:
            active_edges.append((edge[0], edge[1]))
    
    # Draw disabled edges first (grayed out with dashed lines)
    for edge in disabled_edges:
        connection_style = edge_styles.get(edge, edge_styles.get((edge[1], edge[0]), 'arc3,rad=0.1'))
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='#D3D3D3', 
                              width=2, alpha=0.4, ax=ax, connectionstyle=connection_style,
                              style='dashed')
    
    # Draw active edges
    for edge in active_edges:
        is_path = edge in path_edges or (edge[1], edge[0]) in path_edges
        color = '#4CAF50' if is_path else '#999999'
        width = 6 if is_path else 2.5
        alpha = 0.85 if is_path else 0.55
        
        connection_style = edge_styles.get(edge, edge_styles.get((edge[1], edge[0]), 'arc3,rad=0.1'))
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=color, 
                              width=width, alpha=alpha, ax=ax, connectionstyle=connection_style)
    
    # Labels for all nodes
    nx.draw_networkx_labels(G, pos, font_size=17, font_weight='bold', font_color='white', ax=ax)
    
    # Edge labels - show red X for disabled, weight for active
    edge_labels = {}
    for edge in G.edges(data=True):
        edge_key = (edge[0], edge[1])
        if edge[2].get('disabled', False):
            edge_labels[edge_key] = 'X'  # X for disabled links
        else:
            edge_labels[edge_key] = edge[2]['weight']
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=14, font_color='#d32f2f',
                                 font_weight='bold', ax=ax,
                                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85))
    
    # Draw red X on disabled cities using text 'X'
    for node in disabled_cities:
        if node in pos:
            x, y = pos[node]
            ax.text(x, y, 'X', fontsize=32, ha='center', va='center', 
                   color='red', weight='bold', zorder=1000)
    
    ax.set_title("Réseau de Villes - Plus Court Chemin", fontsize=20, fontweight='bold', pad=25, color='#1f77b4')
    
    # VERSION 1: Legend at absolute bottom left - fixed coordinates, no background box
    legend_x = -6.0
    legend_y_start = -7.5
    
    # Legend items - one per row
    legend_items = [
        {'color': '#4CAF50', 'text': 'Départ'},
        {'color': '#F44336', 'text': 'Arrivée'},
        {'color': '#FFC107', 'text': 'Intermédiaires'},
        {'color': '#2196F3', 'text': 'Autres'},
        {'color': '#CCCCCC', 'text': 'Hors service'},
        {'color': '#dc3545', 'text': 'En panne', 'is_x': True}
    ]
    
    # Draw legend items directly without background box
    for i, item in enumerate(legend_items):
        y_pos = legend_y_start + (i * 0.42)
        
        if item.get('is_x', False):
            ax.text(legend_x, y_pos, 'X', fontsize=16, ha='left', va='center',
                   color=item['color'], weight='bold', zorder=1000,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.8))
            ax.text(legend_x + 0.3, y_pos, item['text'], fontsize=13,
                   ha='left', va='center', color='#333333', zorder=1000)
        else:
            ax.plot(legend_x + 0.1, y_pos, 'o', color=item['color'], 
                   markersize=11, markeredgewidth=0, zorder=1000)
            ax.text(legend_x + 0.3, y_pos, item['text'], fontsize=11,
                   ha='left', va='center', color='#333333', zorder=1000)
    
    ax.axis('off')
    ax.set_xlim(-6.2, 6)
    ax.set_ylim(-7.8, 5.5)
    plt.tight_layout(pad=0)
    return fig

def main():
    st.markdown('<div class="main-header">Plus Court Chemin</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Recherche Opérationnelle - Simulation de Pannes</div>', 
                unsafe_allow_html=True)
    
    graph = load_graph()
    nodes = graph.get_nodes()
    city_names = graph.get_city_names_dict()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Configuration")
        
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
        
        run_button = st.button("Calculer", type="primary", use_container_width=True)
    
    # Main content - Always show graph
    if run_button:
        if source == destination:
            st.warning("⚠️ La ville de départ et d'arrivée sont identiques !")
            graph_col = st.container()
        else:
            # Use original graph if no failures, otherwise create modified graph
            if disabled_cities or disabled_links:
                # Create modified graph excluding failures
                modified_graph = Graph()
                modified_graph.graph = {node: [] for node in nodes}
                
                for src, dest, weight in graph.get_edges():
                    # Check both directions since graph is bidirectional
                    if src not in disabled_cities and dest not in disabled_cities and (src, dest) not in disabled_links and (dest, src) not in disabled_links:
                        modified_graph.graph[src].append((dest, weight))
                
                distances, predecessors = modified_graph.dijkstra(source)
                path = modified_graph.reconstruct_path(predecessors, source, destination)
            else:
                # No failures - use original graph
                distances, predecessors = graph.dijkstra(source)
                path = graph.reconstruct_path(predecessors, source, destination)
            
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
                    st.success(f"Chemin optimal")
                    st.metric("Latence", f"{distances[destination]} ms")
                    st.metric("Étapes", len(path) - 1)
                    
                    path_full_names = [city_names[node] for node in path]
                    path_str = " → ".join(path_full_names)
                    st.markdown(f"**Trajet:**")
                    st.info(path_str)
                    
                    if disabled_cities or disabled_links:
                        st.caption(f"{len(disabled_cities)} ville(s), {len(disabled_links)} liaison(s) désactivée(s)")
                graph_col = col1
            
            # Show graph in left column
            with graph_col:
                graph_placeholder = st.empty()
                with graph_placeholder.container():
                    st.markdown("<br>" * 8, unsafe_allow_html=True)
                    with st.spinner('Calcul du chemin et génération du graphe...'):
                        fig = create_network_graph(graph, path, disabled_links, disabled_cities)
                    graph_placeholder.empty()
                st.pyplot(fig, use_container_width=False)
                plt.close()
    
    else:
        col1, col2 = st.columns([3, 1])
        with col2:
            st.info("Configurez et cliquez sur **Calculer**")
        with col1:
            graph_placeholder = st.empty()
            with graph_placeholder.container():
                st.markdown("<br>" * 8, unsafe_allow_html=True)
                with st.spinner('Chargement du graphe...'):
                    fig = create_network_graph(graph, None, set(), set())
                graph_placeholder.empty()
            st.pyplot(fig, use_container_width=False)
            plt.close()

if __name__ == "__main__":
    main()
