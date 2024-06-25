Project Topic: Smooth an image using k-nearest Neighbours algorithm and compare with simple averaging filter result for the same window size 

Steps : 

1. Use the given file (sip_knn_and_simple_avg.exe).
2. GUI pop up will come. Upload image that want to smooth.
3. Accepted formats are .jpg, .png, .jpeg, .gif, .bmp, .webp, .tif
4. Keep size of the image less than 1000 X 1000. Larger values are also accepted by the program but it takes more time to execute.
5. Provide value of window size and k value.
(if widow size is 3 X 3 enter 3, if window size is 5 X 5 enter 5)
(Max value of window size is the minimum(rows, columns) of the input image and max value of k is the value of window size given by user)
6. Click run button.
7. In the back end code will run (Depending on size of window,k and image size it will take time.)
8. Finally the required smoothen images by knn smoothing and simple average smoothing and the difference image will load in gui.
9. The output images are save automatically in the folder.