import warnings
warnings.filterwarnings("ignore", message="Unable to import Axes3D")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt
import tkinter as tk
from tkinter import ttk

# Початкові значення параметрів
initial_values = {
    'amplitude': 1.0,
    'frequency': 1.0,
    'phase': 0.0,
    'noise_mean': 0.0,
    'noise_covariance': 0.1,
    'show_noise': True,
    'filter_order': 3,
    'filter_cutoff': 0,
    'show_filtered': True
}

# Параметри часу
t = np.linspace(0, 1, 1000)

# Ініціалізація змінних
last_noise_covariance = initial_values['noise_covariance']
last_noise_mean = initial_values['noise_mean']
signal = np.zeros_like(t)
noisy_signal = np.zeros_like(t)
original_noisy_signal = np.zeros_like(t)
filtered_signal = np.zeros_like(t)
noise = np.random.normal(initial_values['noise_mean'], np.sqrt(initial_values['noise_covariance']), len(t))
signal_color = 'blue'
noisy_signal_color = 'lightpink'
filtered_signal_color = 'green'

def create_plot():
    fig, ax1 = plt.subplots(figsize=(10, 6))
    line_signal, = ax1.plot(t, signal, label='Signal', color=signal_color)
    line_noisy_signal, = ax1.plot(t, noisy_signal, label='Noisy Signal', color=noisy_signal_color)
    line_filtered_signal, = ax1.plot(t, filtered_signal, label='Filtered Signal', color=filtered_signal_color)
    ax1.legend()
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Harmonic Signal with Noise')
    ax1.grid(True)
    return fig, ax1, line_signal, line_noisy_signal, line_filtered_signal

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise=True):
    global noise, last_noise_covariance, signal, noisy_signal, original_noisy_signal, last_noise_mean
    
    if noise_mean != last_noise_mean or last_noise_covariance != noise_covariance:
        noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
        last_noise_covariance = noise_covariance
        last_noise_mean = noise_mean
    
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    original_noisy_signal = signal + noise
    
    if show_noise:
        noisy_signal = original_noisy_signal
    else:
        noisy_signal = signal
    
    update_filtered_signal()

def update_filtered_signal():
    global filtered_signal
    filter_order = filter_order_var.get()
    filter_cutoff = filter_cutoff_slider.get()
    b, a = butter(filter_order, filter_cutoff, btype='low')
    filtered_signal = filtfilt(b, a, noisy_signal)

def update_plot(val):
    amplitude = amplitude_slider.get()
    frequency = frequency_slider.get()
    phase = phase_slider.get()
    noise_mean = noise_mean_slider.get()
    noise_covariance = noise_covariance_slider.get()
    show_noise = show_noise_var.get()
    show_filtered = show_filtered_var.get()
    
    harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
    
    line_signal.set_ydata(signal)
    line_noisy_signal.set_ydata(noisy_signal)
    line_filtered_signal.set_ydata(filtered_signal)
    
    if show_noise and show_filtered:
        ax1.set_title('Harmonic Signal with Noise and Filtered Signal')
        line_noisy_signal.set_visible(True)
        line_filtered_signal.set_visible(True)
    elif show_noise:
        ax1.set_title('Harmonic Signal with Noise')
        line_noisy_signal.set_visible(True)
        line_filtered_signal.set_visible(False)
    elif show_filtered:
        ax1.set_title('Harmonic Signal and Filtered Signal')
        line_noisy_signal.set_visible(False)
        line_filtered_signal.set_visible(True)
    else:
        ax1.set_title('Harmonic Signal')
        line_noisy_signal.set_visible(False)
        line_filtered_signal.set_visible(False)
    
    ax1.relim()
    ax1.autoscale_view()
    fig.canvas.draw()

