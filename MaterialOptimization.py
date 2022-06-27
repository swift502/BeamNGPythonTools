from collections import defaultdict

import json

context = bpy.context
ob = context.object

me = ob.data
mats = ob.material_slots

with open('pairs.json') as file:
    pairs = json.load(file)

merged = 0
firstMat = 0
renamed = 0
assignedExisting = 0

for mat in mats:
    if(mat.name in pairs):
        texture = pairs[mat.name]
        
        for pairMat, pairTex in pairs.items():
            if(texture == pairTex):
                if(mat.name == pairMat):
                    firstMat += 1
                else:
                    alreadyExists = bpy.data.materials.get(pairMat)
                    
                    if(alreadyExists is None):
                        mat.material.name = pairMat
                        renamed += 1
                    else:
                        mat.material = alreadyExists
                        assignedExisting += 1
                    merged += 1
                break

print('Total: {}'.format(len(mats)))
print('Merged: {}'.format(merged))
print('This is the first material: {}'.format(firstMat))
print('Renamed: {}'.format(renamed))
print('Assigned already existing material: {}'.format(assignedExisting))
print('Materials reduced by: {}%'.format(round(((merged / len(mats))) * 100, 2)))





if True:
    print('Cleaning materials:')
    context = bpy.context
    ob = context.object

    me = ob.data
    slots = ob.material_slots
    def getmname(idx):
        if idx < len(slots):
            name = slots[idx].name
            name = name if name else "None"
        else:
            name = "None"
        return name

    matdic = defaultdict(list)

    for f in me.polygons:
        matdic[getmname(f.material_index)].append(f.index)

    removed = 0
    added = 0

    while len(slots) > len(matdic):
        ob.active_material_index = 1
        bpy.ops.object.material_slot_remove()
        removed += 1

    while len(slots) < len(matdic):
        bpy.ops.object.material_slot_add()
        added += 1
        
    for i, (name, faces) in enumerate(matdic.items()):
        slots[i].material = bpy.data.materials.get(name)
        for f in faces:
            me.polygons[f].material_index = i

    print("removed: " + str(removed))
    print("added: " + str(added))
