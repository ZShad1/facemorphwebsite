# facemorphwebsite
 
This is my first side project.

The project has users upload or take a picture. Then, they select 1-5 celebrities, or have the program randomly select them. An image is returned that morphs/averages all the faces in the picture uploaded with the celebrities faces.

1. Face morphing/averaging requires computer vision and machine learning.
	a. We can't just take 2 images with faces and average them. This would give a distorted image since faces can be in different positions and have different shapes.
	b. Instead, computer vision detects the faces using landmarks. We then take the average landmarks of all the faces and create Delauny triangles on the SHAPE of an average face.	
	c. The original face images are warped so that those faces fit the shape of the 'average' face based on landmarks.
	d. The delauny triangles are then applied to the warped faces to find the average value of the triangles across all images
	e. We add all the triangles to get a warped image!
2. I collected a list of Forbes 100 celebrities from 2005 to 2015
	a. I then used the Wikipedia REST API to find images for all the celebrities.
	b. For those who didn't have an image, I removed them from the list
3. The framework for the website is Django. No practical reason in choosing this. I simply chose it because I know Python and didn't know JavaScript.
4. I used Materialze as the front-end framework


TO DO LIST:
-add buttons to remove selected celebrity
-display image on result page
-remove browser auto fill
-design the result page
-clean up celebrity list (a lot of duplicate names)