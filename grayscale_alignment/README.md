
# 🔥 Thermal-RGB Image Aligner (LoFTR + Inverted Grayscale)

This project aligns thermal images to RGB images using grayscale preprocessing and LoFTR feature matching with homography transformation. It supports inversion of thermal images for better feature extraction.

## 📁 Directory Structure
```plaintext
.
├── align_grayscale.py           # Main script
├── input-images/                # Folder for paired thermal and RGB images
├── output-images/               # Folder for saving aligned outputs
├── requirements.txt             # Required Python packages
└── README.md                    # Project documentation
```

## 📄 File Descriptions
- align_grayscale.py – Main code to perform thermal-to-RGB image alignment.

- input-images/ – Folder containing input image pairs (*_T.JPG for thermal, *_Z.JPG for RGB).

- output-images/ – Output folder where aligned thermal images are saved.

## ⚙️ Setup Instructions

1. Create & Activate Virtual Environment:
```bash
python3.9 -m venv thermal_rgb
source thermal_rgb/bin/activate   # macOS/Linux
thermal_rgb\Scripts\activate      # Windows
```

2. Install CUDA-enabled PyTorch (ensure CUDA 11.8 is available):

```bash
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
```

3. Install the remaining dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage
- Update the following variables in align_grayscale.py:
```python
INPUT_DIR = "path/to/RGB-and-Thermal-images/folder"
OUTPUT_DIR = "path/to/output-images"
```

#### Then run the script:
```bash
python align_grayscale.py
```
- Aligned images will be saved in output-images/ with filenames like:
XYZ_AT.JPG (where XYZ is the shared base name of each image pair).

## 🖼️ Input Image Format

Each input pair should follow this naming pattern:

| Type          | Filename Format | Example            |
| ------------- | --------------- | ------------------ |
| RGB Image     | `XYZ_Z.JPG`     | `FLIR_08922_Z.JPG` |
| Thermal Image | `XYZ_T.JPG`     | `FLIR_08922_T.JPG` |

- Both images should exist in the input-images/ folder.

- Where `XYZ` and `FLIR_08922` shares base name for the pair.

Example:
```bash
input-images/
├── IMG001_T.JPG # Thermal image (to be aligned)
├── IMG001_Z.JPG # Corresponding RGB image
```


## 🔁 Script Flow (Visual Overview)

```plaintext 
┌─────────────────────────────┐
│   Start: Process Each Pair  │
└────────────┬────────────────┘
             │
             ▼
┌───────────────────────────────┐       ┌───────────────────────────────┐
│ Load Thermal image (XYZ_T.JPG)│       │  Load RGB image (XYZ_Z.JPG)   │
└────────────┬──────────────────┘       └────────────┬──────────────────┘
             │                                       │
             ▼                                       ▼
┌───────────────────────────────┐       ┌───────────────────────────────┐
│ Convert to Invert Grayscale   │       │     Convert to Grayscale      │
└────────────┬──────────────────┘       └────────────┬──────────────────┘
             │                                       │
             └─────────────────┬─────────────────────┘
                               ▼
              ┌────────────────────────────────────┐
              │ Resize both images to TARGET_SIZE  │
              │          (1280 x 960)              │
              └────────────────┬───────────────────┘
                               ▼
              ┌────────────────────────────────────┐
              │   Run LoFTR on both preprocessed   │
              │         grayscale images           │
              └────────────────┬───────────────────┘
                               ▼
              ┌────────────────────────────────────┐
              │   Extract matched keypoints (kpts) │
              └────────────────┬───────────────────┘
                               ▼
              ┌────────────────────────────────────┐
              │    Estimate Homography (RANSAC)    │
              └────────────────┬───────────────────┘
                               ▼
              ┌────────────────────────────────────┐
              │ Warp thermal image using H matrix  │
              └────────────────┬───────────────────┘
                               ▼
              ┌────────────────────────────────────┐
              │ Resize aligned result to original  │
              │         RGB resolution             │
              └────────────────┬───────────────────┘
                               ▼
              ┌────────────────────────────────────┐
              │ Save aligned image as XYZ_AT.JPG   │
              └────────────────────────────────────┘

```

## 🔍 Interactive Comparison

🎚️ Slide left/right to compare the original RGB image with the aligned thermal output:

👉 [Click here to view interactive comparison](https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=e96f099a-5bbf-11f0-bb24-0936e1cb08fb)

- Images used are from the FLIR Thermal Starter Dataset


## 📚 Dataset Credits

This project uses image pairs from:

**FLIR Thermal Starter Dataset**

📎 [Download from Kaggle](https://www.kaggle.com/datasets/deepnewbie/flir-thermal-images-dataset)

- Contains thermal and RGB images captured with FLIR automotive-grade sensors.

- **Note:** Thermal and RGB images may not be synchronized perfectly in time. Therefore, **moving objects may appear misaligned.**

- Best results are obtained when:

  - Images are captured simultaneously

  - Scene is static (no fast-moving objects)

  - Input images are sharp and well-contrasted

## 🙏 Acknowledgements

 - 🔗 [PyTorch Previous Versions](https://pytorch.org/get-started/previous-versions/)
 - 🔗 [LoFTR](https://github.com/zju3dv/LoFTR)
 - 🔗 [OpenCV Homography](https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html)

