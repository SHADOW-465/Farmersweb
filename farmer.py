import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
import json
from PIL import Image
import base64
import io
from datetime import datetime
import numpy as np

# ------------------ Page Config ------------------
st.set_page_config(layout="wide", page_title="FarmersHub", page_icon="🌾")

# ------------------ Language Dictionary ------------------
languages = {
    "English": {
        "title": "FarmersHub - AI-Powered Farming Assistant",
        "weather": "Local Weather Updates",
        "crop_advisor": "AI Crop Recommendations",
        "disease_detector": "AI Plant Disease Detection",
        "market_prices": "Current Market Prices",
        "marketplace": "Digital Marketplace",
        "schemes": "Government Scheme Updates",
        "select_language": "Select Language",
        "select_state": "Select State",
        "select_village": "Select Village/Town",
        "showing_data": "Showing data for",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "forecast": "Forecast",
        "village_input": "Village / Town",
        "soil_type": "Soil Type",
        "ph_level": "pH Level",
        "nitrogen": "Nitrogen (kg/ha)",
        "phosphorus": "Phosphorus (kg/ha)",
        "potassium": "Potassium (kg/ha)",
        "recommend": "Get AI Crop Recommendations",
        "recommended_crops": "AI Recommended Crops",
        "crop": "Crop",
        "price": "Price (₹/kg)",
        "product_name": "Product Name",
        "price_kg": "Price per kg",
        "quantity": "Quantity (kg)",
        "contact_info": "Contact Info",
        "post_listing": "Post Listing",
        "product_success": "Product listed successfully!",
        "scheme_1": "PM-KISAN: ₹6000 yearly income support to all farmers.",
        "scheme_2": "PMFBY: Crop insurance at low premium.",
        "scheme_3": "eNAM: Digital platform for buying and selling.",
        "scheme_4": "Soil Health Card: Free testing & crop advice.",
        "upload_image": "Upload Plant Image",
        "detect_disease": "Detect Disease",
        "disease_result": "Disease Detection Result",
        "confidence": "Confidence",
        "treatment": "Recommended Treatment",
        "rainfall": "Annual Rainfall (mm)",
        "season": "Planting Season",
        "kharif": "Kharif (Jun-Oct)",
        "rabi": "Rabi (Nov-Mar)",
        "zaid": "Zaid (Apr-May)",
        "analyzing": "🔍 Analyzing image...",
        "ai_processing": "🤖 AI is processing your request...",
    },
    "தமிழ்": {
        "title": "விவசாயி மையம் - AI உதவியாளர்",
        "weather": "மூல்நிலை வானிலை புதுப்பிப்புகள்",
        "crop_advisor": "AI பயிர் பரிந்துரைகள்",
        "disease_detector": "AI தாவர நோய் கண்டறிதல்",
        "market_prices": "தற்போதைய சந்தை விலைகள்",
        "marketplace": "டிஜிட்டல் சந்தை",
        "schemes": "அரசுத் திட்டங்கள்",
        "select_language": "மொழியை தேர்ந்தெடுங்கள்",
        "select_state": "மாநிலத்தை தேர்ந்தெடுக்கவும்",
        "select_village": "கிராமம் / நகரம் தேர்ந்தெடுக்கவும்",
        "showing_data": "தரவு காண்பிக்கப்படுகிறது:",
        "temperature": "வெப்பநிலை",
        "humidity": "ஈரப்பதம்",
        "forecast": "வானிலை கணிப்பு",
        "village_input": "கிராமம் / நகரம்",
        "soil_type": "மண் வகை",
        "ph_level": "pH நிலை",
        "nitrogen": "நைட்ரஜன் (kg/ha)",
        "phosphorus": "பாஸ்பரஸ் (kg/ha)",
        "potassium": "பொட்டாசியம் (kg/ha)",
        "recommend": "AI பயிர் பரிந்துரை பெறுங்கள்",
        "recommended_crops": "AI பரிந்துரைக்கப்பட்ட பயிர்கள்",
        "crop": "பயிர்",
        "price": "விலை (₹/kg)",
        "upload_image": "தாவர படத்தை பதிவேற்றவும்",
        "detect_disease": "நோயைக் கண்டறியவும்",
        "disease_result": "நோய் கண்டறிதல் முடிவு",
        "confidence": "நம்பகத்தன்மை",
        "treatment": "பரிந்துரைக்கப்பட்ட சிகிச்சை",
        "analyzing": "🔍 படத்தை பகுப்பாய்வு செய்கிறது...",
        "ai_processing": "🤖 AI உங்கள் கோரிக்கையை செயலாக்குகிறது...",
    },
    "हिन्दी": {
        "title": "किसान केंद्र - AI सहायक",
        "weather": "स्थानीय मौसम अपडेट",
        "crop_advisor": "AI फसल सिफारिशें",
        "disease_detector": "AI पौधा रोग पहचान",
        "market_prices": "वर्तमान बाजार मूल्य",
        "marketplace": "डिजिटल मार्केटप्लेस",
        "schemes": "सरकारी योजनाएं",
        "upload_image": "पौधे की तस्वीर अपलोड करें",
        "detect_disease": "बीमारी का पता लगाएं",
        "disease_result": "रोग पहचान परिणाम",
        "confidence": "विश्वसनीयता",
        "treatment": "अनुशंसित उपचार",
        "analyzing": "🔍 छवि का विश्लेषण कर रहा है...",
        "ai_processing": "🤖 AI आपके अनुरोध को संसाधित कर रहा है...",
    }
}

