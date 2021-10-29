from flask import (
    Flask,
    render_template,
    request,
    redirect,
    make_response,
    session,
    jsonify,
)
from models import db, User, Book
import base64
import pdfkit
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)
import base64

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB/db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "F-sy@WKEw!4PH*xMEBfS-wwWV9@drp^h"
app.config["SESSION_COOKIE_NAME"] = "ebook"


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)


def current_user():
    if "id" in session:
        uid = session["id"]
        user = User.query.get(uid)
        return user
    return None


@app.route("/")
def home():
    user = current_user()
    if not user:
        return redirect("/signin?error=Invalid session please sign in")
    success = request.args.get("success", None)
    error = request.args.get("error", None)
    books = Book.query.all()
    resp = make_response(
        render_template(
            "index.html",
            user=user,
            books=books,
            success=success,
            error=error,
        )
    )
    return resp


@app.route("/signup", methods=("GET", "POST"))
def signup():

    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        password2 = request.form.get("password2", None)

        if not username or not password or not password2:
            return redirect("/signup?error=Missing parameters")

        # Check if user exists
        user = User.query.filter(User.username == username).first()
        if user:
            return redirect(
                "/signup?error=This username is already taken please choose another one"
            )

        # Check if passwords match
        if password != password2:
            return redirect("/signup?error=Passwords do not match")

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/signin?success=Account create, please sign in")

    elif request.method == "GET":
        success = request.args.get("success", None)
        error = request.args.get("error", None)

        return render_template("signup.html", success=success, error=error)


@app.route("/signin", methods=("GET", "POST"))
def signin():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Check if user exists
        user = User.query.filter(
            User.username == username, User.password == password
        ).first()
        if not user:
            return redirect("/signin?error=Invalid credentials")

        session["id"] = user.id
        return redirect("/")

    elif request.method == "GET":
        success = request.args.get("success", None)
        error = request.args.get("error", None)

        return render_template("signin.html", success=success, error=error)


# def send_verify_email(email, user):
#     host = os.environ.get("DOMAIN", "localhost")
#     port = os.environ.get("PORT", "5000")

#     link = f"http://{host}:{port}/verify?username={user.username}&verify_token={user.verify_token}"
#     message = Mail(
#         from_email="ebook@congon4tor.com",
#         to_emails=email,
#         subject="Ebook verify your email",
#         html_content=f"""
#         Hi <strong>{user.username}</strong>,
#         Follow this link to verify your email.
#         <a href="{link}">{link}</a>
#         If you did not request this please ignore this email.
#         """,
#     )
#     try:
#         sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
#         response = sg.send(message)
#     except Exception as e:
#         raise e


@app.route("/logout")
def logout():
    session.pop("id", None)
    return redirect("/")


def send_ebook(email, book):
    email = [email] if isinstance(email, str) else email
    rendered = render_template("pdf_template.html", email=email, book=book)
    options = {"enable-javascript": ""}
    pdf = pdfkit.from_string(rendered, False, options=options)
    message = Mail(
        from_email="ebook@congon4tor.com",
        to_emails=",".join(email),
        subject=f"{book.name}",
        html_content=f"""
        Hi <strong>{",".join(email)}</strong>,<br>
        Thanks you so much for ordering a preview of {book.name}.<br>
        We hope you enjoy it!<br>
        <br>
        The Ebook team
        """,
    )

    encoded_file = base64.b64encode(pdf).decode()
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(f"{book.name}.pdf"),
        FileType("application/pdf"),
        Disposition("attachment"),
    )
    message.attachment = attachedFile

    sg = SendGridAPIClient(
        "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"
    )
    response = sg.send(message)
    print(response.status_code)
    print(response.body)


@app.route("/order/<book_id>", methods=("GET", "POST"))
def order(book_id):
    user = current_user()
    if not user:
        return redirect("/signin?error=Invalid session please sign in")

    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        response = make_response(
            jsonify({"success": True}),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    if request.method == "POST":
        email = request.get_json().get("email", None)
        print(email)

        try:
            send_ebook(email, book)
        except Exception as e:
            print(e)
            response = make_response(
                jsonify({"message": f"Error sending email: {e}"}),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        return redirect(f"/?success=Book {book.name} sent to {email}")

    elif request.method == "GET":
        success = request.args.get("success", None)
        error = request.args.get("error", None)

        return render_template(
            "order.html", user=user, book=book, success=success, error=error
        )
