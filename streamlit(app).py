import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(page_title="Tube Bundle Analysis", layout="wide")

st.header("Tube Bundle Fluid Elastic Instability & Natural Frequency Check")

# --- Tube Arrangement Selection ---
tube_arrangement_options = {
    "Triangular (P/D = 1.25 - 1.5)": (3.0, 5.0),
    "Triangular (P/D = 1.5 - 2.5)": (4.0, 7.0),
    "Square (P/D = 1.25 - 1.5)": (2.5, 4.5),
    "Square (P/D = 1.5 - 2.5)": (3.5, 6.5),
    "Rotated Square (P/D = 1.25 - 1.5)": (2.0, 4.0),
    "Rotated Square (P/D = 1.5 - 2.5)": (3.0, 5.5)
}

layout_choice = st.selectbox("Select Tube Arrangement:", list(tube_arrangement_options.keys()))
K_min, K_max = tube_arrangement_options[layout_choice]
K = (K_min + K_max) / 2
st.write(f"Selected Empirical Constant K = {K:.2f}")

# --- Input Section ---
st.subheader("Material, Geometry, and Flow Inputs")

col1, col2 = st.columns(2)

with col1:
    D = st.number_input("Tube Outside Diameter (m)", value=0.025)
    t = st.number_input("Tube Thickness (m)", value=0.0025)
    L = st.number_input("Tube Length (m)", value=1.0)
    pitch = st.number_input("Tube Pitch (m)", value=0.03)
    E = st.number_input("Young’s Modulus (Pa)", value=2.0e11, format="%.2e")

with col2:
    rho_material = st.number_input("Tube Material Density (kg/m³)", value=7850.0)
    U_actual = st.number_input("Shell-side Flow Velocity (m/s)", value=3.0)
    rho_shell = st.number_input("Shell-side Fluid Density (kg/m³)", value=1000.0)
    baffle_spacing = st.number_input("Baffle Spacing (m)", value=0.2)
    diam_clearance = st.number_input("Diametral Clearance (m)", value=0.001)

# --- Calculations ---
I = (np.pi / 64) * (D**4 - (D - 2*t)**4)
m = rho_material * (np.pi * (D**2 - (D - 2*t)**2)) / 4

f_n = (1 / (2 * np.pi)) * np.sqrt(E * I / (m * L**4))
Uc = K * f_n * D

# --- Results ---
st.subheader("Analysis Results")

col1, col2 = st.columns(2)
with col1:
    st.metric("Natural Frequency (Hz)", f"{f_n:.2f}")
    st.metric("Critical Velocity (m/s)", f"{Uc:.2f}")

with col2:
    if U_actual > Uc:
        st.error(f"🚨 Instability Occurs! (U = {U_actual} m/s > Uc = {Uc:.2f} m/s)")
    else:
        st.success(f"✅ Stable (U = {U_actual} m/s < Uc = {Uc:.2f} m/s)")

# --- Velocity Comparison Bar Chart ---
fig, ax = plt.subplots()
ax.bar(["Critical Velocity", "Actual Velocity"], [Uc, U_actual], color=["blue", "red"])
ax.set_ylabel("Velocity (m/s)")
ax.set_title("Critical vs Actual Flow Velocity")
st.pyplot(fig)

# --- Tube Layout ---
st.subheader("Tube Bundle Layout")
layout_type = st.radio("Layout Type:", ["Square Pitch", "Triangular Pitch"])
rows, cols = (10, 10) if layout_type == "Square Pitch" else (12, 9)

x, y = [], []
for i in range(rows):
    for j in range(cols):
        x_pos = i * pitch
        y_pos = j * pitch + (pitch / 2 if layout_type == "Triangular Pitch" and i % 2 else 0)
        x.append(x_pos)
        y.append(y_pos)

fig, ax = plt.subplots()
ax.scatter(x, y, c='orange', edgecolors='black', s=80)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title(f"{layout_type} Tube Layout")
ax.axis("equal")
st.pyplot(fig)

# --- Optional: Shell-Side Flow Visualization ---
st.subheader("Shell-Side Flow Field (Simplified)")
x = np.linspace(0, 1, 10)
y = np.linspace(0, 1, 10)
X, Y = np.meshgrid(x, y)
U = np.sin(2 * np.pi * X)
V = np.cos(2 * np.pi * Y)

fig, ax = plt.subplots()
ax.quiver(X, Y, U, V)
ax.set_title("Velocity Vector Field")
ax.set_xlabel("X")
ax.set_ylabel("Y")
st.pyplot(fig)

st.markdown("Made with ❤️ in Streamlit & VS Code")

