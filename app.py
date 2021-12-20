from flask import Flask
from sorting_alg.merge_sort import MergeSort
from sorting_alg.quick_sort import QuickSort
from sorting_alg.selection_sort import SelectionSort
from sorting_alg.bubble_sort import BubbleSort
from sorting_alg.insertion_sort import InsertionSort

app = Flask(__name__)

array = [5, 4, 3, 2, 1]

@app.route("/")
def home():
    return "Hello World"

@app.route("/merge_sort")
def merge_sort():
    alg = MergeSort()
    alg.mergeSort(array.copy(), 0, len(array)-1)
    array_str = str(alg.sorting_steps)
    return array_str

@app.route("/quick_sort")
def quick_sort():
    alg = QuickSort()
    alg.quickSort(array, 0, len(array)-1)
    array_str = str(array)
    return array_str

@app.route("/selection_sort")
def selection_sort():
    alg = SelectionSort()
    alg.selectionSort(array)
    array_str = str(array)
    return array_str

@app.route("/bubble_sort")
def bubble_sort():
    alg = BubbleSort()
    alg.bubbleSort(array)
    array_str = str(array)
    return array_str

@app.route("/insertion_sort")
def insertion_sort():
    alg = InsertionSort()
    alg.insertionSort(array)
    array_str = str(array)
    return array_str