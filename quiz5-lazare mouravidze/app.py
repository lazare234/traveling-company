from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=5)

users = {
    "admin": "password"
}

movies = [
    {
        "id": 1,
        "title": "Inception",
        "director": "Christopher Nolan",
        "description": "A mind-bending thriller.",
        "year": 2010
    },
    {
        "id": 2,
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "description": "Space exploration and time.",
        "year": 2014
    }
]


@app.route('/')
def index():
    return render_template('index.html', movies=movies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user and pwd:
            session.permanent = True
            session['user'] = user
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Please fill in both fields.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie.html', movie=movie)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_id = len(movies) + 1
        new_movie = {
            "id": new_id,
            "title": request.form['title'],
            "director": request.form['director'],
            "description": request.form['description'],
            "year": int(request.form['year'])
        }
        movies.append(new_movie)
        return redirect(url_for('index'))

    return render_template('add_movie.html')


if __name__ == '__main__':
    app.run(debug=True)
