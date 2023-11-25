Image source:
* https://www.vecteezy.com/video/1785975-cheerful-beautiful-young-asian-woman-feeling-happy-smiling-to-camera-while-traveling-at-chinatown-in-beijing-china
* https://www.vecteezy.com/video/3679210-smiling-portrait-of-handsome-young-asian-man-tourists
* https://www.vecteezy.com/video/8176509-portrait-of-professional-asian-male-doctor-in-white-medical-coat-man-glasses-making-conference-call-and-looking-at-camera-consulting-distance-patient-online-by-webcam-telemedicine-concept



- https://iq.opengenus.org/create-shared-library-in-cpp/
- https://stackoverflow.com/questions/44211194/
- https://forums.developer.nvidia.com/t/can-not-create-video-in-c-python-works-in-jetpack5-0-2-worked-on-jetpack4/234401/6
- https://stackoverflow.com/questions/72984236/passing-pointers-to-dll-function-with-ctypes
- https://habr.com/ru/articles/466499/
- https://stackoverflow.com/questions/10167534/
- https://stackoverflow.com/questions/11264838/how-to-get-the-memory-address-of-a-numpy-array-for-c


```bash
g++ main.cpp

g++ -c -fPIC lib.cpp
g++ -shared -o liblib.so lib.o


g++ -L$(pwd)/lib/ main.cpp -lfmesh
g++ -L./lib/  main.cpp -lfmesh
g++ -Llib/  main.cpp -lfmesh

```