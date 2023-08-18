public class QuickSort extends Sorter {

    public void quickSort(long[] a) {
        int end = a.length - 1;
        qSort(a, 0, end);
    }

    private void qSort(long[] a, int low, int high) {
        if (low < high) {
            int pi = partition(a, low, high);
            qSort(a, low, pi - 1);
            qSort(a, pi + 1, high);
        }
    }

    private int partition(long[] a, int begin, int end) {
        long pivot = a[end];
        int i = begin - 1;

        for (int x = begin; x <= end - 1; x++) {
            if (a[x] <= pivot) {
                i++;
                swap(a, i, x);
            }
        }

        swap(a, i + 1, end);
        return i + 1;
    }
}
