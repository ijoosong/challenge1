from challenge import *
from flask import *
app = Flask(__name__)

@app.route("/table")
def show_table():
    """
    Showing the table route logic.  Renders list so that only what we want (i.e. over 45 minutes and over 100 views) is shown.
    For the purpose of this experiment, I added 4 youtube videos to test with.  
    """
    list = get_list()
    list_to_render = [item for item in list if int(item['views']) >= 100 and is_longer_than_forty_five_minutes(item['duration'])]
    return render_template('view.html', items=list_to_render, title='youtube videos')

def is_longer_than_forty_five_minutes(item):
    """
    Checks to see if video is longer than 45 minutes
    """
    duration = item
    if int(duration[0]) > 0 or int(duration[1]) >= 45:
        return True
    return False

if __name__ == "__main__":
    app.run(debug=True)
