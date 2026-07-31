import streamlit as st
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Smart Classroom Noise Detection",
    page_icon="🎓"
)

st.title("🎓 AI Smart Classroom Noise Detection")
st.write("Detect classroom noise levels in real time using your microphone.")

# -----------------------------
# Initialize Session State
# -----------------------------
if "audio" not in st.session_state:
    st.session_state.audio = None

# -----------------------------
# Function: Calculate dB
# -----------------------------
def calculate_db(audio):

    audio = audio.flatten()

    rms = np.sqrt(np.mean(audio ** 2))

    if rms <= 0:
        return -100

    db = 20 * np.log10(rms)

    return db

# -----------------------------
# Function: Classify Noise
# -----------------------------
def classify_noise(db):

    if db < -45:
        return "Low Noise"

    elif db < -25:
        return "Medium Noise"

    else:
        return "High Noise"

# -----------------------------
# Settings
# -----------------------------
duration = st.slider(
    "Recording Duration (seconds)",
    1,
    10,
    3
)

fs = 44100

# -----------------------------
# Record Audio
# -----------------------------
if st.button("🎤 Record Classroom Sound"):

    st.info("Recording...")

    try:

        audio = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        st.session_state.audio = audio

        st.success("Recording Finished!")

        db = calculate_db(audio)

        status = classify_noise(db)

        st.metric("Noise Level", f"{db:.2f} dB")
        st.metric("Status", status)

        if status == "High Noise":
            st.error("⚠ High noise detected! Please maintain silence.")

        elif status == "Medium Noise":
            st.warning("⚠ Moderate noise. Try to reduce noise.")

        else:
            st.success("✅ Classroom is quiet.")

    except Exception as e:

        st.error(f"Recording Error: {e}")

# -----------------------------
# Waveform
# -----------------------------
if st.checkbox("Show Audio Waveform"):

    if st.session_state.audio is not None:

        fig, ax = plt.subplots(figsize=(9,3))

        ax.plot(st.session_state.audio[:,0])

        ax.set_title("Recorded Audio Waveform")
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")

        st.pyplot(fig)

    else:

        st.warning("Please record audio first.")

st.markdown("---")
st.markdown("**Developed by:** TEHREEN RAMESHA")
