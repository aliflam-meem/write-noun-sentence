import pathlib


snowman_working_directory = pathlib.Path(__file__).parent

# Images
SNOWMAN_GAME_RESULT = snowman_working_directory / 'assets/images/snowman_game_result.png'
SNOWMAN_GAME_SCREEN_BG = snowman_working_directory / 'assets/images/cartoon_style_snowy_landscape.jpg'
SNOWMAN_GAME_SCREEN_BG_TRA = snowman_working_directory / 'assets/images/cartoon_style_snowy_landscape_transparent.png'
snowman_thumbnail = snowman_working_directory / 'assets/images/snowman_thumbnail.jpg'
CHECK_MARK_IMAGE_PATH = snowman_working_directory / 'assets/images/check_mark.png'

# Sounds
snow_melting_sound = snowman_working_directory / 'assets/audio/snow_melting.mp3'

snowman_levels_keys = ["al_atareef", "demonstratives", "pronouns"]
snowman_levels = {
    snowman_levels_keys[0]: {
        "name": "al_atareef",
        "title": "المعرف بأل التعريف",
        "noun_types": ["اسم ظاهر معرف بـأل التعريف،بحالة المفرد",
                       "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المذكر",
                       "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المؤنث",
                       "اسم ظاهر معرف بـأل التعريف،بحالة جمع المؤنث السالم",
                       "اسم ظاهر معرف بـأل التعريف،بحالة جمع المذكر السالم"
                       "اسم ظاهر معرف بـأل التعريف،بحالة جمع التكسير"]
    },
    snowman_levels_keys[1]: {
        "name": "demonstratives",
        "title": "اسم الإشارة",
        "noun_types": ["اسم إشارة"]
    },
    snowman_levels_keys[2]: {
        "name": "pronouns",
        "title": "الضمير",
        "noun_types": ["ضمير مفرد", "ضمير مثنى", "ضمير جمع"]
    }
}
