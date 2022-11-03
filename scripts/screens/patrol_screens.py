from math import ceil
from random import choice, choices

from .base_screens import Screens, draw_menu_buttons, cat_profiles, draw_clan_name

from scripts.utility import draw, draw_large, draw_big
from scripts.game_structure.text import *
from scripts.game_structure.buttons import buttons
from scripts.cat.cats import Cat

class PatrolScreen(Screens):

    able_box = pygame.image.load("resources/images/patrol_able_cats.png")
    patrol_box = pygame.image.load("resources/images/patrol_cats.png")
    cat_frame = pygame.image.load("resources/images/patrol_cat_frame.png")
    app_frame = pygame.image.load("resources/images/patrol_app_frame.png")
    mate_frame = pygame.image.load("resources/images/patrol_mate_frame.png")

    def on_use(self):
        draw_clan_name()
        #verdana.text(
        #    'These cats are currently in the camp, ready for a patrol.',
        #    ('center', 115))
        #verdana.text('Choose up to six to take on patrol.', ('center', 135))
        #verdana.text(
        #    'Smaller patrols help cats gain more experience, but larger patrols are safer.',
        #    ('center', 155))

        screen.blit(PatrolScreen.able_box, (40, 460))
        screen.blit(PatrolScreen.patrol_box, (490, 460))
        screen.blit(PatrolScreen.cat_frame, (300, 165))

        draw_menu_buttons()
        able_cats = []

        for x in range(len(Cat.all_cats.values())):
            the_cat = list(Cat.all_cats.values())[x]
            if not the_cat.dead and the_cat.in_camp and the_cat not in game.patrolled and the_cat.status in [
                    'leader', 'deputy', 'warrior', 'apprentice'
            ] and not the_cat.exiled and the_cat not in game.switches['current_patrol']:
                if the_cat.status == 'leader':
                    able_cats.insert(0, the_cat)
                elif the_cat.status == 'deputy':
                    able_cats.insert(1, the_cat)
                elif the_cat.status == 'warrior':
                    able_cats.insert(2, the_cat)
                elif the_cat.status == 'apprentice':
                    able_cats.append(the_cat)


        all_pages = 1
        if len(able_cats) > 15:
            all_pages = int(ceil(len(able_cats) / 15.0))

        cats_on_page = 0

        pos_y = 500
        pos_x = 50

        random_options = []

        for x in range(len(able_cats)):
            if x + (game.switches['list_page'] - 1) * 15 > len(able_cats):
                game.switches['list_page'] = 1
            if game.switches['list_page'] > all_pages:
                game.switches['list_page'] = 1

            patrol_cat = able_cats[x + (game.switches['list_page'] - 1) * 15]

            if patrol_cat not in game.switches['current_patrol']:
                buttons.draw_button((0 + pos_x, pos_y),
                                    image=patrol_cat.sprite,
                                    cat=patrol_cat,
                                    hotkey=[x + 1, 11])
                random_options.append(patrol_cat)
            else:
                cats_on_page -= 1
                pos_x -= 50

            cats_on_page += 1
            pos_x += 50
            if pos_x >= 300:
                pos_x = 50
                pos_y += 50
            if cats_on_page >= 15 or x + (game.switches['list_page'] - 1) * 15 == len(able_cats) - 1:
                break

        if game.switches['list_page'] > 1:
            buttons.draw_image_button((75, 462),
                                      button_name='patrol_arrow_l',
                                      text='<',
                                      size=(34, 34),
                                      list_page=game.switches['list_page'] - 1,
                                      hotkey=[23]
                                      )
        else:
            buttons.draw_image_button((75, 462),
                                      button_name='patrol_arrow_l',
                                      text='<',
                                      size=(34, 34),
                                      list_page=game.switches['list_page'] - 1,
                                      hotkey=[23],
                                      available=False
                                      )

        if game.switches['list_page'] < all_pages:
            buttons.draw_image_button((241, 462),
                                      button_name='patrol_arrow_r',
                                      text='>',
                                      size=(34, 34),
                                      list_page=game.switches['list_page'] + 1,
                                      hotkey=[21]
                                      )
        else:
            buttons.draw_image_button((241, 462),
                                      button_name='patrol_arrow_r',
                                      text='>',
                                      size=(34, 34),
                                      list_page=game.switches['list_page'] + 1,
                                      hotkey=[21],
                                      available=False
                                      )

        pos_y1 = 508
        pos_x1 = 525

        if game.switches['show_info'] is False:
            for x in range(len(game.switches['current_patrol'])):

                patrol_cat = game.switches['current_patrol'][x]
                game.switches['patrol_remove'] = False

                buttons.draw_button((0 + pos_x1, 0 + pos_y1),
                                    image=patrol_cat.sprite,
                                    patrol_remove=True,
                                    )
                if game.switches['patrol_remove'] is True:
                    game.switches['current_patrol'].remove(patrol_cat)
                    able_cats.append(patrol_cat)

                pos_x1 += 75
                if pos_x1 >= 725:
                    pos_x1 = 525
                    pos_y1 += 50

        if len(game.switches['current_patrol']) < 6:
            buttons.draw_image_button((430, 458),
                                      button_name='random_dice',
                                      size=(34, 34),
                                      cat=choice(able_cats),
                                      hotkey=[12])
        else:
            buttons.draw_image_button((430, 458),
                                      button_name='random_dice',
                                      size=(34, 34),
                                      cat=choice(able_cats),
                                      hotkey=[12],
                                      available=False)


        #  This keeps causing an IndexError whenever you add 6 cats and then try to click on one of those cats.
        #  I am at a loss as to how to fix it

        # if len(game.switches['current_patrol']) == 0:
        #    buttons.draw_image_button((450, 458),
        #                              button_name='add_6',
        #                              size=(34, 34),
        #                              fill_patrol=True,)
        #    if game.switches['fill_patrol'] is True:
        #        game.switches['current_patrol'] = []
        #        for x in range(6):
        #            random_cat = choice(able_cats)
        #            if random_cat not in game.switches['current_patrol']:
        #                game.switches['current_patrol'].insert(1, random_cat)
        #        game.switches['fill_patrol'] = False





        buttons.draw_image_button((560, 627),
                                  button_name='remove_all',
                                  size=(124, 35),
                                  current_patrol=[],
                                  )

        buttons.draw_image_button((505, 460),
                                  button_name='patrol2',
                                  size=(80, 35),
                                  show_info=False
                                  )
        buttons.draw_image_button((590, 460),
                                  button_name='skills_traits',
                                  size=(154, 35),
                                  show_info=True
                                  )

        if game.switches['cat'] is not None:
            self.show_info(able_cats)
        else:
            buttons.draw_button(
                (330, 460),
                image='buttons/add_cat',
                text='Add to Patrol',
                available=False)

        if len(game.switches['current_patrol']) > 0:
            buttons.draw_button(('center', 630),
                                text='Start Patrol',
                                cur_screen='patrol event screen',
                                hotkey=[13])

        else:
            buttons.draw_button(('center', 630),
                                text='Start Patrol',
                                available=False)

    # TODO Rename this here and in `on_use`
    def show_info(self, able_cats):

        # CHOSEN CAT INFO
        chosen_cat = game.switches['cat']  # cat

        y_value = 175
        draw_large(chosen_cat, (320, y_value))  # sprite

        y_value += 150
        verdana.text(str(chosen_cat.name),  # name
                     ('center', y_value))
        y_value += 25
        verdana_small.text(str(chosen_cat.status),  # rank
                           ('center', y_value))
        y_value += 15

        verdana_small.text(str(chosen_cat.trait),  # trait
                           ('center', y_value))
        y_value += 15

        verdana_small.text(str(chosen_cat.skill),  # skill
                           ('center', y_value))
        y_value += 15

        verdana_small.text(
            'experience: ' +
            str(chosen_cat.experience_level),  # exp
            ('center', y_value))
        y_value += 15

        # SHOW MATE SPRITE AND BUTTON
        if chosen_cat.status != 'apprentice':
            if chosen_cat.mate is not None:
                mate = Cat.all_cats[chosen_cat.mate]
                screen.blit(PatrolScreen.mate_frame, (140, 190))
                draw_big(mate, (150, 200))
                if mate in able_cats:
                    buttons.draw_image_button(
                        (148, 322),
                        button_name='patrol_add_mate',
                        size=(104, 30),
                        cat=mate
                        )
                else:
                    buttons.draw_image_button(
                        (148, 322),
                        button_name='patrol_add_mate',
                        size=(104, 30),
                        cat=mate,
                        available=False
                        )
                verdana.text(str(mate.name), (152, 300))

        # SHOW MENTOR SPRITE AND BUTTON
        if chosen_cat.status == 'apprentice':
            if chosen_cat.mentor is not None:
                screen.blit(PatrolScreen.app_frame, (494, 190))
                draw_big(chosen_cat.mentor, (550, 200))
                if chosen_cat.mentor in able_cats:
                    buttons.draw_image_button(
                        (548, 322),
                        button_name='patrol_add_mentor',
                        size=(104, 30),
                        cat=chosen_cat.mentor
                        )
                else:
                    buttons.draw_image_button(
                        (548, 322),
                        button_name='patrol_add_mentor',
                        size=(104, 30),
                        cat=chosen_cat.mentor,
                        available=False
                        )
                verdana.text(str(chosen_cat.mentor.name), (552, 300))
                verdana_small.text(f'mentor: {str(chosen_cat.mentor.name)}', ('center', y_value))

        # SHOW APPRENTICE SPRITE AND BUTTON
        if chosen_cat.apprentice != []:
            screen.blit(PatrolScreen.app_frame, (495, 190))
            draw_big(chosen_cat.apprentice[0], (550, 200))
            if chosen_cat.apprentice[0] in able_cats:
                buttons.draw_image_button(
                    (548, 322),
                    button_name='patrol_add_app',
                    size=(104, 30),
                    cat=chosen_cat.apprentice[0]
                    )
            else:
                buttons.draw_image_button(
                    (548, 322),
                    button_name='patrol_add_app',
                    size=(104, 30),
                    cat=chosen_cat.apprentice[0],
                    available=False
                    )
            verdana.text(str(chosen_cat.apprentice[0].name), (552, 300))

        # ADD CAT TO PATROL
        if len(game.switches['current_patrol']) < 6 and chosen_cat is not None\
                and chosen_cat not in game.switches['current_patrol']:
            buttons.draw_button(
                (330, 460),
                image='buttons/add_cat',
                text='Add to Patrol',
                current_patrol=chosen_cat,
                add=True,
                hotkey=[11],)
        else:
            buttons.draw_button(
                (330, 460),
                image='buttons/add_cat',
                text='Add to Patrol',
                current_patrol=chosen_cat,
                add=True,
                hotkey=[11],
                available=False)
        # remove chosen_cat from able cats once they are added to the patrol
        if chosen_cat in game.switches['current_patrol'] and chosen_cat in able_cats:
            able_cats.remove(chosen_cat)

        # SHOW CURRENT PATROL SKILLS AND TRAITS
        if game.switches['show_info'] is True:
            if game.switches['current_patrol'] is not []:
                patrol_skills = []
                patrol_traits = []
                for x in game.switches['current_patrol']:
                    if x.skill not in patrol_skills:
                        patrol_skills.append(x.skill)
                    if x.trait not in patrol_traits:
                        patrol_traits.append(x.trait)

                pos_x = 510
                pos_y = 510

                verdana_small_dark.blit_text(
                    f'current patrol skills: {self.get_list_text(patrol_skills)}',
                    (pos_x, pos_y),
                    x_limit=750
                )

                pos_y = 575

                verdana_small_dark.blit_text(
                    f'current patrol traits: {self.get_list_text(patrol_traits)}',
                    (pos_x, pos_y),
                    x_limit=750
                )

    def get_list_text(self, patrol_list):
        if not patrol_list:
            return ""
        patrol_set = list(patrol_list)
        return ", ".join(patrol_set)

    def screen_switches(self):
        game.switches['current_patrol'] = []
        game.switches['cat'] = None
        game.patrol_cats = {}
        game.switches['event'] = 0
        cat_profiles()
