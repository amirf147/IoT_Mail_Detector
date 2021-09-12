# IoT_Mail_Detector

A mail detector device that uses an arduino and raspberry pi communicating
with each other serially. The raspberry pi uses the senseHat for detecting
movement of the mail slot as well as providing indoor climate conditions.
The raspberry pi uses a camera to provide images of the mail received.
The arduino controls power to a 12V LED to help in the image capturing and
also monitors hallway brightness with a photoresistor to detect if front
door has been opened. The frontend of the application is in the form of a
telegram bot where the user can make queries on conditions in the home, get
nofications for when the front door is opened and if mail has been received,
an image of the mail is also sent to the user. All data is stored in a local
InfluxDB database and data analysis and presentation is provided with
Grafana.

This project uses an object oriented design to allow the classes to be reused
in other IoT applications with the flexibility of being able to specifiy
which serial protocol to be used for device to device communications and
which database to be used for data storage. Sensors from different devices
are encapsulated in classes to enable modularity and organization.

TO DO:

    Upload the arduino code to the repository

    Refactoring:    
        separate out some of the behaviors in the main file (mail_detect.py)
        into functions

        wrap the timing conditionals in functions so they can be specified
        during set up

        remove * imports

        reduce indentation where possible

        fix some of the class hierarchies to make more logical sense

        change file names to fit with standards and guidelines

    Add logging:
        using the logging library

    Add program monitoring and program restarts on failures:
        to be determined