# ------------------ AI Configuration ------------------
# Hugging Face API Configuration
# Load model directly
# from transformers import AutoImageProcessor, AutoModelForImageClassification

# processor = AutoImageProcessor.from_pretrained("linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification")
# model = AutoModelForImageClassification.from_pretrained("linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification")

HF_API_KEY = "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"  # Replace with your Hugging Face API key
HF_API_URL_DISEASE = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
# Disease treatment database
DISEASE_TREATMENTS = {
    "angular_leaf_spot": {
        "treatment": "Apply copper-based fungicide. Ensure proper spacing between plants for air circulation. Remove infected leaves immediately.",
        "prevention": "Use certified disease-free seeds. Practice crop rotation. Avoid overhead watering."
    },
    "bean_rust": {
        "treatment": "Apply sulfur-based fungicide. Remove infected plant parts. Improve air circulation around plants.",
        "prevention": "Plant resistant varieties. Avoid working with wet plants. Ensure good drainage."
    },
    "healthy": {
        "treatment": "Your plant looks healthy! Continue current care practices.",
        "prevention": "Maintain proper watering, fertilization, and pest monitoring to keep plants healthy."
    },
    "default": {
        "treatment": "Consult with local agricultural extension officer. Apply general plant care practices.",
        "prevention": "Regular monitoring, proper nutrition, and timely pest management."
    }
}

# Kerala-specific crop data for AI recommendations
KERALA_CROPS_DATA = {
    'Rice': {'ph_min': 5.0, 'ph_max': 6.5, 'rainfall_min': 1000, 'rainfall_max': 2000, 'temp_opt': 26},
    'Coconut': {'ph_min': 5.2, 'ph_max': 8.0, 'rainfall_min': 1300, 'rainfall_max': 2300, 'temp_opt': 28},
    'Pepper': {'ph_min': 5.5, 'ph_max': 7.0, 'rainfall_min': 1250, 'rainfall_max': 2000, 'temp_opt': 25},
    'Cardamom': {'ph_min': 5.0, 'ph_max': 6.5, 'rainfall_min': 1500, 'rainfall_max': 4000, 'temp_opt': 23},
    'Rubber': {'ph_min': 5.0, 'ph_max': 6.5, 'rainfall_min': 1500, 'rainfall_max': 2500, 'temp_opt': 27},
    'Tea': {'ph_min': 4.5, 'ph_max': 6.0, 'rainfall_min': 1200, 'rainfall_max': 2500, 'temp_opt': 22},
    'Coffee': {'ph_min': 6.0, 'ph_max': 7.0, 'rainfall_min': 1500, 'rainfall_max': 2000, 'temp_opt': 24},
    'Banana': {'ph_min': 5.5, 'ph_max': 7.0, 'rainfall_min': 1200, 'rainfall_max': 1800, 'temp_opt': 27},
    'Ginger': {'ph_min': 5.5, 'ph_max': 6.5, 'rainfall_min': 1500, 'rainfall_max': 3000, 'temp_opt': 25},
    'Turmeric': {'ph_min': 5.0, 'ph_max': 7.5, 'rainfall_min': 1000, 'rainfall_max': 1500, 'temp_opt': 26}
}

