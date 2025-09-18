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
import re

# ------------------ Page Config ------------------
st.set_page_config(layout="wide", page_title="FarmersHub", page_icon="🌾")

# ------------------ Language Dictionary ------------------
languages = {
    "Malayalam": {
        "title": "കർഷകഹബ് - AI അധിഷ്ഠിത കർഷക സഹായി",
        "profile": "എന്റെ ഫാം പ്രൊഫൈൽ",
        "farmer_name": "കർഷകന്റെ പേര്",
        "save_profile": "പ്രൊഫൈൽ സംരക്ഷിക്കുക",
        "profile_saved": "പ്രൊഫൈൽ വിജയകരമായി സംരക്ഷിച്ചു!",
        "chatbot": "AI ചാറ്റ്ബോട്ട്",
        "chat_placeholder": "എന്തെങ്കിലും ചോദിക്കൂ...",
        "chat_welcome": "ഹലോ! ഞാൻ നിങ്ങളുടെ AI സഹായിയാണ്. വിളകൾ, രോഗങ്ങൾ, കാലാവസ്ഥ എന്നിവയെക്കുറിച്ച് ചോദിക്കുക.",
        "chat_fallback": "ക്ഷമിക്കണം, എനിക്ക് മനസ്സിലായില്ല. വിളകളെക്കുറിച്ചോ രോഗങ്ങളെക്കുറിച്ചോ കാലാവസ്ഥയെക്കുറിച്ചോ ചോദിക്കുക.",
        "chat_weather": "'പ്രാദേശിക കാലാവസ്ഥ അപ്‌ഡേറ്റുകൾ' ടാബിൽ നിങ്ങൾക്ക് കാലാവസ്ഥ പരിശോധിക്കാം.",
        "weather": "പ്രാദേശിക കാലാവസ്ഥ അപ്‌ഡേറ്റുകൾ",
        "crop_advisor": "AI വിള നിർദ്ദേശങ്ങൾ",
        "disease_detector": "AI ചെടി രോഗം കണ്ടെത്തൽ",
        "market_prices": "നിലവിലെ മാർക്കറ്റ് വിലകൾ",
        "marketplace": "ഡിജിറ്റൽ മാർക്കറ്റ്‌പ്ലേസ്",
        "schemes": "സർക്കാർ പദ്ധതികൾ",
        "select_language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "select_state": "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക",
        "select_village": "ഗ്രാമം/നഗരം തിരഞ്ഞെടുക്കുക",
        "showing_data": "ഡാറ്റ കാണിക്കുന്നു:",
        "temperature": "താപനില",
        "humidity": "ആർദ്രത",
        "forecast": "കാലാവസ്ഥ പ്രവചനം",
        "village_input": "ഗ്രാമം / നഗരം",
        "soil_type": "മണ്ണിന്റെ തരം",
        "ph_level": "pH നില",
        "nitrogen": "നൈട്രജൻ (kg/ha)",
        "phosphorus": "ഫോസ്ഫറസ് (kg/ha)",
        "potassium": "പൊട്ടാസ്യം (kg/ha)",
        "recommend": "AI വിള നിർദ്ദേശങ്ങൾ നേടുക",
        "recommended_crops": "AI നിർദ്ദേശിച്ച വിളകൾ",
        "crop": "വിള",
        "price": "വില (₹/kg)",
        "product_name": "ഉൽപ്പന്നത്തിന്റെ പേര്",
        "price_kg": "കിലോയ്ക്ക് വില",
        "quantity": "അളവ് (kg)",
        "contact_info": "ബന്ധപ്പെടാനുള്ള വിവരങ്ങൾ",
        "post_listing": "ലിസ്റ്റ് പോസ്റ്റ് ചെയ്യുക",
        "product_success": "ഉൽപ്പന്നം വിജയകരമായി ലിസ്റ്റ് ചെയ്തു!",
        "scheme_1": "PM-KISAN: എല്ലാ കർഷകർക്കും വാർഷികം ₹6000 സഹായം.",
        "scheme_2": "PMFBY: കുറഞ്ഞ പ്രീമിയത്തിൽ വിള ഇൻഷുറൻസ്.",
        "scheme_3": "eNAM: വാങ്ങാനും വിൽക്കാനും ഡിജിറ്റൽ പ്ലാറ്റ്ഫോം.",
        "scheme_4": "മണ്ണ് ആരോഗ്യ കാർഡ്: സൗജന്യ പരിശോധനയും വിള നിർദ്ദേശവും.",
        "upload_image": "ചെടിയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "detect_disease": "രോഗം കണ്ടെത്തുക",
        "disease_result": "രോഗം കണ്ടെത്തൽ ഫലം",
        "confidence": "വിശ്വാസ്യത",
        "treatment": "നിർദ്ദേശിച്ച ചികിത്സ",
        "rainfall": "വാർഷിക മഴ (mm)",
        "season": "വിതയ്ക്കുന്ന സീസൺ",
        "kharif": "ഖരീഫ് (ജൂൺ-ഒക്ടോബർ)",
        "rabi": "റബി (നവംബർ-മാർച്ച്)",
        "zaid": "സൈഡ് (ഏപ്രിൽ-മെയ്)",
        "analyzing": "🔍 ചിത്രം വിശകലനം ചെയ്യുന്നു...",
        "ai_processing": "🤖 AI നിങ്ങളുടെ അഭ്യർത്ഥന പ്രോസസ്സ് ചെയ്യുന്നു...",
    },
    "English": {
        "title": "FarmersHub - AI-Powered Farming Assistant",
        "profile": "My Farm Profile",
        "farmer_name": "Farmer Name",
        "save_profile": "Save Profile",
        "profile_saved": "Profile saved successfully!",
        "chatbot": "AI Chatbot",
        "chat_placeholder": "Ask me anything...",
        "chat_welcome": "Hello! I'm your AI assistant. Ask me about crops, diseases, or weather.",
        "chat_fallback": "I'm sorry, I don't understand. Try asking about a specific crop, disease, or the weather.",
        "chat_weather": "You can check the current weather in the 'Local Weather Updates' tab.",
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
        "profile": "எனது பண்ணை சுயவிவரம்",
        "farmer_name": "விவசாயி பெயர்",
        "save_profile": "சுயவிவரத்தை சேமிக்கவும்",
        "profile_saved": "சுயவிவரம் வெற்றிகரமாக சேமிக்கப்பட்டது!",
        "chatbot": "AI చాట్‌బాట్",
        "chat_placeholder": "என்னிடம் எதையும் கேளுங்கள்...",
        "chat_welcome": "வணக்கம்! நான் உங்கள் AI உதவியாளர். பயிர்கள், நோய்கள் அல்லது வானிலை பற்றி என்னிடம் கேளுங்கள்.",
        "chat_fallback": "மன்னிக்கவும், எனக்குப் புரியவில்லை. ஒரு குறிப்பிட்ட பயிர், நோய் அல்லது வானிலை பற்றி கேட்க முயற்சிக்கவும்.",
        "chat_weather": "'உள்ளூர் வானிலை அறிவிப்புகள்' தாவலில் தற்போதைய வானிலையை நீங்கள் பார்க்கலாம்.",
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
        "product_name": "பொருள் பெயர்",
        "price_kg": "கிலோவிற்கு விலை",
        "quantity": "அளவு (kg)",
        "contact_info": "தொடர்பு தகவல்",
        "post_listing": "பதிவிடவும்",
        "product_success": "பொருள் வெற்றிகரமாக பதிவிடப்பட்டது!",
        "scheme_1": "PM-KISAN: ஆண்டுக்கு ₹6000 ஆதரவு அனைத்து விவசாயிகளுக்கும்.",
        "scheme_2": "PMFBY: குறைந்த கட்டணத்தில் பயிர் காப்பீடு.",
        "scheme_3": "eNAM: வாங்கும் மற்றும் விற்கும் டிஜிட்டல் தளம்.",
        "scheme_4": "மண் ஆரோக்கிய அட்டை: இலவச பரிசோதனை மற்றும் பயிர் ஆலோசனை.",
        "upload_image": "தாவர படத்தை பதிவேற்றவும்",
        "detect_disease": "நோயைக் கண்டறியவும்",
        "disease_result": "நோய் கண்டறிதல் முடிவு",
        "confidence": "நம்பகத்தன்மை",
        "treatment": "பரிந்துரைக்கப்பட்ட சிகிச்சை",
        "rainfall": "வருடாந்திர மழை (மிமீ)",
        "season": "விதை நடும் பருவம்",
        "kharif": "கரீப் (ஜூன்-அக்டோபர்)",
        "rabi": "ரபி (நவம்பர்-மார்ச்)",
        "zaid": "சைட் (ஏப்ரல்-மே)",
        "analyzing": "🔍 படத்தை பகுப்பாய்வு செய்கிறது...",
        "ai_processing": "🤖 AI உங்கள் கோரிக்கையை செயலாக்குகிறது...",
    },
    "हिन्दी": {
        "title": "किसान केंद्र - AI सहायक",
        "profile": "मेरी फार्म प्रोफाइल",
        "farmer_name": "किसान का नाम",
        "save_profile": "प्रोफ़ाइल सहेजें",
        "profile_saved": "प्रोफ़ाइल सफलतापूर्वक सहेजी गई!",
        "chatbot": "एआई चैटबॉट",
        "chat_placeholder": "मुझसे कुछ भी पूछें...",
        "chat_welcome": "नमस्ते! मैं आपका AI सहायक हूँ। मुझसे फसलों, बीमारियों या मौसम के बारे में पूछें।",
        "chat_fallback": "मुझे खेद है, मैं समझ नहीं पा रहा हूँ। किसी विशिष्ट फसल, बीमारी या मौसम के बारे में पूछने का प्रयास करें।",
        "chat_weather": "आप 'स्थानीय मौसम अपडेट' टैब में वर्तमान मौसम की जांच कर सकते हैं।",
        "weather": "स्थानीय मौसम अपडेट",
        "crop_advisor": "AI फसल सिफारिशें",
        "disease_detector": "AI पौधा रोग पहचान",
        "market_prices": "वर्तमान बाजार मूल्य",
        "marketplace": "डिजिटल मार्केटप्लेस",
        "schemes": "सरकारी योजनाएं",
        "select_state": "राज्य चुनें",
        "select_village": "गांव / शहर चुनें",
        "showing_data": "डेटा दिखाया जा रहा है:",
        "temperature": "तापमान",
        "humidity": "नमी",
        "forecast": "पूर्वानुमान",
        "village_input": "गांव / शहर",
        "soil_type": "मिट्टी का प्रकार",
        "ph_level": "pH स्तर",
        "nitrogen": "नाइट्रोजन (kg/ha)",
        "phosphorus": "फॉस्फोरस (kg/ha)",
        "potassium": "पोटेशियम (kg/ha)",
        "recommend": "AI फसल सिफारिश प्राप्त करें",
        "recommended_crops": "AI अनुशंसित फसलें",
        "crop": "फसल",
        "price": "मूल्य (₹/kg)",
        "product_name": "उत्पाद का नाम",
        "price_kg": "किलोग्राम के लिए मूल्य",
        "quantity": "मात्रा (किलोग्राम)",
        "contact_info": "संपर्क जानकारी",
        "post_listing": "लिस्टिंग पोस्ट करें",
        "product_success": "उत्पाद सफलतापूर्वक सूचीबद्ध किया गया!",
        "scheme_1": "PM-KISAN: सभी किसानों को सालाना ₹6000 की सहायता।",
        "scheme_2": "PMFBY: कम प्रीमियम पर फसल बीमा।",
        "scheme_3": "eNAM: खरीद और बिक्री के लिए डिजिटल प्लेटफार्म।",
        "scheme_4": "मृदा स्वास्थ्य कार्ड: मुफ्त परीक्षण और फसल सलाह।",
        "upload_image": "पौधे की तस्वीर अपलोड करें",
        "detect_disease": "बीमारी का पता लगाएं",
        "disease_result": "रोग पहचान परिणाम",
        "confidence": "विश्वसनीयता",
        "treatment": "अनुशंसित उपचार",
        "rainfall": "वार्षिक वर्षा (मिमी)",
        "season": "बुवाई का मौसम",
        "kharif": "खरीफ (जून-अक्टूबर)",
        "rabi": "रबी (नवंबर-मार्च)",
        "zaid": "जायद (अप्रैल-मई)",
        "analyzing": "🔍 छवि का विश्लेषण कर रहा है...",
        "ai_processing": "🤖 AI आपके अनुरोध को संसाधित कर रहा है...",
    }
}

