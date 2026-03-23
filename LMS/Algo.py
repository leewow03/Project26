"""
detect.py
──────────────────────────────────────────────
프론트에서 업로드한 이미지 / 영상 차량 탐지
──────────────────────────────────────────────
"""

from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────
MODEL_PATH = "yolo11m.pt"

VEHICLE_CLASSES = {
    2: "car",
    5: "bus",
    7: "truck",
}

COLORS = {
    "car"  : (100, 200, 100),
    "bus"  : (100, 180, 255),
    "truck": (255, 160,  80),
}

CONF = 0.4
IOU  = 0.45

model = YOLO(MODEL_PATH)


# ──────────────────────────────────────────
# 공통 — 프레임 한 장 탐지
# ──────────────────────────────────────────
def _detect_frame(frame: np.ndarray) -> tuple[np.ndarray, list[dict]]:
    results = model.predict(
        source  = frame,
        conf    = CONF,
        iou     = IOU,
        classes = list(VEHICLE_CLASSES.keys()),
        verbose = False,
    )[0]

    annotated  = frame.copy()
    detections = []

    for box in results.boxes:
        cls_id          = int(box.cls[0])
        conf            = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        name  = VEHICLE_CLASSES[cls_id]
        color = COLORS[name]
        label = f"{name}  {conf:.2f}"

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(annotated, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
        cv2.putText(annotated, label, (x1 + 3, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        detections.append({
            "class"     : name,
            "confidence": round(conf, 3),
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
        })

    return annotated, detections


# ──────────────────────────────────────────
# 이미지 처리
# ──────────────────────────────────────────
def detect_image(file_path: str) -> dict:
    """
    프론트에서 업로드한 이미지 탐지.

    Returns:
        {
            "result_path": "저장된 결과 이미지 경로",
            "detections" : [{ class, confidence, x1, y1, x2, y2 }, ...]
        }
    """
    frame = cv2.imread(file_path)
    if frame is None:
        raise FileNotFoundError(f"이미지 없음: {file_path}")

    annotated, detections = _detect_frame(frame)

    out_path = str(Path(file_path).with_stem(Path(file_path).stem + "_result"))
    cv2.imwrite(out_path, annotated)

    return {
        "result_path": out_path,
        "detections" : detections,
    }


# ──────────────────────────────────────────
# 영상 처리
# ──────────────────────────────────────────
def detect_video(file_path: str) -> dict:
    """
    프론트에서 업로드한 영상 탐지.

    Returns:
        {
            "result_path": "저장된 결과 영상 경로",
            "total_frames": 전체 프레임 수,
            "detections_per_frame": 프레임별 탐지 결과 리스트
        }
    """
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"영상 없음: {file_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out_path = str(Path(file_path).with_stem(Path(file_path).stem + "_result"))
    writer   = cv2.VideoWriter(
        out_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps, (w, h),
    )

    all_detections = []
    frame_idx      = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        annotated, detections = _detect_frame(frame)
        writer.write(annotated)

        if detections:
            all_detections.append({
                "frame"     : frame_idx,
                "detections": detections,
            })

        frame_idx += 1

    cap.release()
    writer.release()

    return {
        "result_path"        : out_path,
        "total_frames"       : frame_idx,
        "detections_per_frame": all_detections,
    }