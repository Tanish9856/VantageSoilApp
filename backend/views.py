import numpy as np
import joblib
from PIL import Image
from tensorflow.keras.models import load_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.conf import settings
from soil.models import SoilScan, UserProfile

# Load models
soil_model = load_model("model/soil_model.h5", compile=False)
ph_model = joblib.load("model/ph_model.pkl")
moisture_model = joblib.load("model/moisture_model.pkl")


def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def predict_soil(image_path):
    img = preprocess_image(image_path)
    prediction = soil_model.predict(img)
    classes = ['Alluvial soil', 'Black soil', 'Clay soil', 'Laterite soil', 'Red soil', 'Sandy soil', 'non_soil']
    soil_type = classes[np.argmax(prediction)]
    return soil_type


def predict_ph_moisture(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)
    r = np.mean(img_array[:, :, 0])
    g = np.mean(img_array[:, :, 1])
    b = np.mean(img_array[:, :, 2])
    brightness = np.mean(img_array)
    contrast = np.std(img_array)
    saturation = np.max(img_array) - np.min(img_array)
    features = [[r, g, b, brightness, contrast, saturation]]
    ph = ph_model.predict(features)[0]
    moisture = moisture_model.predict(features)[0]
    return round(float(ph), 2), round(float(moisture), 2)


def get_crop(soil_type):
    crop_map = {
        "Alluvial soil":  ["Rice", "Wheat", "Sugarcane", "Maize"],
        "Black soil":     ["Cotton", "Sorghum", "Soybean", "Sunflower"],
        "Clay soil":      ["Rice", "Lettuce", "Broccoli"],
        "Laterite soil":  ["Tea", "Coffee", "Cashew", "Rubber"],
        "Red soil":       ["Millet", "Peanut", "Tobacco", "Potato"],
        "Sandy soil":     ["Groundnut", "Melons", "Carrots", "Potatoes"],
        "non_soil":       ["Not suitable for farming"],
    }
    return crop_map.get(soil_type, ["Rice"])


# ─── AUTH VIEWS ───────────────────────────────────────────

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Find user by email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Incorrect password.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")

    return render(request, 'login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        city = request.POST.get("city")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html')

        # Create user
        username = email.split("@")[0]
        # Make username unique if needed
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
        )

        UserProfile.objects.create(
            user=user,
            mobile=mobile,
            city=city,
        )

        login(request, user)
        return redirect('/')

    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


# ─── MAIN VIEWS ───────────────────────────────────────────

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
def result(request):
    soil_type = None
    ph_value = None
    moisture = None
    crop = None
    image_name = None

    if image:
            # Save using Django storage (Cloudinary)
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import tempfile
            
            # Save to Cloudinary
            file_path = default_storage.save(f'soil_images/{image.name}', ContentFile(image.read()))
            cloudinary_url = default_storage.url(file_path)
            image_name = file_path
            
            # Save temp file locally for ML prediction
            image.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                for chunk in image.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            
            # Use temp file for prediction
            soil_type = predict_soil(tmp_path)
            ph_value, moisture = predict_ph_moisture(tmp_path)
            crop = get_crop(soil_type)
            
            # Clean up temp file
            os.unlink(tmp_path)

            SoilScan.objects.create(
                user=request.user,
                user_name=request.user.first_name or request.user.username,
                image=image.name,
                soil_type=soil_type,
                ph_value=ph_value,
                moisture=str(moisture),
                crop=", ".join(crop),
            )

    return render(request, "result.html", {
        "soil_type": soil_type,
        "ph_value": ph_value,
        "moisture": moisture,
        "crop": crop,
        "image": image_name,
    })


@login_required(login_url='/login/')
def scan_detail(request, id):
    scan = get_object_or_404(SoilScan, id=id, user=request.user)
    crop_list = [c.strip() for c in scan.crop.split(",")] if scan.crop else []
    return render(request, "scan_detail.html", {
        "scan": scan,
        "crop_list": crop_list,
    })


@login_required(login_url='/login/')
def history(request):
    scans = SoilScan.objects.filter(user=request.user, is_visible=True).order_by('-date')
    return render(request, "history.html", {"scans": scans})


@login_required(login_url='/login/')
def export_results(request):
    import csv
    from django.http import HttpResponse
    scans = SoilScan.objects.filter(user=request.user, is_visible=True).order_by('-date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="soil_results.csv"'
    writer = csv.writer(response)
    writer.writerow(['Soil Type', 'PH Value', 'Moisture', 'Crop', 'Date'])
    for scan in scans:
        writer.writerow([scan.soil_type, scan.ph_value, scan.moisture, scan.crop, scan.date])
    return response


def delete_all_results(request):
    SoilScan.objects.filter(user=request.user).update(is_visible=False)
    return redirect("/history/")


def delete_result(request, id):
    scan = get_object_or_404(SoilScan, id=id, user=request.user)
    scan.is_visible = False
    scan.save()
    return redirect("/history/")


@login_required(login_url='/login/')
def about(request):
    return render(request, 'about.html')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'forgot_password.html')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful! Please login.")
            return redirect('/login/')
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")

    return render(request, 'forgot_password.html')