# ------------------ AI Functions ------------------
@st.cache_data(ttl=300)  # Cache for 5 minutes
def detect_plant_disease(image_bytes):
    """
    Detect plant disease using Hugging Face API
    """
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    try:
        # Convert image to base64
        img_b64 = base64.b64encode(image_bytes).decode()
        
        response = requests.post(
            HF_API_URL_DISEASE,
            headers=headers,
            json={"inputs": img_b64}
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                # Get the top prediction
                top_prediction = result[0]
                disease_name = top_prediction.get('label', 'unknown').lower().replace(' ', '_')
                confidence = top_prediction.get('score', 0) * 100
                
                # Get treatment information
                treatment_info = DISEASE_TREATMENTS.get(disease_name, DISEASE_TREATMENTS['default'])
                
                return {
                    'disease': disease_name.replace('_', ' ').title(),
                    'confidence': round(confidence, 2),
                    'treatment': treatment_info['treatment'],
                    'prevention': treatment_info['prevention'],
                    'success': True
                }
        
        return {'success': False, 'error': 'API request failed'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def ai_crop_recommender(ph, nitrogen, phosphorus, potassium, rainfall, temperature, season):
    """
    AI-powered crop recommendation system for Kerala
    """
    try:
        recommendations = []
        
        # Get current weather data for temperature if not provided
        if temperature is None:
            temperature = 26  # Default Kerala temperature
        
        for crop, requirements in KERALA_CROPS_DATA.items():
            # Calculate suitability score based on multiple factors
            ph_score = 1 - abs(ph - ((requirements['ph_min'] + requirements['ph_max']) / 2)) / 2
            ph_score = max(0, ph_score)
            
            rainfall_score = 1 if requirements['rainfall_min'] <= rainfall <= requirements['rainfall_max'] else 0.5
            
            temp_score = 1 - abs(temperature - requirements['temp_opt']) / 10
            temp_score = max(0, temp_score)
            
            # Simple nutrient scoring (basic logic)
            nutrient_score = min(1, (nitrogen + phosphorus + potassium) / 300)
            
            # Calculate overall score
            overall_score = (ph_score * 0.3 + rainfall_score * 0.3 + temp_score * 0.2 + nutrient_score * 0.2)
            
            if overall_score > 0.5:  # Only recommend if score is above threshold
                recommendations.append({
                    'crop': crop,
                    'score': round(overall_score * 100, 1),
                    'suitability': 'High' if overall_score > 0.8 else 'Medium' if overall_score > 0.6 else 'Low'
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
        
    except Exception as e:
        st.error(f"Error in crop recommendation: {str(e)}")
        return []

# ------------------ Top Bar ------------------
col1, col2 = st.columns([10, 1])
with col2:
    lang_choice = st.selectbox("🌐", list(languages.keys()), label_visibility="collapsed")
L = languages[lang_choice]

# ------------------ Header ------------------
st.markdown(f"<h1 style='text-align: center; color: #2E8B57;'>{L['title']}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>🤖 Powered by Artificial Intelligence</p>", unsafe_allow_html=True)

# ------------------ Static Data ------------------
try:
    df = pd.read_csv('states_and_districts.csv')
    states_villages = {state: df[df['State'] == state]['District'].tolist() for state in df['State'].unique()}
except:
    # Fallback data for Kerala
    states_villages = {
        'Kerala': ['Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 'Kottayam', 
                  'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad', 'Malappuram', 'Kozhikode', 
                  'Wayanad', 'Kannur', 'Kasaragod']
    }

# ------------------ Menu ------------------
selected_tab = option_menu(
    menu_title=None,
    options=[L["weather"], L["disease_detector"], L["crop_advisor"], L["market_prices"], L["marketplace"], L["schemes"]],
    icons=["cloud-sun", "bug", "seedling", "graph-up", "shop", "file-text"],
    orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#2E8B57", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#eee", "color": "#222"},
            "nav-link-selected": {"background-color": "#2E8B57", "color": "#fff"},
        }
)

# ------------------ State/Village ------------------
col1, col2 = st.columns(2)
with col1:
    state = st.selectbox(L["select_state"], list(states_villages.keys()))
with col2:
    village = st.selectbox(L["select_village"], states_villages[state])

# ------------------ WEATHER ------------------
def get_weather_from_api(village, state):
    api_key = "e82ac14a7e3449f283b9622c41e505f6"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    complete_url = f"{base_url}q={village},{state}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(complete_url, timeout=10)
        data = response.json()
        
        if data["cod"] != "404":
            main_data = data["main"]
            temperature = main_data["temp"]
            humidity = main_data["humidity"]
            weather_data = data["weather"][0]
            forecast = weather_data["description"]
            return temperature, humidity, forecast
        else:
            return None, None, None
    except:
        return None, None, None

if selected_tab == L["weather"]:
    st.subheader(f"☁ {L['weather']}")
    st.success(f"{L['showing_data']} {village}, {state}")

    temp, humidity, forecast = get_weather_from_api(village, state)
    
    if temp and humidity and forecast:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=L["temperature"], value=f"{temp}°C")
        with col2:
            st.metric(label=L["humidity"], value=f"{humidity}%")
        with col3:
            st.metric(label=L["forecast"], value=forecast.capitalize())
    else:
        st.error("Unable to fetch weather data")

# ------------------ AI PLANT DISEASE DETECTION ------------------
elif selected_tab == L["disease_detector"]:
    st.subheader(f"🔬 {L['disease_detector']}")
    st.markdown("Upload a clear image of your plant leaves to detect diseases using AI")
    
    uploaded_file = st.file_uploader(
        L["upload_image"], 
        type=['png', 'jpg', 'jpeg'],
        help="Take a clear photo of the affected plant leaves in good lighting"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 2])
        
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            if st.button(L["detect_disease"], type="primary", use_container_width=True):
                with st.spinner(L["analyzing"]):
                    # Convert image to bytes
                    img_bytes = uploaded_file.getvalue()
                    
                    # Get disease prediction
                    result = detect_plant_disease(img_bytes)
                    
                    if result['success']:
                        st.success(f"✅ {L['disease_result']}")
                        
                        # Display results
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("🦠 Disease", result['disease'])
                            st.metric(f"🎯 {L['confidence']}", f"{result['confidence']}%")
                        
                        with col_b:
                            # Confidence indicator
                            if result['confidence'] > 80:
                                st.success("High Confidence")
                            elif result['confidence'] > 60:
                                st.warning("Medium Confidence")
                            else:
                                st.info("Low Confidence - Consider consulting an expert")
                        
                        # Treatment recommendations
                        st.subheader(f"💊 {L['treatment']}")
                        st.write(result['treatment'])
                        
                        st.subheader("🛡 Prevention Tips")
                        st.write(result['prevention'])
                        
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error occurred')}")
                        st.info("Please try with a clearer image or contact our support.")

# ------------------ AI CROP ADVISOR ------------------
elif selected_tab == L["crop_advisor"]:
    st.subheader(f"🤖 {L['crop_advisor']}")
    st.markdown("Get AI-powered crop recommendations based on your soil and climate conditions")
    
    with st.form("ai_crop_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input(L["village_input"], value=village, disabled=True)
            soil_type = st.selectbox(L["soil_type"], ["Laterite", "Alluvial", "Black", "Red", "Coastal Sandy"])
            ph_level = st.number_input(L["ph_level"], min_value=3.0, max_value=9.0, value=6.0, step=0.1)
            nitrogen = st.number_input(L["nitrogen"], min_value=0, max_value=300, value=50)
        
        with col2:
            rainfall = st.number_input(L.get("rainfall", "Annual Rainfall (mm)"), min_value=500, max_value=4000, value=1500)
            season = st.selectbox(L.get("season", "Planting Season"), 
                                [L.get("kharif", "Kharif (Jun-Oct)"), 
                                 L.get("rabi", "Rabi (Nov-Mar)"), 
                                 L.get("zaid", "Zaid (Apr-May)")])
            phosphorus = st.number_input(L["phosphorus"], min_value=0, max_value=200, value=30)
            potassium = st.number_input(L["potassium"], min_value=0, max_value=200, value=40)

        if st.form_submit_button(L["recommend"], type="primary", use_container_width=True):
            with st.spinner(L.get("ai_processing", "🤖 AI is processing your request...")):
                # Get weather data for temperature
                temp, _, _ = get_weather_from_api(village, state)
                
                # Get AI recommendations
                recommendations = ai_crop_recommender(ph_level, nitrogen, phosphorus, potassium, rainfall, temp, season)
                
                if recommendations:
                    st.success(f"🎯 {L['recommended_crops']}")
                    
                    # Display recommendations in a nice format
                    for i, rec in enumerate(recommendations):
                        with st.container():
                            col_a, col_b, col_c = st.columns([2, 1, 1])
                            with col_a:
                                st.write(f"{i+1}. {rec['crop']}")
                            with col_b:
                                st.metric("Score", f"{rec['score']}%")
                            with col_c:
                                if rec['suitability'] == 'High':
                                    st.success(rec['suitability'])
                                elif rec['suitability'] == 'Medium':
                                    st.warning(rec['suitability'])
                                else:
                                    st.info(rec['suitability'])
                    
                    # Additional insights
                    st.info(f"💡 *Insight*: Based on your soil pH of {ph_level} and rainfall of {rainfall}mm, these crops are most suitable for your farm in {village}.")
                
                else:
                    st.warning("⚠ Unable to generate recommendations. Please check your input values.")

# ------------------ MARKET PRICES ------------------
elif selected_tab == L["market_prices"]:
    st.subheader(f"💹 {L['market_prices']}")
    
    # Sample Kerala-specific market data
    market_data = {
        L["crop"]: ["Rice", "Coconut", "Pepper", "Cardamom", "Rubber", "Banana", "Ginger"],
        L["price"]: ["₹28-32", "₹15-20", "₹450-500", "₹1200-1400", "₹140-160", "₹25-30", "₹80-100"]
    }
    
    st.table(pd.DataFrame(market_data))
    st.caption(f"Prices for {village} market - Updated: {datetime.now().strftime('%d-%m-%Y')}")

# ------------------ MARKETPLACE ------------------
elif selected_tab == L["marketplace"]:
    st.subheader(f"🛒 {L['marketplace']}")
    
    with st.form("market_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input(L["product_name"])
            price_kg = st.text_input(L["price_kg"])
        with col2:
            quantity = st.text_input(L["quantity"])
            contact_info = st.text_input(L["contact_info"])

        if st.form_submit_button(L["post_listing"], type="primary", use_container_width=True):
            if product_name and price_kg and quantity and contact_info:
                st.success(f"✅ {L['product_success']}")
                
                # Display posted listing
                with st.container():
                    st.write("*Your Listing:*")
                    st.write(f"📦 Product: {product_name}")
                    st.write(f"💰 Price: {price_kg} ₹/kg")
                    st.write(f"⚖ Quantity: {quantity} kg")
                    st.write(f"📞 Contact: {contact_info}")
            else:
                st.error("Please fill in all fields")

# ------------------ GOVERNMENT SCHEMES ------------------
elif selected_tab == L["schemes"]:
    st.subheader(f"📜 {L['schemes']}")
    
    schemes = [
        ("🌾", L['scheme_1']),
        ("🛡", L['scheme_2']),
        ("💻", L['scheme_3']),
        ("🧪", L['scheme_4'])
    ]
    
    for icon, scheme in schemes:
        st.info(f"{icon} {scheme}")

# ------------------ Footer ------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🌾 FarmersHub AI Assistant | Empowering Kerala Farmers with Technology</p>
        <p>Built by POWERHOUSE⚡ for SIH 2025 | AI-Powered Personal Farming Assistant</p>
    </div>
    """, 
    unsafe_allow_html=True
)
