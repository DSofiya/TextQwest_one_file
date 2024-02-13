import pygame
import sys
import os
import json
import random

from functions import (resource_path, read_character_info,
                       load_images, select_font, write_info_player, convert_picture)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 228, 181)
RED = (139, 0, 0)


class JSONReader:
    def read_json_file(self, filename_for_read):
        with open(filename_for_read, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def write_json_file(self, existing_data, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)


class GameInitializer:
    @staticmethod
    def initialize_game():
        pygame.init()
        bg_image_menu = pygame.image.load(resource_path(os.path.join("Menu_images", "picture_character.jpg")))
        bg_image = pygame.image.load(resource_path( os.path.join("Menu_images", "picture_menu.jpg")))
        window_size = bg_image.get_size()
        window = pygame.display.set_mode(window_size)
        button_font, menu_font, big_font, hand_font = select_font()
        image_race, image_clas = load_images()
        return window, window_size, bg_image, bg_image_menu, button_font, big_font, menu_font, hand_font, image_race, image_clas


class Button:
    def __init__(self, x, y, width, height, image_path, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.button_font, self.menu_font, self.big_font ,_ = select_font()
        self.text = text

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface, text_position, button_font):
        surface.blit(self.image, self.rect.topleft)
        text_surface = button_font.render(self.text, True, YELLOW)
        if text_position:
            text_rect = text_surface.get_rect(center=self.rect.midbottom)
        else:
            text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def draw_center(self, surface, button_font):
        surface.blit(self.image, self.rect.topleft)
        lines = str(self.text).splitlines()
        y_offset = 0
        for line in lines:
            text_surface = button_font.render(line, True, YELLOW)
            text_rect = text_surface.get_rect(
                centerx=self.rect.centerx, centery=self.rect.centery + y_offset)
            surface.blit(text_surface, text_rect)
            y_offset += text_rect.height


class ButtonManager:
    def __init__(self, bg_image, window_size, window):
        self.bg_image = bg_image
        self.window = window
        self.window_size = window_size
        self.button_font, _, self.big_font,_ = select_font()
        self.user_name = ""
        self.image_race, self.image_clas = load_images()

    def menu_buttons(self):
        buttons_data = [
            {
                "x": self.window_size[0] / 2.5,
                "y": self.window_size[0] / 5,
                "width": self.window_size[0] / 5,
                "height": self.window_size[1] / 8,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Створити героя",
            },
            {
                "x": self.window_size[0] / 2.5,
                "y": self.window_size[0] / 3.9,
                "width": self.window_size[0] / 5,
                "height": self.window_size[1] / 8,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Обрати пригоду",
            },
            {
                "x": self.window_size[0] / 2.5,
                "y": self.window_size[0] / 3.2,
                "width": self.window_size[0] / 5,
                "height": self.window_size[1] / 8,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Вихід",
            },
        ]
        buttons_menu = [Button(data["x"], data["y"], data["width"], data["height"],
                               data["image_path"], data["text"],)for data in buttons_data]

        return buttons_menu

    def character_buttons(self):
        buttons_data = [
            {
                "x": self.window_size[0] / 8,
                "y": self.window_size[0] / 7.5,
                "width": self.window_size[0] / 8,
                "height": self.window_size[0] / 5.5,
                "image_path": resource_path(os.path.join("Character", "Human_m.png")),
                "image_path_f": resource_path(os.path.join("Character", "Human_f.png")),
                "text": "Людина",
            },
            {
                "x": self.window_size[0] / 1.8,
                "y": self.window_size[0] / 7.5,
                "width": self.window_size[0] / 8,
                "height": self.window_size[0] / 5,
                "image_path": resource_path(os.path.join("Character", "Tieflings_m.png")),
                "image_path_f": resource_path(os.path.join("Character", "Tieflings_f.png")),
                "text": "Тифлінг",
            },
            {
                "x": self.window_size[0] / 2.2,
                "y": self.window_size[0] / 3.5,
                "width": self.window_size[0] / 8,
                "height": self.window_size[0] / 5.5,
                "image_path": resource_path(os.path.join("Character", "Ork_m.png")),
                "image_path_f": resource_path(os.path.join("Character", "Ork_f.png")),
                "text": "Орк",
            },
            {
                "x": self.window_size[0] / 1.5,
                "y": self.window_size[0] / 3.2,
                "width": self.window_size[0] / 8,
                "height": self.window_size[0] / 6.5,
                "image_path": resource_path(os.path.join("Character", "Gnomes_m.png")),
                "image_path_f": resource_path(os.path.join("Character", "Gnomes_f.png")),
                "text": "Гном",
            },
            {
                "x": self.window_size[0] / 2.9,
                "y": self.window_size[0] / 7.5,
                "width": self.window_size[0] / 9,
                "height": self.window_size[0] / 5.5,
                "image_path": resource_path(os.path.join("Character", "Elves_m.png")),
                "image_path_f": resource_path(os.path.join("Character", "Elves_f.png")),
                "text": "Ельф",
            },
            {
                "x": self.window_size[0] / 4.2,
                "y": self.window_size[0] / 3.5,
                "width": self.window_size[0] / 8,
                "height": self.window_size[0] / 5.5,
                "image_path": resource_path(os.path.join("Character", "Aasimar_m.png")),
                "image_path_f": resource_path(os.path.join("Character", "Aasimar_f.png")),
                "text": "Аазімар",
            },
            {
                "x": self.window_size[0] / 1.35,
                "y": self.window_size[0] / 10,
                "width": self.window_size[0] / 10,
                "height": self.window_size[0] / 10,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "image_path_f": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід у головне меню",
            },
        ]

        gender_button1 = Button(
            self.window_size[0] / 1.35,
            self.window_size[0] / 5.1,
            self.window_size[0] / 10,
            self.window_size[0] / 10,
            resource_path(os.path.join("Character", "male", "change.png")),
            "Змінити стать",
        )
        gender_button2 = Button(
            self.window_size[0] / 1.35,
            self.window_size[0] / 5.1,
            self.window_size[0] / 10,
            self.window_size[0] / 10,
            resource_path(os.path.join("Character", "male", "change2.png")),
            "Змінити стать",
        )

        buttons_m = [Button(data["x"], data["y"], data["width"], data["height"], data["image_path"], data["text"],)
                     for data in buttons_data]
        buttons_f = [Button(data["x"], data["y"], data["width"], data["height"], data["image_path_f"], data["text"],)
                     for data in buttons_data]

        return gender_button1, gender_button2, buttons_m, buttons_f

    def clas_buttons(self):
        buttons_data = [
            {
                "x": self.window_size[0] / 5,
                "y": self.window_size[0] / 8,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Bard.png")),
                "text": "Бард",
            },
            {
                "x": self.window_size[0] / 2.2,
                "y": self.window_size[0] / 8,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Cleric.png")),
                "text": "Клірик",
            },
            {
                "x": self.window_size[0] / 2.2,
                "y": self.window_size[0] / 3.2,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Fighter.png")),
                "text": "Воїн",
            },
            {
                "x": self.window_size[0] / 5,
                "y": self.window_size[0] / 3.2,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Wizard.png")),
                "text": "Чарівник",
            },
            {
                "x": self.window_size[0] / 1.35,
                "y": self.window_size[0] / 10,
                "width": self.window_size[0] / 10,
                "height": self.window_size[0] / 10,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід до головного меню ",
            },
        ]

        buttons_clas = [Button(data["x"], data["y"], data["width"], data["height"], data["image_path"], data["text"],)
                        for data in buttons_data]

        return buttons_clas

    def name_buttons(self):
        buttons_data = [
            {
                "x": self.window_size[0] / 1.4,
                "y": self.window_size[0] / 9.8,
                "width": self.window_size[0] / 10,
                "height": self.window_size[0] / 10,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід у головне меню",
            },
            {
                "x": self.window_size[0] / 2.5,
                "y": self.window_size[0] / 3.5,
                "width": self.window_size[0] / 5.5,
                "height": self.window_size[0] / 8,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Записати",
            },
            {
                "x": self.window_size[0] / 6,
                "y": self.window_size[0] / 4.2,
                "width": self.window_size[0] / 5,
                "height": self.window_size[0] / 5,
                "image_path": resource_path(os.path.join("Character", "random", "random1.png")),
                "text": "Рандомний вибір імені",
            },
        ]

        buttons_name = [Button(data["x"], data["y"], data["width"], data["height"], data["image_path"], data["text"],)
                        for data in buttons_data]

        button_random_images = [pygame.image.load(resource_path(os.path.join("Character", "random", "random1.png"))),
                                pygame.image.load(resource_path(os.path.join(
                                    "Character", "random", "random2.png"))),
                                pygame.image.load(resource_path(os.path.join("Character", "random", "random3.png"))),]

        current_image_index = 0

        button_random_rect = button_random_images[current_image_index].get_rect(
        )
        button_random_rect.x, button_random_rect.y = (
            self.window_size[0] / 6.5, self.window_size[0] / 4.2,)

        return buttons_name, button_random_images, button_random_rect

    def adventure_buttons(self):
        buttons_data = [
            {
                "x": self.window_size[0] / 1.38,
                "y": self.window_size[0] / 10,
                "width": self.window_size[0] / 9,
                "height": self.window_size[0] / 8,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід до головного меню ",
            },
            {
                "x": self.window_size[0] / 3.5,
                "y": self.window_size[0] / 4,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.6,
                "image_path": resource_path(os.path.join("Adventure", "castel.jpg")),
                "text": "Вбивство та суд у місті Леоніс",
            },
            {
                "x": self.window_size[0] / 2,
                "y": self.window_size[0] / 4,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.6,
                "image_path": resource_path(os.path.join("Adventure", "hotel.jpg")),
                "text": "Готель 'Етельбург'",
            },
        ]

        buttons_adventure = [Button(data["x"], data["y"], data["width"], data["height"],
                                    data["image_path"], data["text"],)for data in buttons_data]

        return buttons_adventure

    def game_buttons(self, ansver1, ansver2, count_gold):
        buttons_data = [
            {
                "x": self.window_size[0] /1.27,
                "y": self.window_size[1] / 7,
                "width": self.window_size[0] / 10,
                "height": self.window_size[1] /5,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід",
            },
            {
                "x": self.window_size[0] / 1.4,
                "y": self.window_size[1] / 7,
                "width": self.window_size[0] / 10,
                "height": self.window_size[1] / 5,
                "image_path": resource_path(os.path.join("Character", "save1.png")),
                "text": "Зберегти",
            },
            {
                "x": self.window_size[0] / 8,
                "y": self.window_size[1] / 1.7,
                "width": self.window_size[0] / 3,
                "height": self.window_size[0] / 5,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": ansver1,
            },
            {
                "x": self.window_size[0] / 2,
                "y": self.window_size[1] / 1.7,
                "width": self.window_size[0] / 3,
                "height": self.window_size[0] / 5,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": ansver2,
            },
            {
                "x": self.window_size[0] / 5,
                "y": self.window_size[1] /8,
                "width": self.window_size[0] / 10,
                "height": self.window_size[0] /10,
                "image_path": resource_path(os.path.join("Menu_images", "gold.png")),
                "text": count_gold,
            },
        ]

        buttons_game = [Button(data["x"], data["y"], data["width"], data["height"],
                               data["image_path"], data["text"],)for data in buttons_data]

        return buttons_game


class MenuEventHandler:
    @staticmethod
    def handle_events(buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        MenuEventHandler.handle_button_click(button)

    @staticmethod
    def handle_button_click(button):
        if button.text == "Створити героя":
            character_selector = CharacterSelector()
            character_selector.display_menu()
        elif button.text == "Обрати пригоду":
            menu = Menu()
            menu.run()
        elif button.text == "Вихід":
            pygame.quit()
            sys.exit()


class MenuRenderer:
    @staticmethod
    def render_menu(window, bg_image, buttons, font, big_font, window_size, image_race, image_clas):
        window.blit(bg_image, (0, 0))
        for button in buttons:
            button.draw(window, False, font)
        title_text = big_font.render("Меню гри ", True, BLACK)
        window.blit(title_text, (window_size[0] / 2.3, window_size[0] / 5.5))
        window.blit(image_race, (window_size[0] / 7, window_size[1] / 4))
        window.blit(image_clas, (window_size[0] / 1.6, window_size[1] / 2.5))
        pygame.display.flip()

 # Меню створення героя раса


class CharacterSelector:
    def __init__(self):
        self.window, self.window_size, self.bg_image, _, self.button_font, self.big_font, _, _, _, _ = GameInitializer.initialize_game()
        button_manager = ButtonManager(self.bg_image, self.window_size, self.window)
        self.gender_button1, self.gender_button2, self.buttons_m, self.buttons_f = button_manager.character_buttons()

    def display_menu(self):
        change = False
        running = True
        while running:
            self.window.blit(self.bg_image, (0, 0))
            title_text = self.big_font.render(
                "Обери расу персонажа", True, YELLOW)
            self.window.blit(
                title_text, (self.window_size[0] / 3, self.window_size[0] / 10))

            if change:
                gender_button = self.gender_button1
                gender_button.draw(self.window, True, self.button_font)
                self.buttons = self.buttons_m
                for button in self.buttons:
                    button.draw(self.window, True, self.button_font)
            else:
                gender_button = self.gender_button2
                gender_button.draw(self.window, True, self.button_font)
                self.buttons = self.buttons_f
                for button in self.buttons:
                    button.draw(self.window, True, self.button_font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if gender_button.is_clicked(pos):
                        pygame.time.wait(200)
                        change = not change
                    else:
                        for button in self.buttons:
                            if button.is_clicked(pos):
                                if button == self.buttons[-1]:
                                    running = False
                                    main()
                                else:
                                    race_name = button.text
                                    write_info_player(
                                        race_name, "", "", change)
                                    running = False
                                    character_selector_clas = CharacterSelector_Clas()
                                    character_selector_clas.display_menu()


class CharacterSelector_Clas:
    def __init__(self):
        self.window, self.window_size, self.bg_image, _, self.button_font, self.big_font, _, _, _, _ = GameInitializer.initialize_game()
        button_manager = ButtonManager(
            self.bg_image, self.window_size, self.window)
        self.buttons = button_manager.clas_buttons()

    def display_menu(self):
        running = True
        while running:
            self.window.blit(self.bg_image, (0, 0))
            title_text = self.big_font.render(
                "Обери клас персонажа", True, (255, 228, 181))
            self.window.blit(
                title_text, (self.window_size[0] / 3.5, self.window_size[0] / 9))

            for button in self.buttons:
                button.draw(self.window, True, self.button_font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(pos):
                            if button == self.buttons[-1]:
                                running = False
                                main()
                            else:
                                class_name = button.text
                                write_info_player(
                                    "", class_name, "", False)
                                running = False
                                character_selector_name = CharacterSelector_name()
                                character_selector_name.display_menu()


class CharacterSelector_name:
    def __init__(self):
        self.window, self.window_size, self.bg_image, _, self.button_font, self.big_font, _, _, _, _ = GameInitializer.initialize_game()
        self.user_name = ""
        _, _, self.addition, _, _, _ = read_character_info()
        button_manager = ButtonManager(
            self.bg_image, self.window_size, self.window)
        self.buttons_name, self.button_random_images, self.button_random_rect = button_manager.name_buttons()
        self.last_image_change_time = pygame.time.get_ticks()

    def display_menu(self):
        input_rect = pygame.Rect(
            self.window_size[0] / 2.5, self.window_size[0] / 4.2, self.window_size[0] / 5, self.window_size[0] / 20)
        current_image_index = 0
        n = 0
        choose_name_random = False

        running = True
        while running:
            self.window.blit(self.bg_image, (0, 0))
            pygame.draw.rect(self.window, BLACK, input_rect)
            pygame.draw.rect(self.window, YELLOW, input_rect, 2)

            title_text = self.big_font.render(
                "Введіть ім'я персонажа", True, YELLOW)
            self.window.blit(
                title_text, (self.window_size[0] / 2.8, self.window_size[0] / 6))

            text_surface = self.button_font.render(
                self.user_name, True, YELLOW)
            text_rect = text_surface.get_rect(center=input_rect.center)
            self.window.blit(text_surface, text_rect.topleft)

            self.buttons_name[0].draw(self.window, True, self.button_font)
            self.buttons_name[1].draw(self.window, False, self.button_font)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_image_change_time > 400:
                current_image_index = (
                    current_image_index + 1) % len(self.button_random_images)
                self.last_image_change_time = current_time
                n += 1
                if n == 4:
                    choose_name_random = False
                    n = 0

            if choose_name_random:
                self.window.blit(
                    self.button_random_images[current_image_index], self.button_random_rect)
            else:
                self.buttons_name[2].draw(self.window, True, self.button_font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    main()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    elif event.unicode.isprintable():
                        self.user_name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons_name:
                        if button.is_clicked(pos):
                            if button == self.buttons_name[0]:
                                running = False
                                main()
                            elif button == self.buttons_name[2]:
                                choose_name_random = True
                                random_name_file = resource_path(os.path.join(
                                    "Text_patern", f"random_name{self.addition[1]}.txt"))
                                self.user_name = self.get_random_name(
                                    random_name_file)
                            elif button == self.buttons_name[1]:
                                write_info_player(
                                    "", "", self.user_name, False)
                                self.handle_character_creation_success(
                                    self.window)

    def get_random_name(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            random_line = random.choice(lines)
            return random_line.strip()

    def handle_character_creation_success(self, window):
        character_created_message = "Персонаж створений успішно"
        text_surface = self.button_font.render(
            character_created_message, True, YELLOW)
        text_rect = text_surface.get_rect(
            center=(self.window_size[0] // 2, self.window_size[0] // 2))
        window.blit(text_surface, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(1000)
        main()


# Пригодницьке меню
class Menu:
    def __init__(self):
        self.window, self.window_size, self.bg_image, _, self.button_font, self.big_font, self.menu_font, _, self.image_race, self.image_clas = GameInitializer.initialize_game()
        button_manager = ButtonManager(
            self.bg_image, self.window_size, self.window)
        self.buttons_adventure = button_manager.adventure_buttons()

    def start_castle_adventure(self):
        self.setup_adventure_paths(
            resource_path(os.path.join("Murder_in_city", "beginning", "beginning.json")),
            resource_path(os.path.join("Murder_in_city", "items.json")),)

    def start_hotel_adventure(self):
        self.setup_adventure_paths(
            resource_path(os.path.join(
                "Hotel_quest", "beginning", "beginning.json")),
            resource_path(os.path.join("Hotel_quest", "items.json")),)

    def setup_adventure_paths(self, first_file_path, file_path_item):
        path_file = resource_path(os.path.join(
            "Text_patern", "character_info.json"))
        with open(path_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            data["first_file_path"] = first_file_path
            data["file_path_item"] = file_path_item
        with open(path_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        game = Game()
        game.run()

    def render_menu(self):
        self.window.blit(self.bg_image, (0, 0))
        self.window.blit(
            self.image_race, (self.window_size[0] / 12, self.window_size[1] / 4))
        self.window.blit(
            self.image_clas, (self.window_size[0] / 1.4, self.window_size[1] / 2.2))

        for button in self.buttons_adventure:
            button.draw(self.window, True, self.button_font)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in self.buttons_adventure:
                    if button.is_clicked(pos):
                        if button == self.buttons_adventure[0]:
                            main()
                        elif button == self.buttons_adventure[1]:
                            self.start_castle_adventure()
                        elif button == self.buttons_adventure[2]:
                            self.start_hotel_adventure()

    def run(self):
        running = True
        while running:
            self.render_menu()
            self.handle_events()


# Гра
class Game:
    def __init__(self):
        self.renderer = GameRenderer()
        self.logic = GameLogic()

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    main()
                self.logic.handle_event(event)
            self.renderer.render(self.logic)


class GameRenderer:
    def __init__(self):
        self.window, self.window_size, self.bg_image, _, _, _, _, _, self.image_race, self.image_clas = GameInitializer.initialize_game()
        self.clock = None
        self.image_fon = pygame.transform.scale(pygame.image.load(resource_path(os.path.join(
            "Menu_images", "book.png"))), (self.window_size[0] / 2.1, self.window_size[0] / 3),)
        self.image_paper = pygame.transform.scale(pygame.image.load(resource_path(os.path.join(
            "Menu_images", "paper.png"))), (self.window_size[0]/7 , self.window_size[0]/5),)
        self.clock = pygame.time.Clock()

    def render(self, logic):
        self.window.blit(self.bg_image, (0, 0))
        self.window.blit(self.image_fon, (self.window_size[0] / 4, self.window_size[1] / 5))
        self.window.blit(self.image_paper, (self.window_size[0] / 1.37, self.window_size[1] / 2.5))
        logic.update()
        logic.render(self.window)
        pygame.display.flip()


class TextBot:
    def __init__(self):
        (self.race_name, self.clas_name, self.addition, self.name,
         self.first_file_path, self.file_path_item,) = read_character_info()
        self.reader = JSONReader()
        self.chat_response = ""
        self.ansver2 = ""
        self.ansver1 = ""
        self.completed_items=""
        self.gold = 5
        self.interlocutor = None


    def generate_response(self, current_filename):
        json_data = self.reader.read_json_file(current_filename)
        description = json_data.get("description", "")
        ansvers = json_data.get("ansvers", {})
        self.ansver1 = ansvers.get("ansver1", [])
        self.ansver2 = ansvers.get("ansver2", [])
        
        items = json_data.get("items", {})
        items = {key: value for key,value in items.items() if value[0] == "True"}
        
        existing_data = self.reader.read_json_file(self.file_path_item)
        for key, value in items.items():
            existing_data[key] = value if value[0] == "True" else "False"
        self.reader.write_json_file(existing_data, self.file_path_item)
        self.chat_response = description.strip()

        # Обираємо  співрозмовника
        self.interlocutor = (json_data.get("interlocutor", [])if json_data.get("interlocutor")else None)
        

    def process_answer(self, choice_filename):
        choice_filename = resource_path(os.path.join(choice_filename[1], choice_filename[2], choice_filename[3]))
        json_data_choice = self.reader.read_json_file(choice_filename)
        existing_data = self.reader.read_json_file(self.file_path_item)
        
        # В залежності від того, чи зібрані всі потрібні предмети (досягнення) обираємо насупний файл, для непотрібних у ключі пишемо "folse" 
        true_values = [key for key, value in existing_data.items() if value[0] == "True" and "folse" not in key.lower()]
        all_key = [key for key, value in existing_data.items() if "folse" not in key.lower()]
        if len(true_values) == len(all_key):
            next_filename = (json_data_choice.get("next_end", []) if json_data_choice.get("next_end")else None)
        else:
            next_filename = (json_data_choice.get("next", []) if json_data_choice.get("next")else None)
        
        self.completed_items = {
            value[1] for key, value in existing_data.items() if value[0] == "True"
        }
        # Рахуємо золото
        gold = int(json_data_choice.get("currency", {}).get("gold", 0))
        self.gold += gold

        # Змінюємо назву наступного файлу, що буде відображатись в залежності від раси, класу чи гендеру
        selection = json_data_choice.get("selection", {})
        selection = {key: value for key,value in selection.items() if value == "True"}
        suffixes = {"class_selection": self.clas_name[1], "race_selection": self.race_name[1], "gender_selection": self.addition[1], }
        if len(selection):
            selection_key = next(iter(selection.keys()))
            selection_as_string = str(selection_key)
            suffix = suffixes[selection_as_string]
        else:
            suffix = ""
        next_filename = resource_path(os.path.join(
            next_filename[0], next_filename[1], f"{next_filename[2]}{suffix}.json"))

        return next_filename

    def clear_files(self):
        existing_data = self.reader.read_json_file(self.file_path_item)
        for key, value in existing_data.items():
            existing_data[key][0] = "False"
        self.reader.write_json_file(existing_data, self.file_path_item)


class GameLogic:
    def __init__(self):
        self.window, self.window_size, self.bg_image, _, self.button_font, self.big_font, self.menu_font, self.hand_font, self.image_race, _ = GameInitializer.initialize_game()
        self.textbot = TextBot()
        self.char_index = 0
        self.time_passed = 0
        self.textbot.generate_response(self.textbot.first_file_path)
        button_manager = ButtonManager(self.bg_image, self.window_size, self.window)
        self.buttons = button_manager.game_buttons(self.textbot.ansver1[0], self.textbot.ansver2[0], self.textbot.gold)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(pos):
                    if button == self.buttons[0]:
                        self.textbot.clear_files()
                        main()

                    elif button == self.buttons[2]:
                        if self.textbot.ansver1[1] == "":
                            self.textbot.clear_files()
                            main()
                        else:
                            current_filename = self.textbot.process_answer(
                                self.textbot.ansver1)
                            self.textbot.generate_response(current_filename)
                            self.char_index = 0
                    elif button == self.buttons[3]:
                        if self.textbot.ansver1[1] == "":
                            self.textbot.clear_files()
                            main()
                        else:
                            current_filename = self.textbot.process_answer(
                                self.textbot.ansver2)
                            self.textbot.generate_response(current_filename)
                            self.char_index = 0

    def update(self):
        time_delta = pygame.time.get_ticks() - self.time_passed
        self.time_passed += time_delta
        if self.time_passed > 100 and self.char_index < len(self.textbot.chat_response):
            self.char_index += 5
            self.time_passed = 0

    def render(self, surface):
        y_position = self.window_size[1] // 4
        x_position = self.window_size[0] // 3.5
        displayed_text = self.textbot.chat_response[: self.char_index]
        current_line = ""

        for char in displayed_text:
            current_line += char
            text_width, _ = self.menu_font.size(current_line)
            char_width, _ = self.menu_font.size(char)
            if text_width > self.window_size[0] / 3 and char == " " or char == ":":
                chat_surface = self.menu_font.render(char, True, BLACK)
                surface.blit(chat_surface, (x_position, y_position))
                y_position += self.menu_font.get_linesize()
                current_line = char
                x_position = self.window_size[0] / 3.5
            else:
                chat_surface = self.menu_font.render(char, True, BLACK)
                surface.blit(chat_surface, (x_position,y_position))
                x_position += char_width

        y_position += self.menu_font.get_linesize()

        # Виводимо співрозмовника або аватар
        if self.textbot.interlocutor:
            image_character = convert_picture(self.textbot.interlocutor)
        else:
            image_character = self.image_race

        self.window.blit(image_character, (self.window_size[0] / 10, self.window_size[1] / 4))
        # Виводимо кнопки з варіантами відповідей
        button_manager_instance = ButtonManager(self.bg_image, self.window_size, self.window)
        self.buttons = button_manager_instance.game_buttons(self.textbot.ansver1[0], self.textbot.ansver2[0], self.textbot.gold)
        for button in self.buttons[:2]:
            button.draw(surface, True, self.button_font)
       
        for button in self.buttons[2:4]:
            button.draw_center(surface, self.menu_font)
        self.buttons[4].draw_center(surface, self.button_font)
        # Виводимо предмети (досягнення)
        if self.textbot.completed_items:
            y_position_items = self.window_size[1] / 2.2
            for items_text in self.textbot.completed_items:
                completed_items = self.hand_font.render(items_text, True, BLACK)
                surface.blit(completed_items, (self.window_size[0] / 1.35, y_position_items))
                y_position_items += self.menu_font.get_linesize()



def main():
    window, window_size, _, bg_image_menu, button_font, big_font, _, _, image_race, image_clas = GameInitializer.initialize_game()
    button_manager_instance = ButtonManager(bg_image_menu, window_size, window)
    buttons = button_manager_instance.menu_buttons()

    run = True

    while run:
        MenuRenderer.render_menu(window, bg_image_menu, buttons,
                                 button_font, big_font, window_size, image_race, image_clas)
        MenuEventHandler.handle_events(buttons)
        if window._pixels_address is None:
            run = False
            break


if __name__ == "__main__":
    main()
