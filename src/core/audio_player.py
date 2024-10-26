import pygame


def play_background_sound(audio_path, volume=0.5):
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.set_volume(0.6)  # Sets the volume to 50%
    pygame.mixer.music.play(-1)  # The -1 makes the music loop indefinitely


def stop_background_sound():
    pygame.mixer.music.stop()


def play_sound(path, loops):
    audio = pygame.mixer.Sound(path)
    audio.play(loops=loops)
