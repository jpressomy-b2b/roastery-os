import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import re
import os
import base64
import streamlit.components.v1 as components 

# --- MUST BE FIRST ---
st.set_page_config(page_title="Jpresso Roastery OS", layout="wide")

# --- JPRESSO ROYAL PURPLE & GOLD UI + STEALTH CSS ---
st.markdown("""
    <style>
    /* 1. Nuke Header, Footer, and Streamlit Badges */
    #MainMenu, header, footer, .stAppDeployButton, [data-testid="stStatusWidget"], [data-testid="viewerBadge"], div[class^="viewerBadge"], a[href*="streamlit.io"] {
        display: none !important;
    }
    
    /* 2. EXACT JPRESSO ROYAL PURPLE BACKGROUND */
    html, body, [data-testid="stAppViewContainer"], .main, .stApp {
        background-color: #341645 !important; 
    }
    
    /* 3. Force all base text to be light/snow white */
    h1, h2, h3, h4, h5, p, span, label, div {
        color: #fcfaff !important; 
    }

    /* 4. JPRESSO GOLD Typography and Spacing */
    .section-header { 
        color: #DAB07B !important; 
        border-bottom: 2px solid #DAB07B !important; 
        padding-bottom: 10px !important; 
        margin-bottom: 25px !important; 
        font-weight: 300 !important; 
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    
    /* 5. Custom Styling for Input Boxes to match Purple Theme */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea, .stMultiSelect div[data-baseweb="select"] {
        background-color: #250f31 !important;
        color: #fcfaff !important;
        border: 1px solid rgba(218, 176, 123, 0.4) !important;
    }
    
    /* 6. v5.8 LAYOUT LOCK */
    [data-testid="column"]:nth-of-type(2) {
        border-left: 2px solid #DAB07B !important;
        padding-left: 40px !important;
        padding-top: 0px !important; 
        display: flex;
        flex-direction: column;
        justify-content: flex-start !important; 
    }
    
    /* 7. Premium Floating Metric Cards */
    .metric-row { 
        display: flex; 
        justify-content: space-between; 
        gap: 15px; 
        margin-bottom: 25px; 
    }
    .metric-item { 
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(218, 176, 123, 0.3) !important; 
        padding: 20px !important; 
        border-radius: 12px !important; 
        text-align: center !important; 
        flex: 1 !important; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }
    .metric-item:hover {
        transform: translateY(-5px) !important;
        border-color: #DAB07B !important; 
        background: rgba(218, 176, 123, 0.08) !important;
    }
    .metric-item strong { color: #DAB07B !important; font-size: 0.9rem !important; text-transform: uppercase !important; letter-spacing: 1px !important;}
    .metric-item div { font-size: 1.6rem !important; color: #fcfaff !important; font-weight: bold !important; margin-top: 5px !important;}
    
    /* 8. Sleek Spec Box & Cost Card */
    .spec-box { 
        background-color: rgba(0, 0, 0, 0.2) !important; 
        border-left: 5px solid #DAB07B !important; 
        padding: 25px !important; 
        border-radius: 6px !important; 
        margin-bottom: 20px !important;
    }
    .cost-card { 
        background: rgba(218, 176, 123, 0.1) !important; 
        border: 1px solid #DAB07B !important; 
        color: #DAB07B !important; 
        padding: 15px !important; 
        border-radius: 8px !important; 
        margin-bottom: 15px !important; 
        text-align: center !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECURITY: MASTER PASSWORD LOCK ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown('<h1 style="color:#DAB07B;">🔐 Jpresso Intelligence OS</h1>', unsafe_allow_html=True)
        st.text_input("Enter Master Password", type="password", key="password_input")
        if st.button("Access System"):
            if st.session_state["password_input"] == "jpresso2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("😕 Password incorrect.")
        return False
    return True

if not check_password():
    st.stop()

# --- HELPER: BASE64 IMAGE ENCODER ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        pass
    return None

st.title("🔥 Jpresso Roastery Intelligence v187.0")
st.caption("The Royal Edition: Purple & Gold Engine + Guaranteed Print Scaling")

# --- PERSISTENT STATE LOCK ---
if 'batch_history' not in st.session_state: st.session_state.batch_history = []
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'master_notes' not in st.session_state: st.session_state.master_notes = set()
if 'ms_key' not in st.session_state: st.session_state.ms_key = 0 

# --- SIDEBAR: PRODUCTION AUDITOR ---
with st.sidebar:
    st.markdown('<h2 class="section-header">📈 Daily Audit</h2>', unsafe_allow_html=True)
    c_green = sum(float(b.get('Green (kg)', 0.0)) for b in st.session_state.batch_history) if st.session_state.batch_history else 0.0
    c_roasted = sum(float(b.get('Roasted (kg)', 0.0)) for b in st.session_state.batch_history) if st.session_state.batch_history else 0.0
    
    st.metric("Total Green Used Today", f"{c_green:.2f} kg")
    st.metric("Total Roasted Today", f"{c_roasted:.2f} kg")
    
    st.markdown("---")
    st.markdown("### 🗄️ Data Management")
    
    if st.session_state.batch_history:
        df_history = pd.DataFrame(st.session_state.batch_history)
        csv_export = df_history.to_csv(index=False)
        st.download_button(label="💾 DOWNLOAD DATA (CSV)", data=csv_export, file_name=f"Jpresso_Daily_Audit_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    else:
        st.info("Log a batch to enable CSV downloads.")

    if st.button("♻️ RESET SESSION", use_container_width=True): 
        st.session_state.clear()
        st.rerun()

# --- THE EXECUTIVE SUITE TABS ---
tab1, tab2, tab3 = st.tabs(["📦 Production Ledger", "📱 Brand Storyteller", "🎓 Auto-Evaluation Portal"])

# ==========================================
# TAB 1: CORE PRODUCTION LEDGER
# ==========================================
with tab1:
    col_in, col_out = st.columns(2)

    with col_in:
        st.markdown('<h2 class="section-header">📦 Production Core</h2>', unsafe_allow_html=True)
        
        st.markdown("##### 👨‍🔧 Operator & Environment")
        col_env1, col_env2, col_env3 = st.columns(3)
        with col_env1: operator_name = st.text_input("Roaster Name", value="")
        with col_env2: amb_temp = st.text_input("Amb. Temp (°C)", value="")
        with col_env3: humidity = st.text_input("Humidity (%)", value="")
        
        st.markdown("---")
        q_grade = st.selectbox("Quality Standard", ["Specialty Grade", "Commercial Grade"], index=0)
        g_weight = st.number_input("Total Green Input (kg)", value=0.0, step=0.01)
        r_weight = st.number_input("Total Roasted Output (kg)", value=0.0, step=0.01)
        
        mode = st.radio("Production Mode", ["Single Origin", "Blend Architect"], index=0, horizontal=True)
        blend_recipe_display = ""
        
        if mode == "Single Origin":
            sku_name = st.text_input("Bean Name / SKU", value="")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
            g_cost = st.number_input("Green Cost (Per kg)", value=0.0, step=0.01)
        else:
            sku_name = st.text_input("Master Blend SKU", value="")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
            st.markdown("##### Blend Components")
            blend_sum = []
            recipe_parts = []
            for i in range(1, 5):
                with st.expander(f"Component {i}"):
                    c_n = st.text_input(f"Origin Name", key=f"n{i}")
                    c_r = st.slider(f"Ratio (%)", 0, 100, 0, key=f"r{i}")
                    c_c = st.number_input(f"Cost (Per kg)", value=0.0, step=0.01, key=f"c{i}")
                    if c_r > 0: 
                        blend_sum.append(c_c * (c_r/100))
                        recipe_parts.append(f"{c_n if c_n else f'Origin {i}'} ({c_r}%)")
            g_cost = sum(blend_sum)
            if recipe_parts: blend_recipe_display = " | ".join(recipe_parts)
            st.markdown(f'<div class="cost-card"><strong>💰 Weighted Green Cost:</strong> {g_cost:.2f} /kg</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🎡 9-Wheel Sensory Auditor")
        family = st.selectbox("📥 Select Flavor Family to Map", ["🍎 Fruity", "🌸 Floral", "🍯 Sweet", "🍫 Nutty/Cocoa", "🌶️ Spices", "🔥 Roasted", "🌿 Green/Vegetative", "🧪 Other/Defects", "🍷 Sour/Fermented"])
        
        wheel_map = {
            "🍎 Fruity": [("Fruity", ""), ("Berry", "Fruity"), ("Blackberry", "Berry"), ("Raspberry", "Berry"), ("Blueberry", "Berry"), ("Strawberry", "Berry"), ("Dried Fruit", "Fruity"), ("Raisin", "Dried Fruit"), ("Prune", "Dried Fruit"), ("Other Fruit", "Fruity"), ("Coconut", "Other Fruit"), ("Cherry", "Other Fruit"), ("Pomegranate", "Other Fruit"), ("Pineapple", "Other Fruit"), ("Grape", "Other Fruit"), ("Apple", "Other Fruit"), ("Peach", "Other Fruit"), ("Pear", "Other Fruit"), ("Mango", "Other Fruit"), ("Citrus Fruit", "Fruity"), ("Grapefruit", "Citrus Fruit"), ("Orange", "Citrus Fruit"), ("Lemon", "Citrus Fruit"), ("Lime", "Citrus Fruit")],
            "🌸 Floral": [("Floral", ""), ("Black Tea", "Floral"), ("Floral Sub", "Floral"), ("Chamomile", "Floral Sub"), ("Rose", "Floral Sub"), ("Jasmine", "Floral Sub")],
            "🍯 Sweet": [("Sweet", ""), ("Brown Sugar", "Sweet"), ("Molasses", "Brown Sugar"), ("Maple Syrup", "Brown Sugar"), ("Caramelized", "Brown Sugar"), ("Honey", "Brown Sugar"), ("Vanilla", "Sweet"), ("Vanillin", "Sweet"), ("Overall Sweet", "Sweet"), ("Sweet Aromatics", "Sweet")],
            "🍫 Nutty/Cocoa": [("Nutty/Cocoa", ""), ("Nutty", "Nutty/Cocoa"), ("Peanuts", "Nutty"), ("Hazelnut", "Nutty"), ("Almond", "Nutty"), ("Cocoa", "Nutty/Cocoa"), ("Chocolate", "Cocoa"), ("Dark Chocolate", "Cocoa")],
            "🌶️ Spices": [("Spices", ""), ("Pungent", "Spices"), ("Pepper", "Spices"), ("Brown Spice", "Spices"), ("Anise", "Brown Spice"), ("Nutmeg", "Brown Spice"), ("Cinnamon", "Brown Spice"), ("Clove", "Brown Spice")],
            "🔥 Roasted": [("Roasted", ""), ("Pipe Tobacco", "Roasted"), ("Tobacco", "Roasted"), ("Burnt", "Roasted"), ("Acrid", "Burnt"), ("Ashy", "Burnt"), ("Smoky", "Burnt"), ("Brown Roast", "Burnt"), ("Cereal", "Roasted"), ("Grain", "Cereal"), ("Malt", "Cereal")],
            "🌿 Green/Vegetative": [("Green/Vegetative", ""), ("Olive Oil", "Green/Vegetative"), ("Raw", "Green/Vegetative"), ("Green Sub", "Green/Vegetative"), ("Under-ripe", "Green Sub"), ("Peapod", "Green Sub"), ("Fresh", "Green Sub"), ("Dark Green", "Green Sub"), ("Vegetative", "Green Sub"), ("Hay-like", "Green Sub"), ("Herb-like", "Green Sub"), ("Beany", "Green/Vegetative")],
            "🍷 Sour/Fermented": [("Sour/Fermented", ""), ("Sour", "Sour/Fermented"), ("Sour Aromatics", "Sour"), ("Acetic Acid", "Sour"), ("Butyric Acid", "Sour"), ("Isovaleric Acid", "Sour"), ("Citric Acid", "Sour"), ("Malic Acid", "Sour"), ("Alcohol/Fermented", "Sour/Fermented"), ("Winey", "Alcohol/Fermented"), ("Whiskey", "Alcohol/Fermented"), ("Fermented", "Alcohol/Fermented"), ("Overripe", "Alcohol/Fermented")],
            "🧪 Other/Defects": [("Other", ""), ("Chemical", "Other"), ("Rubber", "Chemical"), ("Skunky", "Chemical"), ("Petroleum", "Chemical"), ("Medicinal", "Chemical"), ("Salty", "Chemical"), ("Bitter", "Chemical"), ("Papery/Musty", "Other"), ("Phenolic", "Papery/Musty"), ("Meaty Brothy", "Papery/Musty"), ("Animalic", "Papery/Musty"), ("Musty/Earthy", "Papery/Musty"), ("Musty/Dusty", "Papery/Musty"), ("Moldy/Damp", "Papery/Musty"), ("Woody", "Papery/Musty"), ("Papery", "Papery/Musty"), ("Cardboard", "Papery/Musty"), ("Stale", "Papery/Musty")]
        }
        
        selected_data = wheel_map.get(family, wheel_map["🧪 Other/Defects"])
        df_wheel = pd.DataFrame(selected_data, columns=["Note", "Parent"])
        
        st.plotly_chart(px.sunburst(df_wheel, names='Note', parents='Parent', height=400), use_container_width=True)
        
        picks = st.multiselect("Finalize Sensory Profile Selection", list(df_wheel['Note']), key=f"ms_{st.session_state.ms_key}")
        for p in picks: st.session_state.master_notes.add(p)
        
        st.write("**Combined Map Basket:**")
        st.info(", ".join(st.session_state.master_notes) if st.session_state.master_notes else "No notes selected")
        
        if st.button("🗑️ Clear Map Basket (For Next Batch)"):
            st.session_state.master_notes.clear()
            st.session_state.ms_key += 1 
            st.rerun()

        st.markdown("---")
        cl_t = st.columns(3)
        with cl_t[0]: m_dry = st.number_input("Dry End (m)", key="m_d")
        with cl_t[1]: m_fc = st.number_input("FC Start (m)", key="m_f")
        with cl_t[2]: m_drop = st.number_input("Drop Time (m)", key="m_v")
        
        agtron = st.number_input("Agtron Score (QA)", value=0)
        
        cupping_score = 0.0
        st.markdown("##### ☕ Universal Digital Cupping Form")
        with st.expander("📝 Enter 10-Point Evaluation", expanded=True):
            sc_col1, sc_col2 = st.columns(2)
            with sc_col1:
                s_frag = st.number_input("Fragrance/Aroma", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_flav = st.number_input("Flavor", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_after = st.number_input("Aftertaste", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_acid = st.number_input("Acidity", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_body = st.number_input("Body", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
            with sc_col2:
                s_bal = st.number_input("Balance", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_unif = st.number_input("Uniformity (2pts/cup)", min_value=0, max_value=10, value=0, step=2)
                s_clean = st.number_input("Clean Cup (2pts/cup)", min_value=0, max_value=10, value=0, step=2)
                s_sweet = st.number_input("Sweetness (2pts/cup)", min_value=0, max_value=10, value=0, step=2)
                s_over = st.number_input("Overall", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                
            s_defect = st.number_input("Defect Penalty", min_value=0, max_value=20, value=0, step=2)
            eval_scores = [s_frag, s_flav, s_after, s_acid, s_body, s_bal, s_unif, s_clean, s_sweet, s_over]
            
            if sum(eval_scores) > 0:
                cupping_score = sum(eval_scores) - s_defect
                st.success(f"**Calculated Final Score: {cupping_score:.2f} SCA**")
                
        st.markdown("---")
        batch_notes = st.text_area("📝 General Batch Notes & Observations (Optional)")
        process_btn = st.button("🚀 FINALIZE BATCH REPORT", use_container_width=True)

    with col_out:
        st.markdown('<h2 class="section-header">📊 Jpresso Analysis Dashboard</h2>', unsafe_allow_html=True)
        
        if process_btn:
            if g_weight <= 0 or r_weight <= 0:
                st.error("🛑 DATA LOCK PREVENTED: You must enter Green Input and Roasted Output weights to finalize.")
            else:
                dev_time = m_drop - m_fc if m_drop > 0 and m_fc > 0 else 0
                dtr = (dev_time / m_drop * 100) if m_drop > 0 else 0.0
                w_loss = ((g_weight - r_weight) / g_weight * 100)
                t_cost = ((g_weight * g_cost) / r_weight) + 1.25 
                b_id = f"LOT-{datetime.now().strftime('%m%d%H%M')}"
                
                t_disp = f"{amb_temp}°C" if amb_temp.strip() else "N/A"
                h_disp = f"{humidity}% RH" if humidity.strip() else "N/A"
                op_disp = operator_name.strip() if operator_name.strip() else "Not Specified"
                
                st.session_state.last_analysis = {
                    "batch_id": b_id, "date": datetime.now().strftime('%Y-%m-%d %H:%M'), "operator": op_disp, "env": f"{t_disp} / {h_disp}",
                    "sku": sku_name, "roast_level": roast_level, "grade": q_grade,
                    "g_weight": g_weight, "r_weight": r_weight, "dtr": dtr, "w_loss": w_loss, "cost": t_cost, 
                    "agtron": agtron, "cupping": cupping_score,
                    "flavors": list(st.session_state.master_notes), "recipe": blend_recipe_display, "notes": batch_notes
                }
                
                st.session_state.batch_history.append({
                    "Batch ID": b_id, "Operator": op_disp, "SKU": sku_name, 
                    "Green (kg)": g_weight, "Roasted (kg)": r_weight,
                    "DTR (%)": round(dtr, 1), "Cost/kg": round(t_cost, 2), "SCA Score": round(cupping_score, 2)
                })
                st.rerun()

        if st.session_state.last_analysis:
            ana = st.session_state.last_analysis
            metric_html = f'<div class="metric-row"><div class="metric-item"><strong>DTR %</strong><br><div>{ana["dtr"]:.1f}%</div></div><div class="metric-item"><strong>Weight Loss</strong><br><div>{ana["w_loss"]:.1f}%</div></div><div class="metric-item"><strong>True Cost</strong><br><div>{ana["cost"]:.2f}</div></div></div>'
            st.markdown(metric_html, unsafe_allow_html=True)
            
            recipe_html = f'<p><strong>Recipe:</strong> {ana["recipe"]}</p>' if ana.get('recipe') else ''
            flavors_str = ', '.join(ana["flavors"]) if ana["flavors"] else 'None'
            score_display = f"{ana['cupping']:.2f}"
            notes_html = f'<p><strong>Notes:</strong> {ana["notes"]}</p>' if ana.get('notes') else ''
            
            spec_html = (
                f'<div class="spec-box">'
                f'<h4 style="color:#DAB07B;"><strong>🌟 JPRESSO PRODUCTION SPEC</strong></h4>'
                f'<p><strong>Batch ID:</strong> {ana["batch_id"]} | <strong>Operator:</strong> {ana["operator"]}</p>'
                f'<p><strong>Environment:</strong> {ana["env"]}</p>'
                f'<hr style="margin: 10px 0; border: 1px solid rgba(218,176,123,0.3);">'
                f'<p><strong>SKU / Bean:</strong> {ana["sku"]} ({ana["grade"]})</p>'
                f'<p><strong>Roast Profile:</strong> {ana["roast_level"]}</p>'
                f'{recipe_html}'
                f'<hr style="margin: 10px 0; border: 1px solid rgba(218,176,123,0.3);">'
                f'<p><strong>Green Input:</strong> {ana["g_weight"]} kg | <strong>Output:</strong> {ana["r_weight"]} kg</p>'
                f'<p><strong>Agtron:</strong> {ana["agtron"]} | <strong>QA Score:</strong> {score_display}</p>'
                f'<p><strong>Sensory Map:</strong> {flavors_str}</p>'
                f'{notes_html}'
                f'<hr style="margin: 10px 0; border: 1px solid rgba(218,176,123,0.3);">'
                f'<p><strong>Executive Summary:</strong> {ana["batch_id"]} is a {ana["roast_level"]} roast of {ana["sku"]}. It achieved a DTR of {ana["dtr"]:.1f}% with a {ana["w_loss"]:.1f}% weight loss, resulting in a landed cost of {ana["cost"]:.2f}/kg.</p>'
                f'</div>'
            )
            st.markdown(spec_html, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("### 📋 Session Batch Log")
            if st.session_state.batch_history:
                st.dataframe(pd.DataFrame(st.session_state.batch_history), use_container_width=True)
        else:
            st.info("👈 Key In Data To Generate Analysis.")

# ==========================================
# TAB 2: BRAND STORYTELLER (UNIVERSAL PROMPTS)
# ==========================================
with tab2:
    st.markdown('<h2 class="section-header">📱 Video Prompt Engine</h2>', unsafe_allow_html=True)
    st.write("Generate clean, comma-separated keywords optimized for CapCut, Runway, and Luma.")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### 🎬 Visual Universe")
        scene_setting = st.selectbox("Cinematic Environment", [
            "The Roastery Floor (Classic)", 
            "Modern Café (Urban)", 
            "High-Speed Racing (Adrenaline)", 
            "Outer Space / Cosmic (Sci-Fi)", 
            "Bustling Local Market (Cultural)", 
            "Urban Megacomplex (Cyberpunk/Corporate)",
            "Rugged Wilderness (Adventure)"
        ])
        
        emotion = st.selectbox("Visual Mood", [
            "Premium Moody",
            "High-Energy Bright",
            "Warm Cozy",
            "Cinematic Dramatic",
            "Neon-Lit Gritty",
            "Untamed Nature"
        ])
    with col_m2:
        st.markdown("#### 🎤 Brand Voice")
        target_audience = st.selectbox("Target Audience", ["B2B Wholesale (Café Owners)", "B2C Retail (Home Brewers)"])
        
        vibe = st.selectbox("Storytelling Tone", [
            "The Roasting Scientist (Technical, Precision, Data-Driven)", 
            "The Artistic Craftsman (Creative, Intuitive, Masterful)", 
            "The Origin Explorer (Nature, Ethical, Farm-to-Cup)",
            "The Rugged Explorer (Wild, Bold, Uncharted)"
        ])
        
    if st.button("✨ GENERATE CONTENT", use_container_width=True):
        
        cam_angles = [
            "Macro shot", "Slow-mo tracking shot", 
            "Handheld pan", "Low-angle reveal", 
            "Close-up", "Smooth push in"
        ]
        
        visual_sets = {
            "The Roastery Floor (Classic)": {
                "hooks": ["green coffee beans pouring into brass hopper", "blue flame igniting under steel drum"],
                "scenes": ["thick smoke billowing from cooling tray", "hands adjusting brass airflow dials"],
                "climaxes": ["golden espresso pouring into black cup", "brown beans spinning on cooling tray"]
            },
            "Modern Café (Urban)": {
                "hooks": ["busy coffee shop counter", "portafilter locking into espresso machine"],
                "scenes": ["barista pouring latte art swan", "sunlight hitting a steaming pour-over"],
                "climaxes": ["customer sipping cappuccino", "crema dripping from naked portafilter"]
            },
            "High-Speed Racing (Adrenaline)": {
                "hooks": ["race car drifting, leaving coffee bean trail", "pit-stop crew working fast under stadium lights"],
                "scenes": ["glowing car engine roaring", "racing helmet blur, rapid espresso pulls"],
                "climaxes": ["driver celebrating with espresso cup", "espresso pouring rapidly like fuel"]
            },
            "Outer Space / Cosmic (Sci-Fi)": {
                "hooks": ["coffee beans floating in zero-gravity spacecraft", "glowing nebula morphing into latte art"],
                "scenes": ["astronaut holding steaming coffee pouch", "glowing blue spaceship console"],
                "climaxes": ["robotic arm extracting espresso in zero-gravity", "coffee bean zooming out to galaxy"]
            },
            "Bustling Local Market (Cultural)": {
                "hooks": ["vibrant street market with spices", "local coffee master pulling cloth filter coffee"],
                "scenes": ["steam rising from boiling pots in narrow alley", "spices and green coffee in bamboo baskets"],
                "climaxes": ["aged hands handing over ceramic coffee cup", "coffee splashing over ice in busy market"]
            },
            "Urban Megacomplex (Cyberpunk/Corporate)": {
                "hooks": ["drone shot of futuristic glass megacomplex", "executive walking in corporate lobby with coffee"],
                "scenes": ["neon lights on wet asphalt outside coffee bar", "robotic arm boxing coffee bags"],
                "climaxes": ["power-walk through revolving doors", "espresso pouring in white sterile lab"]
            },
            "Rugged Wilderness (Adventure)": {
                "hooks": ["explorer on misty mountain holding camp mug", "roaring campfire in dark pine forest"],
                "scenes": ["pouring boiling water into titanium camp dripper", "hiking boots on rocks, coffee brewing on stone"],
                "climaxes": ["sipping coffee near massive waterfall", "steaming cup on mossy log, golden hour"]
            }
        }
        
        v_hooks = visual_sets[scene_setting]["hooks"]
        v_scenes = visual_sets[scene_setting]["scenes"]
        v_climaxes = visual_sets[scene_setting]["climaxes"]

        if "Scientist" in vibe:
            vo_hooks = ["Precision is our only metric.", "We don't guess, we calculate.", "The perfect cup starts with perfect thermodynamics.", "Airflow is everything."]
            vo_scenes = ["Every decimal point matters when locking in the Development Time Ratio.", "Managing the Rate of Rise isn't art—it's pure physics.", "Heat transfer dictates extraction. We control the heat."]
            vo_climaxes = ["This results in unparalleled consistency for your café.", "A flawless extraction, every single time.", "Data you can literally taste."]
        elif "Craftsman" in vibe:
            vo_hooks = ["Roasting coffee is a dance with fire.", "Patience, intuition, and absolute focus.", "A masterpiece forged in heat.", "Every batch is a work of art."]
            vo_scenes = ["We listen to the crack, watch the color shift, and guide the beans to their peak.", "Years of intuition condensed into this single roast.", "The drum spins, locking in the soul of the coffee."]
            vo_climaxes = ["Awaken your senses.", "A cup worthy of a master.", "Taste the culmination of absolute dedication."]
        elif "Explorer" in vibe and "Rugged" in vibe:
            vo_hooks = ["Not all who wander are lost. Some are just looking for the perfect cup.", "Born in the wild, brewed in the elements.", "Fuel for the uncharted path.", "Adventure doesn't wait for sunrise."]
            vo_scenes = ["Roasted to withstand the harshest environments and the longest treks.", "No baristas, no cafes. Just raw, unfiltered elements and pure extraction.", "Wherever the compass points, the roast follows."]
            vo_climaxes = ["Taste the wild.", "Conquer your morning, no matter where you wake up.", "Bold enough for the peaks, smooth enough for the journey."]
        else:
            vo_hooks = ["Every bean holds a thousand miles of history.", "From rich soil to your soul.", "Nature provides, we merely translate.", "Coffee in its purest form."]
            vo_scenes = ["Grown at high altitudes and hand-picked with absolute care.", "We respect the farmers by roasting with gentle, intentional heat.", "Preserving the true character of the earth in every batch."]
            vo_climaxes = ["Experience coffee exactly as nature intended.", "A beautiful journey in every sip.", "Honest, pure, and unapologetically real."]

        cta_visuals = [
            "barista handing coffee cup to camera",
            "premium wholesale coffee bag under spotlight",
            "customer taking a sip in moody room"
        ]
        
        if "B2B" in target_audience:
            ctas = ["Click the link in our bio to elevate your coffee program.", "DM us 'WHOLESALE' to get our beans in your cafe.", "Partner with true roasting excellence."]
        else:
            ctas = ["Tap below to order your first batch.", "Bring this premium experience to your morning ritual.", "Click the link in our bio and taste the difference today."]

        final_script = f"""HOOK
🎥 Video Prompt: {random.choice(cam_angles)}, {random.choice(v_hooks)}, {emotion} lighting, 8k, no text.
🎤 Voiceover: "{random.choice(vo_hooks)}"

PROCESS
🎥 Video Prompt: {random.choice(cam_angles)}, {random.choice(v_scenes)}, {emotion} aesthetic, 8k, no text.
🎤 Voiceover: "{random.choice(vo_scenes)}"

CLIMAX
🎥 Video Prompt: {random.choice(cam_angles)}, {random.choice(v_climaxes)}, {emotion} lighting, 8k, no text.
🎤 Voiceover: "{random.choice(vo_climaxes)}"

CALL TO ACTION
🎥 Video Prompt: {random.choice(cam_angles)}, {random.choice(cta_visuals)}, 8k, no text.
🎤 Voiceover: "{random.choice(ctas)}"
"""
        st.markdown("---")
        st.success("✅ **Prompts Ready!** Click the copy icon in the top right of the box below:")
        st.code(final_script, language="text")

# ==========================================
# TAB 3: AUTO-EVALUATION PORTAL (TRUE A4 MATRIX)
# ==========================================
with tab3:
    st.markdown('<h2 class="section-header">🎓 Objective Auto-Evaluation Portal</h2>', unsafe_allow_html=True)
    st.write("Generate objective, technical evaluations based solely on the core roasting metrics.")
    
    col_acad1, col_acad2 = st.columns(2)
    with col_acad1:
        student_name = st.text_input("Roaster / Student Name", placeholder="e.g., Jason")
        machine_used = st.selectbox("Training Machine", ["1kg Bideli", "5kg Has Garanti", "Santoker Air Roaster"])
        target_bean = st.text_input("Training Bean", placeholder="e.g., Colombia Supremo")
    
    with col_acad2:
        target_profile = st.selectbox("Target Roast Profile", ["Light (Filter - 12-16% DTR)", "Medium (Omni - 18-22% DTR)", "Dark (Espresso - 23-27% DTR)"])
        student_dtr = st.number_input("Achieved DTR (%)", value=15.0, step=0.5)

    critique = ""
    gen_score = 0
    
    if "Light" in target_profile:
        if student_dtr < 12: 
            critique = "DTR is too short. The roast risks underdeveloped, grassy, and highly astringent notes. Recommend lowering heat application slightly approaching First Crack to extend the development phase."
            gen_score = 75
        elif 12 <= student_dtr <= 16: 
            critique = "Excellent technical precision. The DTR is locked perfectly in the optimal range for a bright, floral, and sweet Light roast. Ideal heat management demonstrated during the crucial development phase."
            gen_score = 95
        else: 
            critique = "DTR exceeded the Light target threshold. The profile has shifted into medium territory, likely masking delicate acidity with heavy caramelization. Recommend dropping earlier to preserve origin character."
            gen_score = 82
    elif "Medium" in target_profile:
        if student_dtr < 18: 
            critique = "DTR is running too fast for a Medium target. The acidity may be too sharp and unbalanced for espresso applications. Extend development time by slightly reducing gas pressure earlier in the roast."
            gen_score = 80
        elif 18 <= student_dtr <= 22: 
            critique = "Perfect Medium development. The achieved DTR indicates a highly balanced cup with rich polymerized sugars and tamed acidity. Highly suitable for professional Omni or Espresso applications."
            gen_score = 96
        else: 
            critique = "DTR is running dangerously long. The roast risks flat, baked notes and a total loss of vibrant origin character. Increase airflow or execute the drop earlier to maintain cup structure."
            gen_score = 80
    else: 
        if student_dtr < 23: 
            critique = "Development is too fast for a Dark target, risking a severe sour-bitter imbalance. Stretch the development phase longer to fully polymerize the sugars and build heavy mouthfeel."
            gen_score = 78
        elif 23 <= student_dtr <= 27: 
            critique = "Optimal Dark profile achieved. The extended DTR ensures low acidity, heavy body, and rich chocolate/roast notes without tipping the bean temperature into aggressive ashiness."
            gen_score = 94
        else: 
            critique = "DTR is aggressively high. Severe risk of burnt, ashy notes and heavy oil exudation upon cooling. Cut heat much earlier to prevent thermal runaway in the drum."
            gen_score = 70

    st.markdown("---")
    st.info(f"**🤖 Generated AI Evaluation:** {critique}")
        
    if st.button("🏅 Generate Formal Evaluation Certificate", use_container_width=True):
        if student_name and target_bean:
            
            logo_b64 = get_base64_image("Jpresso Gold Transparent.png")
            if logo_b64:
                logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Jpresso Logo" width="180" style="margin-bottom: 5px;">'
            else:
                logo_html = f'<div class="no-print" style="color:red; font-size:12px; margin-bottom:10px;">[Note: Could not find "Jpresso Gold Transparent.png" in your app folder.]</div><h1 style="color:#d4af37; margin:0;">BIG JPRESSO</h1>'

            # --- THE EXACT TRUE A4 MATRIX CSS FIX INJECTED HERE ---
            iframe_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    /* ZERO MARGIN OVERRIDE & EXACT A4 DIMENSIONS */
                    @page {{ size: A4 portrait; margin: 0; }}
                    * {{ box-sizing: border-box; }}
                    
                    body, html {{ 
                        background-color: #fcfaff; 
                        margin: 0; 
                        padding: 0; 
                        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
                        -webkit-print-color-adjust: exact; 
                        print-color-adjust: exact; 
                    }}
                    
                    /* Web Preview Container */
                    .cert-container {{
                        width: 210mm !important;
                        height: 297mm !important;
                        max-height: 297mm !important;
                        margin: 20px auto !important;
                        background-color: #ffffff;
                        padding: 10mm;
                        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                        overflow: hidden !important;
                    }}
                    
                    /* Printer Target Container */
                    @media print {{
                        .no-print {{ display: none !important; }}
                        body {{ background-color: white !important; }}
                        .cert-container {{ 
                            width: 210mm !important; 
                            height: 296mm !important; 
                            max-height: 296mm !important;
                            max-width: none !important; 
                            margin: 0 !important; 
                            padding: 10mm !important; /* Safe print margin */
                            box-shadow: none !important; 
                            page-break-after: avoid; 
                            page-break-inside: avoid; 
                            overflow: hidden !important;
                        }}
                    }}

                    /* Flexible Interior Borders */
                    .border-outer {{
                        border: 10px solid #2b1d42;
                        width: 100%;
                        height: 100%;
                        padding: 10px;
                        box-sizing: border-box;
                    }}
                    
                    .border-inner {{
                        border: 3px solid #d4af37;
                        width: 100%;
                        height: 100%;
                        padding: 20px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: space-between; /* This dynamically stretches content evenly! */
                        text-align: center;
                        position: relative;
                        box-sizing: border-box;
                    }}
                </style>
            </head>
            <body>
                <div class="no-print" style="margin-bottom: 15px; text-align: center;">
                    <button onclick="window.print()" style="background-color: #d4af37; color: #111; padding: 12px 24px; font-size: 16px; border: 2px solid #b8962e; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                        🖨️ CLICK HERE TO PRINT CERTIFICATE
                    </button>
                </div>
                
                <div class="cert-container">
                    <div class="border-outer">
                        <div class="border-inner">
                            
                            <div>
                                {logo_html}
                                <h1 style="color: #2b1d42; font-family: 'Georgia', serif; font-size: 36px; margin: 10px 0 5px 0; text-transform: uppercase; letter-spacing: 2px;">Academy Evaluation</h1>
                                <h3 style="color: #333; font-size: 16px; letter-spacing: 4px; margin: 0; font-weight: 400;">CERTIFICATE OF ANALYSIS</h3>
                            </div>
                            
                            <div>
                                <p style="font-size: 16px; color: #555; margin-bottom: 5px;">This formally certifies the technical audit of</p>
                                <h2 style="font-size: 32px; color: #111; border-bottom: 2px solid #d4af37; display: inline-block; padding: 0 20px 5px 20px; margin: 10px 0; font-family: 'Georgia', serif;">{student_name.upper()}</h2>
                                <p style="font-size: 16px; color: #444; margin: 10px 40px; line-height: 1.5;">has completed a formal roast evaluation protocol. The candidate operated the <strong>{machine_used}</strong>, targeting a <strong>{target_profile.split('(')[0].strip()}</strong> profile utilizing <strong>{target_bean}</strong>.</p>
                            </div>
                            
                            <div style="width: 85%; padding: 20px; background-color: #fcfaff; border-left: 5px solid #d4af37; text-align: left; margin: 0 auto;">
                                <p style="margin: 3px 0; font-size: 15px;"><strong>Target Profile:</strong> {target_profile}</p>
                                <p style="margin: 3px 0; font-size: 15px;"><strong>Achieved DTR:</strong> {student_dtr}%</p>
                                <p style="margin: 3px 0; font-size: 15px;"><strong>Calculated Grade:</strong> {gen_score} / 100</p>
                                <p style="margin: 15px 0 5px 0; font-size: 15px; color: #2b1d42;"><strong>System Evaluation & Critique:</strong></p>
                                <p style="font-style: italic; color: #333; margin: 0; font-size: 15px;">"{critique}"</p>
                            </div>
                            
                            <div style="width: 100%;">
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td style="width: 50%; text-align: center; vertical-align: bottom; padding: 5px;">
                                            <p style="font-size: 16px; margin: 0 0 10px 0; color: #111;">{datetime.now().strftime('%d %B %Y')}</p>
                                            <div style="border-top: 1px solid #999; width: 60%; margin: 0 auto;"></div>
                                            <p style="font-size: 12px; color: #666; margin: 5px 0 0 0; text-transform: uppercase; letter-spacing: 1px;">Date of Audit</p>
                                        </td>
                                        <td style="width: 50%; text-align: center; vertical-align: bottom; padding: 5px;">
                                            <p style="font-family: 'Brush Script MT', cursive; font-size: 28px; color: #111; margin: 0 0 5px 0; line-height: 1;">Jason</p>
                                            <div style="border-top: 1px solid #999; width: 60%; margin: 0 auto;"></div>
                                            <p style="font-size: 14px; color: #111; margin: 5px 0 0 0; font-weight: bold;">Jason</p>
                                            <p style="font-size: 12px; color: #666; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Chief Coffee Officer</p>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            st.markdown("---")
            # Set Streamlit iframe height larger to accommodate the exact A4 screen scaling
            components.html(iframe_html, height=1250, scrolling=False)
            
            st.markdown("---")
            st.download_button(
                label="📥 DOWNLOAD HTML CERTIFICATE (Failsafe)",
                data=iframe_html,
                file_name=f"Jpresso_Certificate_{student_name.replace(' ', '_')}.html",
                mime="text/html"
            )
            
        else:
            st.error("Please enter a Roaster Name and Training Bean to generate an evaluation.")
