import java.util.*;

public class PrimAlgorithm {
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

    public static List<Edge> primMST(int[][] graph) {
        int vertices = graph.length;
        List<Edge> minimumSpanningTree = new ArrayList<>();
        boolean[] visited = new boolean[vertices];

        PriorityQueue<Edge> minHeap = new PriorityQueue<>(Comparator.comparingInt(edge -> edge.weight));
        minHeap.offer(new Edge(0, 0, 0));

        while (!minHeap.isEmpty()) {
            Edge current = minHeap.poll();

            if (!visited[current.destination]) {
                visited[current.destination] = true;
                if (current.source != current.destination) {
                    minimumSpanningTree.add(current);
                }

                for (int neighbor = 0; neighbor < vertices; neighbor++) {
                    if (graph[current.destination][neighbor] != 0 && !visited[neighbor]) {
                        minHeap.offer(new Edge(current.destination, neighbor, graph[current.destination][neighbor]));
                    }
                }
            }
        }

        return minimumSpanningTree;
    }

    public static void main(String[] args) {
        int[][] graph = {
            {0, 2, 0, 6, 0},
            {2, 0, 3, 8, 5},
            // ... Other rows of the graph matrix
        };

        List<Edge> minimumSpanningTree = primMST(graph);

        System.out.println("Minimum Spanning Tree:");
        for (Edge edge : minimumSpanningTree) {
            System.out.println("Edge (" + edge.source + " - " + edge.destination + ") Weight: " + edge.weight);
        }
    }
}
