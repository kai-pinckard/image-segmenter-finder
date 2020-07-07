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
    size = 0
    with open(save_as, "wb") as f:
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
        self.base_dir = os.getcwd()
        self.web_pages_dir = os.path.join(self.base_dir, "web_pages")
        """
        The images must be stored in the directory public
        so that they can be displayed to the user.
        """
        self.static_dir = os.path.join(self.base_dir, "public")

        # Remove any image files previously saved while the server was running
        images = os.listdir(self.static_dir)
        for image in images:
            img_path = os.path.join(self.static_dir, image)
            os.remove(img_path)

        # The file extension will be added when the images are uploaded
        self.rgb_filename = os.path.join(self.static_dir, "rgb.jpg")
        self.label_filename = os.path.join(self.static_dir, "label.jpg")

    # Methods with expose are accessible urls in browser
    @cherrypy.expose
    def index(self):
        html_path = os.path.join(self.web_pages_dir, "index.html")
        return open(html_path)

    # Users are redirected to this page after submiting their files.
    @cherrypy.expose
    def verify(self, rgb_image, label_image):
        # Get the file extensions
        _, rgb_filetype = os.path.splitext(rgb_image.filename) 
        _, label_filetype = os.path.splitext(label_image.filename)
        print(label_filetype)

        # Get the filename
        rgb_filename, _ = os.path.splitext(self.rgb_filename)
        label_filename, _ = os.path.splitext(self.label_filename)
        print(label_filename)

        # Update the filename
        self.rgb_filename = rgb_filename + rgb_filetype
        self.label_filename = label_filename + label_filetype

        save_uploaded_file(rgb_image, self.rgb_filename)
        save_uploaded_file(label_image, self.label_filename)

        html_path = os.path.join(self.web_pages_dir, "verify.html")
        return open(html_path)


    """
    This url route allows the worker to submit updates to the server.
    """
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
    
    """
    This url route is used by the worker to get a manifest of the available images.
    """
    @cherrypy.expose
    def manifest(self):
        images = os.listdir(self.static_dir)
        json_data = json.dumps(images)
        return json_data


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

            html_path = os.path.join(self.web_pages_dir, "monitor.html")
            return open(html_path)
            
        html_path = os.path.join(self.web_pages_dir, "monitor-wait.html")
        return open(html_path)


if __name__ == "__main__":

    conf = {
        'global': {
            'server.socket_host':'0.0.0.0',
            'server.socket_port': 8080,
            'tools.caching.on': False,
            'tools.caching.debug': False
            },

        # This mounts the public directory onto the security directory
        # Anything inside the public directory will appear as if it is in
        # the static directory to the server. 
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.getcwd(), "public"),
            'tools.expires.on': True, # cached browser data expires
            'tools.expires.secs': 1 # cached data expires after 1 sec old
            }
        }
    cherrypy.quickstart(Root(), '/', conf)