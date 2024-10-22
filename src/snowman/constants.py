import pathlib

import pygame.image


snowman_working_directory = pathlib.Path(__file__).parent
SNOWMAN_GAME_RESULT = pygame.image.load(snowman_working_directory / 'assets/images/snowman_game_result.jpg')

snowman_levels_keys = ["al_atareef", "demonstratives", "pronouns"]
snowman_levels = {
    snowman_levels_keys[0]: {
        "name": "al_atareef",
        "title": "المعرف بأل التعريف",
        "noun_types": ["اسم ظاهر معرف بـأل التعريف،حالة المفرد",
                       "اسم ظاهر معرف بـأل التعريف،حالة المثنى",
                       "اسم ظاهر معرف بـأل التعريف،حالة جمع المؤنث السالم",
                       "اسم ظاهر معرف بـأل التعريف،حالة جمع المذكر السالم"
                       "اسم ظاهر معرف بـأل التعريف،حالة جمع التكسير"]
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
