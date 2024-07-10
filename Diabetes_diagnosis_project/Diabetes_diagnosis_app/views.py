from django.shortcuts import render
from .models import Patient, HealthInfo, MedicalHistory
from django.http import HttpResponse
import joblib
import pandas as pd

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def member(request):
    return render(request,'member.html')

def add_patient(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        age = request.POST['age']
        gender = request.POST.get('gender', False)
        gender = 'Nam' if gender == 'male' else 'Nữ'
        phone_number = request.POST['phone_number']

        # Kiểm tra nếu các trường thông tin không trống
        if full_name and age and phone_number:
            
            # Tạo đối tượng Patient chỉ khi các trường thông tin không trống
            patients = Patient.objects.create(
                full_name=full_name,
                age=age,
                gender=gender,
                phone_number=phone_number
            )
            # Lưu patient.id vào session
            request.session['patient_id'] = patients.id

            return render(request, 'chandoanBN.html', {'patient_id': patients.id})
        else:
            # Trả về trang thêm thông tin bệnh nhân nếu có trường thông tin trống
            return render(request, 'thongtinBN.html', {'error_message': 'Vui lòng nhập đầy đủ thông tin.'})
    return render(request, 'thongtinBN.html')

def add_health_info(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ request.POST
        patient_id = request.POST['patients_id']
        checkup_date = request.POST['checkup_date']
        blood_pressure = request.POST.get('hypertension')  
        heart_disease = request.POST.get('heart_disease')
        bmi = request.POST['bmi']
        hba1c = request.POST['HbA1c_level']
        blood_glucose = request.POST['blood_glucose_level']
        result = request.POST['ketqua']
        accuracy=request.POST['accuracy']
        
        health_info = HealthInfo.objects.create(
            patient_id=patient_id,
            checkup_date=checkup_date,
            blood_pressure=blood_pressure,
            heart_disease=heart_disease,
            bmi=bmi,
            hba1c=hba1c,
            blood_glucose=blood_glucose
        )
        # Tạo bản ghi MedicalHistory
        medical_history = MedicalHistory.objects.create(
            patient_id=patient_id,
            result=result,
            accuracy=accuracy
        )
        request.session['message'] = 'Success'
        message = request.session.pop('message', None)

    # Nếu là GET request, render lại trang chủ hoặc trang khác tương ứng
    return render(request, 'chandoanBN.html',{'message': message})


def chandoanBN(request):
    accuracy=None
    ketqua = None
    patient_id = request.session.get('patient_id', None)
    if request.method == 'POST':
        # model = joblib.load('knn_model_Oversampling.pkl')
        # model = joblib.load('logreg_model_SMOTE.pkl')
        model = joblib.load('logreg_model_SMOTE_73.pkl')

        # Lấy dữ liệu từ request.POST và chuyển đổi thành kiểu số
        age = float(request.POST['age'])
        hypertension = float(request.POST.get('hypertension')) 
        heart_disease = float(request.POST.get('heart_disease'))
        bmi = float(request.POST['bmi'])
        HbA1c_level = float(request.POST['HbA1c_level'])
        blood_glucose_level = float(request.POST['blood_glucose_level'])

        data = pd.DataFrame([[age, blood_glucose_level, HbA1c_level, bmi, hypertension, heart_disease]],
                            columns=['age', 'blood_glucose_level', 'HbA1c_level', 'bmi', 'hypertension','heart_disease'])

        # Chạy dữ liệu qua model để dự đoán
        prediction = model.predict(data)
        
        probability = model.predict_proba(data)
        accuracys = probability[0][1] * 100

        if(prediction[0] >= 0.5):
            if(accuracys>50):
                ketqua = "Có nguy cơ bệnh tiểu đường"
            else:
                ketqua = "Không có nguy cơ bệnh tiểu đường"
        else:
            accuracys=100-accuracys
            ketqua = "Không có nguy cơ bệnh tiểu đường"
        accuracy=round(accuracys,4)
    return render(request, 'chandoanBN.html', {'ketqua': ketqua, 'patient_id': patient_id,'accuracy':accuracy})


def chuandoanBN2(request):
    ketqua = None
    accuracy=None
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'read_file' and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('File không hợp lệ, vui lòng chọn file CSV.', status=400)

            # Đọc file CSV và chọn một dòng ngẫu nhiên
            df = pd.read_csv(csv_file)
            random_row = df.sample(n=1).iloc[0]
            
            age = int(random_row['age'])
            hypertension = int(random_row['hypertension']) 
            heart_disease = int(random_row['heart_disease'])
            bmi = float(random_row['bmi'])
            HbA1c_level = float(random_row['HbA1c_level'])
            blood_glucose_level = float(random_row['blood_glucose_level'])

            context = {
                'age': age,
                'hypertension': hypertension,
                'heart_disease': heart_disease,
                'bmi': bmi,
                'HbA1c_level': HbA1c_level,
                'blood_glucose_level': blood_glucose_level,
                # 'ketqua': ketqua,
            }
            request.session['message'] = 'Success_load'
            message = request.session.pop('message', None)
            return render(request, 'chuandoan2.html', context,{'message': message})
        
        elif action == 'predict':
            # model = joblib.load('knn_model.pkl')
            # model = joblib.load('rf_model_SMOTE_7_3.pkl')
            model = joblib.load('logreg_model_SMOTE_73.pkl')
            # model = joblib.load('random_forest_model.pkl')

            # Lấy dữ liệu từ request.POST và chuyển đổi thành kiểu số
            age = int(request.POST['age'])
            hypertension = int(request.POST.get('hypertension')) 
            heart_disease = int(request.POST.get('heart_disease'))
            bmi = float(request.POST['bmi'])
            HbA1c_level = float(request.POST['HbA1c_level'])
            blood_glucose_level = float(request.POST['blood_glucose_level'])

            # Tạo DataFrame từ dữ liệu nhập vào
            data = pd.DataFrame([[age, blood_glucose_level, HbA1c_level, bmi, hypertension, heart_disease]],
                                columns=['age', 'blood_glucose_level', 'HbA1c_level', 'bmi', 'hypertension', 'heart_disease'])

            # Chạy dữ liệu qua model để dự đoán
            prediction = model.predict(data)
            probability = model.predict_proba(data)
            accuracys = probability[0][1] * 100

            if(prediction[0] >= 0.5):
                if(accuracys>50):
                    ketqua = "Có nguy cơ bệnh tiểu đường"
                else:
                    ketqua = "Không có nguy cơ bệnh tiểu đường"
            else:
                accuracys=100-accuracys
                ketqua = "Không có nguy cơ bệnh tiểu đường"
            accuracy=round(accuracys, 4)
            context = {
                'age': age,
                'hypertension': hypertension,
                'heart_disease': heart_disease,
                'bmi': bmi,
                'HbA1c_level': HbA1c_level,
                'blood_glucose_level': blood_glucose_level,
                'ketqua': ketqua,
                'accuracy': accuracy,
            }
            return render(request, 'chuandoan2.html', context)
    
    return render(request, 'chuandoan2.html', {'ketqua': ketqua, 'accuracy': accuracy})












