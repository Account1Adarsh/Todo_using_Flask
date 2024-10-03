#imports
from flask import Flask,render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# My app setup
app=Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db=SQLAlchemy(app)


class Mytask(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(300),nullable=False)
    complete=db.Column(db.Boolean, default=False)
    created=db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


with app.app_context():
        db.create_all()

#Routes to webpages

# homepage

# @app.route("/",)
# def index():
#     return render_template("index.html")
@app.route("/",methods=["POST","GET"])
def index():
    # Add a task
    if request.method == "POST":
        curr_task=request.form['content']
        new_task=Mytask(content=curr_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    # See all current Task
    else:
        task=Mytask.query.order_by(Mytask.created).all()
        return render_template("index.html", tasks=task)



# delete an item
@app.route("/delete/<int:id>")    
def delete(id:int):
    delete_task=Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Eroor:{e}"
    

# edit an item
@app.route("/update/<int:id>", methods=["POST","GET"])
def update(id:int):
    updated_task=Mytask.query.get_or_404(id)
    
    if request.method=="POST":
        updated_task.content=request.form['con']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Eroor:{e}"
    
    else:
        return render_template("update.html",task=updated_task)


#runner and debugger
if __name__=="__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True, port=8000)