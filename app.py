import numpy as np
import streamlit as st

# Metode Trapezoidal Rule
def trapezoidal_rule(x, y):
    n = len(x)  # Jumlah titik (jumlah subinterval + 1)
    integral = (x[-1] - x[0]) * (y[0] + 2 * np.sum(y[1:n-1]) + y[n-1]) / (2 * (n - 1))
    return integral

# Metode Midpoint Rule
def midpoint_rule(x, y):
    n = len(x)  # Jumlah titik (jumlah subinterval + 1)
    integral = 0
    for i in range(n - 1):
        midpoint = (x[i] + x[i+1]) / 2
        integral += (x[i+1] - x[i]) * np.interp(midpoint, x, y)
    return integral

# Metode Simpson 1/3 Rule
def simpson_one_third_rule(x, y):
    n = len(x)  # Jumlah titik (jumlah subinterval + 1)
    if n % 2 == 0:
        raise ValueError("Jumlah titik harus ganjil untuk Simpson 1/3 Rule!")
    integral = y[0] + y[-1]
    for i in range(1, n-1, 2):
        integral += 4 * y[i]
    for i in range(2, n-2, 2):
        integral += 2 * y[i]
    integral *= (x[1] - x[0]) / 3
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

# Validasi metode yang dipilih
if selection is None:
    st.warning("Tolong pilih metode terlebih dahulu!!!")
else:
    st.write(f"Metode yang dipilih: {option_map[selection]}")

    # Input jumlah titik
    st.subheader("Tentukan jumlah nilai x dan y")
    try:
        num_points = st.number_input("Masukkan jumlah nilai x dan y:", min_value=2, step=1, value=4)

        if num_points:
            if selection == 2 and num_points % 2 == 0:
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
                            elif selection == 1:
                                result = midpoint_rule(x_array, y_array)
                            elif selection == 2:
                                result = simpson_one_third_rule(x_array, y_array)

                            st.success(f"Integral menggunakan metode {option_map[selection]} adalah: {result}")
                        except ValueError as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Panjang array x dan y harus sama.")
    except ValueError:
        st.error("Masukkan jumlah nilai x dan y yang valid.")