def reset_values():
    amplitude_slider.set(initial_values['amplitude'])
    frequency_slider.set(initial_values['frequency'])
    phase_slider.set(initial_values['phase'])
    noise_mean_slider.set(initial_values['noise_mean'])
    noise_covariance_slider.set(initial_values['noise_covariance'])
    filter_order_slider.set(initial_values['filter_order'])
    filter_cutoff_slider.set(initial_values['filter_cutoff'])
    show_noise_var.set(initial_values['show_noise'])
    show_filtered_var.set(initial_values['show_filtered'])
    update_plot(None)

# Tkinter GUI setup
root = tk.Tk()
root.title("Harmonic Signal with Noise")

fig, ax1, line_signal, line_noisy_signal, line_filtered_signal = create_plot()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

controls_frame = ttk.Frame(root)
controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

amplitude_label = ttk.Label(controls_frame, text="Amplitude")
amplitude_label.pack(side=tk.LEFT)
amplitude_slider = ttk.Scale(controls_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, length=200, command=update_plot)
amplitude_slider.set(initial_values['amplitude'])
amplitude_slider.pack(side=tk.LEFT)

frequency_label = ttk.Label(controls_frame, text="Frequency")
frequency_label.pack(side=tk.LEFT)
frequency_slider = ttk.Scale(controls_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, length=200, command=update_plot)
frequency_slider.set(initial_values['frequency'])
frequency_slider.pack(side=tk.LEFT)

phase_label = ttk.Label(controls_frame, text="Phase")
phase_label.pack(side=tk.LEFT)
phase_slider = ttk.Scale(controls_frame, from_=0.0, to=2*np.pi, orient=tk.HORIZONTAL, length=200, command=update_plot)
phase_slider.set(initial_values['phase'])
phase_slider.pack(side=tk.LEFT)

noise_mean_label = ttk.Label(controls_frame, text="Noise Mean")
noise_mean_label.pack(side=tk.LEFT)
noise_mean_slider = ttk.Scale(controls_frame, from_=-1.0, to=1.0, orient=tk.HORIZONTAL, length=200, command=update_plot)
noise_mean_slider.set(initial_values['noise_mean'])
noise_mean_slider.pack(side=tk.LEFT)

noise_covariance_label = ttk.Label(controls_frame, text="Noise Covariance")
noise_covariance_label.pack(side=tk.LEFT)
noise_covariance_slider = ttk.Scale(controls_frame, from_=0.01, to=1.0, orient=tk.HORIZONTAL, length=200, command=update_plot)
noise_covariance_slider.set(initial_values['noise_covariance'])
noise_covariance_slider.pack(side=tk.LEFT)


filter_order_var = tk.IntVar(value=initial_values['filter_order'])
filter_order_label = ttk.Label(controls_frame, text="Filter Order")
filter_order_label.pack(side=tk.LEFT)
filter_order_slider = ttk.Scale(controls_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=filter_order_var, length=200, command=update_plot)
filter_order_slider.pack(side=tk.LEFT)

filter_cutoff_label = ttk.Label(controls_frame, text="Filter Cutoff")
filter_cutoff_label.pack(side=tk.LEFT)
filter_cutoff_slider = ttk.Scale(controls_frame, from_=0.01, to=0.5, orient=tk.HORIZONTAL, length=200, command=update_plot)
filter_cutoff_slider.set(initial_values['filter_cutoff'])
filter_cutoff_slider.pack(side=tk.LEFT)

show_noise_var = tk.BooleanVar(value=initial_values['show_noise'])
show_noise_checkbox = ttk.Checkbutton(controls_frame, text="Show Noisy Signal", variable=show_noise_var, command=lambda: update_plot(None))
show_noise_checkbox.pack(side=tk.LEFT)

show_filtered_var = tk.BooleanVar(value=initial_values['show_filtered'])
show_filtered_checkbox = ttk.Checkbutton(controls_frame, text="Show Filtered Signal", variable=show_filtered_var, command=lambda: update_plot(None))
show_filtered_checkbox.pack(side=tk.LEFT)

reset_button = ttk.Button(controls_frame, text="Reset", command=reset_values)
reset_button.pack(side=tk.LEFT)

# Initial plot update
update_plot(None)

root.mainloop()
