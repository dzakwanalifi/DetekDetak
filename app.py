import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

model = joblib.load('models/Decision Tree_model.pkl')

chest_pain_types = {0: 'Nyeri Dada Tipikal', 1: 'Nyeri Dada Atipikal', 2: 'Nyeri Non-Anginal', 3: 'Asimtomatik'}
resting_ecg_types = {0: 'Normal', 1: 'Abnormalitas Gelombang ST-T', 2: 'Hipertrofi Ventrikel Kiri'}
slope_types = {0: 'Naik', 1: 'Datar', 2: 'Menurun'}
thalassemia_types = {0: 'Normal', 1: 'Kerusakan Tetap', 2: 'Kerusakan Dapat Dipulihkan'}
sex_types = {0: 'Perempuan', 1: 'Laki-laki'}
exercise_induced_angina_types = {0: 'Tidak', 1: 'Ya'}

def predict_heart_disease(input_data):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    prediction_label = "💚Aman dari Penyakit Jantung" if prediction == 0 else "💔Indikasi Penyakit Angiografi Jantung"
    return prediction_label

st.title("DetekDetak: Prediksi Penyakit Jantung")

st.success('Aplikasi ini dibuat oleh M. Dzakwan Alifi (@dzakwanalifi) dalam Bootcamp Machine Learning & AI for Beginner DQLab', icon="💡")

with st.expander("Tentang DetekDetak: Prediksi Penyakit Jantung"):
    st.write(
        "Aplikasi DetekDetak adalah alat prediksi penyakit jantung berdasarkan informasi yang Anda masukkan. Anda hanya perlu memasukkan beberapa informasi pribadi dan medis untuk mendapatkan prediksi apakah Anda memiliki risiko penyakit jantung atau tidak."
    )
    st.write(
        "Setelah memasukkan informasi Anda, klik tombol 'Predict' untuk melihat hasil prediksi. Hasil prediksi akan ditampilkan dalam bentuk '💚Aman dari Penyakit Jantung' jika prediksinya adalah tidak ada penyakit jantung, dan '💔Indikasi Penyakit Angiografi Jantung' jika prediksinya adalah ada penyakit jantung."
    )

with st.expander("Informasi Variabel"):
    variables_info = {
        'Age': 'Usia dalam tahun',
        'Sex': 'Jenis kelamin',
        'Chest Pain Type': 'Jenis nyeri dada',
        'Resting Blood Pressure (mm Hg)': 'Tekanan darah istirahat (mm Hg)',
        'Serum Cholestoral (mg/dl)': 'Kolesterol serum (mg/dl)',
        'Fasting Blood Sugar': 'gula darah puasa dalam (mg/dl)',
        'Resting Electrocardiographic Results': 'Hasil elektrokardiografi istirahat',
        'Maximum Heart Rate Achieved': 'Detak jantung maksimal yang dicapai',
        'Exercise Induced Angina': 'Angina yang diinduksi olahraga',
        'ST Depression': 'Depresi ST yang diinduksi oleh latihan relatif terhadap istirahat',
        'Slope of Peak Exercise ST Segment': 'Kemiringan segmen ST puncak latihan',
        'Number of Major Vessels': 'Jumlah pembuluh utama (0-3) yang diwarnai oleh fluoroskopi',
        'Thalassemia': 'Thalassemia'
    }
    variables_df = pd.DataFrame.from_dict(variables_info, orient='index', columns=['Keterangan'])
    st.dataframe(variables_df, use_container_width=True)

st.write("### Mohon isi informasi berikut:")

today = datetime.today().date()
max_dob = today - relativedelta(years=100)
min_dob = today - timedelta(days=0)

dob = st.date_input("Date of Birth", min_value=max_dob, max_value=min_dob, value=today)
age = relativedelta(today, dob).years

sex = st.selectbox("Sex", list(sex_types.values()))

chest_pain = st.selectbox("Chest Pain Type", list(chest_pain_types.values()))
resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 20, 250, value=120)
cholesterol = st.number_input("Serum Cholestoral (mg/dl)", 100, 600, value=150)

fasting_blood_sugar = st.number_input("Fasting Blood Sugar", 80, 300)
fasting_blood_sugar = 1 if fasting_blood_sugar > 120 else 0

resting_ecg = st.selectbox("Resting Electrocardiographic Results", list(resting_ecg_types.values()))
max_heart_rate = st.number_input("Maximum Heart Rate Achieved", 0, 300, value=170)
exercise_induced_angina = st.selectbox("Exercise Induced Angina", list(exercise_induced_angina_types.values()))
st_depression = st.number_input("ST Depression", 0.0, 10.0, value=2.0)
slope = st.selectbox("Slope of Peak Exercise ST Segment", list(slope_types.values()))
num_major_vessels = st.number_input("Number of Major Vessels", 0, 3)
thalassemia = st.selectbox("Thalassemia", list(thalassemia_types.values()))

