
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
        """reduces the number by 1 if there are items in storage"""
        if self.unused > 0:
            temp1 = int(self.getUnused()) - 1
            self.unused = temp1
            temp2 = int(self.getUsed()) + 1
            self.used = temp2

    def putBack(self):
        """returns and object to storage"""
        if self.used > 0:
            temp1 = int(self.getUsed()) - 1
            self.used = temp1
            temp2 = int(self.getUnused()) + 1
            self.unused = temp2


#This is intended to create a new Piece


class extraParts(parts):
    pass

def makePart(type, name, height, width, depth, material, number, used, unused, position):
    part1 = parts(type, name, height, width, depth, material, number, used, unused, position)
    return part1


#random.shuffle(completeListParts)
#This algorithm is intended to check and replace parts:

def findMatch(length, maxHeight, ListParts):
    """
    Given a length and a List of Parts, ListParts, findMatch, looks through it and returns the best fit
    """
    length
    name = 'start'
    n = length
    m = length
    smallest = ''
    smallestH = ''


    for i in reversed(range(len(ListParts))):

            if float(ListParts[i].getHeight()) <= float(maxHeight):
                if ListParts[i].getUnused() > 0:
                    if abs(float(length) - float(ListParts[i].getWidth())) < n:
                        n = abs(float(length) - float(ListParts[i].getWidth()))
                        smallest = ListParts[i]
                    if abs(float(length) - float(ListParts[i].getHeight())) < n:
                        n = abs(float(length) - float(ListParts[i].getHeight()))
                        smallestH = extraParts(str(ListParts[i].getType()), str(ListParts[i].getName()),
                                               float(ListParts[i].getWidth()), 1, 0, str(ListParts[i].getMaterial()),
                                               float(ListParts[i].getNumber()), float(ListParts[i].getUsed()),
                                               float(ListParts[i].getUnused()), float(ListParts[i].getPosition()))

    for j in reversed(range(len(ListParts))):
            if float(ListParts[j].getHeight()) <= float(maxHeight):
                if ListParts[j].getUnused() > 0:
                    for k in range(len(ListParts)):
                        if float(ListParts[k].getHeight()) <= float(maxHeight):
                            ListParts[j].use()

                            if ListParts[k].getUnused() > 0:
                                if abs(float(length) - float(ListParts[j].getWidth()) + float(
                                        ListParts[k].getWidth())) < m:
                                    m = abs(
                                        float(length) - float(ListParts[j].getWidth()) - float(ListParts[k].getWidth()))
                                    first = ListParts[j]
                                    second = ListParts[k]
                                    secondH = extraParts(str(ListParts[k].getType()), str(ListParts[k].getName()),
                                                         float(ListParts[k].getWidth()),
                                                         float(ListParts[k].getHeight()),
                                                         float(ListParts[k].getDepth()),
                                                         str(ListParts[k].getMaterial()),
                                                         float(ListParts[k].getNumber()), 1, 0,
                                                         float(ListParts[k].getPosition()))
                                    if float(ListParts[j].getWidth()) + float(ListParts[k].getWidth()) < 150:
                                        m = float(ListParts[j].getWidth()) + float(ListParts[k].getWidth())
                                if abs(float(length) - (
                                        float(ListParts[j].getWidth()) + float(ListParts[k].getHeight()))) < m:
                                    if abs(float(length) - (
                                            float(ListParts[j].getWidth()) + float(ListParts[k].getWidth()))) > abs(
                                            float(length) - (
                                                    float(ListParts[j].getWidth()) + float(ListParts[k].getHeight()))):
                                        m = abs(float(length) - float(ListParts[j].getWidth()) - float(
                                            ListParts[k].getHeight()))
                                        secondH = extraParts(str(ListParts[k].getType()), str(ListParts[k].getName()),
                                                             float(ListParts[k].getWidth()),
                                                             float(ListParts[k].getHeight()),
                                                             float(ListParts[k].getDepth()),
                                                             str(ListParts[k].getMaterial()),
                                                             float(ListParts[k].getNumber()), 1, 0,
                                                             float(ListParts[k].getPosition()))
                                        first = ListParts[j]
                                        second = ListParts[k]
                                        if float(ListParts[j].getWidth()) + float(ListParts[k].getHeight()) < 150:
                                            m = float(ListParts[j].getWidth()) + float(ListParts[k].getHeight())
                                if abs(float(length) - (
                                        float(ListParts[j].getHeight()) + float(ListParts[k].getWidth()))) < m:
                                    if abs(float(length) - (
                                            float(ListParts[j].getWidth()) + float(ListParts[k].getWidth()))) > abs(
                                            float(length) - (
                                                    float(ListParts[j].getHeight()) + float(ListParts[k].getWidth()))):
                                        m = abs(float(length) - float(ListParts[j].getHeight()) - float(
                                            ListParts[k].getWidth()))
                                        firstH = extraParts(str(ListParts[j].getType()), str(ListParts[j].getName()),
                                                            float(ListParts[j].getWidth()),
                                                            float(ListParts[j].getHeight()),
                                                            float(ListParts[j].getDepth()),
                                                            str(ListParts[j].getMaterial()),
                                                            float(ListParts[j].getNumber()), 1, 0,
                                                            float(ListParts[j].getPosition()))
                                        secondH = extraParts(str(ListParts[k].getType()), str(ListParts[k].getName()),
                                                             float(ListParts[k].getWidth()),
                                                             float(ListParts[k].getHeight()),
                                                             float(ListParts[k].getDepth()),
                                                             str(ListParts[k].getMaterial()),
                                                             float(ListParts[k].getNumber()), 1, 0,
                                                             float(ListParts[k].getPosition()))
                                        first = ListParts[j]
                                        second = ListParts[k]
                                        if float(ListParts[j].getHeight()) + float(ListParts[k].getWidth()) < 150:
                                            m = float(ListParts[j].getHeight()) + float(ListParts[k].getWidth())
                                if abs(float(length) - (
                                        float(ListParts[j].getHeight()) + float(ListParts[k].getHeight()))) < m:
                                    if abs(float(length) - (
                                            float(ListParts[j].getWidth()) + float(ListParts[k].getWidth()))) > abs(
                                            float(length) - (
                                                    float(ListParts[j].getHeight()) + float(ListParts[k].getWidth()))):
                                        m = abs(float(length) - float(ListParts[j].getHeight()) - float(
                                            ListParts[k].getWidth()))
                                        firstH = extraParts(str(ListParts[j].getType()), str(ListParts[j].getName()),
                                                            float(ListParts[j].getWidth()),
                                                            float(ListParts[j].getHeight()),
                                                            float(ListParts[j].getDepth()),
                                                            str(ListParts[j].getMaterial()),
                                                            float(ListParts[j].getNumber()), 1, 0,
                                                            float(ListParts[j].getPosition()))
                                        secondH = extraParts(str(ListParts[k].getType()), str(ListParts[k].getName()),
                                                             float(ListParts[k].getWidth()),
                                                             float(ListParts[k].getHeight()),
                                                             float(ListParts[k].getDepth()),
                                                             str(ListParts[k].getMaterial()),
                                                             float(ListParts[k].getNumber()), 1, 0,
                                                             float(ListParts[k].getPosition()))
                                        first = ListParts[j]
                                        second = ListParts[k]
                                        if float(ListParts[j].getHeight()) + float(ListParts[k].getHeight()) < 150:
                                            m = float(ListParts[j].getHeight()) + float(ListParts[k].getHeight())

                            ListParts[j].putBack()

    if (abs(float(length) - float(smallest.getWidth()))) <= (abs(float(length) - float(first.getWidth()) - float(second.getWidth()))):

        smallest.use()
        if smallestH == '':
            smallestH = smallest

        if abs(float(smallest.getWidth()) - float(length)) <= abs(float(smallestH.getWidth()) - float(length)):
            return [smallest]
        else:
            return [smallestH]
    else:
        first.use()
        second.use()
        firstH = first
        if abs(float(first.getWidth()) + float(second.getWidth()) - length) <= abs(
                float(firstH.getWidth()) + float(second.getWidth()) - length):
            if abs(float(first.getWidth()) + float(second.getWidth()) - length) <= abs(
                    float(first.getWidth()) + float(secondH.getWidth()) - length):
                if abs(float(first.getWidth()) + float(second.getWidth()) - length) <= abs(
                        float(firstH.getWidth()) + float(secondH.getWidth()) - length):
                    return [first, second]
                else:
                    return [firstH, secondH]
            else:
                return [first, secondH]

        else:
            return [firstH, second]

    print('none founded')