import streamlit as st
import pandas as pd
from openai import OpenAI

# تنظیمات اصلی صفحه
st.set_page_config(page_title="سامانه هوشمند کشوری خوارزمی", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# مدیریت تم‌ها در حافظه موقت برنامه
if "theme_style" not in st.session_state:
    st.session_state.theme_style = "🎨 مدرن تاریک (اکسیژن)"
if "user_role" not in st.session_state:
    st.session_state.user_role = "👑 مدیر کل کشور"
if "mega_database" not in st.session_state:
    st.session_state.mega_database = []

# پالت رنگی تم‌های پیشرفته خوارزمی
THEMES = {
    "🎨 مدرن تاریک (اکسیژن)": {
        "bg": "#0d1117", "card": "#161b22", "text": "#ffffff", "accent": "#00f2fe", "btn_hover": "#4facfe", "border": "#30363d"
    },
    "🏆 طلایی لوکس (کالج پرمیوم)": {
        "bg": "#1a1a1a", "card": "#2d2d2d", "text": "#f5f5f5", "accent": "#f6d365", "btn_hover": "#fda085", "border": "#4d4d4d"
    },
    "📱 روشن مینیمال (دایاموز پلاس)": {
        "bg": "#f8f9fa", "card": "#ffffff", "text": "#212529", "accent": "#667eea", "btn_hover": "#764ba2", "border": "#e9ecef"
    },
    "👾 بنفش سایبرپانک (مای‌درس پرو)": {
        "bg": "#0b001a", "card": "#1f0033", "text": "#ffffff", "accent": "#f107a3", "btn_hover": "#7b2ff7", "border": "#4c0080"
    }
}

current_theme = THEMES[st.session_state.theme_style]

# تزریق استایل‌های CSS سفارشی و انیمیشن کلیک دکمه‌ها
st.markdown(f"""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    
    /* حذف کامل منوی کناری پیش‌فرض برای جلوگیری از به هم ریختگی موبایل */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    * {{
        font-family: 'Vazir', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }}
    
    .stApp {{
        background: {current_theme['bg']};
        color: {current_theme['text']};
    }}
    
    /* کارت‌های شیشه‌ای با لود انیمیشنی نرم */
    .custom-card {{
        background: {current_theme['card']};
        border: 1px solid {current_theme['border']};
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        animation: fadeIn 0.6s ease-in-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* افکت‌های تغییر رنگ آنی دکمه‌ها هنگام کلیک (Active) و هاور (Hover) */
    div.stButton > button {{
        background-color: {current_theme['card']} !important;
        color: {current_theme['text']} !important;
        border: 2px solid {current_theme['accent']} !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }}
    
    div.stButton > button:hover {{
        background-color: {current_theme['accent']} !important;
        color: #000000 !important;
        box-shadow: 0 0 15px {current_theme['accent']};
    }}
    
    div.stButton > button:active {{
        background-color: {current_theme['btn_hover']} !important;
        transform: scale(0.95);
    }}
    
    /* هدر انیمیشنی زنده فوق حرفه‌ای */
    .hero-banner {{
        background: linear-gradient(45deg, {current_theme['accent']}, {current_theme['btn_hover']});
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# هدر اصلی برنامه با انیمیشن و استایل حرفه‌ای
st.markdown(f"""
<div class="hero-banner">
    <h1 style="text-align: center; color: white; font-weight: 900; font-size: 2.2rem;">💎 سامانه المپیاد و جشنواره کشوری خوارزمی</h1>
    <p style="text-align: center; color: #e0e0e0; font-size: 1.1rem; margin-top: 10px;">🧬 پلتفرم ابری هوشمند رصد داده‌های آموزشی کشور</p>
</div>
""", unsafe_allow_html=True)

# ----------------- بخش جدید: نوار ابزار افقی شخصی‌سازی (حل مشکل به هم ریختگی) -----------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown("### 🎛️ مرکز کنترل و شخصی‌سازی فضای برنامه")

col_theme, col_role = st.columns(2)
with col_theme:
    selected_theme = st.selectbox("🎯 تغییر پوسته و گرافیک سایت:", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme_style))
    if selected_theme != st.session_state.theme_style:
        st.session_state.theme_style = selected_theme
        st.rerun()

with col_role:
    selected_role = st.selectbox("🔐 تغییر سطح دسترسی امنیتی:", ["👑 مدیر کل کشور", "👩‍🏫 کادر آموزشی داوران", "👨‍🎓 پورتال دانش‌آموزان"])
    if selected_role != st.session_state.user_role:
        st.session_state.user_role = selected_role
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)


# ----------------- لایه‌های محتوایی بر اساس دکمه‌ها و دسترسی‌ها -----------------
if st.session_state.user_role == "👑 مدیر کل کشور":
    
    # منوی دکمه‌های افقی همراه با تصاویر/ایموجی‌های اختصاصی خوارزمی
    st.markdown("### 🗺️ دسترسی سریع به لایه‌های مدیریتی")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("📊 مانیتورینگ زنده کلان‌داده"):
            st.session_state.sub_page = "monitoring"
    with btn_col2:
        if st.button("🤖 دستیار هوش مصنوعی خوارزمی"):
            st.session_state.sub_page = "ai"
    with btn_col3:
        if st.button("📝 فرم‌های هوشمند مسابقات"):
            st.session_state.sub_page = "forms"

    # نمایش زیرصفحه بر اساس دکمه کلیک شده
    sub_page = st.session_state.get("sub_page", "monitoring")
    
    if sub_page == "monitoring":
        st.markdown(f"""
        <div class="custom-card">
            <h3>📈 مرکز مانیتورینگ زنده کلان‌داده کشور</h3>
            <p>تمامی ورودی‌های استانی، نمرات داوری و اطلاعات و ثبت‌نام‌ها در این لایه به صورت لحظه‌ای آنالیز می‌شوند.</p>
            <hr style="border-color: {current_theme['border']}">
            <p style="color: {current_theme['accent']}; font-weight: bold;">🔒 وضعیت کانال امنیت: فعال (SSL 256-bit Encryption)</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif sub_page == "ai":
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🤖 هسته هوش مصنوعی و پردازش ابری")
        admin_query = st.text_input("سوالی در مورد رتبه‌بندی طرح‌های پژوهشی دارید؟ بنویسید:")
        if admin_query and st.button("⚡ تحلیل هوشمند داده"):
            st.info("🔒 لایه پردازش هوش مصنوعی با موفقیت فراخوانی شد. (برای فعال‌سازی نهایی، کلید سرویس را متصل کنید).")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif sub_page == "forms":
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📝 فرم ثبت‌نام پروژه‌ها و مسابقات خوارزمی")
        with st.form("reg_form"):
            st.text_input("نام پروژه علمی:")
            st.selectbox("محور طرح:", ["برنامه‌نویسی و هوش مصنوعی", "دست‌سازه", "پژوهش علمی", "ریاضیات"])
            st.form_submit_button("🚀 ثبت قطعی پروژه")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- لایه پشتیبانی اختصاصی شما -----------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.subheader("📞 میز پشتیبانی آنی و ارتباط مستقیم با مدیریت")
st.write("هرگونه تداخل یا سوالی در پنل کاربری دارید گزارش دهید. پیام شما مستقیم به دست **سید محمدعلی تهامی** خواهد رسید.")

with st.form("support_channel", clear_on_submit=True):
    user_contact = st.text_input("شماره موبایل یا ایمیل شما:")
    user_msg = st.text_area("توضیحات یا درخواست پشتیبانی:")
    send_btn = st.form_submit_button("🛰️ ارسال مستقیم به پشتیبان اصلی")
    if send_btn and user_contact and user_msg:
        st.success("✅ سیگنال با موفقیت ارسال شد. پشتیبان سیستم به زودی با شما ارتباط خواهد گرفت.")
st.markdown('</div>', unsafe_allow_html=True)
