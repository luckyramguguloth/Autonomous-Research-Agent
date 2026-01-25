import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any

class KnowledgeGraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_triplet(self, subject: str, predicate: str, object_: str, metadata: Dict[str, Any] = None):
        """
        Adds a triplet (Subject, Predicate, Object) to the graph.
        """
        self.graph.add_node(subject, type="entity")
        self.graph.add_node(object_, type="entity")
        self.graph.add_edge(subject, object_, relation=predicate, **(metadata or {}))

    def get_summary(self) -> str:
        """
        Returns a text summary of the graph content.
        """
        if self.graph.number_of_nodes() == 0:
            return "Knowledge Graph is empty."
        
        summary = []
        for u, v, data in self.graph.edges(data=True):
            relation = data.get("relation", "related to")
            summary.append(f"{u} -> [{relation}] -> {v}")
        return "\n".join(summary)

    def get_graph_data(self) -> Dict[str, Any]:
        """
        Returns graph data in a format suitable for visualization (e.g., Cytoscape/PyVis).
        """
        return nx.node_link_data(self.graph)

    def draw_graph(self, output_path: str = "graph.png"):
        """
        Saves a static image of the graph.
        """
        plt.figure(figsize=(6, 4))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', 
                node_size=100, font_size=2, font_weight='bold', arrows=True)
        edge_labels = nx.get_edge_attributes(self.graph, 'relation')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.savefig(output_path)
        plt.close()
