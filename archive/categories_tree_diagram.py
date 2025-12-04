import networkx as nx
import matplotlib.pyplot as plt

# Define the nodes and their levels in the hierarchy
level1_health_nonhealth = ['Health', 'Non-Health'] # Now at the top
level2_pathways = ['Reduced Mortality', 'Time Saved', 'NHS', 'QALY', 'Society', 'Amenity', 'Sleep Disturbance']
level3_cobenefits = ['Air Quality', 'Congestion', 'Dampness', 'Excess Cold', 'Excess Heat', 'Noise', 'Physical Activity', 'Diet Change', 'Hassle Costs', 'Road Repairs', 'Road Safety']

G = nx.DiGraph()

# Edges (Level 1: Health/Non-Health -> Level 2: Damage Pathway) - REVERSED
edges_l1_l2 = [
    ('Health', 'Reduced Mortality'), ('Health', 'QALY'), ('Health', 'Sleep Disturbance'),
    ('Non-Health', 'NHS'), ('Non-Health', 'Time Saved'), ('Non-Health', 'Society'), ('Non-Health', 'Amenity'),
]

# Edges (Level 2: Damage Pathway -> Level 3: Co-benefit Type) - REVERSED
edges_l2_l3 = [
    ('Reduced Mortality', 'Air Quality'),
    ('Time Saved', 'Congestion'),
    ('NHS', 'Dampness'), ('QALY', 'Dampness'), ('Society', 'Dampness'),
    ('NHS', 'Excess Cold'), ('QALY', 'Excess Cold'), ('Society', 'Excess Cold'),
    ('NHS', 'Excess Heat'), ('QALY', 'Excess Heat'), ('Society', 'Excess Heat'),
    ('Amenity', 'Noise'), ('Sleep Disturbance', 'Noise'),
    ('Reduced Mortality', 'Physical Activity'),
    ('Reduced Mortality', 'Diet Change'),
    ('Time Saved', 'Hassle Costs'),
    ('Society', 'Road Repairs'),
    ('Reduced Mortality', 'Road Safety'), ('Society', 'Road Safety'),
]

G.add_edges_from(edges_l1_l2)
G.add_edges_from(edges_l2_l3)

# Assign levels for the multipartite layout (reversed hierarchy for vertical top-down)
node_levels = {}
for node in G.nodes():
    if node in level1_health_nonhealth: node_levels[node] = 1
    elif node in level2_pathways: node_levels[node] = 2
    elif node in level3_cobenefits: node_levels[node] = 3
    else: node_levels[node] = 0 # Fallback for any unassigned, though all should be

for node, level in node_levels.items():
    G.nodes[node]['level'] = level

# Use multipartite layout for a clean layered hierarchy
pos = nx.multipartite_layout(G, subset_key='level', align='vertical')

# Custom coloring based on level
color_map = {1: '#2171B5', 2: '#6BAED6', 3: '#C6DBEF'} # Blue gradient
node_colors = [color_map[G.nodes[node]['level']] for node in G.nodes()]
labels = {node: node for node in G.nodes()}

plt.figure(figsize=(14, 20)) # Increased figure size
nx.draw(G, pos,
        node_color=node_colors,
        with_labels=True,
        labels=labels,
        node_size=8000, # Increased node size
        font_size=9, # Increased font size
        font_weight='bold',
        edge_color='gray',
        arrows=True,
        arrowsize=20,
        font_color='black',
        node_shape='s', # Use squares for better visibility
       )
plt.title('Hierarchical Structure of UK Co-benefit Classification (Health/Non-Health Top)', fontsize=16)
plt.tight_layout()
plt.savefig('cobenefit_hierarchy_diagram_vertical_large_text.png')
print("cobenefit_hierarchy_diagram_vertical_large_text.png")