# ------------------ Session State Initialization ------------------
if 'profile' not in st.session_state:
    st.session_state.profile = {"name": "", "state": "Kerala", "village": "Thiruvananthapuram", "soil_type": "Laterite"}
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ AI Configuration ------------------
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Hugging Face API key not found. Please add it to your Streamlit secrets.")
    HF_API_KEY = ""

HF_API_URL_DISEASE = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
DISEASE_TREATMENTS = {
    "angular_leaf_spot": {"treatment": "Apply copper-based fungicide. Ensure proper spacing between plants for air circulation. Remove infected leaves immediately.", "prevention": "Use certified disease-free seeds. Practice crop rotation. Avoid overhead watering."},
    "bean_rust": {"treatment": "Apply sulfur-based fungicide. Remove infected plant parts. Improve air circulation around plants.", "prevention": "Plant resistant varieties. Avoid working with wet plants. Ensure good drainage."},
    "rice_leaf_blast": {"treatment": "Apply fungicides like Tricyclazole or Iprobenfos. Ensure balanced use of nitrogen fertilizers.", "prevention": "Use resistant varieties of rice. Maintain proper water levels in the field and avoid water stress."},
    "coconut_bud_rot": {"treatment": "Remove and burn the infected palm to prevent spread. Apply Bordeaux mixture paste on the crown of surrounding healthy palms.", "prevention": "Ensure good drainage in the garden. Prophylactic spraying with fungicides before the monsoon season can be effective."},
    "healthy": {"treatment": "Your plant looks healthy!", "prevention": "Continue current care practices."},
    "default": {"treatment": "Could not identify the disease with high confidence. Consult with a local agricultural extension officer for an accurate diagnosis.", "prevention": "Regular monitoring, proper nutrition, and timely pest management are key to preventing most diseases."}
}
CROP_INFO = {
    "rice": {"info": "Rice is a staple food for a large part of the world's human population.", "care": "Rice requires significant water. Fields are often flooded. It needs nitrogen-rich fertilizers."},
    "coconut": {"info": "The coconut tree is a member of the palm tree family.", "care": "Coconut palms thrive in sandy soils and require high humidity and regular rainfall."},
    "pepper": {"info": "Black pepper is a flowering vine cultivated for its fruit.", "care": "Pepper needs a support to climb, well-drained soil, and a warm, humid climate."},
}

