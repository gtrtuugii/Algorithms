import CITS2200.Sort;

public class Sorter implements Sort {

    private int count;

    public Sorter() {
        count = 0;
    }

    public int getCount() {
        return count;
    }

    public void reset() {
        count = 0;
    }

    private void swap(long[] a, int x, int y) {
        long temp = a[x];
        a[x] = a[y];
        count += 2; // Increase count for both array assignments
        a[y] = temp;
        count += 2; // Increase count for array assignments
    }
}
