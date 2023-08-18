public class MergeSort extends Sorter {

    public void mergeSort(long[] a) {
        mergeSort(a, 0, a.length - 1);
    }

    private void merge(long[] a, int p, int q, int r) {
        int n1 = q - p + 1;
        int n2 = r - q;

        long[] left = new long[n1];
        long[] right = new long[n2];

        for (int i = 0; i < n1; i++) {
            left[i] = a[p + i];
            count++;
        }
        for (int j = 0; j < n2; j++) {
            right[j] = a[q + j + 1];
            count++;
        }

        int i = 0, j = 0, k = p;
        while (i < n1 && j < n2) {
            if (left[i] <= right[j]) {
                a[k] = left[i];
                i++;
            } else {
                a[k] = right[j];
                j++;
            }
            k++;
            count++; // Increase count for array assignment
        }

        while (i < n1) {
            a[k] = left[i];
            i++;
            k++;
            count++; // Increase count for array assignment
        }

        while (j < n2) {
            a[k] = right[j];
            j++;
            k++;
            count++; // Increase count for array assignment
        }
    }

    private void mergeSort(long[] a, int p, int r) {
        if (p < r) {
            int q = (p + r) / 2;
            mergeSort(a, p, q);
            mergeSort(a, q + 1, r);
            merge(a, p, q, r);
        }
    }
}
