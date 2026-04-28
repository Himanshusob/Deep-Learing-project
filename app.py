import streamlit as st
from PIL import Image
import uuid
import plotly.graph_objects as go
from streamlit_image_comparison import image_comparison

from infer import analyze_image_full

st.set_page_config(page_title="Cyber Forensic Dashboard",layout="wide")

# ---------------- CYBER CSS ----------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#0f2027,#1b2735,#090a0f);
color:white;
}

/* TITLE */

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

/* SECTION HEADER */

.grad{
background: linear-gradient(90deg,#3ea8ff,#9b6bff);
padding:12px;
border-radius:12px;
font-weight:600;
margin-top:25px;
}

/* CYBER CARD */

.cyber-card{
background:#0b0f14;
border:1px solid rgba(255,92,122,0.25);
border-radius:14px;
padding:25px;
text-align:center;
}

/* SCORE CARDS */

.stat-number{
font-size:40px;
font-weight:700;
color:#ff5c7a;
}

.stat-label{
color:#8c97a8;
font-size:14px;
}

.score-card{
background:#0b0f14;
border-radius:14px;
padding:30px;
margin-top:20px;
}

</style>
""",unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">
🕵️ Advanced Fake Image Detector
</div>

<div class="sub-title">
ELA · EXIF · Clone Detection · Noise Analysis · AI Model
</div>
""",unsafe_allow_html=True)

st.write("---")

# ---------------- HOW DETECTION WORKS ----------------

st.markdown("<div class='grad'>How Deepfake Detection Works</div>",unsafe_allow_html=True)

c1,c2,c3=st.columns(3)

with c1:
    st.markdown("""
<div class="cyber-card">
<h3>01</h3>
<h4>Upload Image</h4>
<p>Select image to analyze for manipulation</p>
</div>
""",unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="cyber-card">
<h3>02</h3>
<h4>AI Analysis</h4>
<p>Neural network analyzes image patterns</p>
</div>
""",unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="cyber-card">
<h3>03</h3>
<h4>Get Verdict</h4>
<p>Receive authenticity score instantly</p>
</div>
""",unsafe_allow_html=True)

st.write("---")

# ---------------- INPUT ----------------

col1,col2=st.columns([2,1])

with col1:
    uploaded=st.file_uploader("Upload Image",type=["jpg","png","jpeg"])
    run=st.button("Run Analysis")

with col2:
    st.markdown("### Instructions")
    st.write("Upload image for forensic analysis")
    st.write("System runs AI + forensic checks")

path=None

import uuid

if uploaded:
    img = Image.open(uploaded)
    filename = f"temp_{uuid.uuid4().hex}.jpg"
    img.save(filename)
    path = filename

# ---------------- ANALYSIS ----------------

if run and path:

    # Model temporarily disabled
    # res=analyze_image_full("checkpoints/final_model.h5",path)

    res = {
        "model_label": "fake",
        "model_prob": 0.5,
        "ela_variance": 0,
        "noise_mean_var": 0,
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
        "explanation": ["Model disabled for deployment test"]
    }

    model_label = res["model_label"]
    model_prob = res["model_prob"]

    ela_var = res["ela_variance"]
    noise_var = res["noise_mean_var"]
    clone_matches = res["clone_matches"]

    scores = res["scores"]

# ---------------- ORIGINAL ----------------

    st.markdown("<div class='grad'>Original Image</div>",unsafe_allow_html=True)

    c1,c2=st.columns(2)

    with c1:
        st.image(path,use_container_width=True)

    with c2:

        if model_label=="fake":
            st.error(f"AI Prediction: FAKE ({model_prob:.2f})")
        else:
            st.success(f"AI Prediction: REAL ({model_prob:.2f})")

# ---------------- ELA ----------------

    st.markdown("<div class='grad'>Error Level Analysis</div>",unsafe_allow_html=True)

    c1,c2=st.columns(2)

    with c1:
        st.image(res["ela_arr"])

    with c2:
        image_comparison(
        img1=path,
        img2=res["ela_arr"],
        label1="Original",
        label2="ELA Heatmap"
        )

# ---------------- CLONE ----------------

    st.markdown("<div class='grad'>Clone Detection</div>",unsafe_allow_html=True)

    st.write(f"Clone matches detected: {clone_matches}")

    if res["clone_vis"] is not None:
        st.image(res["clone_vis"])

# ---------------- NOISE ----------------

    st.markdown("<div class='grad'>Noise Variance Heatmap</div>",unsafe_allow_html=True)

    c1,c2=st.columns(2)

    with c1:
        st.image(res["noise_vis"])

    with c2:
        image_comparison(
        img1=path,
        img2=res["noise_vis"],
        label1="Original",
        label2="Noise Heatmap"
        )

# ---------------- SCORES ----------------

    st.markdown("<div class='grad'>Scores</div>",unsafe_allow_html=True)

    s1,s2,s3,s4=st.columns(4)

    with s1:
        st.markdown(f"<div class='cyber-card'><div class='stat-number'>{scores['ela']:.0f}%</div><div class='stat-label'>ELA Score</div></div>",unsafe_allow_html=True)

    with s2:
        st.markdown(f"<div class='cyber-card'><div class='stat-number'>{scores['exif']:.0f}%</div><div class='stat-label'>EXIF Score</div></div>",unsafe_allow_html=True)

    with s3:
        st.markdown(f"<div class='cyber-card'><div class='stat-number'>{scores['clone']:.0f}%</div><div class='stat-label'>Clone Score</div></div>",unsafe_allow_html=True)

    with s4:
        st.markdown(f"<div class='cyber-card'><div class='stat-number'>{scores['noise']:.0f}%</div><div class='stat-label'>Noise Score</div></div>",unsafe_allow_html=True)

# ---------------- GAUGE ----------------

    st.markdown("<div class='grad'>Authenticity Score</div>",unsafe_allow_html=True)

    fig=go.Figure(go.Indicator(
    mode="gauge+number",
    value=scores["final"],
    title={'text':"Authenticity Score"},
    gauge={
    'axis':{'range':[0,100]},
    'steps':[
    {'range':[0,40],'color':'red'},
    {'range':[40,70],'color':'yellow'},
    {'range':[70,100],'color':'green'}
    ]
    }
    ))

    st.plotly_chart(fig,use_container_width=True)

# ---------------- FINAL RESULT ----------------

    st.markdown("<div class='grad'>Final Verdict</div>",unsafe_allow_html=True)

    if scores["final"]>70:
        st.success("Image appears Authentic")

    elif scores["final"]>45:
        st.warning("Image looks Suspicious")

    else:
        st.error("Image likely Manipulated")

# ---------------- EXPLANATION ----------------

    st.markdown("<div class='grad'>Explanation</div>",unsafe_allow_html=True)

    for e in res["explanation"]:
        st.write("•",e)
