from flask import Flask,Response,request,render_template
import io
import joblib
import os
import pandas as pd
from utils.preprocessing import cleaning,preprocessing
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

model_path=os.environ.get("MODEL_PATH","model/sentiment_model.pkl")
vectorizer_path=os.environ.get("TFIDF_VECTORIZER_PATH","model/tfidf_vectorizer.pkl")

model=joblib.load(model_path)
vectorizer=joblib.load(vectorizer_path)
TEXT_COLUMNS=["tweet","tweet_text","text","content","full_text","message","body"]

def find_text_column(columns):
    lower_columns={str(column).lower():column for column in columns}
    for column in TEXT_COLUMNS:
        if column in lower_columns:
            return lower_columns[column]
    return None

def predict_sentiment_label(text):
     cleaned=cleaning(str(text))
     processed=preprocessing(cleaned)
     tweet_vector=vectorizer.transform([processed])
     prediction=model.predict(tweet_vector)[0]
     class_names=["Negative","Positive"]
     return class_names[int(prediction)]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
     tweet=request.form.get("tweet")
     
     if not tweet or tweet.strip()=="":
         return render_template("index.html",result="Enter the tweet!!!")
     
     original_tweet=tweet
     result=predict_sentiment_label(tweet)
     
     return render_template("index.html",result=result,tweet=original_tweet)

@app.route("/predict-csv",methods=["POST"])
def predict_csv():
     uploaded_file=request.files.get("csv_file")

     if uploaded_file is None or uploaded_file.filename=="":
         return render_template("index.html",result="Upload a CSV file first.")

     try:
         batch_df=pd.read_csv(uploaded_file)
     except Exception:
         return render_template("index.html",result="CSV could not be read.")

     text_column=find_text_column(batch_df.columns)
     if text_column is None:
         return render_template("index.html",result="CSV needs a text column such as tweet, tweet_text, text, content, full_text, message, or body.")

     result_df=batch_df.copy()
     result_df["predicted_sentiment"]=[
         predict_sentiment_label(value)
         for value in result_df[text_column].fillna("").astype(str)
     ]

     output=io.StringIO()
     result_df.to_csv(output,index=False)
     return Response(
         output.getvalue(),
         mimetype="text/csv",
         headers={"Content-Disposition":"attachment; filename=tweet_sentiment_predictions.csv"},
     )
 
if __name__=="__main__":
    debug_mode=os.environ.get("DEBUG","False")=="True"
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=debug_mode)
