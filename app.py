from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from sorting_alg.merge_sort import MergeSort
from sorting_alg.quick_sort import QuickSort
from sorting_alg.selection_sort import SelectionSort
from sorting_alg.bubble_sort import BubbleSort
from sorting_alg.insertion_sort import InsertionSort
import csv

app = Flask(__name__)
app.run(debug=True, use_debugger=False, use_reloader=False)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class SortingEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    past_array = db.Column(db.String(10000))
    steps_array = db.Column(db.String(10000))

# Creates all tables in SQLAlchemy
db.create_all()

def convert_str_to_array(value):
    if value == "":
        return []

    array = []
    i = 0
    curr_str_num = ""
    last_comma = 0

    while i < len(value):
        if value[i] == ",":
            array.append(int(curr_str_num))
            last_comma = i
            curr_str_num = ""
        else:
            curr_str_num += value[i]
        i += 1

    # Append last number to array
    array.append(int(value[last_comma + 1:]))
    return array


def select_sorting_alg(select, array):
    if select == "merge_sort":
        sorting_alg = "Merge Sort"
        id = "merge_sort"
        alg = MergeSort()
        alg.mergeSort(array.copy(), 0, len(array) - 1)
        array_str = str(alg.sorting_steps)
    elif select == "bubble_sort":
        sorting_alg = "Bubble Sort"
        id = "bubble_sort"
        alg = BubbleSort()
        alg.bubbleSort(array.copy())
        array_str = str(alg.sorting_steps)
    elif select == "selection_sort":
        sorting_alg = "Selection Sort"
        id = "selection_sort"
        alg = SelectionSort()
        alg.selectionSort(array.copy())
        array_str = str(alg.sorting_steps)
    elif select == "insertion_sort":
        sorting_alg = "Insertion Sort"
        id = "insertion_sort"
        alg = InsertionSort()
        alg.insertionSort(array.copy())
        array_str = str(alg.sorting_steps)
    elif select == "quick_sort":
        sorting_alg = "Quick Sort"
        id = "quick_sort"
        alg = QuickSort()
        alg.quickSort(array.copy(), 0, len(array) - 1)
        array_str = str(alg.sorting_steps)
    else:
        id = "None"
        sorting_alg = "None"
        array_str = "None"

    return sorting_alg, array_str, id


@app.route("/", methods=["POST", "GET"])
def home():
    # Getting all sorting entries from database
    all_sorting_entries = SortingEntry.query.all()

    if request.method == "POST":
        value = request.form["numbers"]
        select = request.form["sorting"]
        array = convert_str_to_array(value)
        sorting_alg = ""

        result = select_sorting_alg(select, array)

        sorting_alg = result[0]
        array_str = result[1]
        id = result[2]

        new_sort = SortingEntry(
            title=id,
            past_array=str(array),
            steps_array=array_str)
        db.session.add(new_sort)
        db.session.commit()
        print(all_sorting_entries)

        return render_template('index.html', sorting=sorting_alg,
                               original=value, arr=array_str, sort_lists=all_sorting_entries)

    else:
        return render_template('index.html', sort_lists=all_sorting_entries)


@app.route("/update/<int:new_sort_id>", methods=["POST", "GET"])
def update(new_sort_id):
    sort = SortingEntry.query.filter_by(id=new_sort_id).first()
    if request.method == "POST":
        value = request.form["number"]
        array = convert_str_to_array(value)
        result = select_sorting_alg(sort.title, array)
        array_str = result[1]
        sort.past_array = str(array)
        sort.steps_array = array_str
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:new_sort_id>")
def delete(new_sort_id):
    sort = SortingEntry.query.filter_by(id=new_sort_id).first()
    db.session.delete(sort)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/create_csv")
def create_csv():
    sort_list = SortingEntry.query.all()
    csv_arr = []
    for new_sort in sort_list[::-1]:
        csv_arr.append([new_sort.id, new_sort.title,
                       new_sort.past_array, new_sort.steps_array])

    with open('sorting_data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for item in csv_arr:
            writer.writerow(item)

    return send_file('sorting_data.csv', as_attachment=True)
