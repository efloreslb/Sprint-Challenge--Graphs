from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            # self.vertices[vertex_id] = set()
            self.vertices[vertex_id] = {d: '?' for d in player.current_room.get_exits()}

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = ['s', 's', 'w', 'w', 'n', 'n']
traversal_path = []
oppositeDirections = {
    "n": "s",
    "e": "w",
    "s": "n",
    "w": "e"
}
gr = Graph()
visited = set()
test_path = Stack()

# for room in world.rooms.values():
#     gr.add_vertex(room)

# print(len(room_graph))
# print(len(gr.vertices))

# while len(gr.vertices) != len(room_graph):

curr_room = player.current_room.id

def explore(room):
    print("--start--")
    print(f'test_path: {test_path.stack}')

    print(f'FINAL Traversal: {traversal_path}')

    if len(gr.vertices) == len(room_graph):
        return

    if len(player.current_room.get_exits()) == 1:
        # print(test_path.stack)
        # print(oppositeDirections[test_path.stack[-1]])
        # player.travel(oppositeDirections[test_path.stack[-1]])
        # test_path.stack.pop()
        # print(test_path.stack)
        # explore(player.current_room.id)

        print(f'only 1 exit - curr_room: {player.current_room.id}')
        print(test_path.stack)
        for x in range(0, test_path.size()):
            print(x)
            # print(f"traveled dir: {traveled_dir}")
            # print(f'opposite: {oppositeDirections[traveled_dir]}')
            # player.travel(oppositeDirections[traveled_dir])
            player.travel(oppositeDirections[test_path.stack[-1]])
            # counter += 1
            test_path.pop()
            # print(f'traveled back - stack: {test_path.stack}')

        print(f'traveled back - curr_room: {player.current_room.id}')

    if player.current_room.id not in gr.vertices:
        gr.add_vertex(player.current_room.id)
        print("adding to vertices")
        visited.add(player.current_room.id)

    for direction in gr.vertices[room]:
        print(f'curr room: {room}')
        print(f'curr room vertices: {gr.vertices[room]}')
        print(f'visited: {visited}')
        # print(direction)

        # random_direction = random.choice(['n','w','s','e'])
        # while gr.vertices[player.current_room.id][random_direction] is not "?" and gr.vertices[player.current_room.id][random_direction] is not None:
        #     random_direction = random.choice(['n','w','s','e'])
        #     print(random_direction)
        # print(f'decided direction: {random_direction}')
        # direction = random_direction
        
        # direction = "s"

        if gr.vertices[player.current_room.id][direction] != "?":
            direction = random.choice(['n','w','s','e'])

        if len(player.current_room.get_exits()) == 1:
            for traveled_dir in test_path.stack:
                player.travel(oppositeDirections[traveled_dir])
                print(test_path.stack)
                test_path.pop()
                print(test_path.stack)
        
        player.travel(direction)
        print(f'after travel: {player.current_room.id}')
        traversal_path.append(direction)
        test_path.push(direction)

        if player.current_room.id not in gr.vertices:
            gr.add_vertex(player.current_room.id)
            visited.add(player.current_room.id)

        explored_room = player.current_room.id
        explored_dir_opp = oppositeDirections[direction]

        gr.vertices[room][direction] = explored_room
        gr.vertices[explored_room][explored_dir_opp] = room

        # if len(player.current_room.get_exits()) == 1:
        #     for traveled_dir in test_path.stack:
        #         player.travel(oppositeDirections[traveled_dir])
        #         test_path.pop()

        print(f'Final Room: {player.current_room.id}')
        # print(explored_room)
        room = explored_room
        
        print(room)
        print(test_path.stack)

        print(gr.vertices)
        print("--end--")
        explore(room)

explore(curr_room)
print(f'FINAL Room: {player.current_room.id}')
print(f'FINAL Traversal: {traversal_path}')

# print(player.current_room.id)
# player.travel('n')
# print(player.current_room.id)
# player.travel('n')
# print(player.current_room.id)
# print(player.current_room.get_exits())
# print(f'vertices {graph.vertices}')


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
