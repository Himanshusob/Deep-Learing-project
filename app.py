import streamlit as st
from PIL import Image
import uuid
import plotly.graph_objects as go
from streamlit_image_comparison import image_comparison

st.set_page_config(page_title="Cyber Forensic Dashboard", layout="wide")

# ---------------- CSS ----------------

st.markdown("""
<style>
.stApp{
background: radial-gradient(circle at top,#0f2027,#1b2735,#090a0f);
color:white;
}
.main-title{
text-align:center;
font-size:52px;
font-weight:800;
background: linear-gradient(90deg,#ff5c7a,#9b6bff,#3ea8ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-top:20px;
}
.sub-title{
text-align:center;
color:#8c97a8;
margin-bottom:25px;
}
.grad{
background: linear-gradient(90deg,#3ea8ff,#9b6bff);
padding:12px;
border-radius:12px;
font-weight:600;
margin-top:25px;
}
.cyber-card{
background:#0b0f14;
border:1px solid rgba(255,92,122,0.25);
border-radius:14px;
padding:25px;
text-align:center;
}
.stat-number{
font-size:40px;
font-weight:700;
color:#ff5c7a;
}
.stat-label{
color:#8c97a8;
font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">🕵️ Advanced Fake Image Detector</div>
<div class="sub-title">ELA · EXIF · Clone Detection · Noise Analysis · AI Model</div>
""", unsafe_allow_html=True)

st.write("---")

# ---------------- INPUT ----------------

col1, col2 = st.columns([2,1])

with col1:
    uploaded = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    run = st.button("Run Analysis")

with col2:
    st.markdown("### Instructions")
    st.write("Upload image for forensic analysis")

path = None

if uploaded:
    img = Image.open(uploaded)
    filename = f"temp_{uuid.uuid4().hex}.jpg"
    img.save(filename)
    path = filename

# ---------------- ANALYSIS ----------------

if run and path:

    # Dummy result (NO AI MODEL)
    res = {
        "model_label": "fake",
        "model_prob": 0.5,
        "clone_matches": 0,
        "scores": {
            "ela": 50,
            "exif": 50,
            "clone": 50,
            "noise": 50,
            "final": 50
        },
        "ela_arr": path,
        "clone_vis": None,
        "noise_vis": path,
        "explanation": ["AI model disabled for deployment"]
    }

    scores = res["scores"]

# ---------------- ORIGINAL ----------------

    st.markdown("<div class='grad'>Original Image</div>", unsafe_allow_html=True)
    st.image(path, use_container_width=True)

    if res["model_label"] == "fake":
        st.error(f"AI Prediction: FAKE ({res['model_prob']:.2f})")
    else:
        st.success(f"AI Prediction: REAL ({res['model_prob']:.2f})")

# ---------------- ELA ----------------

    st.markdown("<div class='grad'>ELA</div>", unsafe_allow_html=True)
    image_comparison(path, path)

# ---------------- SCORES ----------------

    st.markdown("<div class='grad'>Scores</div>", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("ELA", f"{scores['ela']}%")
    c2.metric("EXIF", f"{scores['exif']}%")
    c3.metric("Clone", f"{scores['clone']}%")
    c4.metric("Noise", f"{scores['noise']}%")

# ---------------- GAUGE ----------------

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=scores["final"],
        title={'text':"Authenticity"},
        gauge={
            'axis':{'range':[0,100]},
            'steps':[
                {'range':[0,40],'color':'red'},
                {'range':[40,70],'color':'yellow'},
                {'range':[70,100],'color':'green'}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

# ---------------- RESULT ----------------

    if scores["final"] > 70:
        st.success("Authentic Image")
    elif scores["final"] > 45:
        st.warning("Suspicious Image")
    else:
        st.error("Fake Image")

# ---------------- EXPLANATION ----------------

    st.markdown("<div class='grad'>Explanation</div>", unsafe_allow_html=True)

    for e in res["explanation"]:
        st.write("•", e)
