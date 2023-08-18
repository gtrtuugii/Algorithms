import java.util.*;

public class KruskalAlgorithm {
    static class Edge {
        int source;
        int destination;
        int weight;

        public Edge(int source, int destination, int weight) {
            this.source = source;
            this.destination = destination;
            this.weight = weight;
        }
    }

    static class Subset {
        int parent;
        int rank;

        public Subset(int parent, int rank) {
            this.parent = parent;
            this.rank = rank;
        }
    }

    public static List<Edge> kruskalMST(List<Edge> edges, int vertices) {
        List<Edge> minimumSpanningTree = new ArrayList<>();
        edges.sort(Comparator.comparingInt(edge -> edge.weight));

        Subset[] subsets = new Subset[vertices];
        for (int i = 0; i < vertices; i++) {
            subsets[i] = new Subset(i, 0);
        }

        int index = 0;
        while (minimumSpanningTree.size() < vertices - 1) {
            Edge current = edges.get(index++);

            int rootSource = find(subsets, current.source);
            int rootDestination = find(subsets, current.destination);

            if (rootSource != rootDestination) {
                minimumSpanningTree.add(current);
                union(subsets, rootSource, rootDestination);
            }
        }

        return minimumSpanningTree;
    }

    public static int find(Subset[] subsets, int vertex) {
        if (subsets[vertex].parent != vertex) {
            subsets[vertex].parent = find(subsets, subsets[vertex].parent);
        }
        return subsets[vertex].parent;
    }

    public static void union(Subset[] subsets, int root1, int root2) {
        if (subsets[root1].rank < subsets[root2].rank) {
            subsets[root1].parent = root2;
        } else if (subsets[root1].rank > subsets[root2].rank) {
            subsets[root2].parent = root1;
        } else {
            subsets[root1].parent = root2;
            subsets[root2].rank++;
        }
    }

    public static void main(String[] args) {
        List<Edge> edges = new ArrayList<>();
        edges.add(new Edge(0, 1, 4));
        edges.add(new Edge(0, 2, 6));
        // ... Other edges

        int vertices = 4; // Number of vertices in the graph
        List<Edge> minimumSpanningTree = kruskalMST(edges, vertices);

        System.out.println("Minimum Spanning Tree:");
        for (Edge edge : minimumSpanningTree) {
            System.out.println("Edge (" + edge.source + " - " + edge.destination + ") Weight: " + edge.weight);
        }
    }
}
