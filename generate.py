import sys
import nbtlib
from nbtlib import schema, CompoundSchema
from nbtlib import Compound, String, Byte, List, Int, Double

# List of filenames of boxes to create & the associated egg type, shulker box color is defined in <box>.snbt
boxes = {"combat": "minecraft:spider_spawn_egg"}

# Row to place the created items in; 0-indexed, value of -1 means do not create
SPAWNER_ROW = '6'
VILLAGER_ROW = '7'
COMMAND_BOOK_ROW = '8'


def readBox(name):
    return nbtlib.parse_nbt(open(f"{name}.snbt", 'r').read())


def boxToSpawnerEgg(box, eggType):
    return Compound({
        'id': String(eggType),
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
                            'TileEntityData': box['tag']
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
        'id': String(eggType),
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

    hotbar.root[SPAWNER_ROW] = List[Compound]([{}, {}, {}, {}, {}, {}, {}, {}, {}])
    hotbar.root[VILLAGER_ROW] = List[Compound]([{}, {}, {}, {}, {}, {}, {}, {}, {}])

    for box in boxes.keys():
        boxNBT = readBox(box)
        boxSpawnerEgg = boxToSpawnerEgg(boxNBT, boxes[box])
        boxVillagerEgg = boxToVillagerEgg(boxNBT, boxes[box])

        hotbar.root[SPAWNER_ROW][column] = boxSpawnerEgg
        hotbar.root[VILLAGER_ROW][column] = boxVillagerEgg

    print(hotbar.root['6'][1])
