#!/usr/bin/python3
"""python3 -c 'print(__import__("my_module").MyClass.__doc__)'
"""
from flask import Flask, render_template
from models import storage, State
app = Flask(__name__)
state_list = storage.all(State).values()
sorted_list = sorted(state_list, key=lambda obj: obj.name)
for state in sorted_list:
    state.cities = sorted(state.cities, key=lambda city: city.name)


@app.teardown_appcontext
def close_session(exception=None):
    """ calls the close method on storage with every request
    """
    storage.close


@app.route('/states', strict_slashes=False)
def states():
    """renders an html page that lists all the states in the database
    """
    return render_template('7-states_list.html', objs=sorted_list)


@app.route('/states/<id>', strict_slashes=False)
def city(id):
    """renders an html page for a given state with its cities
    """
    obj = None
    for state in sorted_list:
        if id == state.id:
            obj = state
            break
    return render_template('9-states.html', obj=obj)


if __name__ == '__main__':
    app.run()
