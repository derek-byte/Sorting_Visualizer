class SelectionSort:
    sorting_steps = []
    def selectionSort(self,array):
        i = 0 
        while i < len(array):
            
            j = i 
            ans = array[i]
            index = 0
            while j < len(array):
                if array[j] <= ans:
                    ans = array[j]
                    index = j
                j += 1 
                
            array.insert(i,ans)
            array.pop(index+1)
            
            i += 1
            self.sorting_steps.append(array.copy())
        return array