# ------------------ AI Functions ------------------
import pickle

@st.cache_resource
def load_crop_model():
    try:
        with open('crop_model.pkl', 'rb') as f: return pickle.load(f)
    except FileNotFoundError:
        st.error("Crop model not found.")
        return None

@st.cache_data(ttl=300)
def detect_plant_disease(image_bytes):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    try:
        img_b64 = base64.b64encode(image_bytes).decode()
        response = requests.post(HF_API_URL_DISEASE, headers=headers, json={"inputs": img_b64})
        if response.status_code == 200:
            result = response.json()[0]
            disease_name = result.get('label', 'unknown').lower().replace(' ', '_')
            confidence = result.get('score', 0) * 100
            treatment_info = DISEASE_TREATMENTS.get(disease_name, DISEASE_TREATMENTS['default'])
            return {'disease': disease_name.replace('_', ' ').title(), 'confidence': round(confidence, 2), 'treatment': treatment_info['treatment'], 'prevention': treatment_info['prevention'], 'success': True}
        return {'success': False, 'error': f"API request failed with status code {response.status_code}. Response: {response.text}"}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def ai_crop_recommender(ph, nitrogen, phosphorus, potassium, rainfall, temperature, season, soil_type):
    try:
        model = load_crop_model()
        if model is None: return []
        if temperature is None: temperature = 26
        season_clean = season.split(" ")[0]
        input_data = pd.DataFrame({'temperature': [temperature], 'rainfall': [rainfall], 'ph': [ph], 'nitrogen': [nitrogen], 'phosphorus': [phosphorus], 'potassium': [potassium], 'soil_type': [soil_type], 'season': [season_clean]})
        probabilities = model.predict_proba(input_data)[0]
        recommendations = [{'crop': model.named_steps['classifier'].classes_[i], 'score': round(prob * 100, 1), 'suitability': 'High' if prob > 0.2 else ('Medium' if prob > 0.05 else 'Low')} for i, prob in enumerate(probabilities)]
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return [rec for rec in recommendations if rec['score'] > 1][:5]
    except Exception as e:
        st.error(f"Error in crop recommendation: {str(e)}")
        return []

