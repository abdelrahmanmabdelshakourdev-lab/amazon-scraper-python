import pandas as pd
import io
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Amazon Dynamic Dashboard", page_icon="✨", layout="wide"
)

# 2. تصميم CSS المخصص المحدث (الألوان + الحركات)
st.markdown(
    """
    <style>
    /* تغيير لون الخلفية العامة */
    .main {
        background-color: #f1f5f9;
    }
    
    /* تخصيص الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    .product-card img {
    width: 100%;
    height: 160px;
    object-fit: contain;
    margin-bottom: 10px;
}
    
    /* تصميم كارت المنتج مع تأثيرات الحركة */
    .product-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        /* حركة ناعمة عند ظهور الكارت لأول مرة */
        animation: fadeIn 0.6s ease-out;
        /* إضافة ظل أكثر عمقاً */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        margin-bottom: 24px;
        height: 100%;;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        /* إضافة تأثير Transition للـ Hover */
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    /* تأثير الـ Hover المطور (حركة 3D وضوء خفيف) */
    .product-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #3b82f6; /* تغيير لون الحدود عند الـ Hover للأزرق */
    }
    
    /* تأثير لمعان خفيف عند الـ Hover يظهر على الكارت */
    .product-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(to bottom right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%);
        transform: rotate(45deg);
        transition: all 0.5s;
        opacity: 0;
    }
    
    .product-card:hover::after {
        opacity: 1;
        left: -100%;
        top: -100%;
    }

    /* تحسين العناوين والألوان */
    .product-title {
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.4;
        margin-bottom: 12px;
        /* جعل العنوان يظهر في سطرين فقط ويختفي الباقي */
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .product-price {
        font-size: 20px;
        font-weight: 800;
        color: #16a34a; /* لون أخضر غامق ومميز للسعر */
        letter-spacing: -0.5px;
    }
    
    .product-rating {
        color: #ca8a04; /* لون ذهبي مميز للتقييم */
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* كي إطارات الحركة (Animation Keyframes) */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* تنسيق الأزرار والمدخلات في الشريط الجانبي */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border-color: #cbd5e1;
    }
    .stButton > button {
        background-color: #2563eb; /* لون أزرق احترافي للزرار */
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. العنوان الرئيسي
st.markdown("## 🛍️Amazon Web Scraper", unsafe_allow_html=True)
st.write("Enjoy easy shopping ")


# 4. قراءة البيانات
@st.cache_data
def load_data():
  try:
    return pd.read_excel("amazon_products8.xlsx")
  except FileNotFoundError:
    return None


df = load_data()



if df is not None and not df.empty:
    # 1. Sidebar Header
    st.sidebar.header("Control 🎛️")

    # 2. Download Button
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    st.sidebar.download_button(
        label="📥 Download Excel File",
        data=buffer.getvalue(),
        file_name="amazon_products.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    st.sidebar.markdown("---")

    # 3. Search Input
    search_query = st.sidebar.text_input("🔍 Search for product", placeholder="Ex : Samsung / Sony / Anker")

    # 4. Apply Search Filter
    if search_query:
        df = df[df["title"].str.contains(search_query, case=False, na=False)]

    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Results : {len(df)}")

# 5. Display Products Grid
num_columns = 3

for index, (i, row) in enumerate(df.iterrows()):
    if index % num_columns == 0:
        cols = st.columns(num_columns)
    col = cols[index % num_columns]
    raw_img = str(row.get("img", "")).strip()  # Replace "img" with your exact Excel column header if named differently (e.g., "image" or "image_url")
    img_url = raw_img if raw_img and raw_img.lower() not in ["nan", "none", "no image", ""] else "https://via.placeholder.com/150?text=No+Image"
    #brand = str(row.get("brand", "No brand"))
    raw_brand = str(row.get("brand", "")).strip()
    brand = raw_brand if raw_brand and raw_brand.lower() not in ["nan", "none", "no brand", ""] else "Generic"
    title = str(row.get("title", "No Title"))
    raw_price = str(row.get("price", "")).strip()
    price = raw_price if raw_price and raw_price.lower() not in ["nan", "none", "no price", ""] else "⚠️ Out of Stock"
    rating = str(row.get("rating", "N/A"))
    #price = str(row.get("price", "⚠️ Out of Stock"))
    rating = str(row.get("rating", "N/A"))
    reviews = str(row.get("rating counts", "0"))    # Strip spaces and convert empty/nan values cleanly
    raw_link = str(row.get("link", "")).strip()
    link = raw_link if raw_link and raw_link.lower() not in ["nan", "none", "no link"] else None

    # استخدام HTML المخصص لعرض البيانات بستايل الكارت الجديد
    with col:
      st.markdown(
          f"""
            <div class="product-card">
            <img src="{img_url}" alt="Product Image" />
                <div>
                    <div class="product-brand">{brand}</div>
                    <a href="{link if link else '#'}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="product-title" title="{title}">{title}</div>
                </div>
                <div>
                    <div class="product-price">{price}</div>
                    <div class="product-rating">
                        <span>⭐ {rating}</span> 
                        <span style="color: #94a3b8;">|</span> 
                        <span>💬 {reviews} تقييم</span>
                    </div>
                </div>
            </div>
            """,
          unsafe_allow_html=True,
      )
      if link and link != "#":
        st.link_button("🛒 View on Amazon", link, use_container_width=True)
else:
  st.error(
      "⚠️ عذراً: لم يتم العثور على ملف البيانات. يرجى تشغيل سكريبت الـ Scraper أولاً."
  )