import numpy as np
import matplotlib.pyplot as plt
import redpitaya_scpi as scpi

# Connect to Red Pitaya
rp = scpi.scpi("10.0.0.166")


# Signal parameters
frequency = 40000  # Frequency in Hz
duration = 0.01    # Signal duration in seconds
amplitude = 1.0    # Signal amplitude (peak-to-peak) in Volts

# Get the sample rate from Red Pitaya
sample_rate = 125e6
# Time vector
t = np.linspace(0, duration, int(duration * sample_rate))

# Generate signal
signal = np.cos(2 * np.pi * frequency * (t - duration/2))

# Apply rectification
signal *= (np.abs(t - duration/2) < duration/2)

# Scale the signal to the desired amplitude
signal *= amplitude/2

# Set the generated signal to the DAC channel
rp.tx_txt('SOUR1:FUNC ARBITRARY')
rp.tx_txt('SOUR1:TRAC:DATA:DATA ' + ','.join(map(str, signal)))

# Enable the DAC channel output
#rp.tx_txt('OUTPUT1:STATE ON')

# Enable the ADC channel
rp.tx_txt('ACQ:SOUR1:DATA:TYPE NORMAL')
rp.tx_txt('ACQ:SOUR1:DATA:FORMAT ASCII')

# Set the ADC sampling rate and number of samples
rp.tx_txt('ACQ:SRATE ' + str(sample_rate))
rp.tx_txt('ACQ:POINTS ' + str(len(t)))

# Trigger the ADC to start sampling
rp.tx_txt('ACQ:START')

# Wait for the acquisition to complete
rp.tx_txt('ACQ:TRIG:STATUS WAIT')

# Retrieve the sampled data from the ADC
rp.tx_txt('ACQ:SOUR1:DATA?')
data = rp.rx_txt()

# Convert the data from string to numpy array
data = np.array(list(map(float, data.strip().split(','))))

# Time vector for plotting
time_vector = np.arange(len(data)) / sample_rate

# Plot the sampled data
plt.plot(time_vector, data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Sampled Signal')
plt.show()

# Disable the DAC and ADC channels
rp.tx_txt('OUTPUT1:STATE OFF')
rp.tx_txt('ACQ:STOP')