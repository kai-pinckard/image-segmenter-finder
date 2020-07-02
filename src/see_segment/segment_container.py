if __name__ == "__main__":
    import sys, getopt
    import imageio
    import numpy as np
    import os
    import json
    import requests
    import random
    import time
    from datetime import datetime
    from see import GeneticSearch, Segmentors
    #=====================================================================
    """
    Note: these are all the default values unless they are changed by
    a command line argument these values will hold.
    """

    # These values control the genetic search
    pop_size = 10
    num_gen = 5

    # These values describe wait times before image download attempts
    initial_delay = 5
    download_delay = 2

    # The url of the server to contact
    server_url = "http://0.0.0.0:8080"  

    # These are relative urls and must be combined with the server url
    rgb_url = "static/rgb.jpg"
    label_url = "static/label.jpg"

    #=====================================================================
    # Handle command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:g:l:h")
    except getopt.GetoptError:
        print("For help run:")
        print("python segment_container.py -h")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("flags:")
            print("l: Location")
            print("g: number of Generations")
            print("p: Population size")
            print("To run in a kubernetes cluster run:")
            print("python segment_container.py -l cluster")
            print("To run locally run:")
            print("python segment_container.py -l local")
            print("To run with a population size of 6 and to simulate 7 generations run:")
            print("python segment_container.py -p 6 -g 7")
            print("The defaults:")
            print("By default location=local population=10 generations=5")
            sys.exit()
        elif opt == "-l":
            if opt == "cluster":
                server_url = "http://serverservice"
        elif opt == "-p":
            pop_size = int(opt)
        elif opt == "-g":
            num_gen = int(opt)
    print("Running with parameters:")
    print("population size =", str(pop_size))
    print("number of generations =", str(num_gen))
    print("server url =", server_url)
    print("")



    print("Attempting to download images in", initial_delay, "second(s)")
    time.sleep(initial_delay)

    # Create image urls
    rgb_url = server_url + "/" + rgb_url
    label_url = server_url + "/" + label_url

    # Temporary, needs to be replaced with a means of determining the filetype
    rgb_filename = "rgb.jpg"
    label_filename = "label.jpg"

    # Create image download commands
    get_rgb = "wget -O " + str(rgb_filename) + " " + str(rgb_url)
    get_label = "wget -O " + str(label_filename) + " " + str(label_url)


    # Download the images
    download_status = os.system(get_rgb)
    download_status = download_status + os.system(get_label)

    while download_status != 0:
        print("Download failed retrying in", download_delay, "second(s)")
        time.sleep(download_delay)
        download_status = os.system(get_rgb)
        download_status = download_status + os.system(get_label)

    # Load the images
    img = imageio.imread(rgb_filename)
    gmask = imageio.imread(label_filename)

    # Only needed on some images
    # Convert the RGB 3-channel image into a 1-channel image
    # gmask = (np.sum(gmask, axis=2) > 0)

    # Create an evolver
    my_evolver = GeneticSearch.Evolver(img, gmask, pop_size=pop_size)
    
    # Conduct the genetic search
    population = None

    for i in range(num_gen):

        # if population is uninitialized
        if population is None:
            population = my_evolver.run(ngen=1)
        else:
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
        server_update_url = server_url + "/update"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(server_update_url, data=json.dumps(data), headers=headers) 