import os
import cv2
import numpy as np
import torch
from glob import glob
from torchvision.transforms.functional import to_tensor
from kornia.feature import LoFTR

# Configuration
INPUT_DIR = "path/to/RGB-and-Thermal-images/folder"
OUTPUT_DIR = "path/to/output-images"
TARGET_SIZE = (1280, 960)
INVERT_THERMAL = True
MIN_MATCHED_KEYPOINTS = 10

# Setup
os.makedirs(OUTPUT_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
loftr = LoFTR(pretrained='outdoor').to(device).eval()


def get_base_name(thermal_path):
    return os.path.basename(thermal_path).replace("_T.JPG", "")


def preprocess_for_loftr(image_bgr, invert=False):
    """Convert BGR image to grayscale tensor, resized for LoFTR."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    if invert:
        gray = cv2.bitwise_not(gray)
    resized = cv2.resize(gray, TARGET_SIZE)
    tensor = to_tensor(resized.astype(np.float32) / 255.).unsqueeze(0).to(device)
    return tensor, resized


def align_thermal_to_rgb():
    thermal_paths = glob(os.path.join(INPUT_DIR, "*_T.JPG"))

    if not thermal_paths:
        print(f"No thermal images found in {INPUT_DIR}")
        return

    for thermal_path in thermal_paths:
        base_name = get_base_name(thermal_path)
        rgb_path = os.path.join(INPUT_DIR, base_name + "_Z.JPG")

        if not os.path.exists(rgb_path):
            print(f"Missing RGB image for {base_name}")
            continue

        thermal_color = cv2.imread(thermal_path)
        rgb_color = cv2.imread(rgb_path)

        if thermal_color is None or rgb_color is None:
            print(f"Failed to read image(s) for {base_name}")
            continue

        h_full, w_full = rgb_color.shape[:2]

        thermal_tensor, _ = preprocess_for_loftr(thermal_color, invert=INVERT_THERMAL)
        rgb_tensor, _ = preprocess_for_loftr(rgb_color, invert=False)

        with torch.no_grad():
            output = loftr({'image0': thermal_tensor, 'image1': rgb_tensor})

        kpts0 = output['keypoints0'].cpu().numpy()
        kpts1 = output['keypoints1'].cpu().numpy()

        if len(kpts0) < MIN_MATCHED_KEYPOINTS:
            print(f"Not enough matches for {base_name} ({len(kpts0)} points)")
            continue

        H, status = cv2.findHomography(kpts0, kpts1, cv2.RANSAC)
        if H is None:
            print(f"Homography estimation failed for {base_name}")
            continue

        warped_thermal_resized = cv2.resize(thermal_color, TARGET_SIZE)
        aligned_resized = cv2.warpPerspective(warped_thermal_resized, H, TARGET_SIZE)
        aligned_full = cv2.resize(aligned_resized, (w_full, h_full), interpolation=cv2.INTER_LINEAR)

        out_path = os.path.join(OUTPUT_DIR, f"{base_name}_AT.JPG")
        cv2.imwrite(out_path, aligned_full)
        print(f"Saved aligned thermal image: {out_path}")


if __name__ == "__main__":
    align_thermal_to_rgb()
