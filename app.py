import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import os
import base64
import streamlit.components.v1 as components 

# --- v175.0 FULL STEALTH CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stHeader"] {display:none;}
    </style>
    """, unsafe_allow_html=True)

# --- SECURITY: MASTER PASSWORD LOCK ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Jpresso Intelligence OS")
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
    except Exception: pass
    return None

# --- CONFIGURATION ---
st.set_page_config(page_title="Jpresso Roastery OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fcfaff; }
    .section-header { color: #6a1b9a; border-bottom: 2px solid #ffd700; padding-bottom: 5px; margin-bottom: 20px; font-weight: 700; }
    [data-testid="column"]:nth-of-type(2) {
        border-left: 2px solid #6a1b9a;
        padding-left: 40px !important;
        display: flex;
        flex-direction: column;
        justify-content: flex-start !important; 
    }
    .metric-row { display: flex; justify-content: space-around; align-items: center; background: white; padding: 15px; border-radius: 12px; border: 1px solid #6a1b9a; margin-bottom: 20px; }
    .metric-item { text-align: center; flex: 1; border-right: 1px solid #eee; }
    .metric-item:last-child { border-right: none; }
    .cost-card { background-color: #fdf2f2; border: 1px solid #feb2b2; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .spec-box { background-color: #ffffff; border-left: 5px solid #6a1b9a; padding: 20px; border-radius: 4px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 15px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 Jpresso Roastery Intelligence v175.0")
st.caption("The Master Key: Full Sensory, Storyteller & A4 Matrix Restored")

# --- PERSISTENT STATE ---
if 'batch_history' not in st.session_state: st.session_state.batch_history = []
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'master_notes' not in st.session_state: st.session_state.master_notes = set()
if 'ms_key' not in st.session_state: st.session_state.ms_key = 0 

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h2 class="section-header">📈 Daily Audit</h2>', unsafe_allow_html=True)
    c_green = sum(float(b.get('Green (kg)', 0.0)) for b in st.session_state.batch_history)
    c_roasted = sum(float(b.get('Roasted (kg)', 0.0)) for b in st.session_state.batch_history)
    st.metric("Green Used Today", f"{c_green:.2f} kg")
    st.metric("Roasted Today", f"{c_roasted:.2f} kg")
    if st.session_state.batch_history:
        df_history = pd.DataFrame(st.session_state.batch_history)
        st.download_button(label="💾 DOWNLOAD DATA (CSV)", data=df_history.to_csv(index=False), file_name=f"Jpresso_Audit_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    if st.button("♻️ RESET SESSION", use_container_width=True): 
        st.session_state.clear()
        st.rerun()

tab1, tab2, tab3 = st.tabs(["📦 Production Ledger", "📱 Brand Storyteller", "🎓 Auto-Evaluation Portal"])

# ==========================================
# TAB 1: PRODUCTION LEDGER (RESTORED)
# ==========================================
with tab1:
    col_in, col_out = st.columns(2)
    with col_in:
        st.markdown('<h2 class="section-header">📦 Production Core</h2>', unsafe_allow_html=True)
        col_env1, col_env2, col_env3 = st.columns(3)
        with col_env1: operator_name = st.text_input("Roaster Name")
        with col_env2: amb_temp = st.text_input("Amb. Temp (°C)")
        with col_env3: humidity = st.text_input("Humidity (%)")
        st.markdown("---")
        g_weight = st.number_input("Green Input (kg)", step=0.01)
        r_weight = st.number_input("Roasted Output (kg)", step=0.01)
        mode = st.radio("Mode", ["Single Origin", "Blend Architect"], horizontal=True)
        if mode == "Single Origin":
            sku_name = st.text_input("Bean Name / SKU")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
            g_cost = st.number_input("Green Cost (Per kg)", step=0.01)
        else:
            sku_name = st.text_input("Master Blend SKU")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
            blend_sum = []
            for i in range(1, 3):
                with st.expander(f"Origin {i}"):
                    c_r = st.slider(f"Ratio {i} (%)", 0, 100, 0)
                    c_c = st.number_input(f"Cost {i}", step=0.01)
                    if c_r > 0: blend_sum.append(c_c * (c_r/100))
            g_cost = sum(blend_sum)
            st.markdown(f'<div class="cost-card"><strong>💰 Weighted Cost:</strong> {g_cost:.2f} /kg</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎡 9-Wheel Sensory Auditor")
        family = st.selectbox("Flavor Family", ["🍎 Fruity", "🌸 Floral", "🍯 Sweet", "🍫 Nutty/Cocoa", "🌶️ Spices", "🔥 Roasted", "🌿 Green/Veg", "🧪 Other", "🍷 Sour"])
        
        wheel_map = {
            "🍎 Fruity": [("Fruity", ""), ("Berry", "Fruity"), ("Blackberry", "Berry"), ("Raspberry", "Berry"), ("Blueberry", "Berry"), ("Strawberry", "Berry"), ("Dried Fruit", "Fruity"), ("Raisin", "Dried Fruit"), ("Prune", "Dried Fruit"), ("Citrus Fruit", "Fruity"), ("Grapefruit", "Citrus Fruit"), ("Orange", "Citrus Fruit"), ("Lemon", "Citrus Fruit"), ("Lime", "Citrus Fruit")],
            "🌸 Floral": [("Floral", ""), ("Black Tea", "Floral"), ("Chamomile", "Floral"), ("Rose", "Floral"), ("Jasmine", "Floral")],
            "🍯 Sweet": [("Sweet", ""), ("Brown Sugar", "Sweet"), ("Molasses", "Brown Sugar"), ("Maple Syrup", "Brown Sugar"), ("Caramelized", "Brown Sugar"), ("Honey", "Brown Sugar"), ("Vanilla", "Sweet")],
            "🍫 Nutty/Cocoa": [("Nutty/Cocoa", ""), ("Nutty", "Nutty/Cocoa"), ("Hazelnut", "Nutty"), ("Almond", "Nutty"), ("Cocoa", "Nutty/Cocoa"), ("Chocolate", "Cocoa")],
            "🌶️ Spices": [("Spices", ""), ("Pepper", "Spices"), ("Cinnamon", "Spices"), ("Clove", "Spices")],
            "🔥 Roasted": [("Roasted", ""), ("Tobacco", "Roasted"), ("Burnt", "Roasted"), ("Smoky", "Burnt"), ("Cereal", "Roasted")],
            "🌿 Green/Veg": [("Green/Veg", ""), ("Olive Oil", "Green/Veg"), ("Raw", "Green/Veg"), ("Herbal", "Green/Veg")],
            "🍷 Sour": [("Sour/Fermented", ""), ("Winey", "Sour/Fermented"), ("Whiskey", "Sour/Fermented"), ("Fermented", "Sour/Fermented")],
            "🧪 Other": [("Other", ""), ("Chemical", "Other"), ("Medicinal", "Chemical"), ("Musty/Earthy", "Other"), ("Woody", "Other")]
        }
        
        selected_data = wheel_map.get(family, [("Other", "")])
        df_wheel = pd.DataFrame(selected_data, columns=["Note", "Parent"])
        st.plotly_chart(px.sunburst(df_wheel, names='Note', parents='Parent', height=400), use_container_width=True)
        picks = st.multiselect("Pick Notes", list(df_wheel['Note']), key=f"ms_{st.session_state.ms_key}")
        for p in picks: st.session_state.master_notes.add(p)
        st.info(", ".join(st.session_state.master_notes) if st.session_state.master_notes else "No notes selected")
        if st.button("🗑️ Clear Map"):
            st.session_state.master_notes.clear()
            st.session_state.ms_key += 1 
            st.rerun()

        st.markdown("---")
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1: m_dry = st.number_input("Dry End (m)")
        with col_t2: m_fc = st.number_input("FC Start (m)")
        with col_t3: m_drop = st.number_input("Drop Time (m)")
        agtron = st.number_input("Agtron Score", value=0)
        st.markdown("##### ☕ Evaluation")
        cupping_score = st.slider("SCA Score", 0.0, 100.0, 80.0, 0.25)
        batch_notes = st.text_area("Observations")
        process_btn = st.button("🚀 FINALIZE BATCH REPORT", use_container_width=True)

    with col_out:
        st.markdown('<h2 class="section-header">📊 Jpresso Analysis Dashboard</h2>', unsafe_allow_html=True)
        if process_btn and g_weight > 0 and r_weight > 0:
            dtr = ((m_drop - m_fc) / m_drop * 100) if m_drop > 0 else 0.0
            w_loss = ((g_weight - r_weight) / g_weight * 100)
            t_cost = ((g_weight * g_cost) / r_weight) + 1.25
            b_id = f"LOT-{datetime.now().strftime('%m%d%H%M')}"
            st.session_state.last_analysis = {"batch_id": b_id, "sku": sku_name, "roast_level": roast_level, "dtr": dtr, "w_loss": w_loss, "cost": t_cost, "agtron": agtron, "cupping": cupping_score, "flavors": list(st.session_state.master_notes)}
            st.session_state.batch_history.append({"Batch ID": b_id, "SKU": sku_name, "DTR (%)": round(dtr, 1), "Cost/kg": round(t_cost, 2)})
            st.rerun()
        if st.session_state.last_analysis:
            ana = st.session_state.last_analysis
            st.markdown(f'<div class="metric-row"><div class="metric-item"><strong>DTR</strong><br>{ana["dtr"]:.1f}%</div><div class="metric-item"><strong>Loss</strong><br>{ana["w_loss"]:.1f}%</div><div class="metric-item"><strong>Cost</strong><br>{ana["cost"]:.2f}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-box"><h4>🌟 JPRESSO PRODUCTION SPEC</h4><p><strong>Batch ID:</strong> {ana["batch_id"]}</p><p><strong>SKU:</strong> {ana["sku"]}</p><p><strong>Profile:</strong> {ana["roast_level"]}</p><p><strong>Sensory:</strong> {", ".join(ana["flavors"])}</p></div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.batch_history), use_container_width=True)

# ==========================================
# TAB 2: BRAND STORYTELLER (RESTORED)
# ==========================================
with tab2:
    st.markdown('<h2 class="section-header">📱 Video Prompt Engine</h2>', unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        scene_setting = st.selectbox("Environment", ["The Roastery Floor (Classic)", "Modern Café (Urban)", "High-Speed Racing (Adrenaline)", "Outer Space (Sci-Fi)", "Rugged Wilderness (Adventure)"])
        emotion = st.selectbox("Visual Mood", ["Premium Moody", "High-Energy Bright", "Warm Cozy", "Neon-Lit Gritty", "Untamed Nature"])
    with col_m2:
        target_audience = st.selectbox("Audience", ["B2B Wholesale (Café Owners)", "B2C Retail (Home Brewers)"])
        vibe = st.selectbox("Tone", ["The Roasting Scientist", "The Artistic Craftsman", "The Origin Explorer", "The Rugged Explorer"])
    
    if st.button("✨ GENERATE CONTENT", use_container_width=True):
        visual_sets = {
            "The Roastery Floor (Classic)": {"hooks": ["pouring green beans into hopper", "blue flame igniting"], "scenes": ["smoke from cooling tray", "adjusting brass dials"]},
            "High-Speed Racing (Adrenaline)": {"hooks": ["race car drifting, leaving bean trail", "pit-stop crew working"], "scenes": ["engine roaring, glowing heat", "helmet blur, rapid pulls"]},
            "Rugged Wilderness (Adventure)": {"hooks": ["explorer on misty mountain", "campfire sparks in dark forest"], "scenes": ["pouring boiling water into camp dripper", "brewing on a large stone"]}
        }
        vo_hooks = ["Precision is our only metric.", "Fuel for the uncharted path.", "A masterpiece forged in heat."]
        
        v_set = visual_sets.get(scene_setting, visual_sets["The Roastery Floor (Classic)"])
        final_script = f"""HOOK
