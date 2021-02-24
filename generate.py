import sys
import argparse
import nbtlib
from nbtlib import schema, CompoundSchema
from nbtlib import Compound, String, Byte, List, Int, Double

# List of filenames of boxes to create & the associated egg type, shulker box color is defined in <box>.snbt
boxes = {
    "combat": "spider",
    "tools": "slime",
    "miscellaneous": "pig",
    "mind_the_gap": "horse",
    "drippy_pot": "turtle",
    "drippy_pot[cring]": "vindicator",
    "battle_pan": "wither_skeleton",
    "battle_pan[cring]": "ravager"
}

# Read optional arguments
parser = argparse.ArgumentParser(description="e")
parser.add_argument('-s', default='-1')
parser.add_argument('-v', default='-1')
parser.add_argument('-c', default='-1')
args = parser.parse_args()

SPAWNER_ROW = str(args.s)
VILLAGER_ROW = str(args.v)
COMMAND_BOOK_ROW = str(args.c)

# If no arguments were passed
if SPAWNER_ROW == '-1' and VILLAGER_ROW == '-1' and COMMAND_BOOK_ROW == '-1':
    print(f"Usage: {sys.argv[0]} [-s <row>] [-v <row>] [-c <row>]\n" +
          "\t<row>: 0-indexed saved hotbar row to place the items in.\n" +
          "\ts: Row to put Spawn Eggs for Shulker Box Spawners\n" +
          "\tv: Row to put Spawn Eggs for Villagers that sell Shulker Boxes\n" +
          "\tc: Row to put Command Book Eggs")
    exit()


def readBox(name):
    return nbtlib.parse_nbt(open(f"{name}.snbt", 'r').read())


def boxToSpawnerEgg(box, eggType):
    return Compound({
        'id': String(f"minecraft:{eggType}_spawn_egg"),
        'Count': Byte(1),
        'tag': Compound({
            'EntityTag': Compound({
                'id': String("minecraft:falling_block"),
                'Time': Int(300),
                'BlockState': Compound({
                    'Name': String("minecraft:spawner")
                }),
                'TileEntityData': Compound({
                    'RequiredPlayerRange': Int(2),
                    'SpawnCount': Int(1),
                    'SpawnRange': Double(0.5),
                    'Delay': Int(-1),
                    'MinSpawnDelay': Int(20),
                    'MaxSpawnDelay': Int(20),
                    'SpawnPotentials': List[Compound]([{
                        'Entity': Compound({
                            'id': String("minecraft:falling_block"),
                            'Time': Int(300),
                            'BlockState': Compound({
                                'Name': String(box['id'])
                            }),
                            'TileEntityData': Compound({
                                'CustomName': box['tag']['display']['Name'],
                                'Items': box['tag']['Items']
                            })
                        }),
                        'Weight': Int(1)
                    }])
                })
            }),
            'display': Compound(box['tag']['display'])
        })
    })


def boxToVillagerEgg(box, eggType):
    return Compound({
        'id': String(f"minecraft:{eggType}_spawn_egg"),
        'Count': Byte(1),
        'tag': Compound({
            'EntityTag': Compound({
                'id': String("minecraft:villager"),
                'Invulnerable': Byte(1),
                'CustomNameVisible': Byte(0),
                'CustomName': String(box['tag']['display']['Name']),
                'VillagerData': Compound({
                    'level': Int(99),
                    'profession': String("minecraft:librarian")
                }),
                'Offers': Compound({
                    'Recipes': List[Compound]([{
                        'rewardExp': Byte(0),
                        'maxUses': Int(2147483647),
                        'buy': Compound({
                            'id': String("minecraft:stick"),
                            'Count': Byte(1)
                        }),
                        'sell': Compound({
                            'id': box['id'],
                            'Count': box['Count'],
                            'tag': Compound({
                                'BlockEntityTag': Compound({
                                    'Items': box['tag']['Items']
                                }),
                                'display': box['tag']['display']
                            })
                        })
                    }])
                })
            }),
            'display': Compound(box['tag']['display'])
        })
    })


with nbtlib.load("hotbar.nbt") as hotbar:
    column = 1

    if not SPAWNER_ROW == '-1':
        print(f"Generating Spawners in row {SPAWNER_ROW}")
        hotbar.root[SPAWNER_ROW] = List[Compound]([{}, {}, {}, {}, {}, {}, {}, {}, {}])
    if not VILLAGER_ROW == '-1':
        print(f"Generating Villagers in row {VILLAGER_ROW}")
        hotbar.root[VILLAGER_ROW] = List[Compound]([{}, {}, {}, {}, {}, {}, {}, {}, {}])

    for box in boxes.keys():
        boxNBT = readBox(box)
        print(f"Creating {box} box")

        if not SPAWNER_ROW == '-1':
            boxSpawnerEgg = boxToSpawnerEgg(boxNBT, boxes[box])
            hotbar.root[SPAWNER_ROW][column] = boxSpawnerEgg
        if not VILLAGER_ROW == '-1':
            boxVillagerEgg = boxToVillagerEgg(boxNBT, boxes[box])
            hotbar.root[VILLAGER_ROW][column] = boxVillagerEgg

        column += 1
