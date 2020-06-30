if __name__ == "__main__":
    import imageio
    import numpy as np
    from see import GeneticSearch, Segmentors
    import os
    import json
    import requests
    import random
    from datetime import datetime

    # 
    POP_SIZE = 10
    NUM_GENERATIONS = 10
    INPUT_IMAGE = "input.jpg"
    LABEL_IMAGE = "label.png"
    SERVER_URL = "http://serverservice/update"  

    rgb_url = "https://github.com/colbrydi/see-segment/blob/master/Image_data/Examples/Chameleon.jpg"
    label_url = "https://github.com/colbrydi/see-segment/blob/master/Image_data/Examples/Chameleon_GT.png"

    def make_download_command(url, save_as):
        """
        Used to construct a curl command to download
        the image at the specified url.
        """
        return "wget -O " + str(save_as) + " " + str(url) + "?raw=true"

    # Download the images
    os.system(make_download_command(rgb_url, INPUT_IMAGE))
    os.system(make_download_command(label_url, LABEL_IMAGE))

    # Load the images
    img = imageio.imread(INPUT_IMAGE)
    gmask = imageio.imread(LABEL_IMAGE)

    #only need on some images
    # Convert the RGB 3-channel image into a 1-channel image
    #gmask = (np.sum(gmask, axis=2) > 0)

    # Create an evolver
    my_evolver = GeneticSearch.Evolver(img, gmask, pop_size=POP_SIZE)
    
    # Conduct the genetic search
    population = None

    for i in range(POP_SIZE):

        # if population is uninitialized
        if population is None:
            population = my_evolver.run(ngen=1)

        # Simulate a generation and store population in population variable
        population = my_evolver.run(ngen=1, population=population)

        # Take the best segmentor from the hof and use it to segment the rgb image
        seg = Segmentors.algoFromParams(my_evolver.hof[0])
        mask = seg.evaluate(img)

        # Calculate and print the fitness value of the segmentor
        fitness = Segmentors.FitnessFunction(mask, gmask)[0]
        params = my_evolver.hof[0]

        # Combine data into a single object
        data = {}
        data["fitness"] = fitness
        data["params"] = params

        # Convert the data to json format
        data = json.dumps(data)

        # Send data to web server
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(SERVER_URL, data=json.dumps(data), headers=headers) 