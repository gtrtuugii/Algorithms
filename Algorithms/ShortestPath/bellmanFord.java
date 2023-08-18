import java.util.Arrays;

public class BellmanFordAlgorithm {

    static class Edge {
        int source, destination, weight;

        public Edge(int source, int destination, int weight) {
            this.source = source;
            this.destination = destination;
            this.weight = weight;
        }
    }

    static int INF = Integer.MAX_VALUE;

    public static void bellmanFord(int[][] graph, int source) {
        int V = graph.length;
        int[] distances = new int[V];
        Arrays.fill(distances, INF);
        distances[source] = 0;

        for (int i = 0; i < V - 1; i++) {
            for (Edge edge : edges) {
                int u = edge.source;
                int v = edge.destination;
                int weight = edge.weight;
                if (distances[u] != INF && distances[u] + weight < distances[v]) {
                    distances[v] = distances[u] + weight;
                }
            }
        }

        // Print the shortest distances
        for (int i = 0; i < V; i++) {
            System.out.println("Distance from source to vertex " + i + " is " + distances[i]);
        }
    }

    public static void main(String[] args) {
        int V = 5;
        int[][] graph = new int[][]{
                {0, 1, -1},
                {0, 2, 4},
                {1, 2, 3},
                {1, 3, 2},
                {1, 4, 2},
                {3, 2, 5},
                {3, 1, 1},
                {4, 3, -3}
        };

        bellmanFord(graph, 0);
    }
}
