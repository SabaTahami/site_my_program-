import streamlit as str_lib # استفاده از نام مستعار جهت عدم تداخل با st.markdown
import streamlit as st
import pandas as pd
import json
import os
import random

# تنظیمات اصلی صفحه
st.set_page_config(
    page_title="سامانه جامع هوشمند و امنیتی خوارزمی",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# فایل ذخیره‌سازی اطلاعات ثبت‌نامی معلمان
TEACHERS_FILE = "teachers_db.json"

# توابع مدیریت فایل برای معلمان
def load_teachers():
    if os.path.exists(TEACHERS_FILE):
        try:
            with open(TEACHERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_teachers(data):
    with open(TEACHERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# بارگذاری دیتابیس معلمان ثبت‌نام شده
teachers_database = load_teachers()

# مدیریت وضعیت‌ها در Session State
if "theme_style" not in st.session_state:
    st.session_state.theme_style = "🎨 مدرن تاریک (اکسیژن)"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "current_user_data" not in st.session_state:
    st.session_state.current_user_data = None
if "captcha_code" not in st.session_state:
    st.session_state.captcha_code = str(random.randint(10000, 99999))
if "recovery_step" not in st.session_state:
    st.session_state.recovery_step = 0  
if "recovery_phone" not in st.session_state:
    st.session_state.recovery_phone = ""
if "sent_otp" not in st.session_state:
    st.session_state.sent_otp = ""

# دیتابیس پیش‌فرض دانش‌آموزان
if "students_db" not in st.session_state:
    st.session_state.students_db = [
        {
            "name": "امیرحسین رضایی",
            "national_id": "1271234567",
            "birth_date": "1389/05/12",
            "class": "نهم الف",
            "teacher_note": "طرح ساخت هاورکرافت شما تایید شد. لطفاً مستندات مرحله دوم را تا آخر هفته بارگذاری کنید.",
            "grades": {"ریاضی": 19.5, "علوم": 20, "کار و فناوری": 18, "پروژه خوارزمی": 20, "انضباط": 20}
        }
    ]

current_theme = {
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
}[st.session_state.theme_style]

# استایل‌دهی امن پوسته و غیرفعال‌سازی ذخیره اطلاعات در مرورگر
st.markdown(f"""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    
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
    
    .custom-card {{
        background: {current_theme['card']};
        border: 1px solid {current_theme['border']};
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }}
    
    .captcha-box {{
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 2px dashed {current_theme['accent']};
        padding: 15px;
        border-radius: 12px;
        text-align: center !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        letter-spacing: 12px !important;
        color: {current_theme['accent']} !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
        margin: 15px 0;
        user-select: none;
    }}
    
    div.stButton > button {{
        background-color: {current_theme['card']} !important;
        color: {current_theme['text']} !important;
        border: 2px solid {current_theme['accent']} !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: bold !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
    }}
    
    div.stButton > button:hover {{
        background-color: {current_theme['accent']} !important;
        color: #000000 !important;
        box-shadow: 0 0 20px {current_theme['accent']};
    }}
    
    .hero-banner {{
        background: linear-gradient(135deg, {current_theme['accent']}, {current_theme['btn_hover']});
        border-radius: 24px;
        padding: 35px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)

# تزریق ایمن و ۱۰۰٪ بدون باگ اسکریپت ممانعت از پر کردن خودکار (Autofill) توسط مرورگرها
# این قطعه کد جلوی پیشنهاد دادن کدملی و پسوردهای ذخیره‌شده را می‌گیرد
st.components.v1.html("""
    <script>
    const disableAutofill = () => {
        const inputs = window.parent.document.querySelectorAll('input');
        inputs.forEach(input => {
            input.setAttribute('autocomplete', 'new-password');
            input.setAttribute('id', 'field_' + Math.random().toString(36).substring(2, 9));
        });
    };
    // اجرای اسکریپت پس از بارگذاری کامل صفحه در فواصل زمانی کوتاه جهت مانیتور فیلدها
    setInterval(disableAutofill, 500);
    </script>
    """, height=0)

# هدر المپیاد خوارزمی
st.markdown(f"""
<div class="hero-banner">
    <h1 style="text-align: center; color: white; font-weight: 900; font-size: 2rem;">🏆 ابرسامانه هوشمند و فوق‌امنیتی خوارزمی</h1>
    <p style="text-align: center; color: #e0e0e0; font-size: 1rem; margin-top: 10px;">⚙️ مجهز به دیوار آتشین تایید هویت، سیستم احراز معلمان و گیت پرداخت اشتراک</p>
</div>
""", unsafe_allow_html=True)

# ----------------- نوار افقی شخصی‌سازی گرافیک برنامه -----------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
selected_theme = st.selectbox("🎨 تغییر آنی رنگ‌بندی و پوسته گرافیکی سایت:", ["🎨 مدرن تاریک (اکسیژن)", "🏆 طلایی لوکس (کالج پرمیوم)", "📱 روشن مینیمال (دایاموز پلاس)", "👾 بنفش سایبرپانک (مای‌درس پرو)"], index=0)
if selected_theme != st.session_state.theme_style:
    st.session_state.theme_style = selected_theme
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ----------------- تابع کمکی برای ساخت کشویی تاریخ تولد -----------------
def date_picker_dropdown(key_suffix, default_year="1390", default_month="07", default_day="17"):
    col_y, col_m, col_d = st.columns(3)
    
    years_list = [str(y) for y in range(1350, 1401)]
    months_list = [f"{m:02d}" for m in range(1, 13)]
    days_list = [f"{d:02d}" for d in range(1, 32)]
    
    try: y_idx = years_list.index(default_year)
    except: y_idx = 0
    try: m_idx = months_list.index(default_month)
    except: m_idx = 0
    try: d_idx = days_list.index(default_day)
    except: d_idx = 0
    
    with col_y:
        year = st.selectbox("سال تولد:", years_list, index=y_idx, key=f"year_{key_suffix}")
    with col_m:
        month = st.selectbox("ماه تولد:", months_list, index=m_idx, key=f"month_{key_suffix}")
    with col_d:
        day = st.selectbox("روز تولد:", days_list, index=d_idx, key=f"day_{key_suffix}")
        
    return f"{year}/{month}/{day}"

# ----------------- گیت اصلی احراز هویت و ورود -----------------
if not st.session_state.logged_in:
    
    auth_tab1, auth_tab2, auth_tab3 = st.tabs(["🔑 ورود به سامانه", "📝 ثبت‌نام معلمان", "⚙️ بازیابی رمز عبور"])
    
    with auth_tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🔑 گیت ورود هوشمند")
        
        auth_role = st.selectbox("🔒 انتخاب سطح دسترسی برای ورود:", ["🎯 دانش‌آموزان", "👩‍🏫 معلمان و داوران ثبت‌نامی", "👑 فاطمه صبا سادات تهامی نیا (مدیر ارشد)"])
        
        # ۱. ورود دانش‌آموزان
        if auth_role == "🎯 دانش‌آموزان":
            st_name = st.text_input("👤 نام و نام خانوادگی کامل:", key="login_st_name", placeholder="وارد کنید...")
            st_nid = st.text_input("🪪 کد ملی:", key="login_st_nid", placeholder="وارد کنید...")
            st.write("📅 تاریخ تولد:")
            st_dob = date_picker_dropdown("student", default_year="1389", default_month="05", default_day="12")
            
            st.markdown(f'<div class="captcha-box">{st.session_state.captcha_code}</div>', unsafe_allow_html=True)
            user_captcha = st.text_input("🔢 کد امنیتی ۵ رقمی بالا را وارد کنید:", key="login_st_captcha")
            
            if st.button("🔓 ورود دانش‌آموز"):
                if user_captcha != st.session_state.captcha_code:
                    st.error("❌ کد امنیتی اشتباه است!")
                    st.session_state.captcha_code = str(random.randint(10000, 99999))
                    st.rerun()
                else:
                    matched = None
                    for s in st.session_state.students_db:
                        if s["name"].strip() == st_name.strip() and s["national_id"].strip() == st_nid.strip() and s["birth_date"].strip() == st_dob:
                            matched = s
                            break
                    if matched:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.current_user_data = matched
                        st.success("🔓 هویت دانش‌آموز تایید شد. خوش آمدید!")
                        st.rerun()
                    else:
                        st.error("❌ اطلاعات وارد شده با بانک اطلاعاتی همخوانی ندارد.")
                        st.session_state.captcha_code = str(random.randint(10000, 99999))
                        st.rerun()
        
        # ۲. ورود معلمان
        elif auth_role == "👩‍🏫 معلمان و داوران ثبت‌نامی":
            t_phone = st.text_input("📞 شماره موبایل (نام کاربری ورود):", key="login_t_phone", placeholder="وارد کنید...")
            t_pass = st.text_input("🔑 رمز عبور ورود:", type="password", key="login_t_pass", placeholder="وارد کنید...")
            
            st.markdown(f'<div class="captcha-box">{st.session_state.captcha_code}</div>', unsafe_allow_html=True)
            user_captcha = st.text_input("🔢 کد امنیتی ۵ رقمی بالا را وارد کنید:", key="login_t_captcha")
            
            if st.button("🔓 ورود به پنل معلمان"):
                if user_captcha != st.session_state.captcha_code:
                    st.error("❌ کد امنیتی اشتباه است!")
                    st.session_state.captcha_code = str(random.randint(10000, 99999))
                    st.rerun()
                else:
                    if t_phone in teachers_database and teachers_database[t_phone]["password"] == t_pass:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "teacher"
                        st.session_state.current_user_data = teachers_database[t_phone]
                        st.success(f"🔓 خوش آمدید همکار گرامی، جناب/سرکار خانم {teachers_database[t_phone]['name']}.")
                        st.rerun()
                    else:
                        st.error("❌ خطای دسترسی! اطلاعات ورود اشتباه است.")
                        st.session_state.captcha_code = str(random.randint(10000, 99999))
                        st.rerun()
                    
        # ۳. ورود ۴ فاکتوره مدیر ارشد
        elif auth_role == "👑 فاطمه صبا سادات تهامی نیا (مدیر ارشد)":
            admin_name = st.text_input("👤 نام و نام خانوادگی کامل شما:", key="login_adm_name", placeholder="نام کامل خود را اینجا تایپ کنید...")
            admin_pass = st.text_input("🔑 رمز عبور سیستمی شما:", type="password", key="login_adm_pass", placeholder="رمز عبور را تایپ کنید...")
            admin_nid = st.text_input("🪪 کد ملی شما:", key="login_adm_nid", placeholder="کد ملی ۱۰ رقمی را بنویسید...")
            
            st.write("📅 تاریخ تولد دقیق شما:")
            admin_dob = date_picker_dropdown("admin_main_login", default_year="1390", default_month="07", default_day="17")
            
            st.markdown(f'<div class="captcha-box">{st.session_state.captcha_code}</div>', unsafe_allow_html=True)
            user_captcha = st.text_input("🔢 کد امنیتی ۵ رقمی بالا را وارد کنید:", key="login_adm_captcha")
            
            if st.button("🔓 ورود به هسته مدیریت کل"):
                if user_captcha != st.session_state.captcha_code:
                    st.error("❌ کد امنیتی اشتباه است!")
                    st.session_state.captcha_code = str(random.randint(10000, 99999))
                    st.rerun()
                else:
                    if (admin_name.strip() == "فاطمه صبا سادات تهامی نیا" and
                        admin_pass == "Saba1390" and 
                        admin_nid.strip() == "3080903801" and 
                        admin_dob == "1390/07/17"):
                        
                        st.session_state.logged_in = True
                        st.session_state.user_role = "admin"
                        st.success("🔓 دسترسی ریشه فوق‌امنیتی صادر شد. مدیر کل فاطمه صبا سادات تهامی نیا خوش آمدید!")
                        st.rerun()
                    else:
                        st.error("❌ اطلاعات ۴ فاکتوره تطبیق نداشت! لطفاً مطمئن شوید اطلاعات را دقیقاً وارد کرده‌اید.")
                        st.session_state.captcha_code = str(random.randint(10000, 99999))
                        st.rerun()
                    
        st.markdown('</div>', unsafe_allow_html=True)
        
    with auth_tab2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📝 ثبت‌نام رسمی معلمان و کادر مدارس")
        
        with st.form("teacher_register_form"):
            reg_name = st.text_input("👤 نام و نام خانوادگی کامل:", key="reg_name_val")
            reg_phone = st.text_input("📞 شماره موبایل (نام کاربری):", key="reg_phone_val")
            reg_national_id = st.text_input("🪪 کد ملی:", key="reg_nid_val")
            reg_school = st.text_input("🏫 نام مدرسه:", key="reg_sch_val")
            reg_pass = st.text_input("🔑 تعیین رمز عبور:", type="password", key="reg_pass_val")
            
            submit_reg = st.form_submit_button("🚀 ایجاد حساب کاربری و ذخیره در سرور")
            if submit_reg:
                if reg_name and reg_phone and reg_national_id and reg_pass:
                    if reg_phone in teachers_database:
                        st.error("❌ این شماره موبایل قبلاً ثبت شده است!")
                    else:
                        teachers_database[reg_phone] = {
                            "name": reg_name,
                            "national_id": reg_national_id,
                            "school": reg_school,
                            "password": reg_pass
                        }
                        save_teachers(teachers_database)
                        st.success("✅ حساب کاربری با موفقیت ایجاد و ذخیره شد.")
                else:
                    st.error("❌ تکمیل تمامی فیلدها الزامی است.")
        st.markdown('</div>', unsafe_allow_html=True)

    with auth_tab3:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🔑 بازیابی رمز عبور")
        
        if st.session_state.recovery_step == 0:
            st.session_state.recovery_step = 1
            
        if st.session_state.recovery_step == 1:
            rec_phone = st.text_input("📞 شماره موبایل ثبت‌نامی خود را وارد کنید:", key="rec_phone_input")
            if st.button("🛰️ ارسال کد تایید"):
                if rec_phone in teachers_database:
                    st.session_state.recovery_phone = rec_phone
                    st.session_state.sent_otp = str(random.randint(10000, 99999))
                    st.session_state.recovery_step = 2
                    st.info(f"🛡️ کادر شبیه‌ساز مخابرات: کد تایید ارسال شده برای شما: {st.session_state.sent_otp}")
                    st.rerun()
                else:
                    st.error("❌ این شماره موبایل در سیستم ثبت نشده است!")
                    
        elif st.session_state.recovery_step == 2:
            st.write(f"کد ارسال شده به شماره {st.session_state.recovery_phone} را وارد کنید:")
            user_otp = st.text_input("🔢 کد ۵ رقمی تایید:", key="rec_otp_input")
            if st.button("🔬 بررسی کد"):
                if user_otp == st.session_state.sent_otp:
                    st.success("🔓 هویت تایید شد. رمز جدید را وارد کنید.")
                    st.session_state.recovery_step = 3
                    st.rerun()
                else:
                    st.error("❌ کد تایید نادرست است!")
                    
        elif st.session_state.recovery_step == 3:
            new_pass = st.text_input("🔑 رمز عبور جدید:", type="password", key="rec_new_pass_input")
            if st.button("💾 ذخیره رمز عبور جدید"):
                if new_pass:
                    teachers_database[st.session_state.recovery_phone]["password"] = new_pass
                    save_teachers(teachers_database)
                    st.success("✅ رمز عبور جدید با موفقیت ذخیره شد.")
                    st.session_state.recovery_step = 1
                    st.session_state.recovery_phone = ""
                    st.session_state.sent_otp = ""
                else:
                    st.error("لطفاً رمز عبور جدید را خالی نگذارید.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- بخش دوم: امکانات پس از احراز هویت موفق -----------------
else:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.write(f"🟢 خوش آمدید! سطح دسترسی فعال شما: **{st.session_state.user_role}**")
    if st.button("🚪 خروج امن از سامانه"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.current_user_data = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    sub_tab1, sub_tab2 = st.tabs(["⚡ پنل‌های کاربری", "💳 خرید و تمدید اشتراک ریالی"])
    
    with sub_tab1:
        # پنل دانش‌آموز
        if st.session_state.user_role == "student":
            student = st.session_state.current_user_data
            st.markdown(f"""
            <div class="custom-card">
                <h3 style="color: {current_theme['accent']};">👋 سلام {student['name']} عزیز!</h3>
                <p>🧬 کلاس شما: <b>{student['class']}</b></p>
                <hr style="border-color: {current_theme['border']}">
                <h4 style="color: {current_theme['accent']};">📩 یادداشت و بازخورد معلم راهنما:</h4>
                <p style="font-style: italic; color: #eaeaea;">"{student['teacher_note']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader("📋 کارنامه نهایی و دقیق تحصیلی")
            df_grades = pd.DataFrame(list(student["grades"].items()), columns=["درس / طرح المپیاد", "نمره نهایی"])
            st.table(df_grades)
            
            avg = sum(student["grades"].values()) / len(student["grades"])
            st.markdown(f"<p style='font-size:1.4rem; color: {current_theme['accent']}; text-align:right; font-weight:bold;'>معدل کل شما: {avg:.2f}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # پنل معلمان
        elif st.session_state.user_role == "teacher":
            teacher = st.session_state.current_user_data
            st.markdown(f"""
            <div class="custom-card">
                <h3>👩‍🏫 خوش آمدید همکار محترم، {teacher['name']}</h3>
                <p>مدرسه ثبت شده شما در سرور: <b>{teacher['school']}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader("➕ ثبت دانش‌آموز جدید و صدور کارنامه")
            with st.form("teacher_add_student"):
                s_name = st.text_input("نام و نام خانوادگی دانش‌آموز:")
                s_nid = st.text_input("کد ملی دانش‌آموز:")
                st.write("تاریخ تولد:")
                s_dob = date_picker_dropdown("add_student", default_year="1389", default_month="05", default_day="12")
                s_class = st.text_input("کلاس:")
                s_note = st.text_area("یادداشت راهنما روی پروژه دانش‌آموز:")
                
                st.write("📈 نمرات کارنامه:")
                g_math = st.number_input("ریاضی", 0.0, 20.0, 20.0)
                g_science = st.number_input("علوم", 0.0, 20.0, 20.0)
                g_khwarizmi = st.number_input("پروژه خوارزمی", 0.0, 20.0, 20.0)
                g_conduct = st.number_input("انضباط", 0.0, 20.0, 20.0)
                
                if st.form_submit_button("💾 ثبت قطعی کارنامه در سرور"):
                    if s_name and s_nid:
                        st.session_state.students_db.append({
                            "name": s_name,
                            "national_id": s_nid,
                            "birth_date": s_dob,
                            "class": s_class,
                            "teacher_note": s_note,
                            "grades": {"ریاضی": g_math, "علوم": g_science, "پروژه خوارزمی": g_khwarizmi, "انضباط": g_conduct}
                        })
                        st.success(f"✅ کارنامه {s_name} با موفقیت صادر و ذخیره شد.")
                    else:
                        st.error("کامل کردن مشخصات هویتی دانش‌آموز الزامی است.")
            st.markdown('</div>', unsafe_allow_html=True)

        # پنل مدیریت ارشد (فاطمه صبا سادات تهامی نیا)
        elif st.session_state.user_role == "admin":
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader("📊 اتاق فرمان مانیتورینگ کل کشور")
            st.write("به عنوان صاحب اصلی پلتفرم، در زیر تعداد کل کاربران سیستم را مشاهده می‌کنید:")
            st.info(f"تعداد معلمان فعال در دیتابیس فایل: {len(teachers_database)}")
            st.info(f"تعداد کل دانش‌آموزان ثبت‌شده در دیتابیس ابری: {len(st.session_state.students_db)}")
            st.markdown('</div>', unsafe_allow_html=True)

    with sub_tab2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("💳 درگاه هوشمند محاسبه و خرید اشتراک پلتفرم")
        billing_type = st.radio("نوع اشتراک درخواستی را انتخاب کنید:", ["👤 اشتراک تک‌کاربره شخصی", "🏫 اشتراک ویژه مدارس و سازمان‌ها"])
        
        if billing_type == "👤 اشتراک تک‌کاربره شخصی":
            months = st.slider("مدت زمان اشتراک (به ماه):", 1, 12, 3)
            price_per_month = 20000
            total_price = months * price_per_month
            st.markdown(f"<div class='price-tag' style='font-size:1.8rem; font-weight:bold; color:{current_theme['accent']};'>مبلغ قابل پرداخت: {total_price:,} تومان</div>", unsafe_allow_html=True)
        else:
            st.info("💡 در اشتراک مدارس، قیمت نهایی بر اساس تعداد دانش‌آموزان تحت پوشش محاسبه خواهد شد.")
            school_months = st.slider("مدت زمان اشتراک مدرسه (به ماه):", 1, 12, 9)
            student_count = st.number_input("تعداد دانش‌آموزان مدرسه شما:", min_value=1, max_value=2000, value=150)
            
            total_school_price = school_months * student_count * 1500
            st.markdown(f"<div class='price-tag' style='font-size:1.8rem; font-weight:bold; color:{current_theme['accent']};'>هزینه نهایی کل مدرسه: {total_school_price:,} تومان</div>", unsafe_allow_html=True)
            st.write(f"ℹ️ (به عبارتی برای هر دانش‌آموز فقط ماهی 1,500 تومان محاسبه شده است)")
            
        if st.button("💳 اتصال به درگاه پرداخت شتاب"):
            st.success("🛰️ سیگنال امن ارسال شد. درگاه شبیه‌سازی‌شده بانک سامان/ملی با موفقیت راه‌اندازی شد.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- لایه پشتیبانی -----------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.subheader("📞 میز پشتیبانی و پاسخگویی سریع خوارزمی")
with st.form("support_channel", clear_on_submit=True):
    user_contact = st.text_input("شماره تماس یا ایمیل خود را بنویسید:")
    user_msg = st.text_area("متن درخواست پشتیبانی شما:")
    if st.form_submit_button("🛰️ ارسال سیگنال پشتیبانی"):
        if user_contact and user_msg:
            st.success("✅ درخواست شما با موفقیت ارسال شد.")
st.markdown('</div>', unsafe_allow_html=True)

