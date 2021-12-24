class InsertionSort:
    sorting_steps = []
    def insertionSort(self, array):
        #Actual Insertion Sort code starts here:
        if len(array) <= 1:
            return array
        i = 1
        while i < len(array):
            j = i-1
            while array[i] < array[j]: 
                # Insert value of array[i] into index j and everything gets pushed right
                array.insert(j,array[i])
                array.pop(i+1)

                if j != 0:
                    i -= 1  
                    j -= 1
                self.sorting_steps.append(array.copy())
            i += 1 
        return array 