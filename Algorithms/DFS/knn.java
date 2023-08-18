import java.util.*;

class KNNNeighbors {
    static class Point {
        int x, y;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }
    }

    static class Neighbor implements Comparable<Neighbor> {
        Point point;
        double distance;

        public Neighbor(Point point, double distance) {
            this.point = point;
            this.distance = distance;
        }

        @Override
        public int compareTo(Neighbor other) {
            return Double.compare(this.distance, other.distance);
        }
    }

    public static List<Point> kNearestNeighbors(List<Point> points, Point queryPoint, int k) {
        PriorityQueue<Neighbor> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

        for (Point point : points) {
            double distance = calculateDistance(point, queryPoint);
            maxHeap.offer(new Neighbor(point, distance));

            if (maxHeap.size() > k) {
                maxHeap.poll();
            }
        }

        List<Point> result = new ArrayList<>();
        while (!maxHeap.isEmpty()) {
            result.add(maxHeap.poll().point);
        }

        Collections.reverse(result);
        return result;
    }

    public static double calculateDistance(Point p1, Point p2) {
        int dx = p1.x - p2.x;
        int dy = p1.y - p2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    public static void main(String[] args) {
        List<Point> points = new ArrayList<>();
        points.add(new Point(1, 2));
        points.add(new Point(4, 5));
        points.add(new Point(6, 9));
        points.add(new Point(3, 2));
        points.add(new Point(7, 8));

        Point queryPoint = new Point(5, 4);
        int k = 3;

        List<Point> nearestNeighbors = kNearestNeighbors(points, queryPoint, k);

        System.out.println("K Nearest Neighbors:");
        for (Point neighbor : nearestNeighbors) {
            System.out.println("(" + neighbor.x + ", " + neighbor.y + ")");
        }
    }
}
