# written by Marian Schoen 

def read_clg_data(path_to_data = "data/DataScienceCodingChallenge/data/CustomerData_LeadGenerator.csv"): 
    """ 
    Read 'CustomData_LeadGenerator.csv', including handling potentially missing data error
    """
    import os, sys
    from zipfile import ZipFile
    import pandas as pd

    print(os.getcwd())

    if os.path.exists("data"): 
        folder = "./"
    else: 
        folder = "../"

    path_to_data = folder + path_to_data

    if not os.path.isfile(path_to_data): 
        path_to_zipfile = folder + "data/DataScienceCodingChallenge.zip" 

        print("There is no csv data at '" + path_to_data + "'. Try to unpack zip file at '" + path_to_zipfile + "'.")

        try:
            os.path.isfile(path_to_zipfile)
            file_handler = ZipFile(path_to_zipfile, "r")
            file_handler.extractall(folder + "data")
            file_handler.close()
            # the data is extracted into a "__MACOSX" folder. This is either due to my setup, or the way the zip file is created. 
            # the following shell call extracts everything into "folder", and removes the unwanted "__MACOSX/" directory.
            os.popen("cp -r " + folder + "__MACOSX/* " + folder + "/data; rm -R " + folder + "data/__MACOSX/")
        except: 
            print("There is no file at " + path_to_zipfile + ". Please check the Readme in the data folder.")
            sys.exit(1)
    
    try: 
        the_data = pd.read_csv(path_to_data)
        return(the_data)
    except: 
        print("Can't read csv file at '" + path_to_data + "'")
        sys.exit(2)

    
