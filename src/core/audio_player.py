import pygame


def play_background_sound(audio_path, volume=0.5):
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.set_volume(volume)  # Sets the volume to 50%
    pygame.mixer.music.play(-1)  # The -1 makes the music loop indefinitely

def pause_background_sound(pause):
    if pause == True:
        pygame.mixer.music.pause()
    else:
       pygame.mixer.music.unpause()
    

def stop_background_sound():
    pygame.mixer.music.stop()


def play_sound(path, volume=0.5):
    audio = pygame.mixer.Sound(path)
    audio.set_volume(volume)
    audio.play()
