import cv2

def boxes2point(boxes, format_boxes):

    if format_boxes == 'row_col':
        y_str = boxes[0]
        y_end = boxes[1]
        x_str = boxes[2]
        x_end = boxes[3]

    elif format_boxes == 'str_end':
        x_str = int(boxes[0])
        y_str = int(boxes[1])
        x_end = int(boxes[2])
        y_end = int(boxes[3])

    elif format_boxes == 'center_w_h':
        x_c = int(boxes[0])
        y_c = int(boxes[1])
        w = int(boxes[2])
        h = int(boxes[3])

        offset_w = int(w/2)
        offset_h = int(h/2)

        x_str = x_c - offset_w
        y_str = y_c - offset_h
        x_end = x_c + offset_w
        y_end = x_c + offset_h

    start_point = (x_str, y_str)
    end_point = (x_end, y_end)

    return start_point, end_point

def drawMultiRectangle(img, boxes, format_boxes = 'row_col', color = (0,0,255), thickness = 1,
                       label=None):
    '''
        color = BGR
    '''
    nBoxes = boxes.shape[0]
    imgOut = img.copy()
    for ibox in range(nBoxes):
        box = boxes[ibox]
        start_point, end_point = boxes2point(box, format_boxes)

        # imgOut = cv2.rectangle(imgOut, (list_point[0], list_point[1]), (list_point[2], list_point[3]),
        #                         color=color, thickness=thickness)
        imgOut = cv2.rectangle(imgOut, start_point, end_point,
                                color=color, thickness=thickness)

        if not label is None:
            text = str(int(label[ibox]))
            start_point_text = (start_point[0], start_point[1] - thickness)
            imgOut = cv2.putText(imgOut, text, start_point_text, cv2.FONT_HERSHEY_DUPLEX, 0.8,
                                 color, 1, cv2.LINE_AA)

    return imgOut
