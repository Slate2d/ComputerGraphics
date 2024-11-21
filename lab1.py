import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import colorsys

updating = False


def update_from_rgb():
    global updating
    if updating:
        return
    updating = True

    r = r_value.get()
    g = g_value.get()
    b = b_value.get()

    c, m, y, k = rgb_to_cmyk(r, g, b)
    c_value.set(c)
    m_value.set(m)
    y_value.set(y)
    k_value.set(k)

    h, l, s = rgb_to_hls(r, g, b)
    h_value.set(h)
    l_value.set(l)
    s_value.set(s)

    update_color_display(r, g, b)
    updating = False


def update_from_cmyk():
    global updating
    if updating:
        return
    updating = True

    c = c_value.get()
    m = m_value.get()
    y = y_value.get()
    k = k_value.get()

    r, g, b = cmyk_to_rgb(c, m, y, k)
    r_value.set(r)
    g_value.set(g)
    b_value.set(b)

    h, l, s = rgb_to_hls(r, g, b)
    h_value.set(h)
    l_value.set(l)
    s_value.set(s)

    update_color_display(r, g, b)
    updating = False


def update_from_hls():
    global updating
    if updating:
        return
    updating = True

    h = h_value.get()
    l = l_value.get()
    s = s_value.get()

    r, g, b = hls_to_rgb(h, l, s)
    r_value.set(r)
    g_value.set(g)
    b_value.set(b)

    c, m, y, k = rgb_to_cmyk(r, g, b)
    c_value.set(c)
    m_value.set(m)
    y_value.set(y)
    k_value.set(k)

    update_color_display(r, g, b)
    updating = False


def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1

    r_prime = r / 255
    g_prime = g / 255
    b_prime = b / 255

    k = 1 - max(r_prime, g_prime, b_prime)

    if k == 1:
        return 0, 0, 0, 1

    c = (1 - r_prime - k) / (1 - k)
    m = (1 - g_prime - k) / (1 - k)
    y = (1 - b_prime - k) / (1 - k)

    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)


def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return int(r), int(g), int(b)


def rgb_to_hls(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return round(h * 360, 2), round(l * 100, 2), round(s * 100, 2)


def hls_to_rgb(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)


def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[0]
    if color_code:
        r, g, b = map(int, color_code)
        r_value.set(r)
        g_value.set(g)
        b_value.set(b)
        update_from_rgb()


def update_color_display(r, g, b):
    color_hex = f"#{r:02x}{g:02x}{b:02x}"
    color_display.config(bg=color_hex)


def on_rgb_change(*args):
    update_from_rgb()


def on_cmyk_change(*args):
    update_from_cmyk()


def on_hls_change(*args):
    update_from_hls()


root = tk.Tk()
root.geometry("700x500")
root.title("Color Model Converter")

color_display = tk.Label(root, bg="black", width=20, height=4)
color_display.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

# RGB Inputs
rgb_label = ttk.Label(root, text="RGB:")
rgb_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

r_value = tk.IntVar()
g_value = tk.IntVar()
b_value = tk.IntVar()

r_value.trace("w", on_rgb_change)
g_value.trace("w", on_rgb_change)
b_value.trace("w", on_rgb_change)

r_entry = ttk.Entry(root, textvariable=r_value, width=5)
r_entry.grid(row=1, column=1, padx=5, pady=5)

g_entry = ttk.Entry(root, textvariable=g_value, width=5)
g_entry.grid(row=1, column=2, padx=5, pady=5)

b_entry = ttk.Entry(root, textvariable=b_value, width=5)
b_entry.grid(row=1, column=3, padx=5, pady=5)

r_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", variable=r_value)
r_slider.grid(row=2, column=1, sticky="we", padx=5, pady=5)

g_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", variable=g_value)
g_slider.grid(row=2, column=2, sticky="we", padx=5, pady=5)

b_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", variable=b_value)
b_slider.grid(row=2, column=3, sticky="we", padx=5, pady=5)

# CMYK Inputs
cmyk_label = ttk.Label(root, text="CMYK:")
cmyk_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

c_value = tk.DoubleVar()
m_value = tk.DoubleVar()
y_value = tk.DoubleVar()
k_value = tk.DoubleVar()

c_value.trace("w", on_cmyk_change)
m_value.trace("w", on_cmyk_change)
y_value.trace("w", on_cmyk_change)
k_value.trace("w", on_cmyk_change)

c_entry = ttk.Entry(root, textvariable=c_value, width=5)
c_entry.grid(row=3, column=1, padx=5, pady=5)

m_entry = ttk.Entry(root, textvariable=m_value, width=5)
m_entry.grid(row=3, column=2, padx=5, pady=5)

y_entry = ttk.Entry(root, textvariable=y_value, width=5)
y_entry.grid(row=3, column=3, padx=5, pady=5)

k_entry = ttk.Entry(root, textvariable=k_value, width=5)
k_entry.grid(row=3, column=4, padx=5, pady=5)

c_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=c_value)
c_slider.grid(row=4, column=1, sticky="we", padx=5, pady=5)

m_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=m_value)
m_slider.grid(row=4, column=2, sticky="we", padx=5, pady=5)

y_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=y_value)
y_slider.grid(row=4, column=3, sticky="we", padx=5, pady=5)

k_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=k_value)
k_slider.grid(row=4, column=4, sticky="we", padx=5, pady=5)

# HLS Inputs
hls_label = ttk.Label(root, text="HLS:")
hls_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")

h_value = tk.DoubleVar()
l_value = tk.DoubleVar()
s_value = tk.DoubleVar()

h_value.trace("w", on_hls_change)
l_value.trace("w", on_hls_change)
s_value.trace("w", on_hls_change)

h_entry = ttk.Entry(root, textvariable=h_value, width=5)
h_entry.grid(row=5, column=1, padx=5, pady=5)

l_entry = ttk.Entry(root, textvariable=l_value, width=5)
l_entry.grid(row=5, column=2, padx=5, pady=5)

s_entry = ttk.Entry(root, textvariable=s_value, width=5)
s_entry.grid(row=5, column=3, padx=5, pady=5)

h_slider = tk.Scale(root, from_=0, to=360, orient="horizontal", variable=h_value)
h_slider.grid(row=6, column=1, sticky="we", padx=5, pady=5)

l_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=l_value)
l_slider.grid(row=6, column=2, sticky="we", padx=5, pady=5)

s_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=s_value)
s_slider.grid(row=6, column=3, sticky="we", padx=5, pady=5)

choose_color_btn = ttk.Button(root, text="Choose Color", command=choose_color)
choose_color_btn.grid(row=7, column=0, columnspan=5, padx=5, pady=5)

root.mainloop()
