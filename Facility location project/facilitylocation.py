'''
    
This is a project for solving facility location problems.

Input:
    Ask user for a radius of coverage.
Output:
    A kml file, based on the radius of coverage user enters. 
    Visualized the solution in Google Earth.

Modules :
    string
    
Method:
    First of all, data preprocessing, read the geographic data from a file and store the data in an appropriate data structure.
    
    Then, solve the facility location problm on this geopraphic data set
    
    Finally, output the solution to the facility locaton problem in a format that can be visualized
    in a mapping software such as google maps.
    
    
Author:Yuan Tu



'''




'''phase 1

Read the geographic data from a file and store the data in an appropriate data structure

'''
import string

def storeCity(line, cities) :
    ''' Extracts the city name and state and stores it. '''
    city  = line[:line.index(',')].strip()
    state = line[line.index(',')+1:line.index('[')].strip()
    cities.append(city + ' ' + state)
    
def storePopulation(line, population) :
    ''' Extracts the population from a line and stores it. '''
    population.append(int(line[line.index(']')+1:]))
    
def storeCoordinates(line, coordinates) :
    ''' Extracts the coordinates from a line and stores them. '''
    coordinates.append((line[line.index('[')+1 : line.index(']')].split(',')))

def storeDistances(cities, newDistances, distances) :
    ''' Stores the distances to/from each city to the current city. '''
    
    # Skip over the first city since its distances haven't been seen yet
    if not cities: 
        return
    
    # Convert all new distances to integers
    newDistances = [int(x) for x in newDistances]
    
    # Compute dimension of new distances array - 1
    n = len(newDistances)-1
    
    # Set the distance of city from itself to zero
    distances.append([0])

    # For each city already seen
    for i in range(n+1) : 
        # Append the distance to this city
        distances[n-i] = distances[n-i]    + [newDistances[i]]
        # Insert the distance from this city
        distances[n+1] = [newDistances[i]] + distances[n+1]
               
def isCityLine(line) :
    ''' Returns whether a line contains city information.'''
    return line[0].isalpha()

def isDistanceLine(line) :
    ''' Returns whether a line contains distance information.'''
    return line[0].isdigit()

def createDataStructure():
    ''' Reads from miles.dat and returns a data structure containing all the information in miles.dat.
        The data structure is a list of 4 items. The first item is a length-128 list of city names.
        The second item is a length-128 list of coordinates. The third item is a length-128 list of 
        populations. The 4th item is a 128 by 128 matrix of distances.'''

    cities      = []     # List of valid city names (city name and state)
    coordinates = []     # Coordinates (lat and long) of each city
    population  = []     # Population of each city
    distances   = []     # Distances to/from each pair of cities

    accDist = []     # Accumulates distances seen over several lines

    f = open("miles.dat", "r")
    for line in f:
        # If this line has distances, accumulate the new distances
        if isDistanceLine(line) :
            accDist = accDist + line.split()
        # If this line has data for a new city
        elif isCityLine(line) :
            # Store the distances accumulated for the previous city
            storeDistances(cities,accDist,distances)
            accDist = []
            # Store the name, coordinates, and popuation for this city
            storeCity(line,cities)
            storeCoordinates(line,coordinates)
            storePopulation(line,population)
    f.close()

    # Store the distances for the last city
    storeDistances(cities,accDist,distances)
 
    return [cities, coordinates, population, distances]


def getCoordinates(name, data) :
    ''' Returns the coordinates for a city as a list of lat and long.
        Returns an empty list if the city name is invalid. '''
    
    cities = data[0]
    coordinates = data[1]

    result = []
    if name in cities :
        result = coordinates[cities.index(name)]
        #print (coordinates[cities.index(name)])
        
    return result

def getPopulation(name, data) :
    ''' Returns the popultion for a city.
        Returns None if the city name is invalid.'''

    cities = data[0]
    population = data[2]
           
    result = None
    if name in cities :
        result = population[cities.index(name)]
    return result
       
def getDistance(name1, name2, data) :
    ''' Returns the distance between two cities. 
        Returns None if either city's name is invalid.'''
 
    cities = data[0]
    distances = data[3]
           
    result = None
    if name1 in cities and name2 in cities :
        result = distances[cities.index(name1)][cities.index(name2)]
    return result

def nearbyCities(name, r, data) :
    ''' Returns a list of cities within distance r of named city
        sorted in alphabetical order.
        Returns an empty list if city name is invalid. '''
 
    cities = data[0]
    distances = data[3]
           
    result = []
    if name in cities :                # If the city name is valid
        i = cities.index(name)           # Get the index of the named city
        for j in range(len(cities)) :      # For every other city
            if distances[i][j] <= r :      # If within r of named city
                result = result + [cities[j]]  # Add to result
    result.sort() 
    return result





#phase 2 starts here:

'''solve the facility location problm on this geopraphic data set'''

def served(data):
    ''' initialize the served list
        returns a list that every elements in the list with a value of false'''
    
    cities = data[0]
    servedList=[]

    for i in range(len(data[0])):
        servedList.append(False)
    return (servedList)



