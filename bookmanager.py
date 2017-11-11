import os  #access path on file system

from flask import Flask #flask library
from flask import render_template #render html templates
from flask import request #hndle HTTP requests
from flask import redirect #handles redirections

from flask_sqlalchemy import SQLAlchemy #ORM  (object relational mapper)


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db")) #setup database file in project directory
#sqlite:/// prefix tells flask what database engine to use

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file #tell webapp where database will be stored

db = SQLAlchemy(app) #initialize connection with the database, store in db variable

#Home Route
@app.route("/", methods=["GET", "POST"])
def home():
	if request.form:
		book = Book(title=request.form.get("title"))
		db.session.add(book)
		db.session.commit() #commit changes to persist them

		print(request.form)
	books = Book.query.all()
	return render_template("home.html", books=books)

#Update Route
@app.route("/update", methods=["POST"])
#gets the old book and updated title from the form
def update():
	newtitle = request.form.get("newtitle")
	oldtitle = request.form.get("oldtitle")
	book = Book.query.filter_by(title=oldtitle).first() #fetches the book with the old title from the database
	book.title = newtitle #updates the book title to the new title

	db.session.commit()
	return redirect("/") #redirects the user to the homepage


@app.route("/delete", methods=["POST"])
def delete():
	title = request.form.get("title") #find book with given title
	book = Book.query.filter_by(title=title).first() #find the book by title, link to book variable
	db.session.delete(book) #remove book from database
	db.session.commit() #db persistence
	#return redirect("/") #redirect to homepage
	return redirect('http://fb.com')

#Book class inherits from database model
#SQLalchemy creates a table called book
class Book(db.Model):
	#create class attribute title
	#SQLAlchemy will use this as a column name in the book table
	title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

	#define how to represent book objects as string
	def __repr__(self):
		return "<Title: {}>".format(self.title)

if __name__ == "__main__":
	app.run(debug=True)
