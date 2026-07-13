import streamlit as st
import pandas as pd

# تنظیمات اصلی صفحه
st.set_page_config(page_title="سامانه کشوری خوارزمی", page_icon="🚀", layout="wide")

# استایل‌دهی راست‌چین برای زبان فارسی
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 90%; }
    h1, h2, h3, h4, p, div, table, th, td, label, .stButton {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Tahoma', sans-serif !important;
    }
    div.stButton > button:first-child {
        background-color: #2e7d32;
        color: white;
        width: 100%;
    }
    .stAlert { direction: rtl !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 سامانه کشوری خوارزمی | پنل اختصاصی 👑")
st.subheader("🌐 مرکز ابری پایش داده‌های آموزشی کشور")

# ایجاد یک حافظه موقت (Session State) برای ذخیره دانش‌آموزان ثبت‌نامی
if 'students_db' not in st.session_state:
    st.session_state['students_db'] = []

# منوی اصلی برنامه در سایدبار (منوی کناری)
st.sidebar.markdown("<h2 style='text-align: right;'>منوی مدیریت</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("یک بخش را انتخاب کنید:", ["ثبت‌نام دانش‌آموز جدید", "مشاهده و مدیریت بانک اطلاعاتی", "گزارش‌گیری و آمار کشوری"])

# ----------------- بخش اول: ثبت نام -----------------
if page == "ثبت‌نام دانش‌آموز جدید":
    st.header("📝 فرم ثبت‌نام طرح‌ها و مسابقات")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("نام و نام خانوادگی دانش‌آموز:")
            national_id = st.text_input("کد ملی:")
            phone = st.text_input("شماره تماس:")
        with col2:
            province = st.selectbox("استان:", ["تهران", "خراسان رضوی", "اصفهان", "فارس", "آذربایجان شرقی", "مازندران", "خوزستان", "سایر"])
            grade = st.selectbox("پایه تحصیلی:", ["هفتم", "هشتم", "نهم", "دهم", "یازدهم", "دوازدهم"])
            field = st.selectbox("محور مسابقه (طرح خوارزمی):", ["پژوهش", "دست‌سازه", "زبان و ادبیات فارسی", "زبان انگلیسی", "ریاضیات", "فعالیت‌های آزمایشگاهی", "برنامه‌نویسی و هوش مصنوعی"])
            
        submit_btn = st.form_submit_button("ثبت قطعی در دیتابیس ابری")
        
        if submit_btn:
            if name and national_id:
                # ذخیره در حافظه
                new_student = {
                    "نام و نام خانوادگی": name,
                    "کد ملی": national_id,
                    "استان": province,
                    "پایه تحصیلی": grade,
                    "محور مسابقه": field,
                    "شماره تماس": phone,
                    "وضعیت تایید": "در حال بررسی اولیه"
                }
                st.session_state['students_db'].append(new_student)
                st.success(f"✅ اطلاعات دانش‌آموز '{name}' با موفقیت در شبکه سراسری ثبت شد.")
            else:
                st.error("❌ لطفا فیلدهای ضروری (نام و کد ملی) را پر کنید.")

# ----------------- بخش دوم: مشاهده و مدیریت -----------------
elif page == "مشاهده و مدیریت بانک اطلاعاتی":
    st.header("📊 لیست دانش‌آموزان ثبت‌نام شده")
    
    if len(st.session_state['students_db']) == 0:
        st.info(".دیتابیس سراسری کشور در حال حاضر داده‌ای ندارد. از منوی کناری وارد بخش ثبت‌نام شوید")
    else:
        df = pd.DataFrame(st.session_state['students_db'])
        
        # فیلترهای جستجو
        search_query = st.text_input("🔍 جستجو بر اساس نام یا کد ملی:")
        if search_query:
            df = df[df['نام و نام خانوادگی'].str.contains(search_query) | df['کد ملی'].str.contains(search_query)]
            
        st.dataframe(df, use_container_width=True)
        
        # امکان دانلود فایل اکسل داده‌ها
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 دانلود کل بانک اطلاعاتی (فایل CSV مخصوص اکسل)",
            data=csv,
            file_name='khwarizmi_students_database.csv',
            mime='text/csv',
        )

# ----------------- بخش سوم: آمار -----------------
elif page == "گزارش‌گیری و آمار کشوری":
    st.header("📈 نمودارها و آمار لحظه‌ای کشور")
    
    if len(st.session_state['students_db']) == 0:
        st.info("داده‌ای برای تحلیل آماری وجود ندارد.")
    else:
        df = pd.DataFrame(st.session_state['students_db'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("تعداد ثبت‌نامی‌ها بر اساس استان")
            st.bar_chart(df['استان'].value_counts())
        with col2:
            st.subheader("محبوبیت محورهای مسابقه")
            st.bar_chart(df['محور مسابقه'].value_counts())
