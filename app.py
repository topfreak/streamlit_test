import numpy as np
import streamlit as st

def trapezoidal_rule(x, y):
    n = len(x)  # jumlah titik (jumlah subinterval + 1)
    integral = (x[-1] - x[0]) * (y[0] + 2 * np.sum(y[1:n-1]) + y[n-1]) / (2 * (n - 1))
    return integral

def midpoint_rule(x, y):
    n = len(x) - 1
    h = (x[-1] - x[0]) / n
    midpoints = (x[:-1] + x[1:]) / 2
    y_midpoints = np.interp(midpoints, x, y)
    integral = h * np.sum(y_midpoints)
    return integral

def simpson_one_third_rule(x, y):
    n = len(x) - 1
    if n % 2 != 0:
        raise ValueError("Jumlah titik harus ganjil untuk Simpson 1/3 Rule!")
    h = (x[-1] - x[0]) / n
    integral = y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])
    integral *= h / 3
    return integral

# Judul aplikasi
st.title("Metode Integrasi Numerik")

# Pilihan metode integrasi
st.subheader("Pilih metode integrasi")
option_map = {
    0: "Trapezoidal Rule",
    1: "Midpoint Rule",
    2: "Simpson 1/3 Rule",
}
selection = st.pills(
    "Pilih metode:",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)

if selection is None:
    st.warning("Tolong pilih metode terlebih dahulu!!!")
else:
    st.write(f"Metode yang dipilih: {option_map[selection]}")

# Input jumlah nilai x dan y
st.subheader("Tentukan jumlah nilai x dan y")
try:
    num_points = st.number_input("Masukkan jumlah nilai x dan y:", min_value=2, step=1, value=4)

    if num_points:
        # Validasi jika metode Simpson 1/3 dipilih
        if selection == 2 and (num_points - 1) % 2 != 0:
            st.error("Jumlah titik harus ganjil untuk Simpson 1/3 Rule!")
        else:
            # Input nilai x dan y secara manual
            st.subheader("Masukkan nilai x dan y")

            x_values = []
            y_values = []

            for i in range(num_points):
                cols = st.columns(2)
                with cols[0]:
                    x = st.number_input(f"x[{i+1}]:", key=f"x_{i}", format="%.10f")
                with cols[1]:
                    y = st.number_input(f"y[{i+1}]:", key=f"y_{i}", format="%.10f")
                x_values.append(x)
                y_values.append(y)

            if st.button("Hitung Integral"):
                x_array = np.array(x_values)
                y_array = np.array(y_values)

                if len(x_array) == len(y_array):
                    try:
                        if selection == 0:
                            result = trapezoidal_rule(x_array, y_array)
                            st.success(f"Integral menggunakan metode {option_map[selection]} adalah: {result}")
                        elif selection == 1:
                            result = midpoint_rule(x_array, y_array)
                            st.success(f"Integral menggunakan metode {option_map[selection]} adalah: {result}")
                        elif selection == 2:
                            result = simpson_one_third_rule(x_array, y_array)
                            st.success(f"Integral menggunakan metode {option_map[selection]} adalah: {result}")
                    except ValueError as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Panjang array x dan y harus sama.")
except ValueError:
    st.error("Masukkan jumlah nilai x dan y yang valid.")
