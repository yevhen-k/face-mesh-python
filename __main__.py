import argparse
import ctypes
import cv2
import numpy as np


def init_lib() -> ctypes.CDLL:
    lib = ctypes.CDLL("lib/libfmesh.so")

    # init graph
    lib.init_graph.restype = ctypes.c_void_p

    # prepare graph
    lib.prepare_graph.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_char),
    ]

    # prepare poller
    lib.prepare_poller.restype = ctypes.c_void_p
    lib.prepare_poller.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_char),
    ]

    # start run
    lib.start_run.argtypes = [
        ctypes.c_void_p,
    ]

    # process frame
    lib.process_frame.restype = ctypes.c_int
    lib.process_frame.argtypes = [
        ctypes.c_int,  #     rows,
        ctypes.c_int,  #     cols,
        ctypes.c_int,  #     channels,
        ctypes.c_int,  #     type,
        ctypes.POINTER(ctypes.c_char),  #     data,
        ctypes.POINTER(ctypes.c_char),  #     output_frame_mat.data,
        ctypes.c_void_p,  #     status_poller,
        ctypes.c_void_p,  #     graph,
        ctypes.POINTER(ctypes.c_char),  #     kInputStream,
    ]

    # shut down
    lib.shut_down.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_char)]

    # delete graph
    lib.delete_graph.argtypes = [
        ctypes.c_void_p,
    ]

    # delete status poller
    lib.delete_status_poller.argtypes = [
        ctypes.c_void_p,
    ]

    return lib


parser = argparse.ArgumentParser()
parser.add_argument(
    "--calculator-graph-config-file",
    help="Name of file containing text format CalculatorGraphConfig proto.",
    type=str,
    required=True,
)

parser.add_argument(
    "--input-video-path",
    help="Full path of video to load. If not provided, attempt to use a webcam.",
    type=str,
    required=False,
)

parser.add_argument(
    "--output-video-path",
    help="Full path of where to save result (.mp4 only). If not provided, show result in a window.",
    type=str,
    required=False,
)


def prepare_capture(
    capture: cv2.VideoCapture,
    load_video: bool,
    save_video: bool,
    input_video_path: str,
    kWindowName: str,
):
    print("Initialize the camera or load the video.")

    if load_video:
        capture.open(input_video_path)
    else:
        capture.open(0)

    if not capture.isOpened():
        print("Failed to open video capture")
        exit(1)
    if not save_video:
        cv2.namedWindow(kWindowName, cv2.WINDOW_AUTOSIZE)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        capture.set(cv2.CAP_PROP_FPS, 30)


def main():
    lib = init_lib()
    args = parser.parse_args()

    kInputStream = "input_video"
    kOutputStream = "output_video"
    kWindowName = "MediaPipe"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    save_video = bool(args.output_video_path)
    load_video = bool(args.input_video_path)

    calculator_graph_config_file = args.calculator_graph_config_file

    input_video_path = args.input_video_path
    output_video_path = args.output_video_path

    if_break = ctypes.c_int(0)
    grab_frames = True

    capture = cv2.VideoCapture()
    writer = cv2.VideoWriter()

    # init graph
    graph = lib.init_graph()

    # prepare graph
    lib.prepare_graph(graph, calculator_graph_config_file.encode())

    # prepara capture
    prepare_capture(capture, load_video, save_video, input_video_path, kWindowName)

    # prepare poller
    status_poller = lib.prepare_poller(graph, kOutputStream.encode())

    # start run
    lib.start_run(graph)

    while grab_frames:
        ret, camera_frame_raw = capture.read()
        if not ret:
            if not load_video:
                print("Ignore empty frames from camera.")
                continue
            print("Empty frame, end of video reached.")
            break
        camera_frame = cv2.cvtColor(camera_frame_raw, cv2.COLOR_BGR2RGB)
        if not load_video:
            camera_frame = cv2.flip(camera_frame, 1)

        # actual processing
        rows = camera_frame.shape[0]
        cols = camera_frame.shape[1]
        channels = camera_frame.shape[2]
        dtype = 16
        # data, _read_only_flag = camera_frame.__array_interface__["data"]
        # NOTE: read source for `data` property
        data = ctypes.c_char_p(camera_frame.ctypes.data)
        output_frame_mat = np.copy(camera_frame)
        out_data = ctypes.c_char_p(output_frame_mat.ctypes.data)

        if_break = lib.process_frame(
            rows,
            cols,
            channels,
            dtype,
            data,
            out_data,
            status_poller,
            graph,
            kInputStream.encode(),
        )
        if if_break < 0:
            break
        if save_video:
            if not writer.isOpened():
                print("Prepare video writer.")
                writer.open(
                    filename=output_video_path,
                    fourcc=fourcc,
                    fps=capture.get(cv2.CAP_PROP_FPS),
                    frameSize=output_frame_mat.shape[:2][::-1],
                    isColor=True,
                )
                if not writer.isOpened():
                    print("Failed to wrine to file, file closed.")
                    exit(1)
            writer.write(output_frame_mat)
        else:
            cv2.imshow(kWindowName, output_frame_mat)
            pressed_key = cv2.waitKey(5)
            if pressed_key == ord("q"):
                grab_frames = False

    # close resources
    if writer.isOpened():
        writer.release()

    # shut down
    lib.shut_down(graph, kInputStream.encode())

    # delete graph
    lib.delete_graph(graph)

    # delete status poller
    lib.delete_status_poller(status_poller)

    print("SUCCESS!!!")


if __name__ == "__main__":
    main()
