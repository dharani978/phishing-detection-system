from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,phishing_detection,detection_accuracy,detection_ratio

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)

        return render(request, 'RUser/Register1.html')
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_URL_Type(request):
    if request.method == "POST":

        if request.method == "POST":
            url = request.POST.get('url')

        data = pd.read_csv("Datasets.csv",encoding='latin-1')

        def apply_results(results):
            if (results == "benign"):
                return 0
            elif (results == "phishing"):
                return 1

        data['Results'] = data['type'].apply(apply_results)

        x = data['url']
        y = data['Results']

        cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))

        print(x)
        print("Y")
        print(y)

        x = cv.fit_transform(x)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        # Note:: If user want to add more classifier,can add here and test the prediction

        print("SVM")
        from sklearn import svm

        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print("ACCURACY")
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Random Forest Classifier")
        from sklearn.ensemble import RandomForestClassifier
        rf_clf = RandomForestClassifier()
        rf_clf.fit(X_train, y_train)
        rfpredict = rf_clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, rfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, rfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, rfpredict))
        models.append(('RandomForestClassifier', rf_clf))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        url1 = [url]
        vector1 = cv.transform(url1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = str(pred.replace("]", ""))

        prediction = int(pred1)

        if prediction == 0:
            val = 'Normal URL'
        elif prediction == 1:
            val = 'Phishing URL'

        print(prediction)
        print(val)

        phishing_detection.objects.create(url=url,Prediction=val)

        return render(request, 'RUser/Predict_URL_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_URL_Type.html')



