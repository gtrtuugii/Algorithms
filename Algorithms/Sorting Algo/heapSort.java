public class HeapSort extends Sorter {

    public void heapSort(long[] a) {
        int n = a.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(a, n, i);
        }
        for (int i = n - 1; i >= 0; i--) {
            swap(a, 0, i);
            heapify(a, i, 0);
        }
    }

    private void heapify(long[] a, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n && a[left] > a[largest]) {
            largest = left;
        }

        if (right < n && a[right] > a[largest]) {
            largest = right;
        }

        if (largest != i) {
            swap(a, i, largest);
            heapify(a, n, largest);
        }
    }
}
