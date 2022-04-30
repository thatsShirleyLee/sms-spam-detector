from sre_constants import GROUPREF_UNI_IGNORE
from flask import Flask,render_template,request,jsonify, current_app
from encoders import BertVectorizer
import tensorflow as tf # 2.8.0
import tensorflow_text
# import tf-models-official
from pathlib import Path
import mimetypes
import joblib
from tensorflow.python.ops.numpy_ops import np_config


np_config.enable_numpy_behavior()
mimetypes.add_type('application/javascript', '.js')

# build encoder
bert = BertVectorizer()

# load model to predict sms
default_model = tf.saved_model.load(str(Path("saved_model", "sms_bert_model_en")))

# model_dict = [
#     joblib.load(str(Path("saved_model","GaussianNB.joblib"))),
#     joblib.load(str(Path("saved_model","SVC.joblib"))),
#     joblib.load(str(Path("saved_model","LinearSVC.joblib"))),
#     joblib.load(str(Path("saved_model","LogisticRegression.joblib"))),
#     joblib.load(str(Path("saved_model","SGDClassifier.joblib"))),
#     joblib.load(str(Path("saved_model","KNeighborsClassifier.joblib"))),
#     joblib.load(str(Path("saved_model","MLPClassifier.joblib"))),
# ]

model_dict = {
    "GaussianNB": joblib.load(str(Path("saved_model","GaussianNB.joblib"))),
    "SVC": joblib.load(str(Path("saved_model","SVC.joblib"))),
    "LinearSVC": joblib.load(str(Path("saved_model","LinearSVC.joblib"))),
    "LogisticRegression": joblib.load(str(Path("saved_model","LogisticRegression.joblib"))),
    "SGDClassifier": joblib.load(str(Path("saved_model","SGDClassifier.joblib"))),
    "KNeighborsClassifier": joblib.load(str(Path("saved_model","KNeighborsClassifier.joblib"))),
    "MLPClassifier": joblib.load(str(Path("saved_model","MLPClassifier.joblib"))),
}


app = Flask(__name__, static_url_path='/src', static_folder=Path("sms-detector","dist"))


@app.route('/')
def home():
    return current_app.send_static_file('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        sms_req = request.form['sms_req']
        selected_model = request.form['selectedClf']
        data = [s for s in sms_req.split('\n') if len(s)>0 and not s.isspace()]
        if selected_model!="":
            result = model_dict[selected_model].predict(bert.fit_transform(data)).tolist() # [1, 0, 1, 0, 0]
        else:
            result = [i[0] for i in default_model(tf.constant(data))]
            # [
            #     [0.9873866777, 0.3458667772],
            #     [0.9873866777, 0.9873866777],
            #     [0.9873866777, 0.3458667772],
            #     [0.9873866777, 0.9873866777],
            #     [0.9873866777, 0.9873866777],
            # ]
        pre_result = []
        for i in range(len(result)):
            pre_result.append({'content': data[i], 'result': 'spam' if round(result[i])==1 else 'ham'}) 
        return jsonify(pre_result)

if __name__ == '__main__':
    app.run()