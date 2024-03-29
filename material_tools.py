import json
import clipboard
import re

newLine = '\n'
tab = '   '

def jsonToLegacy(path):

    output = ''

    with open(path) as f:
        data = json.load(f)

    for key, value in data.items():

        name = value['name']
        mapTo = value['mapTo']
        stage = value['Stages'][0]

        colorMap = color = None
        
        if('colorMap' in stage):
            colorMap = stage['colorMap']
            if('/' in colorMap):
                array = colorMap.split('/')
                colorMap = array[len(array)-1]
        elif ('diffuseColor' in stage):
            color = stage['diffuseColor']

        mat = {}
        mat['name'] = name
        mat['mapTo'] = mapTo
        if (colorMap is not None): mat['colorMap'] = colorMap
        if (color is not None): mat['color'] = color
        output += getLegacyFormat(mat)

    clipboard.copy(output)

def getLegacyFormat(material):

    legacy = ''
    legacy += 'singleton material({}){}'.format(material['name'], newLine)
    legacy += '{' + newLine
    # legacy += tab + 'mapTo = "{}";{}'.format(material['mapTo'], newLine)
    # if('colorMap' in material):
    #         legacy += tab + 'colorMap[0] = "{}";{}'.format(material['colorMap'], newLine)
    # if('color' in material):
    #     legacy += tab + 'diffuseColor[0] = "{} {} {} {}";{}'.format(str(material['color'][0]), str(material['color'][1]), str(material['color'][2]), str(material['color'][3]), newLine)
    # legacy += tab + 'specularPower[0] = "1";' + newLine
    # legacy += tab + 'translucentBlendOp = "None";' + newLine
    # legacy += tab + 'vertColor[0] = "1";' + newLine
    # legacy += tab + 'useAnisotropic[0] = "1";' + newLine

    for param, value in material.items():
        legacy += tab + '{} = "{}";{}'.format(param, value, newLine)

    legacy += '};' + newLine
    legacy += newLine

    return legacy

def readLegacy(path):

    file = open(path)

    materials = {}
    currentlyReading = None

    for line in file:
        if(currentlyReading is None):
            result = re.search('singleton material\\((.*)\\)', line)
            if(result is not None):
                name = result.group(1)
                currentlyReading = {}
                currentlyReading['name'] = name
                materials[name] = currentlyReading
        else:
            if("=" in line):
                array = line.split("=")
                currentlyReading[array[0].strip(' "')] = array[1].strip(' ";\n')
            elif("};" in line):
                currentlyReading = None

    return materials

def analyzeLegacy(path):

    materials = readLegacy(path)

    nameDuplicates = 0
    textureDuplicates = 0
    nonTexture = 0

    checkedNames = []
    checkedTextures = []

    for material in materials.values():

        # Material names
        if('name' in material):
            if(material['name'] in checkedNames):
                nameDuplicates += 1
            else:
                checkedNames.append(material['name'])

        if('colorMap[0]' in material):
            if(material['colorMap[0]'] in checkedTextures):
                textureDuplicates += 1
            else:
                checkedTextures.append(material['colorMap[0]'])
        else:
            nonTexture += 1

    print('Number of materials: {}'.format(len(materials)))
    print('Name duplicates: {}'.format(nameDuplicates))
    print('Texture duplicates: {}'.format(textureDuplicates))
    print('Without textures: {}'.format(nonTexture))



def removeTextureDoublesLegacy(path):

    materials = readLegacy(path)
    optimisedMaterials = []

    for material in materials.values():

        duplicate = False
        for otherMaterial in optimisedMaterials:
            if('colorMap[0]' in material and 'colorMap[0]' in otherMaterial):
                if(material['colorMap[0]'] == otherMaterial['colorMap[0]']):
                    duplicate = True
                    break

        if(duplicate == False):
            # if('colorMap[0]' in material): material['colorMap'] = material['colorMap[0]']
            # if('diffuseColor[0]' in material): material['color'] = material['diffuseColor[0]']
            optimisedMaterials.append(material)

    output = ''
    for material in optimisedMaterials:
        output += getLegacyFormat(material)

    # print(output)

    clipboard.copy(output)

    print('Original size: {}'.format(len(materials)))
    print('Removed materials: {}'.format(len(materials) - len(optimisedMaterials)))
    print('Reduced by {}%'.format(str(round((1-(len(optimisedMaterials) / len(materials))) * 100, 2))))


def getMapToTexturePairs(path):
    materials = readLegacy(path)

    pairs = {}
    for material in materials.values():
        if('mapTo' in material and 'colorMap[0]' in material):
            pairs[material['mapTo']] = material['colorMap[0]']

    with open('pairs.json', 'w') as json_file:
        json.dump(pairs, json_file)


# jsonToLegacy("C:\\Users\\blaha\\Desktop\\mats.json")
# analyzeLegacy("C:\\Users\\blaha\\Desktop\\mat_temp\\materials.cs")
removeTextureDoublesLegacy("C:\\Users\\blaha\\Desktop\\mat_temp\\materials.cs")

# getMapToTexturePairs("C:\\Users\\blaha\\Desktop\\mat_temp\\materials.cs")