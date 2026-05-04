#  Fake Image Detection using Deep Learning  
### (Based on Hybrid MS-HDLA Architecture)
##  Overview
This project focuses on detecting **forged (fake) and original images** using Deep Learning techniques.  
It is inspired by the research paper:

> **"Classification of Forged Images vs Original Images Using Deep Learning"**

The system leverages CNN-based models along with forensic preprocessing techniques to identify manipulated images effectively.

##  Problem Statement
With the rise of image editing tools and AI-generated content, it has become increasingly difficult to distinguish between real and fake images.

Traditional methods fail to detect:
- Copy-move forgery  
- Image splicing  
- Retouching  
- AI-generated images (GANs, diffusion models)

This project aims to build an intelligent system that can classify images as:
 **Real**  
 **Fake**

##  Methodology

The project is inspired by the **Multi-Stage Hybrid Deep Learning Architecture (MS-HDLA)** proposed in the research paper.

###  Implemented Steps (Project)
1. Image Input  
2. Preprocessing  
3. Feature Extraction using CNN / Transfer Learning  
4. Model Training  
5. Binary Classification (Real vs Fake)

---

### Research Paper Architecture (Reference)

The paper proposes an advanced hybrid pipeline:

- **Error Level Analysis (ELA)** for detecting compression artifacts  
- **High-pass residual extraction** for noise inconsistencies  
- **Multi-scale patch extraction**  
- **Multi-model feature extraction:**
  - ResNet50  
  - Shallow CNN  
  - MobileNetV2  
- **Feature Fusion**
- **Mask R-CNN for localization of forged regions**

---

## Technologies Used

- Python  
- TensorFlow / Keras  
- OpenCV  
- NumPy  
- Matplotlib  

---

##  Dataset
The model can be trained on datasets such as:
- CASIA Dataset  
- MICC Dataset  
- Custom dataset (real & fake images)

---

## Features

✅ Detects fake vs real images  
✅ Uses Deep Learning (CNN / Transfer Learning)  
✅ Scalable for real-world applications  
✅ Inspired by advanced forensic techniques  

---

##  Limitations

- Only performs **classification (not localization)**  
- Does not yet implement:
  - Mask R-CNN  
  - Multi-model fusion  
  - Patch-based analysis  

---

##  Future Improvements

To fully align with the research paper (MS-HDLA), the following can be added:

- 🔹 Error Level Analysis (ELA) preprocessing  
- 🔹 Multi-scale patch extraction  
- 🔹 Hybrid model (ResNet + MobileNet + CNN)  
- 🔹 Forgery localization using Mask R-CNN  
- 🔹 Explainable AI (XAI)  

---

## Expected Outcome

- Accurate classification of images (Real vs Fake)  
- Can be extended for:
  - Cybersecurity  
  - Social media verification  
  - Digital forensics  

---

##  Research Reference

This project is based on the research paper:

**"Classification of Forged Images vs Original Images Using Deep Learning"**

The paper proposes a hybrid deep learning architecture achieving:
-  98–99% accuracy  
-  Both classification and localization capabilities  
##  Conclusion

This project is a **practical implementation of image forgery detection** using deep learning.  
While it currently focuses on classification, it lays the foundation for a complete forensic system as proposed in the research paper.
