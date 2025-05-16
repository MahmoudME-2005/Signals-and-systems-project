import numpy as np # Will be used in almost everything
import soundfile as sf # To read the audio file as input
import matplotlib.pyplot as plt # For plotting
from scipy import signal 
import sounddevice as sd

# A function that takes both the signal's td_mags and the signal's length as input and
# returns the value of the signal's energy
def calculate_energy_timedomain(signal_mags,signal_len):
    Energy = 0

    for i in range(0,signal_len):
        Energy += signal_mags[i]**2
    
    return Energy

def calculate_energy_freqdomain(signal_mags,signal_len):
    Energy = 0

    for i in range(0, signal_len):
        Energy += (np.abs(signal_mags[i]))**2
    
    return Energy/signal_len

again = True

while(again):
    # Read audio
    loop = True
    while (loop):
        Response = input("Would you like to use a specific audio file or the default one?(S/D): ").lower()
        if (Response == "s"):
            filename = input("Enter the path to the audio file: ")
            loop = False
        elif (Response == "d"):
            filename = "Audio\Main inputs\Input.wav"
            loop = False
        else:
            print("Please enter S for specific audio file or D for default audio file.")
    td_mags, td_freq = sf.read(filename)

    # Adjusting the time axis values
    data_len = len(td_mags)
    duration = data_len / td_freq
    time = np.linspace(0, duration, len(td_mags))

    # Playing the signal in time domain
    loop = True
    while (loop):
        response = input("Would you like to listen to the input audio file?(Y/N): ").lower()
        if(response == "y" or response == "yes"):
            sd.play(td_mags,td_freq)

            # Plotting the time domain signal using the python library matplotlib
            plt.plot(time, td_mags)
            plt.xlabel("Time in seconds")
            plt.ylabel("Amplitude")
            plt.title("Time Domain Signal")
            plt.grid()
            plt.show()

            sd.wait()
            loop = False
        elif (response == "n" or response == "no"):
            # Plotting the time domain signal using the python library matplotlib
            plt.plot(time, td_mags)
            plt.xlabel("Time in seconds")
            plt.ylabel("Amplitude")
            plt.title("Time Domain Signal")
            plt.grid()
            plt.show()
            loop = False
        else:
            print("Please enter Y if you want to listen or N if not.")


    # Signal's energy calculation in time domain
    Energy_timedomain = calculate_energy_timedomain(td_mags,data_len)
    print("-" * 80 + "\nEnergy calculations in both domains:\n")
    print(f"Time domain energy of the signal: {Energy_timedomain}")
    input("Press enter to continue.")

    # Trasforming the signal from time domain to freq domain using fft algorithim which is
    # built into the python library numpy
    fd_freqs = np.fft.fftfreq(data_len, 1/(td_freq)) #getting the values for the freq axis but not in order
    fd_mags = np.fft.fft(td_mags) # getting the magnitudes of the freq domain but not in order
    fd_freqs = np.fft.fftshift(fd_freqs) # Arranging the values on the freq axis for plotting
    fd_mags = np.fft.fftshift(fd_mags) # Arranging the values on the magnitude axis for plotting 

    # Plotting the freq domain signal
    plt.plot(fd_freqs, np.abs(fd_mags))
    plt.title("Frequency Domain Representation")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

    # Calculating the energy of the signal in freq domain
    Energy_freqdomain = calculate_energy_freqdomain(fd_mags,data_len)
    print(f"Freq domain Energy of the signal: {Energy_freqdomain}\n")
    print(f"The differnce between energies in both domains: {Energy_timedomain - Energy_freqdomain}\nAs we can see they are almost equal as the difference is only due to floating point errors")
    input("Press enter to continue.")

    # Applying butterworth low pass filter
    cutoff_freq = int(input("Specify the cutoff frequency(recommended: 2000): "))
    nyquist = 0.5 * td_freq
    normal_cutoff = cutoff_freq / nyquist

    # Design 10th-order Butterworth LPF
    b, a = signal.butter(10, normal_cutoff, btype='lowpass')

    # Apply filter (zero-phase)
    td_filtered_mags = signal.filtfilt(b, a, td_mags)

    # Playing the filtered signal in time domain
    loop = True
    while (loop):
        response = input("-" * 80 + "\nWould you like to listen to the filtered audio file?(Y/N): ").lower()
        if(response == "y" or response == "yes"):
            sd.play(td_filtered_mags,td_freq)

            # Plot the filtered signal in time domain
            plt.plot(time, td_filtered_mags)
            plt.title("Filtered Signal (Time Domain)")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.show()

            sd.wait()
            loop = False
        elif (response == "n" or response == "no"):
            # Plot the filtered signal in time domain
            plt.plot(time, td_filtered_mags)
            plt.title("Filtered Signal (Time Domain)")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.show()
            loop = False
        else:
            print("Pleas enter Y if you want to listen or N if not.")


    # Transforming the filtered signal in time domain to the frequency domain
    fd_filtered_mags = np.fft.fft(td_filtered_mags)
    fd_filtered_mags = np.fft.fftshift(fd_filtered_mags)

    # Plot the filtered signal in frequency domain
    plt.plot(fd_freqs, np.abs(fd_filtered_mags))
    plt.title("Filtered Signal (Frequency Domain)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

    # Saving the processed audio file after applying the filter
    output_file_name = input("Enter the name for the output audio file: ")
    output_file_path = f"Audio\Main outputs\{output_file_name}.WAV"
    sf.write(output_file_path, td_filtered_mags, td_freq)
    print("\n" + "-" * 80 + "\n\nThe processed audio file was successfuly saved on your drive under the name " + output_file_name + " in the Main outputs folder\n\n" + "-" * 80)

    loop = True
    while (loop):
        response = input("would you like to try another audio file?(Y/N): ").lower()

        if(response == "y" or response == "yes"):
            again = True
            loop = False
        elif (response == "n" or response == "no"):
            again = False
            print("Thank you for using our app.")
            loop = False
        else:
            print("Press enter Y if you want to try another file or N if not.")