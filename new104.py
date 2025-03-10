# import os
# import zipfile
# import shutil


# z = zipfile.ZipFile('./main.zip','w')

# # z.write('./main.zip')
# z.close()
# print(z.filelist)


# for itm in os.walk('./python_amir'):
#     print(item)
#     rott_dir = item[0]
#     sub= item[1]
#     subfiles= item[2]
    
#     z.write(toor_dir)
    
#     for sd in sub:
#         z.write(f'{root_dir}\\{sd}')
    
#     for f in subfiles:
#         z.write(f'{rott_dir}\\{f}')

# z.close()





# shutil.make_archive('./backup','zip','./backup')  #  دومین نوشته مریوط به نوع فرمت فایل است 

# shutil.unpack_archive('./bachup.zip','./exrtacted')

