
#module main.py
    instantiate a ClientGUI

#class ClientGUI()
    constructor
        // creates ClientGUI Window w/ TX box, RX box, buttons
        // put checkMyEmail() in its own thread
        // instantiate an AlignWindow
        // alignButton()
        // instantiate a ParamsWindow
        // hide ParamsWindow
    setMessage(string) //prints to receive console
    transmitButton() //send whatever's in the transmit box to encodeDecode.py
        // blocks checkMyEmail
        // calls send() method
        // unblocks checkMyEmail
    alignButton() //unhides alignWindow
        // blocks checkMyEmail
        // waits until alignWindow closed
        // unblocks checkMyEmail
    paramsButton() //unhides alignWindow
        // blocks checkMyEmail
        // waits until alignWindow closed
        // unblocks checkMyEmail
    checkMyEmail() //runs continuously in another thread after alignWindow hidden
        // call receive in encodeDecode.py
        // setMessage(output of encodeDecode.py)

#class AlignWindow()
    constructor // target GPS box, "virtual oscilloscope"
    setGPS() //set target GPS locally
    startButton(AlignWindow object) //send target GPS to align.py to start alignment procedure [start(targetGPS)]
    plot(diodeData) //update oscope readout
    bigRedButton() //stop thread in which start() in align.py is running
    closeButton() //hides AlignWindow
    setFinished() //boolean: alignment complete

#class ParamsWindow()
    constructor // fields: PPM-level, pulse length, sample rate, threshold
    updateParams() //read from fields and send to encodeDecode.py and hide ParamsWindow

#module align.py 
    // takes in target/home GPS and IMU inputs
    getAlignmentData() //ask parser.py for IMU data

    start(targetGPS, alignWindow) // runs in new thread object
        // alignment procedure:    
            // call beamHold(on) in parser.py
            alignRough() // compute necessary alt/az change from GPS+IMU data and target point
                call move(deltaAlt, deltaAz) in parser.py
            while(getDiodeData() < threshold) //called in parser.py
                // wait for reciever input
            fineAdjust()
                while(true)
                    getAlignmentData() //call parser.py
                    getDiodeData() //call parser.py
                    alignWindow.plot(diodeData)
                    // make move decision
                    move(deltaAlt,deltaAz)
                    // decide if done
                        break()
        alignWindow.setFinished()


#module encodeDecode.py    
    send (string message)
        processMessage(string message)
            // compresses and formats message
        // calls sendMessage in parser.py
    recieve()
        if (message = checkMessages() in parser.py)
            return decode(message)
    decode(message)
        checkForErrors(message)

#module/class parser.py 
    //interprets incoming serial and encodes outgoing serial  //locks to prevent conflicts
    beamHold(bool) 
    getAlignmentData() //read from serial buffer and parse into vector of values (and return)
    move(deltaAlt, deltaAz)
    getDiodeData() //read from serial buffer and parse into vector of values (and return)
    sendMessage(string message)
    checkMessages() //returns a message (string) if one has been recieved by the hardware
    //Parsing protocol:
        // Header:
            // 3 Character Message Type
            // Integer message length 