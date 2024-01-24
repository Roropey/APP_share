import os




def find_images_folder(folder_path,image_format):
        print("find_images_folder")
        if os.path.exists(folder_path):
            os.chdir(folder_path)
            files = os.listdir(folder_path)
            nb_chr_format = len(image_format) + 1
            suffixe_expected = "."+image_format
            for file in files:

                if file[len(file)-nb_chr_format:] == suffixe_expected:
                    file_splitted = file.split("_")
                    name_image = file_splitted[5]
                    os.rename(file,name_image+suffixe_expected)
        else:
            raise Exception(f"No such folder : {folder_path}")    

def main():
    find_images_folder("C:/Users/romai/Documents/INP/ENSEEIHT/3A/S9/APP/Part2_progs/Test_rendu",'png')

if __name__ == '__main__':
    main()