VantageSoilApp – Full-Stack Soil Analysis System
VantageSoilApp is an end-to-end mobile and cloud solution designed for a Private Limited (Pvt Ltd) entity to identify soil types and provide real-time health metrics like moisture and pH levels. The system leverages Machine Learning to assist in agricultural decision-making and crop selection.

🚀 Technical Architecture
The project is built using a modern decoupled architecture to ensure scalability and reliability:

Android Frontend: Developed in Java/XML using Android Studio, targeting API 36 while maintaining backward compatibility for legacy devices (Min SDK 24).

Django Backend: A robust API hosted on Railway.com that handles authentication, data persistence, and ML model inference.

Machine Learning: Utilizes TensorFlow/Keras (h5) for image classification and Scikit-learn (joblib) for predictive pH and moisture analysis.

Cloud Storage: Integrated with Cloudinary API to manage and serve user-uploaded soil images globally.

Database: PostgreSQL (via Railway) for secure storage of user profiles and historical soil scan data.

✨ Key Features
Image-Based Identification: Users can capture or upload soil photos to identify types (Alluvial, Black, Clay, etc.) using a CNN model.

Predictive Analytics: Estimates soil pH and moisture content based on visual features.

Crop Recommendation: Provides a curated list of suitable crops based on the identified soil profile.

Scan History: Users can track their previous scans, complete with timestamps and GPS-simulated data.

Secure Authentication: Mobile-first login/signup system with profile management.

🛠️ Installation & Setup
Backend (Railway/Local)
Clone the repository and navigate to the backend/ directory.

Install dependencies: pip install -r requirements.txt.

Configure environment variables for Cloudinary and your Secret Key.

Run migrations: python manage.py migrate.

Android
Open the android/ folder in Android Studio.

Ensure the minSdk is set to 24 for older device support.

Build the signed APK using V1 and V2 signatures for maximum compatibility.

📈 Project Status
Backend: Live and deployed on Railway.

App Distribution: Currently in the Google Play Console Organizational Verification phase.

Verification: Registered under a verified D-U-N-S number for corporate compliance.

👥 Contributors
Tanish Goyal – Lead Developer (Android & Backend)
