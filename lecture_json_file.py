import json
import os
import shutil
def reading(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data['views']
    
def find_images_folder(folder_input,folder_output,image_format,data):
        if os.path.exists(folder_input):
            for view in data:
                path_input = folder_input + "/" + view['viewId'] + '.' + image_format
                path_source_split = view['path'].split("/")
                image_name_input = path_source_split[-1].split(".")
                path_output = folder_output + "/" + image_name_input[0] + '.' + image_format
                shutil.copyfile(path_input,path_output)



        
            # #os.chdir(folder_input)
            # files = os.listdir(folder_input)
            # nb_chr_format = len(image_format) + 1
            # suffixe_expected = "."+image_format
            # for file in files:

            #     if file[len(file)-nb_chr_format:] == suffixe_expected:
            #         file_splitted = file.split("_")
            #         name_image = file_splitted[3][1:]
            #         os.rename(file,name_image+suffixe_expected)
        else:
            raise Exception(f"No such folder : {folder_input}") 

def main():
    data = reading("C:/Users/romai/Documents/INP/ENSEEIHT/3A/S9\APP/MeshroomCache/CameraInit/e25428db16c4c4c062362a115adfc1d5bea0431a/cameraInit.sfm")
    find_images_folder("C:/Users/romai/Documents/INP\ENSEEIHT/3A/S9/APP/MeshroomCache/ImageMasking/c6f28ae2f05b899ce8cb30491738aeb4694dc47e"
                       ,"C:/Users/romai/Documents/INP/ENSEEIHT/3A/S9/APP/Part2_progs/masque_rename","png",data)

if __name__ == '__main__':
    main()