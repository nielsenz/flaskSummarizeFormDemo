from flask import Flask, render_template_string, request, session, redirect
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap

from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets

from gensim.summarization.summarizer import summarize 

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'secret-key-if-no-environmental-key-is-set-up'

class PostForm(FlaskForm):
    body = StringField(u'Text', widget=TextArea())
    slider = h5fields.IntegerField('% Summerized',widget=h5widgets.NumberInput(min=1,max=100))
    submit = SubmitField('Summerize')

@app.route('/', methods=['POST', 'GET'])
def form():
    form = PostForm()
    html =  """
        <h1> Summerize Text</h1>
        <p> Paste in Text to be summerized. Text should be longer than one sentence </p>
        <form action="/summerized" method="post" novalidate>
        <p>
            {{ form.body.label }}<br>
            {{ form.body(cols="35", rows="20") }}<br>
        </p>
        <p>
            {{ form.slider.label }}<br>
            {{ form.slider(size=12) }}<br>
        </p>
        <p>{{ form.submit() }}</p>
        </form>
        """

    return render_template_string(html,form=form)

@app.route('/summerized', methods=['GET', 'POST'])
def summerized():
    text = request.form.get('body')
    num = request.form.get('slider')
    summ_per = summarize(text, ratio = int(num)/100) 
    html =  """
        <h1> Summerize Text</h1>
        <p> Summerized Text: </p>
        <p>
        {{summ_per}}
        </p>
        """    
    return render_template_string(html,summ_per=summ_per)
if __name__ == "__main__":
    app.run()