def get_chatbot_response(query: str, lang_dict: dict):
    query = query.lower().strip()
    if any(greet in query for greet in ["hello", "hi", "hey"]): return lang_dict.get("chat_welcome")
    if re.search(r'\bweather\b', query): return lang_dict.get("chat_weather")
    for crop, data in CROP_INFO.items():
        if re.search(rf'\b{crop}\b', query):
            if re.search(r'\b(care|grow|cultivate)\b', query): return data["care"]
            return data["info"]
    for disease in DISEASE_TREATMENTS:
        if disease.replace('_', ' ') in query: return f"**Treatment for {disease.replace('_', ' ').title()}:** {DISEASE_TREATMENTS[disease]['treatment']}"
    return lang_dict.get("chat_fallback")

def get_weather_from_api(village, state):
    api_key = "e82ac14a7e3449f283b9622c41e505f6"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={village},{state}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url, timeout=10)
        data = response.json()
        if data["cod"] != "404": return data["main"]["temp"], data["main"]["humidity"], data["weather"][0]["description"]
        else: return None, None, None
    except: return None, None, None

# ------------------ UI Layout ------------------
col1, col2 = st.columns([10, 1])
with col2:
    lang_choice = st.selectbox("🌐", list(languages.keys()), label_visibility="collapsed")
