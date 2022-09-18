#include <iostream>
#include <opencv2/opencv.hpp>

int main(int, char**) {
    std::cout << "Starting OpenCV project!\n";
    auto filename = "../../../../Media/lena.jpg";
    auto image = cv::imread(filename);

    cv::imshow("image",image);
    cv::waitKey();
}
