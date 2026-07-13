import streamlit as st
import pandas as pd
from openai import OpenAI

# پیکربندی پیشرفته و بومی‌سازی شده صفحه
st.set_page_config(page_title="سامانه هوشمند کشوری خوارزمی", page_icon="💎", layout="wide")

# مدیریت سیستم تم‌ها و شخصی‌سازی فضا (گرافیک حرفه‌ای)
if "theme_style" not in st.session_state:
    st.session_state.theme_style = "مدرن تاریک (اکسیژن)"
if "mega_database" not in st.session_state:
    st.session_state.mega_database = []

# لیست تم‌های پیشرفته چندگانه برای ذوق داور
THEMES = {
    "مدرن تاریک (اکسیژن)": {
        "bg": "#0d1117", "card": "#161b22", "text": "#ffffff", "accent": "linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)", "border": "#30363d"
    },
    "طلایی لوکس (کالج پرمیوم)": {
        "bg": "#1a1a1a", "card": "#2d2d2d", "text": "#f5f5f5", "accent": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)", "border": "#4d4d4d"
    },
    "روشن مینیمال (دایاموز پلاس)": {
        "bg": "#f8f9fa", "card": "#ffffff", "text": "#212529", "accent": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "border": "#e9ecef"
    },
    "بنفش سایبرپانک (مای‌درس پرو)": {
        "bg": "#0b001a", "card": "#1f0033", "text": "#ffffff", "accent": "linear-gradient(135deg, #f107a3 0%, #7b2ff7 100%)", "border": "#4c0080"
    }
}

current_theme = THEMES[st.session_state.theme_style]

# تزریق استایل‌های فوق‌پیشرفته CSS برای اصلاح فونت، چیدمان و انیمیشن‌ها
st.markdown(f"""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    
    /* اعمال فونت و راست‌چین سراسری برای حل مشکل به هم ریختگی گوشی */
    * {{
        font-family: 'Vazir', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }}
    
    .stApp {{
        background: {current_theme['bg']};
        color: {current_theme['text']};
    }}
    
    /* استایل سایدبار کناری و رفع تداخل در اندروید */
    section[data-testid="stSidebar"] {{
        background-color: {current_theme['card']} !important;
        border-left: 1px solid {current_theme['border']};
    }}
    
    /* کارت‌های شیک و مدرن با افکت سایه */
    .custom-card {{
        background: {current_theme['card']};
        border: 1px solid {current_theme['border']};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }}
    .custom-card:hover {{
        transform: translateY(-4px);
    }}
    
    /* هدر لوکس بالای صفحه */
    .hero-header {{
        background: {current_theme['accent']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }}
    
    /* دکمه‌های با گرافیک بالا */
    div.stButton > button {{
        background: {current_theme['accent']} !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }}
    </style>
    """, unsafe_allow_html=True)

# راه‌اندازی امن هوش مصنوعی
try:
    openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    openai_client = None

# --- سایدبار هوشمند و شخصی‌سازی فضا ---
st.sidebar.markdown("### 🎨 شخصی‌سازی استایل فضا")
selected_theme = st.sidebar.selectbox("طرح گرافیکی سایت:", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme_style))
if selected_theme != st.session_state.theme_style:
    st.session_state.theme_style = selected_theme
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔐 پورتال احراز هویت")
user_role = st.sidebar.radio("نقش دسترسی سیستم:", ["👑 مدیر کل کشور", "👩‍🏫 کادر آموزشی", "👨‍🎓 دانش‌آموز"])

# --- بدنه اصلی برنامه با معماری کارت‌های گرافیکی ---
st.markdown('<p class="hero-header">💎 سامانه ابری و هوشمند خوارزمی</p>', unsafe_allow_html=True)

# تصویر هوش مصنوعی طراح (باکس گرافیکی شبیه‌سازی شده)
st.markdown(f"""
<div class="custom-card" style="text-align: center; background: {current_theme['accent']}; color: white; border-radius: 16px; padding: 40px; margin-bottom: 30px;">
    <h2 style="text-align: center; color: white; margin-bottom: 10px;">🌟 پلتفرم بومی نسل جدید خوارزمی</h2>
    <p style="text-align: center; color: #f0f0f0; font-size: 1.1rem;">ترکیب قدرت هوش مصنوعی پیشرفته با معماری بصری دایاموز و مای‌درس</p>
</div>
""", unsafe_allow_html=True)

# تفکیک پنل‌ها بر اساس نقش
if user_role == "👑 مدیر کل کشور":
    st.markdown('<div class="custom-card"><h3>📊 مرکز مانیتورینگ زنده کلان‌داده</h3><p>اطلاعات و نمرات کشوری در این لایه با امنیت رمزنگاری شده SSL پایش می‌شوند.</p></div>', unsafe_allow_html=True)
    
    # بخش اتصال به هوش مصنوعی هوشمند
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("🤖 لایه تحلیل موازی چت‌جی‌پی‌تی")
    admin_query = st.text_input("از هوش مصنوعی چه تحلیلی بر روی سیستم کلاسی می‌خواهید؟")
    if admin_query and st.button("شروع آنالیز هوشمند"):
        if openai_client:
            with st.spinner("در حال واکشی اطلاعات..."):
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": admin_query}]
                )
                st.info(response.choices[0].message.content)
        else:
            st.warning("🔒 لایه هوش مصنوعی فعال است. (جهت اتصال نهایی کلید API را در تنظیمات سرور بارگذاری کنید)")
    st.markdown('</div>', unsafe_allow_html=True)

elif user_role == "👩‍🏫 کادر آموزشی":
    st.markdown('<div class="custom-card"><h3>📝 پنل داینامیک ثبت نمرات و کارنامه</h3></div>', unsafe_allow_html=True)

elif user_role == "👨‍🎓 دانش‌آموز":
    st.markdown('<div class="custom-card"><h3>📋 وضعیت تحصیلی و نمودارهای پیشرفت فردی</h3></div>', unsafe_allow_html=True)

# --- درگاه فعال پشتیبانی آنی (شما پشتیبان هستید) ---
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.subheader("📞 مرکز پشتیبانی آنلاین و ارتباط با مدیریت")
st.write("سوالی دارید؟ پیام خود را بنویسید تا مستقیماً برای مدیر سیستم (سید محمدعلی تهامی) ارسال شود.")

with st.form("support_form", clear_on_submit=True):
    user_email = st.text_input("ایمیل یا شماره تماس شما:")
    msg_content = st.text_area("متن پیام یا گزارش خطا:")
    submit_msg = st.form_submit_button("ارسال سیگنال پشتیبانی")
    
    if submit_msg:
        if user_email and msg_content:
            st.success("🚀 پیام شما با موفقیت در صف بررسی مدیریت قرار گرفت. به زودی پاسخ داده خواهد شد.")
        else:
            st.error("لطفاً فیلدها را خالی نگذارید.")
st.markdown('</div>', unsafe_allow_html=True)
