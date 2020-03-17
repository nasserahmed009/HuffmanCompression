from queue import PriorityQueue
import pickle

# constructing node class to build the tree
class Node:
  def __init__(self, char, probability):
    self.char = char
    self.probability = probability

# reading the text file
textFile = open("originalText.txt", "r")
originalText = textFile.read()
textFile.close()

# if the file is empty terminate
if not originalText.strip():
    print("File is empty")
    exit()

charFrequencies = {}
totalChars = len(originalText)


# getting the frequency of each char
for char in originalText:
    if char in charFrequencies:
        charFrequencies[char] += 1
    else:
        charFrequencies[char] = 1
    
# getting the probability of each char
for char in charFrequencies:
  charFrequencies[char] = charFrequencies[char] / totalChars

queue = PriorityQueue()

# adding the chars to the priority queue
for char in charFrequencies:
    charNode = Node(char, charFrequencies[char])
    queue.put( (charNode.probability , id(charNode) ,charNode) )

if queue.qsize() == 1:
    print('Text with only one letter doesn\'t need compression')
    exit()

# constructing the tree
while queue.qsize() > 1: 
    min1 = queue.get()[2]
    min2 = queue.get()[2]

    newNode = Node('', min1.probability + min2.probability)
    newNode.left = min1
    newNode.right = min2

    queue.put( (newNode.probability , id(newNode) ,newNode) )

codesDic = {}

def constructCode( node, code ):

    if hasattr(node, "char") and  node.char != '':
        codesDic[node.char] = code
        return
    else:
        if hasattr(node, "left"):
            constructCode(node.left, code+'0')
        if hasattr(node, "right"):
            constructCode(node.right, code+'1')

treeHeadNode = queue.get()[2] #tree head node

constructCode(treeHeadNode, '')

# constructing encoded text
encodedText = ''

for char in originalText:
    encodedText += codesDic[char]

# adding encoded text to a file
encodedTextFile = open("encoded.txt", "w")
encodedTextFile.write(encodedText)
encodedTextFile.close()


encodedBinaryFile = open("encoded.bin", "wb")

# encoding by converting the binary into int
# pickle.dump(int("1"+encodedText, 2) , encodedBinaryFile ) 

# encoding by converting each 8 bits to a byte
numOfZerosAtEnd = 8 - (len(encodedText) % 8)
encodedText += numOfZerosAtEnd * '0'
encodedArray = [numOfZerosAtEnd]

for i in range(0, len(encodedText), 8):
    encodedArray.append( int( encodedText[i:i+8] ,2) )

encodedBinaryFile.write(bytearray(encodedArray))
encodedBinaryFile.close()

# Decoding process

# 1- Decoding using tree
######################

#  a function that takes the code and return the char
# def getChar(node, encodedChars):
#         # base condition
#         if encodedChars == '':
#             return node.char if node.char != '' else None

#         if encodedChars[0] == '0':
#             return getChar(node.left, encodedChars[1:] ) if hasattr(node, 'left') else None
#         elif encodedChars[0] == '1':
#             return getChar(node.right, encodedChars[1:] ) if hasattr(node, 'right') else None

# def decode(encodedText, decodingTree):
#     startIndex = 0
#     endIndex = 1
#     decodedText=''
#     while startIndex < len(encodedText):
#         decodedChar = getChar(decodingTree, encodedText[startIndex:endIndex])
        
#         if  decodedChar != None:
#             decodedText += decodedChar
#             startIndex = endIndex
        
#         endIndex+=1
    
#     return decodedText


# 2- Decoding using dictionary
############################

def decode(encodedText, codesDictionary):
    startIndex = 0
    endIndex = 1
    decodedText=''
    codesDicInverse = {}
    
    # forming inverse codes dic where the code is the key
    for char, code in codesDictionary.items():
        codesDicInverse[code] = char

    while startIndex < len(encodedText):
        currentCode = encodedText[startIndex:endIndex]

        if currentCode in codesDicInverse:
            decodedText += codesDicInverse[currentCode]
            startIndex = endIndex
        
        endIndex +=1

    return decodedText

encodedBinaryFile = open("encoded.bin", "rb")

# decoding by converting the int to the equivalent binary
# encodedText = bin(pickle.load(encodedBinaryFile))[3:]

# decoding by using array of bytes
encodedArray = encodedBinaryFile.read()
numOfZerosAtEnd = encodedArray[0]
encodedText = ""
 
for index, val in enumerate(encodedArray):
        encodedText += format(val, '08b')

encodedText = encodedText[8:len(encodedText)-numOfZerosAtEnd]
encodedBinaryFile.close()



# adding decoded text to the text file
encodedTextFile = open("decoded.txt", "w")
# encodedTextFile.write( decode(encodedText, treeHeadNode) ) 
encodedTextFile.write( decode(encodedText, codesDic) )
encodedTextFile.close()
