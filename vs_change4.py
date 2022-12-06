import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import datetime
    
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class MyVideoCapture:
    def __init__(self, video_source):
        # Open the video source
        self.webcam = cv2.VideoCapture(video_source)
        if not self.webcam.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.webcam.isOpened():
            ret, frame = self.webcam.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.webcam.isOpened():
            self.webcam.release()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go to page one",
                  command=master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Go to page two",
                  command=master.switch_frame(PageTwo)).pack()

class PageOne(tk.Frame):
    def __init__(self,  master):
        tk.Frame.__init__(self, master)
        video_source = 0
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()


        # Button that lets the user take a snapshot
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.fps = self.vid.webcam.get(cv2.CAP_PROP_FPS)
        self.delay = round(1000.0/self.fps)
        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        self.after(self.delay, self.update)

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        video_source = 1
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.fps = self.vid.webcam.get(cv2.CAP_PROP_FPS)
        self.delay = round(1000.0/self.fps)
        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        self.after(self.delay, self.update)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()