🎥 Video Prompt: Macro shot, {random.choice(v_set['hooks'])}, {emotion} lighting, 8k, no text.
🎤 Voiceover: "{random.choice(vo_hooks)}"

PROCESS
🎥 Video Prompt: Slow-mo tracking, {random.choice(v_set['scenes'])}, {emotion} aesthetic, 8k, no text.
🎤 Voiceover: "Data you can literally taste."

CALL TO ACTION
🎥 Video Prompt: Handheld pan, customer taking a sip, 8k, no text.
🎤 Voiceover: "Click the link in our bio to elevate your morning ritual."
"""
        st.code(final_script, language="text")

# ==========================================
# TAB 3: AUTO-EVALUATION PORTAL (RESTORED)
# ==========================================
with tab3:
    st.markdown('<h2 class="section-header">🎓 Auto-Evaluation Portal</h2>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st_name = st.text_input("Roaster Name", placeholder="e.g. Jason")
        st_bean = st.text_input("Training Bean", placeholder="e.g. Colombia Supremo")
    with col_e2:
        st_profile = st.selectbox("Target Profile", ["Light (Filter - 12-16% DTR)", "Medium (Omni - 18-22% DTR)", "Dark (Espresso - 23-27% DTR)"])
        st_dtr = st.number_input("Achieved DTR (%)", value=15.0, step=0.1)

    if st.button("🏅 Generate Formal Certificate", use_container_width=True) and st_name and st_bean:
        logo_b64 = get_base64_image("Jpresso Gold Transparent.png")
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="180">' if logo_b64 else '<h1>BIG JPRESSO</h1>'
        
        iframe_html = f"""
        <!DOCTYPE html><html><head><style>
        @page {{ size: A4 portrait; margin: 0; }}
        body {{ font-family: sans-serif; margin: 0; padding: 0; background: #fcfaff; print-color-adjust: exact; }}
        .cert-container {{ width: 210mm; height: 296mm; margin: 0 auto; background: #fff; padding: 10mm; box-sizing: border-box; }}
        .border-outer {{ border: 10px solid #2b1d42; height: 100%; padding: 10px; box-sizing: border-box; }}
        .border-inner {{ border: 3px solid #d4af37; height: 100%; padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; box-sizing: border-box; }}
        </style></head><body>
        <div class="cert-container"><div class="border-outer"><div class="border-inner">
            <div>{logo_html}<h1 style="color:#2b1d42; font-size:36px; margin:10px 0;">ACADEMY EVALUATION</h1><h3 style="letter-spacing:4px;">CERTIFICATE OF ANALYSIS</h3></div>
            <div><p>This formally certifies the technical audit of</p><h2 style="font-size:32px; border-bottom:2px solid #d4af37; display:inline-block; padding:0 20px;">{st_name.upper()}</h2><p>Completed a formal roast evaluation targeting {st_profile} utilizing {st_bean}.</p></div>
            <div style="background:#fcfaff; padding:20px; border-left:5px solid #d4af37; text-align:left; width:80%;">
                <p><strong>Achieved DTR:</strong> {st_dtr}%</p>
                <p><strong>Status:</strong> Technical Requirements Met</p>
            </div>
            <div style="width:100%; display:flex; justify-content:space-around; align-items:flex-end;">
                <div><p style="margin:0;">{datetime.now().strftime('%d %B %Y')}</p><hr><p style="font-size:12px;">DATE OF AUDIT</p></div>
                <div><p style="font-family:cursive; font-size:24px; margin:0;">Jason</p><hr><p style="font-size:12px;">CHIEF COFFEE OFFICER</p></div>
            </div>
            <div class="no-print"><button onclick="window.print()" style="background:#d4af37; padding:10px 20px; border:none; cursor:pointer; font-weight:bold;">🖨️ CLICK TO PRINT A4</button></div>
        </div></div></div></body></html>
        """
        st.markdown("---")
        components.html(iframe_html, height=1200, scrolling=False)
