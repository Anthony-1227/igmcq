from pdf2image import convert_from_path
pages = convert_from_path('test.pdf', 500, poppler_path=r"C:\Users\Ant\Documents\igmcq\pythonstuff\Release-24.08.0-0\poppler-24.08.0\Library\bin")
for i in range(len(pages)):
        pages[i].save('image_name'+ str(i) +'.jpg', 'JPEG')