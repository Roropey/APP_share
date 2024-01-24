import argparse
import os
import shutil
import numpy as np
from PIL import Image
#import matplotlib as plt


class one_mask_fusion:
    def __init__(self,input_images, output, mode=0):
        self.input_images = input_images
        self.output_fusion = output
        self.mode_fusion = mode     # 0 for intersection, 1 for union

    def open_image(path_image):
        return np.array(Image.open(path_image))

    def intersection(image_1,image_2):
        return image_1*image_2
    
    def union(image_1,image_2):
        return ((image_1 + image_2)>0).astype(int)
    
    def mask_fusion(self):
        result = self.open_image(self.input_images[0])
        for index in range(len(self.input_images)-1):
            next_image = self.open_image(self.input_images[index+1])
            if self.mode_fusion == 0:
                result = self.intersection(result,next_image)
            elif self.mode_fusion == 1:
                result = self.union(result,next_image)
            else:
                raise Exception(f"Mode given not recognize : {self.mode_fusion}")
        image_result = Image.fromarray(result)
        image_result.save(self.output)

class image():
    def __init__(self,folder_path,name,format):
        self.folder = folder_path
        self.name = name
        self.format = format
        self.path = os.path.join(self.folder,self.name+r'.'+self.format)
        self.data = self.data = np.array(Image.open(self.path))   


class masking_fusion:

    def __init__(self, inputs_images={}, output_f=[], image_format="",mode=0,option_saving_before=False):

        self.inputs_images = inputs_images
        self.nb_images = 0
        self.first_folder = None
        self.output_f = output_f
        self.image_format = image_format
        self.mode_fusion = mode 
        self.option_saving_before = option_saving_before

    def creation_parser(self):
        parser = argparse.ArgumentParser("Masks fusion")

        parser.add_argument('-ft','--fusion_type',type = str, default = 'intersection', 
                            help = "Type of fusion done between the masks. Accept 'i', 'I' or 'intersection' for intersection between masks (AND) or 'u', 'U' or 'union' for union between masks (OR).")
        parser.add_argument('-i','--inputs', action='append', type = str, help = "Path for the folders for the output of the fusions (stack all path with % as separation).")
        parser.add_argument('-o','--output', type = str, default = None, help = "Output folder, the name of each fusion will be the same as the first image use for the fusion (names from the first folder for the input).")
        parser.add_argument('-imf','--image_format',type = str, default = 'png', help="Format of the images inputed (for example 'png').")
        parser.add_argument('-so','--save_output',type=bool,default=False,help="Make a copy of the previous file in the output folder if the new image has the same name as as an image already present in the output.")
        return parser
    
    def find_images_folder(self,folder_path):
        print("find_images_folder")
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            images_path = []
            nb_chr_format = len(self.image_format) + 1
            suffixe_expected = "."+self.image_format
            for file in files:
                if file[len(file)-nb_chr_format:] == suffixe_expected:
                    images_path.append(file[:len(file)-nb_chr_format])
            return images_path
        else:
            raise Exception(f"No such folder : {folder_path}")      

    def intersection(self,image_1,image_2):
        return image_1*image_2*255
    
    def union(self,image_1,image_2):
        return np.uint8((((image_1 + image_2)>0)*255))
    
    def mask_fusion(self,input_images,output):
        result = input_images[0].data
        for index in range(len(input_images)-1):
            next_image = input_images[index+1].data
            if self.mode_fusion == 0:
                result = self.intersection(result,next_image)
            elif self.mode_fusion == 1:
                result = self.union(result,next_image)
            else:
                raise Exception(f"Mode given not recognize : {self.mode_fusion}")
        if os.path.isfile(output) and self.option_saving_before:
            splitted_output = output.split("\\")
            splitted_output.insert(len(splitted_output)-1,"saving_previous")
            folder_saving = '\\'.join(splitted_output[:-1])
            if not(os.path.isdir(folder_saving)):
                os.mkdir(folder_saving)
            saving_path = '\\'.join(splitted_output)
            shutil.copyfile(output,saving_path)
        image_result = Image.fromarray(result)
        image_result.save(output)

    def iteration_images(self,index):
        images_index = []
        for key in iter(self.inputs_images):
            images_index.append(self.inputs_images[key][index])
        return images_index
    
    def process(self):
        for index in range(self.nb_images):
            print(f"Image {index}")
            images_for_masking = self.iteration_images(index)
            output = os.path.join(self.output_f,self.inputs_images[self.first_folder][index].name + '.' + self.image_format)
            self.mask_fusion(images_for_masking,output)


    def masking_fusion_main(self,args = None):
        if not(args):
            args = self.creation_parser().parse_args()
            print(args)
            raise Exception("Stop")
            if args.fusion_type=='i' or args.fusion_type=='I' or args.fusion_type=='intersection':
                self.mode_fusion = 0
            elif args.fusion_type=='u' or args.fusion_type=='U' or args.fusion_type=='union':
                self.mode_fusion = 1
            else:
                raise Exception(f"Not recognize type of fusion : {args.fusion_type}")
            self.image_format = args.image_format
            
            list_inputs = args.inputs.split('%')
            if len(list_inputs) < 2:
                raise Exception(f"Only {len(list_inputs)} input, not enough for fusion")
            else:
                for folder in list_inputs:
                    images = self.find_images_folder(folder)
                    if self.nb_images > 0 and self.nb_images != len(images):
                        raise Exception("Not same number of images in the folders")
                    elif self.nb_images == 0:
                        self.nb_images = len(images)
                    images_in_folder = []
                    for image_name in images:
                        image_obj = image(folder,image_name,self.image_format)
                        images_in_folder.append(image_obj)
                    self.inputs_images.update({folder: images_in_folder})

                    if not(self.first_folder):
                        self.first_folder = folder
            if args.output:
                self.output_f = args.output
            else:
                self.output_f = self.inputs_f[0] 
            self.option_saving_before = args.save_output
            self.process()
        else:
            raise Exception("Not managed")

def main():
    masking_fusion_obj = masking_fusion()
    masking_fusion_obj.masking_fusion_main()        

if __name__ == '__main__':
    main()

        


    
    
