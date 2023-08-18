public class InsertionSort extends Sorter {

    public void insertionSort(long[] a) {
        for (int i = 1; i < a.length; i++) {
            long key = a[i];
            int prev = i - 1;
            while (prev >= 0 && a[prev] > key) {
                a[prev + 1] = a[prev];
                prev--;
                count += 2; // Increase count for both array assignments
            }
            a[prev + 1] = key;
            count += 2; // Increase count for array assignment and key placement
        }
    }
}