L = languages[lang_choice]
st.markdown(f"<h1 style='text-align: center; color: #2E8B57;'>{L['title']}</h1>", unsafe_allow_html=True)

try:
    df_states = pd.read_csv('states_and_districts.csv')
    states_villages = {state: df_states[df_states['State'] == state]['District'].tolist() for state in df_states['State'].unique()}
except:
    states_villages = {'Kerala': ['Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 'Kottayam', 'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad', 'Malappuram', 'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod']}

menu_keys = ["profile", "chatbot", "weather", "disease_detector", "crop_advisor", "market_prices", "marketplace", "schemes"]
menu_options = [L.get(key, key.title()) for key in menu_keys]
menu_icons = ["person-badge", "chat-dots", "cloud-sun", "bug", "seedling", "graph-up", "shop", "file-text"]
selected_tab = option_menu(
    menu_title=None, options=menu_options, icons=menu_icons, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#2E8B57"}}
)

state = st.session_state.profile['state']
village = st.session_state.profile['village']

# Map selected tab back to key for logic
selected_key = menu_keys[menu_options.index(selected_tab)]

if selected_key == "profile":
    st.subheader(f"👤 {L.get('profile')}")
    with st.form("profile_form"):
        name = st.text_input(L.get("farmer_name"), value=st.session_state.profile.get("name", ""))
        try: state_index = list(states_villages.keys()).index(st.session_state.profile.get("state", "Kerala"))
        except ValueError: state_index = 0
        new_state = st.selectbox(L["select_state"], list(states_villages.keys()), index=state_index)
        try:
            if new_state in states_villages and states_villages[new_state]: village_index = states_villages[new_state].index(st.session_state.profile.get("village", "Thiruvananthapuram"))
            else: village_index = 0
        except ValueError: village_index = 0
        new_village = st.selectbox(L["select_village"], states_villages.get(new_state, []), index=village_index)
        soil_types = ["Laterite", "Alluvial", "Black", "Red", "Coastal Sandy"]
        try: soil_index = soil_types.index(st.session_state.profile.get("soil_type", "Laterite"))
        except ValueError: soil_index = 0
        new_soil_type = st.selectbox(L["soil_type"], soil_types, index=soil_index)
        if st.form_submit_button(L.get("save_profile"), type="primary", use_container_width=True):
            st.session_state.profile = {"name": name, "state": new_state, "village": new_village, "soil_type": new_soil_type}
            st.success(L.get("profile_saved"))
            st.rerun()
    st.info(f"**Current Profile:** Name: `{st.session_state.profile['name']}` | Location: `{st.session_state.profile['village']}, {st.session_state.profile['state']}` | Soil: `{st.session_state.profile['soil_type']}`")

elif selected_key == "chatbot":
    st.subheader(f"🤖 {L.get('chatbot')}")
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": L.get("chat_welcome")})
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input(L.get("chat_placeholder")):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = get_chatbot_response(prompt, L)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

elif selected_key == "weather":
    st.subheader(f"☁ {L['weather']}")
    st.success(f"{L['showing_data']} {village}, {state}")
    temp, humidity, forecast = get_weather_from_api(village, state)
    if temp and humidity and forecast:
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(label=L["temperature"], value=f"{temp}°C")
        with col2: st.metric(label=L["humidity"], value=f"{humidity}%")
        with col3: st.metric(label=L["forecast"], value=forecast.capitalize())
    else: st.error("Unable to fetch weather data")

elif selected_key == "disease_detector":
    st.subheader(f"🔬 {L['disease_detector']}")
    uploaded_file = st.file_uploader(L["upload_image"], type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        with col2:
            if st.button(L["detect_disease"], type="primary", use_container_width=True):
                with st.spinner(L["analyzing"]):
                    result = detect_plant_disease(uploaded_file.getvalue())
                    if result['success']:
                        st.success(f"✅ {L['disease_result']}")
                        st.metric("🦠 Disease", result['disease'])
                        st.metric(f"🎯 {L['confidence']}", f"{result['confidence']}%")
                        st.subheader(f"💊 {L['treatment']}")
                        st.write(result['treatment'])
                        st.subheader("🛡 Prevention Tips")
                        st.write(result['prevention'])
                    else:
                        st.error(f"Error: {result.get('error')}")

elif selected_key == "crop_advisor":
    st.subheader(f"🤖 {L['crop_advisor']}")
    with st.form("ai_crop_form"):
        col1, col2 = st.columns(2)
        soil_types = ["Laterite", "Alluvial", "Black", "Red", "Coastal Sandy"]
        try: soil_index = soil_types.index(st.session_state.profile.get("soil_type", "Laterite"))
        except ValueError: soil_index = 0
        with col1:
            st.text_input(L["village_input"], value=village, disabled=True)
            soil_type = st.selectbox(L["soil_type"], soil_types, index=soil_index)
            ph_level = st.number_input(L["ph_level"], min_value=3.0, max_value=9.0, value=6.0, step=0.1)
            nitrogen = st.number_input(L["nitrogen"], min_value=0, max_value=300, value=50)
        with col2:
            rainfall = st.number_input(L.get("rainfall"), min_value=500, max_value=4000, value=1500)
            season = st.selectbox(L.get("season"), [L.get("kharif"), L.get("rabi"), L.get("zaid")])
            phosphorus = st.number_input(L["phosphorus"], min_value=0, max_value=200, value=30)
            potassium = st.number_input(L["potassium"], min_value=0, max_value=200, value=40)
        if st.form_submit_button(L["recommend"], type="primary", use_container_width=True):
            with st.spinner(L.get("ai_processing")):
                temp, _, _ = get_weather_from_api(village, state)
                recommendations = ai_crop_recommender(ph_level, nitrogen, phosphorus, potassium, rainfall, temp, season, soil_type)
                if recommendations:
                    st.success(f"🎯 {L['recommended_crops']}")
                    for i, rec in enumerate(recommendations):
                        with st.container():
                            # ... (display recommendations)
                            pass
                else:
                    st.warning("⚠ Unable to generate recommendations.")

elif selected_key == "market_prices":
    st.subheader(f"💹 {L['market_prices']}")
    market_data = {L["crop"]: ["Rice", "Coconut", "Pepper", "Cardamom", "Rubber", "Banana", "Ginger"], L["price"]: ["₹28-32", "₹15-20", "₹450-500", "₹1200-1400", "₹140-160", "₹25-30", "₹80-100"]}
    st.table(pd.DataFrame(market_data))
    st.caption(f"Prices for {village} market - Updated: {datetime.now().strftime('%d-%m-%Y')}")

elif selected_key == "marketplace":
    st.subheader(f"🛒 {L['marketplace']}")
    with st.form("market_form"):
        # ... (marketplace form)
        pass

elif selected_key == "schemes":
    st.subheader(f"📜 {L['schemes']}")
    # ... (schemes content)
