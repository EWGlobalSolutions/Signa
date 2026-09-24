"""Shared MediaPipe landmark extraction + normalization.

Every other script imports from here, so the pose math lives in one place.
"""

import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands

N_HAND_LANDMARKS = 21
FEATURES_PER_FRAME = 2 * N_HAND_LANDMARKS * 3  # 2 hands x 21 points x (x,y,z) = 126


def make_detectors():
    """Create the MediaPipe Hands detector (video mode)."""
    return mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )


def _normalize_hand(hand_landmarks):
    """Wrist-relative, scale-invariant features for one hand.

    Subtracting the wrist removes *where* the hand is in the frame;
    dividing by hand size removes *how close* it is to the camera.
    What remains is the hand's *shape* -- exactly what a sign
    classifier should learn from.
    """
    pts = np.array(
        [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark],
        dtype=np.float32,
    )
    pts -= pts[0]  # wrist becomes the origin
    hand_size = np.linalg.norm(pts[9]) + 1e-6  # wrist -> middle-finger base
    return (pts / hand_size).flatten()


def frame_to_features(frame_bgr, hands):
    """Turn one video frame into a 126-dim feature vector.

    Layout: [left hand (63), right hand (63)]. A hand that isn't
    visible is all zeros, so the vector is always the same size.
    """
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    feats = np.zeros((2, N_HAND_LANDMARKS * 3), dtype=np.float32)
    if result.multi_hand_landmarks and result.multi_handedness:
        for landmarks, handedness in zip(
            result.multi_hand_landmarks, result.multi_handedness
        ):
            label = handedness.classification[0].label  # 'Left' / 'Right'
            slot = 0 if label == "Left" else 1
            feats[slot] = _normalize_hand(landmarks)
    return feats.flatten()