input_data = {
    'Age': age,
    'Sex': [k for k, v in sex_types.items() if v == sex][0],
    'ChestPainType': [k for k, v in chest_pain_types.items() if v == chest_pain][0],
    'RestingBP': resting_bp,
    'Cholesterol': cholesterol,
    'FastingBloodSugar': fasting_blood_sugar,
    'RestingECG': [k for k, v in resting_ecg_types.items() if v == resting_ecg][0],
    'MaxHeartRate': max_heart_rate,
    'ExerciseInducedAngina': [k for k, v in exercise_induced_angina_types.items() if v == exercise_induced_angina][0],
    'STDepression': st_depression,
    'Slope': [k for k, v in slope_types.items() if v == slope][0],
    'NumMajorVessels': num_major_vessels,
    'Thalassemia': [k for k, v in thalassemia_types.items() if v == thalassemia][0]
}

if st.button("Mulai Prediksi"):
    prediction_label = predict_heart_disease(input_data)
    st.metric("Prediction", prediction_label)
    if prediction_label == "💚Aman dari Penyakit Jantung":
        st.success("""
### Rekomendasi

Berikut adalah beberapa langkah efektif dalam menjaga kesehatan jantung Anda:

1. **Pilihan Makanan Sehat**: Konsumsi makanan yang baik untuk jantung setiap hari. Ikan beromega 3, kacang-kacangan, buah beri, dan alpukat dapat membantu menjaga kesehatan jantung Anda.

2. **Batasan Makanan Pantangan**: Hindari atau batasi konsumsi makanan yang dapat mempengaruhi kesehatan jantung Anda.

3. **Minum Air Putih Cukup**: Rajin minum air putih membantu menjaga keseimbangan tubuh dan jantung Anda.

4. **Kontrol Tekanan Darah**: Pertahankan tekanan darah dalam batas normal, karena tekanan darah tinggi dapat meningkatkan risiko penyakit jantung.

5. **Pantau Kadar Kolesterol**: Jaga kadar kolesterol dan trigliserida Anda agar arteri tetap sehat.

6. **Stop Merokok**: Hindari kebiasaan merokok, karena merokok adalah faktor risiko utama penyakit jantung.

7. **Olahraga Rutin**: Lakukan olahraga selama sekitar 30 menit setiap hari untuk menjaga jantung dan tubuh Anda.

8. **Berat Badan Ideal**: Pertahankan berat badan yang sehat dengan gaya hidup aktif dan pola makan yang baik.

9. **Istirahat yang Cukup**: Tidur berkualitas membantu pemulihan jantung Anda.

10. **Kelola Stres**: Temukan cara untuk mengelola stres, karena stres dapat berdampak negatif pada kesehatan jantung.

11. **Pemeriksaan Kesehatan Rutin**: Lakukan pemeriksaan kesehatan secara teratur untuk mendeteksi risiko penyakit jantung sejak dini.
""")
        
    else:
        st.error("""
### Rekomendasi
                 
Jika Anda telah didiagnosis menderita penyakit jantung, berikut beberapa langkah yang dapat membantu Anda mengelola kondisi ini:

1. **Ikuti Saran Medis**: Patuhi semua petunjuk dan rekomendasi dari dokter Anda mengenai pengobatan dan gaya hidup yang sehat.

2. **Ubah Pola Makan**: Fokus pada makanan rendah lemak, tinggi serat, dan rendah garam untuk menjaga kesehatan jantung Anda.

3. **Atur Asupan Cairan**: Batasi konsumsi kafein dan alkohol, serta pastikan Anda minum cukup air putih.

4. **Rutin Berolahraga**: Konsultasikan dengan dokter Anda untuk rekomendasi jenis dan intensitas olahraga yang sesuai dengan kondisi jantung Anda.

5. **Mengelola Stres**: Temukan cara efektif untuk mengurangi stres, seperti meditasi, yoga, atau berbicara dengan seseorang yang Anda percayai.

6. **Rutin Cek Kesehatan**: Lakukan pemeriksaan kesehatan secara berkala untuk memantau perkembangan kondisi jantung Anda.

7. **Terhubung dengan Komunitas**: Bergabunglah dengan kelompok dukungan atau komunitas online yang sama-sama menghadapi penyakit jantung.
""")
        