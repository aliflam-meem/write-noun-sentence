# Constants
import pathlib

whack_a_mole_working_directory = pathlib.Path(__file__).parent

GRID_SIZE_X = 400
GRID_SIZE_Y = 180
X_OFFSET = 120
Y_OFFSET = 260
WM_TITLE_HEIGHT = 60
LINES_SPACING = 40
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WIN_GAME_iMAGE = whack_a_mole_working_directory / 'assets/images/Win.jpg'
LOSE_GAME_IMAGE = whack_a_mole_working_directory / 'assets/images/Game_Over.jpg'
WM_MUSIC = whack_a_mole_working_directory / 'assets/audio/game_music.mp3'
