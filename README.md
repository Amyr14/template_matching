## Description
Image processing course assignment on the topic of template matching methods. It was required the recording of a short video with a moving object on sight. Then, a template image of this object was to be extracted from the video frames. Using openCV, this template was to be used to test different template matching methods. The maximum and minimum values from each method's results were to be graphed, so as to allow the identification of the best method by a metric that was to be elaborated upon. Finally, the chosen method was to be used to produce a tracking video of the object. The code can be verified in the jupyter notebook and in the file tm.py, while a more detailed description of the experiments can be found in the Template Matching.pdf file, which is the portuguese-written report of the assignment.

## Chosen Method
As said in the description, the maximum-minimum graphs were used to identify the best template matching method. The maximum and minimum values from the results are used to measure correlation (in correlation-driven methods) and squared differences (in squared differences methods) respectively. So, intuitively:

* In correlation-driven methods, high peaks in the maximum values can be interpreted as the presence of the object in the frame
* In square-difference-driven methods, low valleys in the minimum values can be interpreted as the presence of the object in the frame
  
Therefore, if a method exhibits this behaviour in a consistent manner, allowing clear distinction from frames where the object is present on the scene from frames where it isn't, it can be considered the best method.
As it's written in the report, the normalized correlation coefficient method was chosen by a visual identification of this behaviour in the maximum-minimum graph.

![graph(2)](https://github.com/Amyr14/template_matching/assets/69065770/10dcc0e6-9a32-4813-a0fb-6755815bd7b9)

*The method's maximum-minimum graph*

## Produced Tracking Video
As the chosen method is correlation-driven, the location of the maximum values can be interpreted as the top-left corner of the object in the frame. Because the dimensions of the template image are know, a rectangle with same dimensions can be drawn in the frame, representing the object's location. Bellow is the resulting tracking video.

![tracking-ezgif com-resize](https://github.com/Amyr14/template_matching/assets/69065770/334800d3-d3c6-42d7-a5ca-36d051cb2664)

One interesting observation is the method's inability to identify the object when it's rotated. That's because the method is not rotation invariant.
