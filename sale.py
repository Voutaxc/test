SCREEN_SIZE = (800, 600)
FISH_COUNT = 20

import pygame
from pygame.locals import *
from random import randint
from pygame import Vector2


class State(object):
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachineAI(object):
    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def think(self):
        if self.active_state is None:
            return
        self.active_state.do_actions()
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        if self.active_state is not None:
            self.active_state.exit_actions()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


class World(object):
    def __init__(self):
        self.creatures = {}
        self.creature_id = 0
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))

    def add_creature(self, creature):
        self.creatures[self.creature_id] = creature
        creature.id = self.creature_id
        self.creature_id += 1

    def remove_creature(self, creature):
        del self.creatures[creature.id]

    def get(self, creature_id):
        if creature_id in self.creatures:
            return self.creatures[creature_id]
        else:
            return None

    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        for creature in self.creatures.values():
            creature.process(time_passed_seconds)

    def render(self, surface):
        surface.blit(self.background, (0, 0))
        for creature in self.creatures.itervalues():
            creature.render(surface)

    def get_close_creature(self, name, location, range=100.):
        location = Vector2(*location)
        for creature in self.creatures.itervalues():
            if creature.name == name:
                distance = location.get_distance_to(creature.location)
                if distance < range:
                    return creature
        return None


class GameCreature(object):

    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.
        self.brain = StateMachineAI()
        self.id = 0

    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x - w / 2, y - h / 2))

    def process(self, time_passed):
        self.brain.think()
        if self.speed > 0. and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading


class Trash(GameCreature):
    def __init__(self, world, image):
        GameCreature.__init__(self, world, "trash", image)
        self.speed = 5


class Shark(GameCreature):
    def __init__(self, world, image):
        GameCreature.__init__(self, world, "shark", image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.rank = 5
        self.speed = 50


    def render(self, surface):
        GameCreature.render(self, surface)
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h / 2
        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))

    def process(self, time_passed):
        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        GameCreature.process(self, time_passed)



class fish(GameCreature):
    def __init__(self, world, image):
        GameCreature.__init__(self, world, "fish", image)
        wondering_state = StateWondering(self)
        seeking_state = StateSeeking(self)
        hunting_state = StateHunting(self)
        escaping_state=StateEscaping(self)
        self.brain.add_state(wondering_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(hunting_state)
        self.brain.add_state(escaping_state)

    def eaten(self, surface):
            hunter = pygame.sprite.spritecollide(self.food, self.hunter, True)

    def render(self, surface):
        GameCreature.render(self, surface)

class StateWondering(State):
    def __init__(self, ant):
        State.__init__(self, "wondering")
        self.fish = fish

    def random_destination(self):
        w, h = SCREEN_SIZE
        self.fish.destination = Vector2(randint(0, w), randint(0, h))

    def do_actions(self):
        if randint(1, 20) == 1:
            self.random_destination()

    """def check_conditions(self):
        food = self.fish.world.get_close_creature("food", self.fish.location)
        if food is None:
            return "seeking"""""

    def entry_actions(self):
        self.fish.speed = 120. + randint(-30, 30)
        self.random_destination()


class StateSeeking(State):
    def __init__(self, fish):
        State.__init__(self, "seeking")
        self.fish = fish
        self.food_id = None

    def check_conditions(self):
        food = self.fish.world.get(self.fish.food_id)
        if food is not None:
            self.fish.food_id = food.id
            return "hunting"
        if hunter is not None:
            if self.fish.location.get_distance_to(hunter.location) < 100.:
                self.fish.hunter_id = hunter.id
                return "escape"
        if self.food.location.get_distance_to(food.location) < 5.0:
            self.ant.world.remove_creature(food)
        return "wondering"

        return None

    def entry_actions(self):
        food = self.fish.world.get(self.fish.food_id)
        if food is not None:
            self.fish.destination = food.location
            self.fish.speed = 160. + randint(-20, 20)


class StateEscaping(State):
    def __init__(self, fish):
        State.__init__(self, "escaping")
        self.fish = fish

    def check_conditions(self):
        if Vector2(*hunter).get_distance_to(self.fish.location) < NEST_SIZE:
            if (randint(1, 10) == 1):
                self.ant.drop(self.ant.world.background)
                return "exploring"
        return None

    def entry_actions(self):
        self.ant.speed = 60.
        random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(*NEST_POSITION) + random_offset


class StateHunting(State):
    def __init__(self, ant):
        State.__init__(self, "hunting")
        self.ant = ant
        self.got_kill = False

    def do_actions(self):
        food = self.fish.world.get(self.fish.food_id)
        if food is None:
            return
        self.fish.destination = food.location
        if self.fish.location.get_distance_to(food.location) < 15.:
                food.eaten()
                self.get_eat

    def check_conditions(self):
        if self.got_eat:
            return "wondering"
        spider = self.ant.world.get(self.ant.spider_id)
        return None

    def entry_actions(self):
        self.speed = 160

    def exit_actions(self):
        self.got_eat = False"""


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    world = World()
    w , h = SCREEN_SIZE
    clock = pygame.time.Clock()

    fish0_image = pygame.image.load("fish0.png").convert_alpha()
    fish1_image = pygame.image.load("fish1.png").convert_alpha()
    fish2_image = pygame.image.load("fish2.png").convert_alpha()
    fish3_image = pygame.image.load("fish3.png").convert_alpha()
    fish4_image = pygame.image.load("fish4.png").convert_alpha()
    shark_image = pygame.image.load("shark.png").convert_alpha()
    trash_imaage = pygame.image.load("trash.png").convert_alpha()

   for fish_no in range(FISH_COUNT):
        fish = FISH_COUNT(world, fish0_image)
       fish.location = Vector2(randint(w, w+100), randint(0, h))
        fish.brain.set_state("seeking")
        world.add_creature(fish)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        time_passed = clock.tick(30)

        if randint(1, 10) == 1:
            food = food(world, food_image)
            food.location = Vector2(randint(0, w), randint(0, h))
            world.add_entity(fish)

        if randint(1, 100) == 1:
             = (world, fish0_image)
            hunter.location = Vector2(-50, randint(0, h))
            spider.destination = Vector2(w + 50, randint(0, h))
            world.add_entity(hunter)

        world.process(time_passed)
        world.render(screen)

        pygame.display.update()


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    world = World()
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()
    ant_image = pygame.image.load("ant.png").convert_alpha()
    leaf_image = pygame.image.load("leaf.png").convert_alpha()
    spider_image = pygame.image.load("spider.png").convert_alpha()

    for ant_no in xrange(ANT_COUNT):
        ant = Ant(world, ant_image)
        ant.location = Vector2(randint(0, w), randint(0, h))
        ant.brain.set_state("exploring")
        world.add_entity(ant)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        time_passed = clock.tick(30)

        if randint(1, 10) == 1:
            leaf = Leaf(world, leaf_image)
            leaf.location = Vector2(randint(0, w), randint(0, h))
            world.add_entity(leaf)

        if randint(1, 100) == 1:
            spider = Spider(world, spider_image)
            spider.location = Vector2(-50, randint(0, h))
            spider.destination = Vector2(w + 50, randint(0, h))
            world.add_entity(spider)

        world.process(time_passed)
        world.render(screen)

        pygame.display.update()


if __name__ == "__main__":
    run()

