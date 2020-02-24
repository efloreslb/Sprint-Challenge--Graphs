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
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
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

gr = Graph()
visited = set()

# for room in world.rooms.values():
#     gr.add_vertex(room)

print(len(room_graph))
print(len(gr.vertices))

# while len(gr.vertices) < len(room_graph):
print(player.current_room.id)
if player.current_room.id not in gr.vertices:
    gr.add_vertex(player.current_room.id)
    visited.add(player.current_room.id)
    # print(gr.vertices[player.current_room.id])
    # print(visited)

for direction in gr.vertices[player.current_room.id]:
    print(f'current room: {player.current_room.id}')
    print(gr.vertices)
    if gr.vertices[player.current_room.id][direction] == "?":
        player.travel(direction)

        # wander
        if player.current_room.id not in gr.vertices:
            gr.add_vertex(player.current_room.id)
            visited.add(player.current_room.id)



    


# for direction in graph.vertices[0].items():
#     # if graph.vertices[0] == '?':
#     #     print("found ?")
#     print(direction)

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
