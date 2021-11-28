class QuickSort:
    def partition(self,array, low, high):
        i = (low-1)         # index of smaller element
        pivot = array[high]     # pivot

        for j in range(low, high):

            # If current element is smaller than or
            # equal to pivot
            if array[j] <= pivot:

                # increment index of smaller element
                i = i+1
                array[i], array[j] = array[j], array[i]
        array[i+1], array[high] = array[high], array[i+1]
        return (i+1) 

    def quickSort(self,array, low, high):
        if len(array) == 1:
            return array
        if low < high:

            # pi is partitioning index, arr[p] is now
            # at right place
            pi = self.partition(array, low, high)
        
            # Separately sort elements before
            # partition and after partition
            self.quickSort(array, low, pi-1)
            self.quickSort(array, pi+1, high)