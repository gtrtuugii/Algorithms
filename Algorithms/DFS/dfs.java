import java.util.ArrayList;
import java.util.List;

public class DFS {
    private int vertices;
    private List<List<Integer>> adjacencyList;

    public DFS(int vertices) {
        this.vertices = vertices;
        this.adjacencyList = new ArrayList<>(vertices);
        for (int i = 0; i < vertices; i++) {
            adjacencyList.add(new ArrayList<>());
        }
    }

    public void addEdge(int source, int destination) {
        adjacencyList.get(source).add(destination);
    }

    public void depthFirstSearch(int startVertex) {
        boolean[] visited = new boolean[vertices];
        dfsTraversal(startVertex, visited);
    }

    private void dfsTraversal(int vertex, boolean[] visited) {
        visited[vertex] = true;
        System.out.print(vertex + " ");

        List<Integer> neighbors = adjacencyList.get(vertex);
        for (Integer neighbor : neighbors) {
            if (!visited[neighbor]) {
                dfsTraversal(neighbor, visited);
            }
        }
    }

    public static void main(String[] args) {
        DFS graph = new DFS(6);
        graph.addEdge(0, 1);
        graph.addEdge(0, 2);
        graph.addEdge(1, 3);
        graph.addEdge(2, 4);
        graph.addEdge(2, 5);

        System.out.println("Depth First Traversal (starting from vertex 0):");
        graph.depthFirstSearch(0);
    }
}
