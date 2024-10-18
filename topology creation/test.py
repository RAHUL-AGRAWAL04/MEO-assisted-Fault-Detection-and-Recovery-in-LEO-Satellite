# # def read_tle_with_total(input_filename):
# #     """
# #     Reads the TLE file, returns the total number of satellites and the TLE data with satellite name and ID.
# #     """
# #     with open(input_filename, 'r') as infile:
# #         lines = infile.readlines()

# #     total_satellites = int(lines[0].strip())  # First line contains total number of satellites
# #     tle_data = []
    
# #     # Process the file in chunks of 3 lines for each satellite
# #     tle_chunk_size = 3
# #     for i in range(1, len(lines), tle_chunk_size):  # Start from line 1 since line 0 is total count
# #         if i + 2 >= len(lines):
# #             break  # Ensure we do not go out of bounds
# #         # Extract the name <id> and TLE lines
# #         tle_name_line = lines[i].strip().split()  # e.g., ["SAT1", "1"]
# #         sat_name = tle_name_line[0]  # Satellite name
# #         sat_id = tle_name_line[1]    # Satellite ID
# #         tle_data.append((sat_name, sat_id))  # Store (name, id) pair for satellite

# #     return total_satellites, tle_data

# # def generate_grid(total_satellites):
# #     """
# #     Generates grid dimensions based on the total number of satellites.
# #     Example: for a total of 9 satellites, the grid will be 3x3.
# #     """
# #     # Find the closest square root to form an approximately square grid
# #     grid_size = int(total_satellites ** 0.5)  # Square root gives us the approximate dimension
# #     if grid_size * grid_size < total_satellites:
# #         grid_size += 1  # Adjust grid size if total satellites don't fit perfectly
    
# #     return grid_size

# # def assign_satellite_positions(tle_data, grid_size):
# #     """
# #     Assigns satellites to a 2D grid based on the grid size and returns a grid with satellite IDs.
# #     """
# #     satellite_grid = []
# #     index = 0
# #     for row in range(grid_size):
# #         grid_row = []
# #         for col in range(grid_size):
# #             if index < len(tle_data):
# #                 grid_row.append(tle_data[index][1])  # Add satellite ID to grid
# #                 index += 1
# #             else:
# #                 grid_row.append(None)  # Empty slot if no satellite available
# #         satellite_grid.append(grid_row)

# #     return satellite_grid

# # def generate_edges(satellite_grid):
# #     """
# #     Generates a list of edges (ISLs) for each satellite in the grid in 4 directions:
# #     Front (North), Back (South), Left (West), Right (East).
# #     """
# #     rows = len(satellite_grid)
# #     cols = len(satellite_grid[0]) if rows > 0 else 0
# #     edge_list = []

# #     for row in range(rows):
# #         for col in range(cols):
# #             current_sat = satellite_grid[row][col]
# #             if current_sat is None:
# #                 continue  # Skip empty grid slots
            
# #             # Front (North)
# #             if row > 0 and satellite_grid[row - 1][col] is not None:
# #                 edge_list.append((current_sat, satellite_grid[row - 1][col]))

# #             # Back (South)
# #             if row < rows - 1 and satellite_grid[row + 1][col] is not None:
# #                 edge_list.append((current_sat, satellite_grid[row + 1][col]))

# #             # Left (West)
# #             if col > 0 and satellite_grid[row][col - 1] is not None:
# #                 edge_list.append((current_sat, satellite_grid[row][col - 1]))

# #             # Right (East)
# #             if col < cols - 1 and satellite_grid[row][col + 1] is not None:
# #                 edge_list.append((current_sat, satellite_grid[row][col + 1]))
    
# #     return edge_list

# # def write_edges_to_file(edge_list, output_filename):
# #     """
# #     Writes the edge list to the output file, each edge on a new line.
# #     """
# #     with open(output_filename, 'w') as outfile:
# #         for edge in edge_list:
# #             outfile.write(f"{edge[0]} {edge[1]}\n")
    
# #     print(f"Edge list saved to {output_filename}")

# # # Example usage
# # input_tle_file = 'input_tle.txt'  # Input TLE file containing satellite data
# # output_edges_file = 'output_edges.txt'  # Output file for edge list

# # # Step 1: Read the TLE data with total number of satellites
# # total_satellites, tle_data = read_tle_with_total(input_tle_file)

# # # Step 2: Generate the grid size based on the total number of satellites
# # grid_size = generate_grid(total_satellites)

# # # Step 3: Assign satellites to the 2D grid based on the grid size
# # satellite_grid = assign_satellite_positions(tle_data, grid_size)

# # # Step 4: Generate the edges (ISLs) based on the grid layout
# # edge_list = generate_edges(satellite_grid)

# # # Step 5: Write the edges to the output file
# # write_edges_to_file(edge_list, output_edges_file)



# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt

# # Sample list of nodes (x, y, z coordinates)
# nodes = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (2, 5, 7), (9, 2, 3), (6, 1, 4)]  # replace with your node list

# def euclidean_distance(node1, node2):
#     return np.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2 + (node1[2] - node2[2])**2)

# # Creating the graph
# G = nx.Graph()

# # Add nodes
# for idx, node in enumerate(nodes):
#     G.add_node(idx, pos=node)

# # Add edges by finding the 4 nearest neighbors for each node
# for i, node in enumerate(nodes):
#     distances = [(j, euclidean_distance(node, other_node)) for j, other_node in enumerate(nodes) if i != j]
#     # Sort distances and pick the closest 4 neighbors
#     closest_neighbors = sorted(distances, key=lambda x: x[1])[:4]
#     for neighbor in closest_neighbors:
#         G.add_edge(i, neighbor[0])

# # Get positions of nodes for plotting
# pos = {i: node for i, node in enumerate(nodes)}

# # Visualize the graph
# nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue')
# plt.show()



import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

# Earth's radius in kilometers
R = 6371.0

# Function to calculate Haversine distance
def haversine(coord1, coord2):
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Return distance in kilometers

# Sample list of nodes with geo-coordinates (latitude, longitude, altitude(optional))
nodes = [(28.7041, 77.1025), (37.7749, -122.4194), (51.5074, -0.1278), (40.7128, -74.0060),
         (35.6895, 139.6917), (48.8566, 2.3522)]  # replace with your coordinates

# Create the graph
G = nx.Graph()

# Add nodes to the graph
for idx, node in enumerate(nodes):
    G.add_node(idx, pos=node)

# Add edges by finding the 4 nearest neighbors for each node
for i, node in enumerate(nodes):
    distances = [(j, haversine(node, other_node)) for j, other_node in enumerate(nodes) if i != j]
    # Sort distances and pick the closest 4 neighbors
    closest_neighbors = sorted(distances, key=lambda x: x[1])[:4]
    for neighbor in closest_neighbors:
        G.add_edge(i, neighbor[0])

# Extract positions for visualization (ignoring altitude for plotting purposes)
pos = {i: (node[1], node[0]) for i, node in enumerate(nodes)}  # flip for lat-long plotting

# Plot the graph
nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue')
plt.show()
