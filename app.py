
from website import create_app
#!TODO: implement yolo object detection
#!TODO: count cells, do the maths, render results to upload template
#!TODO: add visual feedback with coordinate pairs to support count, render to template
#!TODO: clean up

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)