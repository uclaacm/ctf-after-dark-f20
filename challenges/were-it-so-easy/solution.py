from pydub import AudioSegment  
from pydub.playback import play  

# Import an audio file  
# Format parameter only 
# for readability  
wav_file = AudioSegment.from_file(file = "music.wav", format = "wav")

# Split stereo into channels
channels = wav_file.split_to_mono()

# Reverse the right channel
right_mono_channel = channels[1]
right_mono_channel += 25
backwards = right_mono_channel.reverse()

# Export the solution
backwards.export("sol.wav", format = "wav")

