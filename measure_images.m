clear all
close all

path_images_sources = "C:\Users\romai\Documents\INP\ENSEEIHT\3A\S9\APP\glock_19_g\fond_texture\IMG_20230406_185";
format_source = ".JPG";
path_images_output = "C:\Users\romai\Documents\INP\ENSEEIHT\3A\S9\APP\Part2_progs\Test_rendu\185";
format_output = ".png";
path_masks = "C:\Users\romai\Documents\INP\ENSEEIHT\3A\S9\APP\Part2_progs\masque_rename\IMG_20230406_185";
format_masks = ".png";

range_images = 849:957;
index_pass = ones(size(range_images));
images_output = [];

for i = 1:length(range_images)
    try
        index = range_images(i);
        image = imread(path_images_output+num2str(index)+format_output);
        images_output = cat(4,images_output,image);
    catch
        index_pass(i) = 0;
    end
end    

images_input = [];
masks = [];
for i = 1:length(range_images)
    if index_pass(i)== 1
        index = range_images(i);
        image = imread(path_images_sources+num2str(index)+format_source);
        if size(image,1) == size(images_output,2)
            image = imrotate(image,-90);
        end
        images_input = cat(4,images_input,image);
        if strlength(path_masks) > 0
            mask = imread(path_masks+num2str(index)+format_masks);
            masks = cat(3,masks,image);
        end
    end
end 
if length(masks) > 0
    for i = 1:size(images_output,4)
            mask = (masks(:,:,i) == 0);
        for j = 1:size(images_output,3)
            image_i = images_input(:,:,j,i);
            image_i(mask) = 0;
            images_input(:,:,j,i) = image_i ;
            image_o = images_output(:,:,j,i);
            image_o(mask) = 0;
            images_output(:,:,j,i) = image_o;
        end
    end
end

%images_input = images_input(:,:,:,2:4);
%images_output = images_output(:,:,:,2:4);
mse_error = mean((images_input-images_output).*(images_input-images_output),'all')
mae_error = mean(abs((images_input-images_output)),'all') 
ssim_error = 0;
for i = 2:size(images_output,4)
    ssim_error = ssim_error + ssim(images_input(:,:,:,i),images_output(:,:,:,i));
end    
ssim_error = ssim_error/size(images_output,4)

