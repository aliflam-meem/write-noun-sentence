import pygame

def play_background_sound(audio_path, volume=0.5):
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(-1)  # The -1 makes the music loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # Sets the volume to 50%


def stop_background_sound():
    pygame.mixer.music.stop()

def play_audio(path):
    audio = pygame.mixer.Sound(path)
    audio.play()
