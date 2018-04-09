import time
import psycopg2
from flask import Flask, render_template, g

app = Flask(__name__)

def get_db():
  """
  Returns the connection to the database, opening a new
  one if there is none
  """
  if not hasattr(g, 'db_1'):
    g.db = psycopg2.connect(dbname='seerene',
                            user='seerene',
                            password='seerene',
                            host='db')

  return g.db

@app.teardown_appcontext
def close_db(error):
  """
  Closes the database connection on teardown
  """
  if hasattr(g, 'db'):
    g.db.close()

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/data')
def db():
    sql = """
        SELECT 
        id, name 
        FROM 
        seerene_data
        LIMIT
        100;
    """
    cur = get_db().cursor()
    cur.execute(sql)
 
    datas = []
    for data_in_db in cur.fetchall():
        datas.append({
        'id': data_in_db[0],
        'name': data_in_db[1]
        })
 
    cur.close()
 
    print(datas)
    return render_template('index.html', datas=datas)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
