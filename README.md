# environment-monitor

**Hardwares**
|Name                                                                                                          | Cost ($) | Quality | Purchase Link                                                                                                                                                                                                                                                                                                                       |
|---------------------------------------------------------------------------------------------------------------|----------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Raspberry Pi 4 Model B-4GB                                                                                     | 55       | 1       | [Link](https://www.adafruit.com/product/4564)                                                                                                                                                                                                                                                                                        |
| microSD Card                                                                                                   | 16.58    | 1       | [Link](https://www.amazon.com/SanDisk-Extreme-microSDXC-Memory-Adapter/dp/B09X7BK27V/ref=sr_1_3?crid=2DEK2XMBKXQ9G&dib=eyJ2IjoiMSJ9.LAX3f6DsoasKl5zu7gLGJszm-20t9tUipJc0G6hN18K2K93XYFdcXFn5_rOc2xQVcXjHgTWoILtiHJecEj1bBxSGw8-85puEUG5t_Dvdc3aV9JaU4qEHLKxavmjFImDQ3qInGKMPmvK2IaphXHFH9r_zY4JCfhhTyIZXjsywkw35dsHP_pjL0lwSQFVA_rx_B6VWo_Xn_FnEr78GIG0BBBwexV3SScK7IFPW0WIY6Do.NVGlC2Ig2Jrbkgfjon-p27gV1_MvdUrC6OMkQnAMHes&dib_tag=se&keywords=microsd&qid=1723747577&sprefix=microsd%2Caps%2C116&sr=8-3&th=1)                        |
| BME280 Temperature Humidity Pressure                                                                           | 14.95    | 1       | [Link](https://www.adafruit.com/product/2652)                                                                                                                                                                                                                                                                                        |
| TSL2591 Light sensor                                                                                           | 6.95     | 1       | [Link](https://www.adafruit.com/product/1980)                                                                                                                                                                                                                                                                                        |
| 4-pin JSH SH Connector (QT-QT)                                                                                 | 0.95     | 1       | [Link](https://www.adafruit.com/product/4210)                                                                                                                                                                                                                                                                                        |
| 4-pin JSH SH Connector (QT-female)                                                                             | 0.95     | 1       | [Link](https://www.adafruit.com/product/4397)                                                                                                                                                                                                                                                                                        |
| Miuzei Case for Raspberry Pi 4, Raspberry Pi 4b Case with Fan 35mm, with 5V 3A Power Supply, 4 pcs Heatsinks   | 13       |    1     | [Link](https://www.amazon.com/Miuzei-Raspberry-Power-Supply-Heatsinks/dp/B089NQBBBK/ref=asc_df_B089NQBBBK/?tag=hyprod-20&linkCode=df0&hvadid=693601922380&hvpos=&hvnetw=g&hvrand=11153586277896083454&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9199035&hvtargid=pla-1031445451341&psc=1&mcid=f74d0a2cddce3775ae7e00013eab2d21) |
| Official MicroHDMI to HDMI Cable                                                                               | 6        | 1       | [Link](https://www.canakit.com/official-micro-hdmi-to-hdmi-cable.html?defpid=4651)                                                                                                                                                                                                                                                   |
| 2 Pcs USB 2.0 Mini Microphone                                                                                  | 9        | 1       | [Link](https://www.amazon.com/KISEER-Microphone-Desktop-Recording-YouTube/dp/B071WH7FC6/ref=sr_1_4?crid=2FA27Z6X10FBE&dib=eyJ2IjoiMSJ9.r83My3OTOt2C8UyGuN1JG6eYGefdzGWm3HPXX9bxHmtQTC6TUt8EFQ1GoIkB38QIaKlB1PVxSIK9oX6woOp_ZTECz9uPre5q06FBr9DmC85lbyGX4yHm4s2G4dbYIA2LtNeblszEKmxRJ45kRJORXlYmGrJhkDbK_Io3TYaEMPSYa-kUSIdyKopLLhUAGrE2yRncYIi8Tr4xcmvc8txKP2DS4g252gYFjQODcSMTGkAx6wFnVrpAdZaO7aTHogdVFQcf26SPNk9FCtMu6Yboazx7BkfvTazaTl5ZAyjf-D8.-uMzI98_TYLryeeb1vcaBZiOsxbKqIVgLnpwN-3L6Hw&dib_tag=se&keywords=usb+microphone+for+raspberry+pi&qid=1723754617&s=electronics&sprefix=USB+Microphone+for+ras%2Celectronics%2C114&sr=1-4) |




**Hardware circuits and rasp pi Installation**

1. install raspberry pi os to the microSD card, set up the config file

    *download raspberry pi os imager: https://www.raspberrypi.com/software/*

2. Connect usb-mouse/keyboard, hdmi-moniter to raspberry pi 4
3. Insert SD card and power on raspberry pi to check if the system is correctly installed

4. (optional)remote control 

5. Connect sensiors to raspberry pi: https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test
   

        red to pin 1, power 3.3

        black to pin 6, gound

        blue to pin 2, data

        yellow to pin 3, clock

6. Enable I2C communication
    ```
    sudo raspi-config: enable the i2C
    sudo reboot
    ```
    Test I2C Communication
    ```
    sudo i2cdetect -y 1
    ```



**Software**
1. Virtual enviromentand package requirement

    ```
    python3 -m venv env-name
    source env-name/bin/activate
    pip3 install Flask Flask-Cors adafruit-circuitpython-tsl2591 adafruit-circuitpython-bme280 pyaudio numpy
    ```
2. Server
    ```
    cd project folder
    source env-name/bin/activate
    python3 api.py

    ```

3. Client (gui.py)
    create the virtual enviroment as described above
    ```
    pip3 install requests pandas

    ```


4. deploy the gui to an executable file

    ```
    pip install pyinstaller
    cd to the python script is located
    pyinstaller --onefile --windowed gui.py


    for custom icon
    pyinstaller --onefile --windowed --icon=your_icon.ico your_script_name.py

    ```
