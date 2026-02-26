import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import re
import os
import base64
import streamlit.components.v1 as components 

# --- v173.0 FULL STEALTH CSS INJECTION ---
# This block forcibly hides the Header, GitHub icons, and "Manage App" button
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

# --- CONFIGURATION & BRANDING ---
st.set_page_config(page_title="Jpresso Roastery OS", layout="wide", initial_sidebar_state="expanded")

# --- MASTER STABILITY CSS ---
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
    .prompt-box { background-color: #f4f0ff; border-left: 5px solid #6a1b9a; padding: 20px; border-radius: 8px; font-family: 'Courier New', Courier, monospace; font-size: 14px; white-space: pre-wrap; line-height: 1.5; color: #333; border: 1px solid #d1c4e9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 Jpresso Roastery Intelligence v173.0")
st.caption("Full Stealth Build: UI Elements Scrubbed & Secured")

# --- PERSISTENT STATE ---
if 'batch_history' not in st.session_state: st.session_state.batch_history = []
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'master_notes' not in st.session_state: st.session_state.master_notes = set()
if 'ms_key' not in st.session_state: st.session_state.ms_key = 0 

# --- SIDEBAR: AUDITOR ---
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

# --- TAB 1: PRODUCTION ---
with tab1:
    col_in, col_out = st.columns(2)
    with col_in:
        st.markdown('<h2 class="section-header">📦 Production Core</h2>', unsafe_allow_html=True)
        col_env1, col_env2, col_env3 = st.columns(3)
        with col_env1: operator_name = st.text_input("Roaster Name")
        with col_env2: amb_temp = st.text_input("Amb. Temp (°C)")
        with col_env3: humidity = st.text_input("Humidity (%)")
        st.markdown("---")
        q_grade = st.selectbox("Quality Standard", ["Specialty Grade", "Commercial Grade"])
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
        family = st.selectbox("Flavor Family", ["🍎 Fruity", "🌸 Floral", "🍯 Sweet", "🍫 Nutty/Cocoa", "🌶️ Spices", "🔥 Roasted", "🌿 Green", "🧪 Other", "🍷 Sour"])
        wheel_map = {"🍎 Fruity": [("Fruity", ""), ("Berry", "Fruity"), ("Citrus", "Fruity")], "🌸 Floral": [("Floral", ""), ("Jasmine", "Floral")], "🍫 Nutty/Cocoa": [("Nutty", ""), ("Chocolate", "Nutty")], "🍯 Sweet": [("Sweet", ""), ("Caramel", "Sweet")]}
        selected_data = wheel_map.get(family, [("Other", "")])
        df_wheel = pd.DataFrame(selected_data, columns=["Note", "Parent"])
        st.plotly_chart(px.sunburst(df_wheel, names='Note', parents='Parent', height=400), use_container_width=True)
        picks = st.multiselect("Sensory Profile", list(df_wheel['Note']), key=f"ms_{st.session_state.ms_key}")
        for p in picks: st.session_state.master_notes.add(p)
        st.info(", ".join(st.session_state.master_notes) if st.session_state.master_notes else "No notes")
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
        st.markdown("##### ☕ Cupping Evaluation")
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

# --- TAB 2: STORYTELLER ---
with tab2:
    st.markdown('<h2 class="section-header">📱 Video Prompt Engine</h2>', unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        scene_setting = st.selectbox("Environment", ["The Roastery Floor (Classic)", "High-Speed Racing (Adrenaline)", "Rugged Wilderness (Adventure)"])
        emotion = st.selectbox("Mood", ["Premium Moody", "Untamed Nature"])
    with col_m2:
        target_audience = st.selectbox("Audience", ["B2B Wholesale", "B2C Retail"])
        vibe = st.selectbox("Tone", ["The Roasting Scientist", "The Rugged Explorer"])
    if st.button("✨ GENERATE CONTENT", use_container_width=True):
        visuals = {"hooks": ["coffee beans pouring into hopper", "explorer holding camp mug"], "scenes": ["smoke from cooling tray", "pouring boiling water into titanium camp dripper"]}
        final_script = f"HOOK\n🎥 Video Prompt: Macro shot, {random.choice(visuals['hooks'])}, {emotion} lighting, 8k, no text.\n🎤 Voiceover: 'Precision is everything.'\n\nPROCESS\n🎥 Video Prompt: {random.choice(visuals['scenes'])}, 8k, no text."
        st.code(final_script, language="text")

# --- TAB 3: CERTIFICATE (TRUE A4 MATRIX) ---
with tab3:
    st.markdown('<h2 class="section-header">🎓 Auto-Evaluation Portal</h2>', unsafe_allow_html=True)
    st_name = st.text_input("Student Name")
    st_bean = st.text_input("Bean")
    st_dtr = st.number_input("DTR (%)", value=15.0)
    if st.button("🏅 Generate Certificate", use_container_width=True) and st_name and st_bean:
        logo_b64 = get_base64_image("Jpresso Gold Transparent.png")
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="180">' if logo_b64 else '<h1>BIG JPRESSO</h1>'
        iframe_html = f"""<!DOCTYPE html><html><head><style>@page {{ size: A4 portrait; margin: 0; }} body, html {{ background-color: #fcfaff; margin: 0; padding: 0; font-family: sans-serif; print-color-adjust: exact; }} .cert-container {{ width: 210mm; height: 296mm; margin: 0 auto; background: #fff; padding: 15mm; }} .border-outer {{ border: 10px solid #2b1d42; height: 100%; padding: 5mm; }} .border-inner {{ border: 3px solid #d4af37; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; padding: 10mm; }}</style></head><body><div class="cert-container"><div class="border-outer"><div class="border-inner"><div>{logo_html}<h1 style="color:#2b1d42;">Academy Evaluation</h1></div><div><h2>{st_name.upper()}</h2><p>Completed roast audit utilizing {st_bean}.</p></div><div style="background:#fcfaff; padding:10mm; border-left:5mm solid #d4af37; text-align:left; width:80%;"><p><strong>Achieved DTR:</strong> {st_dtr}%</p></div><div><button onclick="window.print()" style="background:#d4af37; padding:5mm; cursor:pointer;">🖨️ PRINT</button></div></div></div></div></body></html>"""
        components.html(iframe_html, height=1200, scrolling=False)
