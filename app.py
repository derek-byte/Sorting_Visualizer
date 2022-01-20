from select import select
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from sorting_alg.merge_sort import MergeSort
from sorting_alg.quick_sort import QuickSort
from sorting_alg.selection_sort import SelectionSort
from sorting_alg.bubble_sort import BubbleSort
from sorting_alg.insertion_sort import InsertionSort

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    past_array = db.Column(db.String(10000))
    steps_array = db.Column(db.String(10000))
    # complete = db.Column(db.Boolean)


def convert_array(value):
    if value == "":
        return []

    array = []
    i = 0
    num = ""
    last_comma = 0
    while i < len(value):
      if value[i] == ",":
        array.append(int(num))
        last_comma = i
        num = ""
      else:
          num += value[i]
      i += 1 
    array.append(int(value[last_comma+1:]))
    return array

def sort1(select, array):
    if select == "merge_sort":
        sorting_alg = "Merge Sort"
        alg = MergeSort()
        alg.mergeSort(array.copy(), 0, len(array)-1)
        array_str = str(alg.sorting_steps)

    elif select == "bubble_sort":
        sorting_alg = "Bubble Sort"
        alg = BubbleSort()
        alg.bubbleSort(array.copy())
        array_str = str(alg.sorting_steps)

    elif select == "selection_sort":
        sorting_alg = "Selection Sort"
        alg = SelectionSort()
        alg.selectionSort(array.copy())
        array_str = str(alg.sorting_steps)

    elif select == "insertion_sort":
        sorting_alg = "Insertion Sort"
        alg = InsertionSort()
        alg.insertionSort(array.copy())
        array_str = str(alg.sorting_steps)

    elif select == "quick_sort":
        sorting_alg = "Quick Sort"
        alg = QuickSort()
        alg.quickSort(array.copy(), 0, len(array)-1)
        array_str = str(alg.sorting_steps)

    else:
        sorting_alg = "None"
        array_str = "None"

    return sorting_alg, array_str

@app.route("/", methods = ["POST", "GET"])
def home():
    db.create_all()

    sort_list = Sort.query.all()
    print(sort_list)
    if request.method == "POST":
        value = request.form["numbers"]
        select = request.form["sorting"]
        array = convert_array(value)
        sorting_alg = ""

        result = sort1(select, array)

        sorting_alg = result[0]
        array_str = result[1]

        new_sort = Sort(title=sorting_alg, past_array=str(array), steps_array=array_str)
        db.session.add(new_sort)
        db.session.commit()
        print(sort_list)

        return render_template('index.html', sorting= sorting_alg, original=value, arr=array_str, sort_lists=sort_list)

    else:
        return render_template('index.html', sort_lists=sort_list)


@app.route("/update/<int:new_sort_id>", methods = ["POST", "GET"])
def update(new_sort_id):
        sort = Sort.query.filter_by(id=new_sort_id).first()
        # array = sort.
        print(request.method)
        print(new_sort_id)
        if request.method == "POST":
            value = request.form["number"]
            array = convert_array(value)
            result = sort1(select, array)
            array_str = result[1]
            sort.past_array = str(array)
            sort.steps_array = array_str
        db.session.commit()
        return redirect(url_for("home"))


@app.route("/delete/<int:new_sort_id>")
def delete(new_sort_id):
        sort = Sort.query.filter_by(id=new_sort_id).first()
        db.session.delete(sort)
        db.session.commit()
        return redirect(url_for("home"))