class BubbleSort:
    def bubbleSort(self,array): 
        l = len(array)
        i = 0
        while i < l:
            j = i + 1
            while j < l:
                if array[i] > array[j]:
                    array.insert(i,array[j])
                    array.pop(j+1)
                j += 1
            i += 1