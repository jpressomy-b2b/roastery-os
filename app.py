import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import os
import base64
import streamlit.components.v1 as components 

# --- v177.0 STEALTH CSS ---
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

st.title("🔥 Jpresso Roastery Intelligence v177.0")
st.caption("Final Equilibrium: Restored Storyteller & Guaranteed A4 Print Fit")

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
    st.metric("Total Green Today", f"{c_green:.2f} kg")
    st.metric("Total Roasted Today", f"{c_roasted:.2f} kg")
    if st.session_state.batch_history:
        df_history = pd.DataFrame(st.session_state.batch_history)
        st.download_button(label="💾 DOWNLOAD CSV", data=df_history.to_csv(index=False), file_name=f"Jpresso_Audit_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    if st.button("♻️ RESET SESSION", use_container_width=True): 
        st.session_state.clear()
        st.rerun()

tab1, tab2, tab3 = st.tabs(["📦 Production Ledger", "📱 Brand Storyteller", "🎓 Auto-Evaluation Portal"])

# ==========================================
# TAB 1: PRODUCTION LEDGER
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
        g_weight = st.number_input("Green Input (kg)", value=0.0, step=0.01)
        r_weight = st.number_input("Roasted Output (kg)", value=0.0, step=0.01)
        mode = st.radio("Mode", ["Single Origin", "Blend Architect"], horizontal=True)
        if mode == "Single Origin":
            sku_name = st.text_input("Bean SKU")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
            g_cost = st.number_input("Green Cost/kg", value=0.0, step=0.01)
            blend_recipe = ""
        else:
            sku_name = st.text_input("Blend SKU")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
            blend_sum = []
            for i in range(1, 4):
                with st.expander(f"Origin {i}"):
                    c_r = st.slider(f"Ratio {i} (%)", 0, 100, 0)
                    c_c = st.number_input(f"Cost {i}", value=0.0, step=0.01)
                    if c_r > 0: blend_sum.append(c_c * (c_r/100))
            g_cost = sum(blend_sum)
            blend_recipe = "Custom Blend"
            st.markdown(f'<div class="cost-card">💰 Weighted Cost: {g_cost:.2f} /kg</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎡 9-Wheel Sensory Auditor")
        family = st.selectbox("📥 Select Family", ["🍎 Fruity", "🌸 Floral", "🍯 Sweet", "🍫 Nutty/Cocoa", "🌶️ Spices", "🔥 Roasted", "🌿 Green", "🧪 Other", "🍷 Sour"])
        wheel_map = {
            "🍎 Fruity": [("Fruity", ""), ("Berry", "Fruity"), ("Dried Fruit", "Fruity"), ("Citrus", "Fruity")],
            "🌸 Floral": [("Floral", ""), ("Jasmine", "Floral"), ("Rose", "Floral")],
            "🍫 Nutty/Cocoa": [("Nutty", ""), ("Chocolate", "Nutty")],
            "🍯 Sweet": [("Sweet", ""), ("Caramel", "Sweet"), ("Honey", "Sweet")]
        }
        selected_data = wheel_map.get(family, [("Other", "")])
        df_wheel = pd.DataFrame(selected_data, columns=["Note", "Parent"])
        st.plotly_chart(px.sunburst(df_wheel, names='Note', parents='Parent', height=400), use_container_width=True)
        picks = st.multiselect("Pick Sensory Notes", list(df_wheel['Note']), key=f"ms_{st.session_state.ms_key}")
        for p in picks: st.session_state.master_notes.add(p)
        st.info(", ".join(st.session_state.master_notes) if st.session_state.master_notes else "No notes selected")
        if st.button("🗑️ Clear Map"):
            st.session_state.master_notes.clear()
            st.session_state.ms_key += 1 
            st.rerun()

        st.markdown("---")
        col_t = st.columns(3)
        with col_t[0]: m_dry = st.number_input("Dry End (m)")
        with col_t[1]: m_fc = st.number_input("FC Start (m)")
        with col_t[2]: m_drop = st.number_input("Drop Time (m)")
        agtron = st.number_input("Agtron Score", value=0)
        cupping_score = st.slider("Cupping Score", 0.0, 100.0, 80.0, 0.25)
        process_btn = st.button("🚀 FINALIZE BATCH REPORT", use_container_width=True)

    with col_out:
        st.markdown('<h2 class="section-header">📊 Jpresso Analysis Dashboard</h2>', unsafe_allow_html=True)
        if process_btn and g_weight > 0 and r_weight > 0:
            dtr = ((m_drop - m_fc) / m_drop * 100) if m_drop > 0 else 0.0
            w_loss = ((g_weight - r_weight) / g_weight * 100)
            t_cost = ((g_weight * g_cost) / r_weight) + 1.25
            b_id = f"LOT-{datetime.now().strftime('%m%d%H%M')}"
            st.session_state.last_analysis = {"batch_id": b_id, "sku": sku_name, "dtr": dtr, "w_loss": w_loss, "cost": t_cost, "agtron": agtron, "cupping": cupping_score, "flavors": list(st.session_state.master_notes)}
            st.session_state.batch_history.append({"Batch ID": b_id, "SKU": sku_name, "DTR (%)": round(dtr, 1), "Cost/kg": round(t_cost, 2)})
            st.rerun()
        if st.session_state.last_analysis:
            ana = st.session_state.last_analysis
            st.markdown(f'<div class="metric-row"><div class="metric-item"><strong>DTR</strong><br>{ana["dtr"]:.1f}%</div><div class="metric-item"><strong>Loss</strong><br>{ana["w_loss"]:.1f}%</div><div class="metric-item"><strong>Cost</strong><br>{ana["cost"]:.2f}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-box"><h4>🌟 JPRESSO SPEC</h4><p><strong>Batch:</strong> {ana["batch_id"]}</p><p><strong>SKU:</strong> {ana["sku"]}</p><p><strong>Sensory:</strong> {", ".join(ana["flavors"])}</p></div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.batch_history), use_container_width=True)

# ==========================================
# TAB 2: BRAND STORYTELLER (FULL RESTORATION)
# ==========================================
with tab2:
    st.markdown('<h2 class="section-header">📱 Video Prompt Engine</h2>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        scene = st.selectbox("Environment", ["The Roastery Floor (Classic)", "Modern Café (Urban)", "High-Speed Racing (Adrenaline)", "Outer Space (Sci-Fi)", "Bustling Local Market (Cultural)", "Urban Megacomplex (Cyberpunk)", "Rugged Wilderness (Adventure)"])
        mood = st.selectbox("Visual Mood", ["Premium Moody", "High-Energy Bright", "Warm Cozy", "Neon-Lit Gritty", "Untamed Nature"])
    with col_v2:
        target = st.selectbox("Audience", ["B2B Wholesale", "B2C Retail"])
        tone = st.selectbox("Tone", ["The Roasting Scientist", "The Artistic Craftsman", "The Origin Explorer", "The Rugged Explorer"])
    
    if st.button("✨ GENERATE CONTENT"):
        prompts = {"hooks": ["beans pouring into hopper", "explorer holding mug"], "scenes": ["smoke from tray", "barista pouring latte art"]}
        final_script = f"HOOK\n🎥 Video Prompt: Macro shot, {random.choice(prompts['hooks'])}, {mood} lighting, 8k.\n🎤 Voiceover: 'Precision is everything.'\n\nPROCESS\n🎥 Video Prompt: {random.choice(prompts['scenes'])}, 8k."
        st.code(final_script, language="text")

# ==========================================
# TAB 3: EVALUATION PORTAL (A4 FIT FIX)
# ==========================================
with tab3:
    st.markdown('<h2 class="section-header">🎓 Auto-Evaluation Portal</h2>', unsafe_allow_html=True)
    col_acad1, col_acad2 = st.columns(2)
    with col_acad1:
        st_name = st.text_input("Roaster Name", placeholder="Jason")
        t_bean = st.text_input("Bean", placeholder="Colombia")
    with col_acad2:
        t_prof = st.selectbox("Profile", ["Light (Filter)", "Medium (Omni)", "Dark (Espresso)"])
        st_dtr = st.number_input("Result DTR (%)", value=15.0)

    if st.button("🏅 Generate Certificate") and st_name and t_bean:
        logo_b64 = get_base64_image("Jpresso Gold Transparent.png")
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="160">' if logo_b64 else '<h1>BIG JPRESSO</h1>'
        iframe_html = f"""<!DOCTYPE html><html><head><style>
        @page {{ size: A4 portrait; margin: 0; }}
        body {{ font-family: sans-serif; margin: 0; padding: 0; background: #fcfaff; print-color-adjust: exact; }}
        .cert-container {{ width: 210mm; height: 297mm; max-height: 297mm; margin: 0 auto; background: #fff; padding: 10mm; box-sizing: border-box; display:flex; flex-direction:column; overflow: hidden; }}
        .border-outer {{ border: 8px solid #2b1d42; height: 100%; padding: 5mm; flex-grow:1; display:flex; flex-direction:column; box-sizing: border-box; }}
        .border-inner {{ border: 2px solid #d4af37; height: 100%; padding: 15mm; display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; box-sizing: border-box; }}
        </style></head><body>
        <div class="cert-container"><div class="border-outer"><div class="border-inner">
            <div>{logo_html}<h1 style="color:#2b1d42; font-size:32px; margin:5px 0;">ACADEMY EVALUATION</h1><h3 style="letter-spacing:3px; font-size:14px;">CERTIFICATE OF ANALYSIS</h3></div>
            <div><p style="font-size:14px;">This certifies the technical audit of</p><h2 style="font-size:28px; border-bottom:2px solid #d4af37; display:inline-block; padding:0 15px; margin:10px 0;">{st_name.upper()}</h2><p style="font-size:14px;">Completed roast targeting {t_prof} utilizing {t_bean}.</p></div>
            <div style="background:#fcfaff; padding:15px; border-left:4px solid #d4af37; text-align:left; width:85%;">
                <p style="font-size:14px; margin:5px 0;"><strong>Result DTR:</strong> {st_dtr}%</p>
                <p style="font-size:14px; margin:5px 0;"><strong>Status:</strong> Technical Requirements Met</p>
            </div>
            <div style="width:100%; display:flex; justify-content:space-around; align-items:flex-end;">
                <div><p style="font-size:14px; margin:0;">{datetime.now().strftime('%d %B %Y')}</p><hr><p style="font-size:10px;">DATE OF AUDIT</p></div>
                <div><p style="font-family:cursive; font-size:22px; margin:0;">Jason</p><hr><p style="font-size:10px;">CHIEF COFFEE OFFICER</p></div>
            </div>
            <div class="no-print"><button onclick="window.print()" style="background:#d4af37; padding:8px 15px; border:none; cursor:pointer; font-weight:bold; border-radius:5px;">🖨️ PRINT A4</button></div>
        </div></div></div></body></html>"""
        st.markdown("---")
        components.html(iframe_html, height=1200, scrolling=False)
