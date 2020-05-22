# Grayoptics
## General
This project is for estimating angle of a checkerboard.

It works with the following assumptions:
- Checkerboard is exactly perpendicular to the camera z-axis
- Checkerboard is clear enough and has it least 2*2 visible squares
- The angle difference from horizontal axis is less than PI/4 (45 Degrees)

Example can be found in [The test file](test.py)

It was tested with Python 3.7.4 
It depends on OpenCV

## Paramteres

### resize_factor
Floating value between ]0,1]
- 1 Means no resizing
- 0.5 means half of the original size
- and so on ...

Resizing the image before trying to detect the angle for performance sake. However, resizing results in lower angle resolution.

### crop_factor

Floating value between ]0,1]
- 1 Means no cropping
- 0.5 means half of the width and half of the height -> 0.25 of the area is preserved.
- and so on ...
- 
Cropping the image at the center for performance sake. Please keep in mind that if cropping results in very smal checkerboard (less than 2*2), the algorithm fails.

### pattern_size
The checkerboard size [rows, columns]. It works in decreasing manner. So, actually, it is the highest possible checkerboard size. For example, if you provided [5 ,5], the ALgorithm will search for [5,5], if not found for [5,4], if not found for [4,5] and so on till [2,2].

Using high value results in low FPS since detecting the checkerboard is the most performance intensive operation by far.
