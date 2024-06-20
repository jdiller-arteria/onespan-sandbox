from flask import Flask, render_template, render_template_string, request, redirect
from onespan.client import Client
app = Flask(__name__, static_folder="static")

@app.route("/")
def hello_world():
    return render_template("start.html")

@app.route("/create_signing_session", methods=["POST"])
def create_signing_session():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email  = request.form.get('email')
    doc = request.files.get('document')
    extra_auth = request.form.get('extraAuth')
    sms_verification = None
    questions = None

    if extra_auth == 'question':
        question = request.form.get('question')
        answer = request.form.get('answer')
        questions = [{'question': question, 'answer': answer}]
    elif extra_auth == 'sms':
        sms_verification = request.form.get('phoneNumber')
    onespan_client = Client()
    package = onespan_client.create_package(first_name,
                                            last_name,
                                            email,
                                            doc,
                                            questions=questions,
                                            sms_verification=sms_verification)
    if not package.ok:
        return render_template_string("{{content}}", content=package.text)
    package_id = package.json()['id']
    signing_url = onespan_client.get_signing_url(package_id)
    return render_template("signing_session.html", signing_url=signing_url.json()['url'])

