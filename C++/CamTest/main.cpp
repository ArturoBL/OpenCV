#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>

using namespace cv;
using namespace std;

int main(int, char**) {
    VideoCapture cap(0);
    /*VideoCapture cap(2,CAP_DSHOW);
    cap.set(CAP_PROP_FRAME_WIDTH,640);
    cap.set(CAP_PROP_FRAME_HEIGHT,480);
    cap.set(CAP_PROP_FPS,60);*/
    Mat img;

    while(true){
        cap.read(img);
        imshow("image",img);
        if (waitKey(5) >= 0)
            break;
    }
}
