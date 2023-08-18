import java.util.Arrays;

public class FloydWarshallAlgorithm {

    static int INF = Integer.MAX_VALUE;

    public static void floydWarshall(int[][] graph) {
        int V = graph.length;
        int[][] distances = new int[V][V];

        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                distances[i][j] = graph[i][j];
            }
        }

        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {
                    if (distances[i][k] != INF && distances[k][j] != INF && distances[i][k] + distances[k][j] < distances[i][j]) {
                        distances[i][j] = distances[i][k] + distances[k][j];
                    }
                }
            }
        }

        // Print the shortest distances
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                System.out.print(distances[i][j] + " ");
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        int V = 4;
        int[][] graph = {
                {0, INF, -2, INF},
                {4, 0, 3, INF},
                {INF, INF, 0, 2},
                {INF, -1, INF, 0}
        };

        floydWarshall(graph);
    }
}
