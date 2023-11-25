# Demo of Mediapipe FaceMesh as Shared Lib with Python

The repo demonstrates proof-of-concept of making shared library in Mediapipe and running Mediapipe apps with Python.

The repos is an adaptation of famous Mediapipe [FaceMesh example](https://github.com/google/mediapipe/tree/1c46e430883c56faefb8d829ad9f51cc94c25f5b/mediapipe/examples/desktop/face_mesh).

## Quick Start

### Requirements
- bazel
- opencv

### Initialize Repo

Clone the repo:
```bash
git clone --recurse-submodules https://github.com/yevhen-k/face-mesh-python.git
```

Initialize prerequisites:
```bash
./init.sh
```

The following vars are optional to make simple tests of cpp demo: `TEST_DEMO=1`, `TEST_DEMO=2`, `TEST_DEMO=3`:
```bash
TEST_DEMO=1 ./init.sh
```

See [init.sh](init.sh) for more details.

### Start Python Demo

To see help:
```bash
LD_LIBRARY_PATH=./lib/ python . --help
```

To test FaceMesh with your WebCam:
```bash
LD_LIBRARY_PATH=./lib/ python . --calculator-graph-config-file=thirdparty/mediapipe/graphs/face_mesh/face_mesh_desktop_live.pbtxt
```

To test FaceMesh on a video file with output to opencv window:
```bash
LD_LIBRARY_PATH=./lib/ python . --calculator-graph-config-file=thirdparty/mediapipe/graphs/face_mesh/face_mesh_desktop_live.pbtxt --input-video-path=test.mp4
```

To test FaceMesh on video and save result as a video:
```bash
LD_LIBRARY_PATH=./lib/ python . --calculator-graph-config-file=thirdparty/mediapipe/graphs/face_mesh/face_mesh_desktop_live.pbtxt --input-video-path=test.mp4 --output-video-path=out.mp4
```

## References

1. `ctypes`
   - https://stackoverflow.com/questions/44211194/
   - https://stackoverflow.com/questions/72984236/passing-pointers-to-dll-function-with-ctypes
   - https://stackoverflow.com/questions/11264838/how-to-get-the-memory-address-of-a-numpy-array-for-c
   - https://habr.com/ru/articles/466499/
2. Shared libs in C++
   - https://iq.opengenus.org/create-shared-library-in-cpp/
3. Numpy to OpenCV data passing
   - https://forums.developer.nvidia.com/t/can-not-create-video-in-c-python-works-in-jetpack5-0-2-worked-on-jetpack4/234401/6
4. OpenCV
   - https://stackoverflow.com/questions/10167534/
5. Sources for testing
   - https://www.vecteezy.com/video/1785975-cheerful-beautiful-young-asian-woman-feeling-happy-smiling-to-camera-while-traveling-at-chinatown-in-beijing-china
   - https://www.vecteezy.com/video/3679210-smiling-portrait-of-handsome-young-asian-man-tourists
   - https://www.vecteezy.com/video/8176509-portrait-of-professional-asian-male-doctor-in-white-medical-coat-man-glasses-making-conference-call-and-looking-at-camera-consulting-distance-patient-online-by-webcam-telemedicine-concept
