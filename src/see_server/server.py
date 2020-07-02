import cherrypy
import json
import os
import imageio
from see import GeneticSearch, Segmentors

"""
uploaded_file must match the name field of the input element
in the relevant html file. 

save_as is the desired file name for the uploaded file to be
stored as.
"""
def save_uploaded_file(uploaded_file, save_as):
    saved_file_path = os.path.join(os.getcwd(), save_as)
    size = 0
    with open(saved_file_path, "wb") as f:
        while True:
            # Read the image data in chunks of 8192
            data = uploaded_file.file.read(8192)
            if not data:
                break
            # Write the current chunk into the file to save on disk
            f.write(data)
            size += len(data)
            

class Root:

    def __init__(self):
        self.best_fit = -1
        self.best_ind = {}

        """
        The images must be stored in the directory public
        so that they can be displayed to the user.

        Note: if the filenames are changed then they must also be updated
        in segment_container.py
        """
        self.rgb_filename = os.path.join("public", "rgb.jpg")
        self.label_filename = os.path.join("public", "label.jpg")

    # Methods with expose are accessible urls in browser
    @cherrypy.expose
    def index(self):
        html_dir = os.path.join(os.getcwd(), "web_pages", "index.html")
        return open(html_dir)

    # Users are redirected to this page after submiting their files.
    @cherrypy.expose
    def upload(self, rgb_image, label_image):
        save_uploaded_file(rgb_image, self.rgb_filename)
        save_uploaded_file(label_image, self.label_filename)

        html_dir = os.path.join(os.getcwd(), "web_pages", "upload.html")
        return open(html_dir)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def update(self):
        result = {"operation": "request", "result": "success"}

        input_json = cherrypy.request.json
        input_json = json.loads(input_json)

        if self.best_fit == -1 or self.best_ind["fitness"] > input_json["fitness"]:
            self.best_ind = input_json
            self.best_fit = self.best_ind["fitness"]
        return result

    @cherrypy.expose
    def monitor(self):
        if self.best_fit != -1:
            img = imageio.imread(self.rgb_filename)
            gmask = imageio.imread(self.label_filename)

            print(self.best_ind["params"])
            self.best_ind["params"]
            seg = Segmentors.algoFromParams(self.best_ind["params"])
            mask = seg.evaluate(img)

            static_dir = os.path.join(os.getcwd(), "public")
            imageio.imwrite(os.path.join(static_dir, "mask.jpg"), mask)

            html_dir = os.path.join(os.getcwd(), "web_pages", "monitor.html")
            return open(html_dir)
            
        html_dir = os.path.join(os.getcwd(), "web_pages", "monitor-wait.html")
        return open(html_dir)


if __name__ == "__main__":

    conf = {
        'global': {
            'server.socket_host':'0.0.0.0',
            'server.socket_port': 8080
            },

        # This mounts the public directory onto the security directory
        # Anything inside the public directory will appear as if it is in
        # the static directory to the server. 
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.getcwd(), "public")
            }
        }
    cherrypy.quickstart(Root(), '/', conf)