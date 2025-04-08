import numpy as np

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

# --- Input Section ---
print("=== Tube Natural Frequency Calculator ===\n")
D = get_float("Enter Tube Outside Diameter (D) in meters: ")
t = get_float("Enter Tube Thickness (t) in meters: ")
L = get_float("Enter Tube Length (L) in meters: ")
rho_material = get_float("Enter Density of Tube Material (kg/m³): ")
E = get_float("Enter Modulus of Elasticity (E) in Pa: ")

# Additional parameters (optional, not used in calculation)
baffle_thickness = get_float("Enter Baffle Thickness (m): ")
diam_clearance = get_float("Enter Diametral Clearance (m): ")
tube_pitch = get_float("Enter Tube Pitch (m): ")
rho_shell = get_float("Enter Shell Side Fluid Density (kg/m³): ")
rho_tube = get_float("Enter Tube Side Fluid Density (kg/m³): ")
V_flow = get_float("Enter Flow Velocity (m/s): ")
baffle_spacing_inlet = get_float("Enter Baffle Spacing (Inlet Span in m): ")
baffle_spacing_mid = get_float("Enter Baffle Spacing (Mid Span in m): ")
baffle_spacing_outlet = get_float("Enter Baffle Spacing (Outlet Span in m): ")

# --- Validation ---
if D <= 0 or t <= 0 or L <= 0:
    raise ValueError("Diameter, thickness, and length must be positive.")
if D <= 2 * t:
    raise ValueError("Tube thickness is too large for the given diameter (D must be > 2t).")

# --- Calculations ---
I = (np.pi / 64) * (D**4 - (D - 2*t)**4)  # Moment of inertia (m^4)
m = rho_material * (np.pi * (D**2 - (D - 2*t)**2)) / 4  # Mass per unit length (kg/m)
f_n = (1 / (2 * np.pi)) * np.sqrt(E * I / (m * L**2))  # Natural frequency (Hz)

# --- Output ---
print("\n--- Tube Vibration Analysis Summary ---")
print(f"Tube Outer Diameter:        {D:.4f} m")
print(f"Tube Thickness:             {t:.4f} m")
print(f"Tube Length:                {L:.4f} m")
print(f"Material Density:           {rho_material:.2f} kg/m³")
print(f"Modulus of Elasticity:      {E:.2e} Pa")
print(f"Second Moment of Area (I):  {I:.4e} m⁴")
print(f"Mass per Unit Length (m):   {m:.4f} kg/m")
print(f"Natural Frequency:          {f_n:.2f} Hz")
