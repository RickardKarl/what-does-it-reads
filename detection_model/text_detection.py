# Packages
from imutils.object_detection import non_max_suppression
import numpy as np
import time
import cv2

# Module files
from read_input import TextDetectionInputParser

# Mean subtraction values
mean_red = 123.68 
mean_green = 116.78
mean_blue = 103.94

if __name__ == "__main__":

    # Parse arguments
    parser = TextDetectionInputParser()
    args = parser.args

    # Get image and save original
    image = cv2.imread(args['image'])
    orig = image.copy()
    (orig_height, orig_width) = image.shape[:2]

    # Reshape image
    resized_width = args['width']
    resized_height = args['height']
    scale_width = orig_width / float(resized_width)
    scale_height = orig_height / float(resized_height)
    
    image = cv2.resize(image, (resized_width, resized_height))
    # Get heigth and width of reshaped image
    (height, width) = image.shape[:2]


    # Define the output layer names for EAST
    layer_names = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]
    # Load the pre-trained EAST text detector
    print("Loading EAST text detector from {}.".format(args['east']))
    network_model = cv2.dnn.readNet(args['east'])


    # Preprocess image to blob
    blob = cv2.dnn.blobFromImage(image, 1.0, (width, height),
	(mean_red, mean_green, mean_blue), swapRB=True, crop=False)

    # Run network model
    network_model.setInput(blob)
    (scores, geometry) = network_model.forward(layer_names)
    print("Text detection done.")

    # Extract boxes and probabilities
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    
    # Loop over rows
    for j in range(0, numRows):
        scoresData = scores[0, 0, j]
        xData0 = geometry[0, 0, j]
        xData1 = geometry[0, 1, j]
        xData2 = geometry[0, 2, j]
        xData3 = geometry[0, 3, j]
        anglesData = geometry[0, 4, j]


        for i in range(0, numCols):
            # Check confidence level
            if scoresData[i] < args["min_confidence"]:
                continue


            # Get a offset
            (offsetX, offsetY) = (i * 4.0, j * 4.0)

            # Angle data
            angle = anglesData[i]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # Get height and width of box
            h = xData0[i] + xData2[i]
            w = xData1[i] + xData3[i]

            # Compute box coordinates
            endX = int(offsetX + (cos * xData1[i]) + (sin * xData2[i]))
            endY = int(offsetY - (sin * xData1[i]) + (cos * xData2[i]))
            startX = int(endX - w)
            startY = int(endY - h)

            # Add final rectangle coordinates and probabilites
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[i])


rects = non_max_suppression(np.array(rects), probs=confidences)

# loop over the bounding boxes
for (startX, startY, endX, endY) in rects:
	# Scale boxes according to scale ratio
	startX = int(startX * scale_width)
	startY = int(startY * scale_height)
	endX = int(endX * scale_width)
	endY = int(endY * scale_height)

	# Draw bounding box
	cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)


# Save image or plot
if args['save_image'] != None:
    file_name = args['save_image'] + '.jpg'
    cv2.imwrite(file_name, orig)
else:
    figure = cv2.imshow("Result", orig)
    cv2.waitKey(0)




    