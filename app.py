import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import re
import os
import base64
import streamlit.components.v1 as components 

# --- v176.0 FULL STEALTH CSS INJECTION ---
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
    .prompt-box { background-color: #f4f0ff; border-left: 5px solid #6a1b9a; padding: 20px; border-radius: 8px; font-family: 'Courier New', Courier, monospace; font-size: 14px; white-space: pre-wrap; line-height: 1.5; color: #333; border: 1px solid #d1c4e9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 Jpresso Roastery Intelligence v176.0")
st.caption("The Final Master Key: Full Features + Stealth Security")

# --- PERSISTENT STATE LOCK ---
if 'batch_history' not in st.session_state: st.session_state.batch_history = []
if 'last_analysis' not in st.session_state: st.session_state.last_analysis = None
if 'master_notes' not in st.session_state: st.session_state.master_notes = set()
if 'ms_key' not in st.session_state: st.session_state.ms_key = 0 

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h2 class="section-header">📈 Daily Audit</h2>', unsafe_allow_html=True)
    c_green = sum(float(b.get('Green (kg)', 0.0)) for b in st.session_state.batch_history)
    c_roasted = sum(float(b.get('Roasted (kg)', 0.0)) for b in st.session_state.batch_history)
    st.metric("Total Green Used Today", f"{c_green:.2f} kg")
    st.metric("Total Roasted Today", f"{c_roasted:.2f} kg")
    st.markdown("---")
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
        q_grade = st.selectbox("Quality Standard", ["Specialty Grade", "Commercial Grade"], index=0)
        g_weight = st.number_input("Total Green Input (kg)", value=0.0, step=0.01)
        r_weight = st.number_input("Total Roasted Output (kg)", value=0.0, step=0.01)
        mode = st.radio("Production Mode", ["Single Origin", "Blend Architect"], index=0, horizontal=True)
        if mode == "Single Origin":
            sku_name = st.text_input("Bean Name / SKU")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
            g_cost = st.number_input("Green Cost (Per kg)", value=0.0, step=0.01)
            blend_recipe_display = ""
        else:
            sku_name = st.text_input("Master Blend SKU")
            roast_level = st.selectbox("Roast Level", ["Light", "Med-Light", "Medium", "Med-Dark", "Dark"], index=2)
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
            blend_recipe_display = " | ".join(recipe_parts)
            st.markdown(f'<div class="cost-card"><strong>💰 Weighted Green Cost:</strong> {g_cost:.2f} /kg</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🎡 9-Wheel Sensory Auditor")
        family = st.selectbox("📥 Select Flavor Family", ["🍎 Fruity", "🌸 Floral", "🍯 Sweet", "🍫 Nutty/Cocoa", "🌶️ Spices", "🔥 Roasted", "🌿 Green/Veg", "🧪 Other", "🍷 Sour"])
        
        wheel_map = {
            "🍎 Fruity": [("Fruity", ""), ("Berry", "Fruity"), ("Blackberry", "Berry"), ("Raspberry", "Berry"), ("Blueberry", "Berry"), ("Strawberry", "Berry"), ("Dried Fruit", "Fruity"), ("Raisin", "Dried Fruit"), ("Prune", "Dried Fruit"), ("Other Fruit", "Fruity"), ("Coconut", "Other Fruit"), ("Cherry", "Other Fruit"), ("Pomegranate", "Other Fruit"), ("Pineapple", "Other Fruit"), ("Grape", "Other Fruit"), ("Apple", "Other Fruit"), ("Peach", "Other Fruit"), ("Pear", "Other Fruit"), ("Mango", "Other Fruit"), ("Citrus Fruit", "Fruity"), ("Grapefruit", "Citrus Fruit"), ("Orange", "Citrus Fruit"), ("Lemon", "Citrus Fruit"), ("Lime", "Citrus Fruit")],
            "🌸 Floral": [("Floral", ""), ("Black Tea", "Floral"), ("Floral Sub", "Floral"), ("Chamomile", "Floral"), ("Rose", "Floral"), ("Jasmine", "Floral")],
            "🍯 Sweet": [("Sweet", ""), ("Brown Sugar", "Sweet"), ("Molasses", "Brown Sugar"), ("Maple Syrup", "Brown Sugar"), ("Caramelized", "Brown Sugar"), ("Honey", "Brown Sugar"), ("Vanilla", "Sweet"), ("Vanillin", "Sweet")],
            "🍫 Nutty/Cocoa": [("Nutty/Cocoa", ""), ("Nutty", "Nutty/Cocoa"), ("Peanuts", "Nutty"), ("Hazelnut", "Nutty"), ("Almond", "Nutty"), ("Cocoa", "Nutty/Cocoa"), ("Chocolate", "Cocoa"), ("Dark Chocolate", "Cocoa")],
            "🌶️ Spices": [("Spices", ""), ("Pungent", "Spices"), ("Pepper", "Spices"), ("Brown Spice", "Spices"), ("Anise", "Brown Spice"), ("Nutmeg", "Brown Spice"), ("Cinnamon", "Brown Spice"), ("Clove", "Brown Spice")],
            "🔥 Roasted": [("Roasted", ""), ("Pipe Tobacco", "Roasted"), ("Tobacco", "Roasted"), ("Burnt", "Roasted"), ("Acrid", "Burnt"), ("Ashy", "Burnt"), ("Smoky", "Burnt"), ("Brown Roast", "Burnt"), ("Cereal", "Roasted")],
            "🌿 Green/Veg": [("Green/Veg", ""), ("Olive Oil", "Green/Veg"), ("Raw", "Green/Veg"), ("Green Sub", "Green/Veg"), ("Peapod", "Green Sub"), ("Fresh", "Green Sub"), ("Vegetative", "Green Sub"), ("Herb-like", "Green Sub"), ("Beany", "Green/Veg")],
            "🍷 Sour": [("Sour/Fermented", ""), ("Sour", "Sour/Fermented"), ("Acetic Acid", "Sour"), ("Butyric Acid", "Sour"), ("Isovaleric Acid", "Sour"), ("Citric Acid", "Sour"), ("Malic Acid", "Sour"), ("Alcohol/Fermented", "Sour/Fermented"), ("Winey", "Alcohol/Fermented"), ("Whiskey", "Alcohol/Fermented"), ("Fermented", "Alcohol/Fermented"), ("Overripe", "Alcohol/Fermented")],
            "🧪 Other": [("Other", ""), ("Chemical", "Other"), ("Rubber", "Chemical"), ("Skunky", "Chemical"), ("Petroleum", "Chemical"), ("Medicinal", "Chemical"), ("Salty", "Chemical"), ("Bitter", "Chemical"), ("Papery/Musty", "Other"), ("Phenolic", "Papery/Musty"), ("Meaty Brothy", "Papery/Musty"), ("Animalic", "Papery/Musty"), ("Musty/Earthy", "Papery/Musty"), ("Woody", "Papery/Musty"), ("Papery", "Papery/Musty"), ("Cardboard", "Papery/Musty"), ("Stale", "Papery/Musty")]
        }
        
        selected_data = wheel_map.get(family, [("Other", "")])
        df_wheel = pd.DataFrame(selected_data, columns=["Note", "Parent"])
        st.plotly_chart(px.sunburst(df_wheel, names='Note', parents='Parent', height=400), use_container_width=True)
        picks = st.multiselect("Finalize Sensory", list(df_wheel['Note']), key=f"ms_{st.session_state.ms_key}")
        for p in picks: st.session_state.master_notes.add(p)
        st.info(", ".join(st.session_state.master_notes) if st.session_state.master_notes else "No notes selected")
        if st.button("🗑️ Clear Map"):
            st.session_state.master_notes.clear()
            st.session_state.ms_key += 1 
            st.rerun()

        st.markdown("---")
        col_t = st.columns(3)
        with col_t[0]: m_dry = st.number_input("Dry End (m)", key="m_d")
        with col_t[1]: m_fc = st.number_input("FC Start (m)", key="m_f")
        with col_t[2]: m_drop = st.number_input("Drop Time (m)", key="m_v")
        agtron = st.number_input("Agtron Score", value=0)
        
        st.markdown("##### ☕ Cupping Form")
        with st.expander("📝 10-Point SCA Form", expanded=True):
            sc1, sc2 = st.columns(2)
            with sc1:
                s_frag = st.number_input("Aroma", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_flav = st.number_input("Flavor", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_after = st.number_input("Aftertaste", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_acid = st.number_input("Acidity", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_body = st.number_input("Body", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
            with sc2:
                s_bal = st.number_input("Balance", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
                s_unif = st.number_input("Uniformity", min_value=0, max_value=10, value=0, step=2)
                s_clean = st.number_input("Clean Cup", min_value=0, max_value=10, value=0, step=2)
                s_sweet = st.number_input("Sweetness", min_value=0, max_value=10, value=0, step=2)
                s_over = st.number_input("Overall", min_value=0.0, max_value=10.0, value=0.0, step=0.25)
            s_defect = st.number_input("Defect Penalty", min_value=0, max_value=20, value=0, step=2)
            eval_scores = [s_frag, s_flav, s_after, s_acid, s_body, s_bal, s_unif, s_clean, s_sweet, s_over]
            cupping_score = sum(eval_scores) - s_defect
            if sum(eval_scores) > 0: st.success(f"**Score: {cupping_score:.2f} SCA**")
                
        batch_notes = st.text_area("📝 Observations")
        process_btn = st.button("🚀 FINALIZE BATCH REPORT", use_container_width=True)

    with col_out:
        st.markdown('<h2 class="section-header">📊 Jpresso Analysis Dashboard</h2>', unsafe_allow_html=True)
        if process_btn and g_weight > 0 and r_weight > 0:
            dtr = ((m_drop - m_fc) / m_drop * 100) if m_drop > 0 else 0.0
            w_loss = ((g_weight - r_weight) / g_weight * 100)
            t_cost = ((g_weight * g_cost) / r_weight) + 1.25 
            b_id = f"LOT-{datetime.now().strftime('%m%d%H%M')}"
            st.session_state.last_analysis = {"batch_id": b_id, "operator": operator_name, "env": f"{amb_temp}°C / {humidity}%", "sku": sku_name, "roast_level": roast_level, "grade": q_grade, "g_weight": g_weight, "r_weight": r_weight, "dtr": dtr, "w_loss": w_loss, "cost": t_cost, "agtron": agtron, "cupping": cupping_score, "flavors": list(st.session_state.master_notes), "recipe": blend_recipe_display, "notes": batch_notes}
            st.session_state.batch_history.append({"Batch ID": b_id, "Operator": operator_name, "SKU": sku_name, "Green (kg)": g_weight, "Roasted (kg)": r_weight, "DTR (%)": round(dtr, 1), "Cost/kg": round(t_cost, 2), "SCA Score": round(cupping_score, 2)})
            st.rerun()

        if st.session_state.last_analysis:
            ana = st.session_state.last_analysis
            st.markdown(f'<div class="metric-row"><div class="metric-item"><strong>DTR %</strong><br>{ana["dtr"]:.1f}%</div><div class="metric-item"><strong>Weight Loss</strong><br>{ana["w_loss"]:.1f}%</div><div class="metric-item"><strong>True Cost</strong><br>{ana["cost"]:.2f}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-box"><h4>🌟 JPRESSO PRODUCTION SPEC</h4><p><strong>Batch ID:</strong> {ana["batch_id"]} | <strong>Operator:</strong> {ana["operator"]}</p><p><strong>Environment:</strong> {ana["env"]}</p><hr><p><strong>SKU:</strong> {ana["sku"]} ({ana["grade"]})</p><p><strong>Roast:</strong> {ana["roast_level"]}</p><p><strong>Recipe:</strong> {ana["recipe"]}</p><hr><p><strong>Green:</strong> {ana["g_weight"]} kg | <strong>Output:</strong> {ana["r_weight"]} kg</p><p><strong>SCA:</strong> {ana["cupping"]:.2f} | <strong>Agtron:</strong> {ana["agtron"]}</p><p><strong>Sensory:</strong> {", ".join(ana["flavors"])}</p><p><strong>Notes:</strong> {ana["notes"]}</p></div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.batch_history), use_container_width=True)

# --- TAB 2: STORYTELLER (RESTORED FULL) ---
with tab2:
    st.markdown('<h2 class="section-header">📱 Video Prompt Engine</h2>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        scene_setting = st.selectbox("Cinematic Environment", ["The Roastery Floor (Classic)", "Modern Café (Urban)", "High-Speed Racing (Adrenaline)", "Outer Space (Sci-Fi)", "Bustling Market (Cultural)", "Urban Megacomplex (Cyberpunk)", "Rugged Wilderness (Adventure)"])
        emotion = st.selectbox("Visual Mood", ["Premium Moody", "High-Energy Bright", "Warm Cozy", "Neon-Lit Gritty", "Untamed Nature"])
    with col_v2:
        target_audience = st.selectbox("Audience", ["B2B Wholesale", "B2C Retail"])
        vibe = st.selectbox("Storytelling Tone", ["Scientist (Technical)", "Craftsman (Masterful)", "Explorer (Nature)", "Rugged (Uncharted)"])
    
    if st.button("✨ GENERATE CONTENT"):
        visual_sets = {
            "The Roastery Floor (Classic)": {"hooks": ["green coffee beans pouring into brass hopper", "blue flame igniting under steel drum"], "scenes": ["thick smoke from cooling tray", "hands adjusting brass dials"], "climaxes": ["golden espresso pouring into black cup", "brown beans spinning"]},
            "High-Speed Racing (Adrenaline)": {"hooks": ["race car drifting, leaving bean trail", "pit-stop crew working fast"], "scenes": ["glowing engine roaring", "helmet blur, rapid pulls"], "climaxes": ["driver celebrating with espresso", "espresso pouring like fuel"]},
            "Rugged Wilderness (Adventure)": {"hooks": ["explorer on misty mountain", "campfire sparks in dark forest"], "scenes": ["pouring boiling water into titanium camp dripper", "brewing on stone"], "climaxes": ["sipping coffee near waterfall", "cup on mossy log"]}
        }
        v_set = visual_sets.get(scene_setting, visual_sets["The Roastery Floor (Classic)"])
        final_script = f"""HOOK\n🎥 Video Prompt: Macro shot, {random.choice(v_set['hooks'])}, {emotion} lighting, 8k, no text.\n🎤 Voiceover: "Precision is our only metric."\n\nPROCESS\n🎥 Video Prompt: Slow-mo, {random.choice(v_set['scenes'])}, {emotion}, 8k.\n🎤 Voiceover: "Roasting is a dance with fire."\n\nCLIMAX\n🎥 Video Prompt: Macro, {random.choice(v_set['climaxes'])}, 8k.\n🎤 Voiceover: "Taste the culmination of dedication."\n\nCALL TO ACTION\n🎥 Video Prompt: Customer taking a sip, 8k.\n🎤 Voiceover: "Tap below to order your first batch." """
        st.code(final_script, language="text")

# --- TAB 3: EVALUATION PORTAL (RESTORED FULL A4) ---
with tab3:
    st.markdown('<h2 class="section-header">🎓 Objective Auto-Evaluation Portal</h2>', unsafe_allow_html=True)
    col_acad1, col_acad2 = st.columns(2)
    with col_acad1:
        st_name = st.text_input("Roaster Name", placeholder="e.g., Jason")
        m_used = st.selectbox("Machine", ["1kg Bideli", "5kg Has Garanti", "Santoker Air Roaster"])
        t_bean = st.text_input("Training Bean", placeholder="e.g., Colombia Supremo")
    with col_acad2:
        t_prof = st.selectbox("Target Profile", ["Light (Filter - 12-16% DTR)", "Medium (Omni - 18-22% DTR)", "Dark (Espresso - 23-27% DTR)"])
        st_dtr = st.number_input("Result DTR (%)", value=15.0, step=0.1)

    if st.button("🏅 Generate Formal Certificate") and st_name and t_bean:
        logo_b64 = get_base64_image("Jpresso Gold Transparent.png")
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="180">' if logo_b64 else '<h1>BIG JPRESSO</h1>'
        iframe_html = f"""<!DOCTYPE html><html><head><style>
        @page {{ size: A4 portrait; margin: 0; }}
        body {{ font-family: sans-serif; margin: 0; padding: 0; background: #fcfaff; print-color-adjust: exact; }}
        .cert-container {{ width: 210mm; height: 296mm; margin: 0 auto; background: #fff; padding: 10mm; box-sizing: border-box; display:flex; flex-direction:column; }}
        .border-outer {{ border: 10px solid #2b1d42; height: 100%; padding: 10px; flex-grow:1; }}
        .border-inner {{ border: 3px solid #d4af37; height: 100%; padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; }}
        </style></head><body>
        <div class="cert-container"><div class="border-outer"><div class="border-inner">
            <div>{logo_html}<h1 style="color:#2b1d42; font-size:36px; margin:10px 0;">ACADEMY EVALUATION</h1><h3 style="letter-spacing:4px;">CERTIFICATE OF ANALYSIS</h3></div>
            <div><p>This formally certifies the technical audit of</p><h2 style="font-size:32px; border-bottom:2px solid #d4af37; display:inline-block; padding:0 20px;">{st_name.upper()}</h2><p>Completed a formal roast evaluation targeting {t_prof} utilizing {t_bean}.</p></div>
            <div style="background:#fcfaff; padding:20px; border-left:5px solid #d4af37; text-align:left; width:80%;"><p><strong>Result DTR:</strong> {st_dtr}%</p><p><strong>Machine:</strong> {m_used}</p></div>
            <div style="width:100%; display:flex; justify-content:space-around; align-items:flex-end;">
                <div><p style="margin:0;">{datetime.now().strftime('%d %B %Y')}</p><hr><p style="font-size:12px;">DATE OF AUDIT</p></div>
                <div><p style="font-family:cursive; font-size:24px; margin:0;">Jason</p><hr><p style="font-size:12px;">CHIEF COFFEE OFFICER</p></div>
            </div>
            <div class="no-print"><button onclick="window.print()" style="background:#d4af37; padding:10px 20px; border:none; cursor:pointer; font-weight:bold;">🖨️ PRINT A4</button></div>
        </div></div></div></body></html>"""
        components.html(iframe_html, height=1250, scrolling=False)
