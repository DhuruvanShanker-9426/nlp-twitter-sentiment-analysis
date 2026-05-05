from flask import Flask,request,render_template
import joblib
import os
from utils.preprocessing import cleaning,preprocessing
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

model_path=os.environ.get("MODEL_PATH","model/sentiment_model.pkl")
vectorizer_path=os.environ.get("TFIDF_VECTORIZER_PATH","model/tfidf_vectorizer.pkl")

model=joblib.load(model_path)
vectorizer=joblib.load(vectorizer_path)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
     tweet=request.form.get("tweet")
     
     if not tweet or tweet.strip()=="":
         return render_template("index.html",result="Enter the tweet!!!")
     
     original_tweet=tweet
     tweet = cleaning(tweet)
     tweet = preprocessing(tweet)
     
     tweet_vector=vectorizer.transform([tweet])
     
     prediction=model.predict(tweet_vector)[0]
     
     class_names=["Negative","Positive"]
     
     result=class_names[int(prediction)]
     
     print(f'''
           Tweet :{tweet},
           Sentiment:{result}
           ''')
     
     return render_template("index.html",result=result,tweet=original_tweet)
 
if __name__=="__main__":
    debug_mode=os.environ.get("DEBUG","False")=="True"
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=debug_mode)