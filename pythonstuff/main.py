from pdf2image import convert_from_path
pages = convert_from_path(r'C:\Users\Ant\Documents\igmcq\pythonstuff\test.pdf', 500, poppler_path=r"C:\poppler-24.08.0\Library\bin")
for i in range(len(pages)):
        pages[i].save('image_name'+ str(i) +'.jpg', 'JPEG')
        print(i)