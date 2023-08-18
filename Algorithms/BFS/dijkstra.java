import java.util.*;

public class DijkstraAlgorithm {
    static class Edge {
        int destination;
        int weight;

        public Edge(int destination, int weight) {
            this.destination = destination;
            this.weight = weight;
        }
    }

    public static int[] dijkstra(int[][] graph, int source) {
        int vertices = graph.length;
        int[] distance = new int[vertices];
        Arrays.fill(distance, Integer.MAX_VALUE);
        distance[source] = 0;

        PriorityQueue<Edge> minHeap = new PriorityQueue<>(Comparator.comparingInt(edge -> edge.weight));
        minHeap.offer(new Edge(source, 0));

        while (!minHeap.isEmpty()) {
            Edge current = minHeap.poll();

            for (int neighbor = 0; neighbor < vertices; neighbor++) {
                if (graph[current.destination][neighbor] != 0) {
                    int newDistance = current.weight + graph[current.destination][neighbor];
                    if (newDistance < distance[neighbor]) {
                        distance[neighbor] = newDistance;
                        minHeap.offer(new Edge(neighbor, newDistance));
                    }
                }
            }
        }

        return distance;
    }

    public static void main(String[] args) {
        int[][] graph = {
            {0, 4, 0, 0, 0, 0, 0, 8, 0},
            {4, 0, 8, 0, 0, 0, 0, 11, 0},
            // Other rows of the graph matrix can be added here
        };

        int source = 0;
        int[] distances = dijkstra(graph, source);

        System.out.println("Shortest distances from source " + source + ":");
        for (int i = 0; i < distances.length; i++) {
            System.out.println("Vertex " + i + ": " + distances[i]);
        }
    }
}
