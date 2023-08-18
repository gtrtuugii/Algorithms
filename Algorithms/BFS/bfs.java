import java.util.LinkedList;
import java.util.Queue;

public class BFS {

    private int V; // Number of vertices
    private LinkedList<Integer>[] adjacencyList; // Adjacency list representation

    public BFS(int v) {
        V = v;
        adjacencyList = new LinkedList[v];
        for (int i = 0; i < v; ++i) {
            adjacencyList[i] = new LinkedList<>();
        }
    }

    // Add an edge to the graph
    public void addEdge(int v, int w) {
        adjacencyList[v].add(w);
    }

    // Perform BFS traversal starting from vertex s
    public void bfsTraversal(int s) {
        boolean[] visited = new boolean[V];
        Queue<Integer> queue = new LinkedList<>();

        visited[s] = true;
        queue.add(s);

        while (!queue.isEmpty()) {
            s = queue.poll();
            System.out.print(s + " ");

            for (Integer vertex : adjacencyList[s]) {
                if (!visited[vertex]) {
                    visited[vertex] = true;
                    queue.add(vertex);
                }
            }
        }
    }

    public static void main(String[] args) {
        BFS g = new BFS(7);
        g.addEdge(0, 1);
        g.addEdge(0, 2);
        g.addEdge(1, 3);
        g.addEdge(1, 4);
        g.addEdge(2, 5);
        g.addEdge(2, 6);

        System.out.println("BFS traversal starting from vertex 0:");
        g.bfsTraversal(0);
    }
}
