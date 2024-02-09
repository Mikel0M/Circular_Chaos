
class parts(object):
    """name is a string, height, width and depth are ints or floats and represent centimeters,
    material is a string and number is an integer """

    def __init__(self, type, name, height, width, depth, material, number, used, unused, position):
        self.type = type
        self.name = name
        self.height = height
        self.width = width
        self.depth = depth
        self.material = material
        self.number = number
        self.used = used
        self.unused = unused
        self.position = position

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getDepth(self):
        return self.depth

    def getMaterial(self):
        return self.material

    def getNumber(self):
        return self.number

    def getUsed(self):
        return self.used

    def getUnused(self):
        return self.unused

    def getPosition(self):
        return self.position

    def setPosition(self, newPosition):
        self.position = newPosition

    def use(self):
        """
        reduces the number by 1 if there are items in storage
        """
        if self.unused > 0:
            temp1 = int(self.getUnused()) - 1
            self.unused = temp1
            temp2 = int(self.getUsed()) + 1
            self.used = temp2

    def putBack(self):
        """
        returns and object to storage
        """
        if self.used > 0:
            temp1 = int(self.getUsed()) - 1
            self.used = temp1
            temp2 = int(self.getUnused()) + 1
            self.unused = temp2

class extraParts(parts):
    """"
    this class is intended to fill the gaps and is not using re-used parts.
    """
    pass

def makePart(type, name, height, width, depth, material, number, used, unused, position):
    """
    creates a new part fulfilling the requested parameters
    """
    part1 = parts(type, name, height, width, depth, material, number, used, unused, position)
    return part1


def checkPart(length, maxHeight, ListParts):
    """
    Given a length and a List of Parts, ListParts, findMatch, looks through it and returns the best fit.
    It generates extra parts if needed.
    """
    name = 'start'
    n = length
    m = length
    smallest = ''
    smallestH = ''

    # the function tries to fill the gap with one part or the combination of two parts, and tries it rotating the elements
    for part1 in reversed(range(len(ListParts))):
            #checks that the height of the part doesn't exceed the height of the element to substitute
            if float(ListParts[part1].getHeight()) <= float(maxHeight):
                #checks if the element in the list has been already asigned in another position
                if ListParts[part1].getUnused() > 0:
                    #checks if the length of the part is smaller than the length of the element to substitute
                    if abs(float(length) - float(ListParts[part1].getWidth())) < n:
                        n = abs(float(length) - float(ListParts[part1].getWidth()))
                        #if all those conditions are true, then it considers as a possible part to combine
                        checkedPart = ListParts[part1]
    return checkedPart

def checkPartRotated(length, maxHeight, ListParts):
        """
        Given a length and a List of Parts, ListParts, findMatch, looks through it and returns the best fit.
        It generates extra parts if needed.
        """
        name = 'start'
        n = length
        m = length
        smallest = ''
        smallestH = ''

        # the function tries to fill the gap with one part or the combination of two parts, and tries it rotating the elements
        for part1 in reversed(range(len(ListParts))):
            # checks that the height of the part doesn't exceed the height of the element to substitute
            if float(ListParts[part1].getHeight()) <= float(maxHeight):
                # checks if the element in the list has been already asigned in another position
                if ListParts[part1].getUnused() > 0:
                    # checks if the height of the part is smaller than the height of the element to substitute
                    if abs(float(length) - float(ListParts[part1].getHeight())) < n:
                        n = abs(float(length) - float(ListParts[part1].getHeight()))
                        #if all those conditions are true, then it considers as another possible part to combine
                        checkedPartRotated = extraParts(str(ListParts[part1].getType()), str(ListParts[part1].getName()),
                                               float(ListParts[part1].getWidth()), 1, 0, str(ListParts[part1].getMaterial()),
                                               float(ListParts[part1].getNumber()), float(ListParts[part1].getUsed()),
                                               float(ListParts[part1].getUnused()), float(ListParts[part1].getPosition()))

        return checkedPartRotated
#Now we can check if an element is good or not for a list. Now I am missing a function that checks one element, and findst the best fit of all rotated or unrotated of the whole list

#After that another function that tries starting from every single available object.