def CitynotServed(c, r,data,checklist):
    ''' returns all cities that have not been served yet.'''
    
    citiesWithinR=nearbyCities(c, r, data)
    cities = data[0]
    result=[]
    for name in citiesWithinR:
        i = cities.index(name)
        ##if city name is false in checklist, then append to result list
        if checklist[i] ==False:
            result.append(name)
    return (result)

##do not forget to reset servedlist!!!!!!!!!!
        
def resetCitytoServed(city,data,checklist):
    '''  input a city that is served and change its value to true(means served).
         returns list that shows the serveing status of all the cities'''
    
    cities = data[0]
    if city in cities:
        i=cities.index(city)
        checklist[i]=True
    return (checklist)
    

def findMaxNeibor(data,r,checklist):
    '''return a city that can serve the most cities within the rage r to minimize the cost'''
    
    cities = data[0]
    neibors=[]
    i=0
    for city in cities:
        
        CityUnserved=CitynotServed(city, r, data,checklist)
        neibors.append(len(CityUnserved))
    
    maxNeibor=max(neibors)
    if maxNeibor==0:
        return False
    i=neibors.index(maxNeibor)
   
    return cities[i]



def locateFacilities(data,r):
    '''return1 :all the facilities
       return2:a dictionary (key: every facility; value: a list of city that has been served by a key/faclility )
     '''
    
    checklist=served(data)
    cities = data[0]
    result1=[]
    result2={}
    while findMaxNeibor(data,r,checklist)!=False:
        city=findMaxNeibor(data,r,checklist)

        CityUnserved=CitynotServed(city, r, data,checklist)
        
        if CityUnserved!=[]:
    
            result1.append(city)
            result2[city]=CityUnserved
            for c in CityUnserved:
                checklist=resetCitytoServed(c,data,checklist)
                
    result1.sort()
    return result1,result2



'''phase 3:
    output the solution to the facility locaton problem in a format that can be visualized
    in a mapping software such as google maps.
'''

def display(facility,data):
    ''' writing KML file...'''
    
    facilityList=facility[0]
    facilityAndThisNeiborCity=facility[1]
    f=open("visualization"+str(r)+".kml","w")
    f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n<Document> \n<Style id='smallLine'>\n<LineStyle> \n<color>7f00007f</color> \n<width>1</width> \n</LineStyle>\n<PolyStyle>\n<color>#ff1111ff</color>\n</PolyStyle>\n</Style>\n")
    
    for c in facilityList:
        latitude=(int(getCoordinates(c, data)[0]))/100.0
        longitude=(int(getCoordinates(c, data)[1])/(-100.0))
        f.write("   <Placemark>\n")
        f.write("       <name>" + c + " (facility)" +"</name>\n")
        f.write("       <description>" + c + "</description>\n")
        f.write("       <Point>\n")
        f.write("           <coordinates>" + str(longitude)+","+str(latitude)+","+ '0' +"</coordinates>\n")
        #print (getCoordinates(c, data))
        f.write("       </Point>\n")
        f.write("   </Placemark>\n")
        for city in facilityAndThisNeiborCity[c]:
            if city!=c:
                lat=(int(getCoordinates(city, data)[0]))/100.0
                long=(int(getCoordinates(city, data)[1])/(-100.0))
                #pin:
                f.write("   <Placemark>\n")
                f.write("       <name>" + city + "</name>\n")
                f.write("       <description>" + city + "</description>\n")
                f.write("       <Point>\n")
                f.write("           <coordinates>" + str(long)+","+str(lat)+","+ '0' +"</coordinates>\n")
                f.write("       </Point>\n")
                f.write("   </Placemark>\n")
                
                #line:
                f.write("   <Placemark>\n")
                f.write("        <LineString>\n")
                f.write("               <coordinates>\n")
                f.write("               "+str(longitude)+","+str(latitude)+","+ '0\n\t\t'+
                        str(long)+","+str(lat)+","+ '0\n'+"               </coordinates>\n")
                f.write("        </LineString>\n")
                f.write("  <Style> \n   <LineStyle>\n"+
                        "        <color>#ff0000ff</color>\n   </LineStyle> \n"+
                        "  </Style>\n</Placemark>\n")
                        
                
    f.write("</Document>\n</kml>")
    f.close()
    return "The mission is completed."

if __name__=="__main__":
    data = createDataStructure()
    t=True
    while t:
        while True:
            while True:
                r=input("Enter the radius of coverage (Ex. 300 or 800):")
                try:
                    r=int(r)
                    
                    break
                except Exception:
                    print ("Bad input.Please try it again")

            if r<300 or r>800:
                print ("Bad input.Please try it again")
            
            else:
                print ("Program is running......")
                break
        facility=locateFacilities(data,r)
        display(facility,data)
        print ("Done!\n")
        while True:
            continueCheck=input("Do you want to try a different radius of coverage? Y/N")
            if continueCheck=="Y" or continueCheck=="y":
                print ("continue.\n")
                break
            elif continueCheck=="N" or continueCheck=="n":
                print ("See you!")
               
                t=False
                break
            else :
                print("Bad input.Please try it again")
            
    
