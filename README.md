# Enterprise-VoIP-Report-Django-app
This is a django app I created for internal use at C Spire

The reason for the creation of this app was to make it easier to identify what inventory we had in rate centers in different service locations.

Home <- View Class

![image](https://user-images.githubusercontent.com/53827194/139950128-117224e3-c66e-406a-9986-7d1a718eeeda.png)

GET request:
The page would prompt the user with a form asking them for number status and service location.

POST request:
Creates a QueryInfoModel object for that particular user.
Then it queries for rate centers with the users info populated into the query (query not shown in file).
FilteredRateCenters objects get deleted and then remade specific to that user if it passes the check from us_state_abbrev (not included in the repository for confidentially).
Redirects the user to the FilterData view.

FilterData <- View Class

![image](https://user-images.githubusercontent.com/53827194/139950251-44f7fdb6-bc44-4c16-b4eb-c6ee711e7e26.png)


GET Request:
Prompts the user with a form asking them to choose the rate center and if they want ported in numbers (yes / no) or all of them

POST Request:
Deletes all objects associated with the DisplayModel
initializes the form with the POST request and the USER request
if the form is valid the latest QueryInfoModel object is grabbed
if the port_in value from the form is equal to 2 it queries all the info and displays them via a data table
else it will handle it appropiatley for which port in choice was given 

Data table
![image](https://user-images.githubusercontent.com/53827194/139951774-344d243a-6874-48ea-8fdd-615f9821ccff.png)
