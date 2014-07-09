from flask import Flask, render_template, request
import translator

app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/query', methods=['GET'])
def query():
	originalForm = str(request.args['original'])
	type_translate = str(request.args['translate'])
	if type_translate == 'eng2chi':
		translated = translator.english_to_chinese(originalForm)
	elif type_translate == 'eng2spa':
		translated = "We currently do not support English to Spanish. Check back soon."
	elif type_translate == 'eng2kor':
		translated = "We currently do not support English to Korean. Check back soon."
	return render_template('query.html', translated=translated, original=originalForm)

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/contact/')
def contact():
	return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404