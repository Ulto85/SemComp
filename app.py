from os import nice
from flask import Flask,render_template,request
import spacy
import numpy as np
from scipy.spatial import distance
nlp  =spacy.load('en_core_web_md')
def nice_function(main_phrase: str,other_phrases: list) -> dict:
    main_vector= 0
    done = None
    for tok in nlp(main_phrase):
        if done==None:
            main_vector=tok.vector
            done=1
        else:
            main_vector+=tok.vector
    vectors = []
    
    for item in other_phrases:
        temp_vec = None
        done=None
        for tok in nlp(item):
            if done ==None:
                temp_vec = tok.vector
                done=1
            else:
                temp_vec+=tok.vector
        vectors.append(temp_vec)
    distances = distance.cdist([main_vector], vectors, "cosine")[0]
    min_index = np.argmin(distances)
    sim = 1- distances[min_index]
    closest_match = other_phrases[min_index]
    return {"text":closest_match,"sim":sim}

app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def index():
    if request.method =="POST":
        main_phrase=str(request.form.get('main_phrase'))
        other_phrases=str(request.form.get('other_phrases')).split(',')
        results=nice_function(main_phrase,other_phrases)
        try:
            sim=str(round(results["sim"]*100))
        except:
            sim=0
        return render_template('app.html',word=results["text"],sim=sim)
    if request.method=="GET":
        return render_template('app.html',word='none',sim='0')
    return render_template('app.html',word='none',sim='0')
app.run(host='0.0.0.0',port=8080)