from flask import Flask,request,redirect,url_for,render_template
from flask.scaffold import F
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////todo.db'  #databasemiz ile orm yi birleştirmek kısmı sağ tarafta bulunan kısım kendi data base yolumuz
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = ToDo.query.all()   #bu komut bize bir liste dönücek. listede ise todo özelliklerimiz sözlük halinde bulunacak.
    return render_template("index.html", todos = todos)

@app.route("/complete/<string:id>")  #string id dinamik url buradaki id yi altta fonksiyonumuza verdik
def completeTodo(id):
    todo = ToDo.query.filter_by(id = id).first()  #burada id = id yaptık buda demek ki örnek id si 1 olan veriyi al ve todo değişkenine ata
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete # üstteki if durumunu ile aynı işlevi görüyor

    db.session.commit()

    return redirect(url_for("index"))

@app.route("/add", methods = ["POST"])
def addToDo():
    title = request.form.get("title") #title name'ine sahip fromdaki değerimizi request yardımı ile aldık
    newTodo = ToDo(title = title, complete = False)  #oluşturduğumuz classdan yeni bir todo objesi oluşturup değerleri verdik
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deletetodo(id):
    todo = ToDo.query.filter_by(id = id).first()  #burada id = id yaptık buda demek ki örnek id si 1 olan veriyi al ve todo değişkenine ata
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))


class ToDo(db.Model):    #buradaki tablo oluşturma class'ı ile ToDo isimli tabloyu db.Modelden (orm nin içindeki model yapısından) türettik
    
    id = db.Column(db.Integer, primary_key=True)   #özelliklerimizi ekliyoruz
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


if __name__ == "__main__":   #server ayağa kalktı
    db.create_all() # class ımız databasemize ekleicek. 
    app.run(debug=True)



