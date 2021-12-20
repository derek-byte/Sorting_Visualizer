class MergeSort:
    sorting_steps = []

    def mergeSort(self, array, l, h):
        if l < h:
            mid = (l + h) // 2 
            self.mergeSort(array, l, mid)
            self.mergeSort(array, mid + 1, h)
            self.merge(array, l, mid, h)

    def merge(self, array, l, mid, h):
        i1 = l
        i2 = mid + 1
        while i2 <= h and i1 < h: 
            if array[i1] > array[i2]:
                array.insert(i1, array[i2])
                array.pop(i2 + 1)
                i2 += 1 
            self.sorting_steps.append(array.copy())
            i1 += 1