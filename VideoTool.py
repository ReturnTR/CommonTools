import cv2


def capture_img_from_video(video_path,image_path,image_num=10):



    # 读取视频
    cap = cv2.VideoCapture(video_path)
    # 获取视频总帧数
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(frame_count)
    # 截图时帧的间距，这里10是要等间距截取10张图
    frame_interval = int(frame_count // image_num)
    # 起始截取帧位置
    start_frame = 1

    flag = 0
    while (cap.isOpened()):
        cap.set(cv2.CAP_PROP_POS_MSEC, flag)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        print(flag)
        ret, img = cap.read()
        cv2.waitKey(2000)
        cv2.imwrite((image_path + "/{}.jpg").format(flag), img)
        flag += 1
        start_frame += frame_interval
        # if not ret:
        if start_frame >= frame_count:
            break
    cap.release()
    cv2.destroyAllWindows()

capture_img_from_video("test.mp4","img_test",20)
