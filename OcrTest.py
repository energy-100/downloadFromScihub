from PIL import Image
import numpy as np
import pytesseract
from pdf2image import convert_from_path
import fitz
from io import StringIO,BytesIO
from PIL import Image
from googletrans import Translator
from Thread2 import translatethread
# def pdf_ocr(fname, **kwargs):
# 	images = convert_from_path(fname, **kwargs)
# 	text = ''
# 	for img in images:
# 		img = np.array(img)
# 		text += pytesseract.image_to_string(img)
# 	return text
# text = pdf_ocr("D:/工作文件2/光散射/人体参数/Optical properties of human skin subcutaneous and mucous tissues.pdf")



# def PDF_to_imgs(PDF_path, save_path):
# 	# 打开PDF文件，生成一个对象
# 	doc = fitz.open(PDF_path)
# 	imagelist=[]
# 	matlist=[]
# 	# 将PDF文件的每一页都转化为图片
# 	for pg in range(doc.pageCount):
# 		page = doc[pg]
# 		rotate = int(0)
# 		# 每个尺寸的缩放系数为2，这将为我们生成分辨率提高4倍的图像。
# 		zoom_x = 2
# 		zoom_y = 2
# 		trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
# 		pm = page.getPixmap(matrix=trans, alpha=False).getImageData()
# 		# print(type(pm))
# 		# pm.writePNG(save_path + '%s.png' % pg)
# 		imagelist.append(pm)
# 		matlist.append(page)
# 	# return matlist
# 	return imagelist
#
# images = PDF_to_imgs(r'D:/工作文件2/光散射/人体参数/Optical properties of human skin subcutaneous and mucous tissues.pdf', '')
# text=""
# for img in images:
# 	# img=Image.frombytes(img)
# 	img=Image.open(BytesIO(img))
#
# 	# img = Image.fromarray(np.array(img))
# 	# img = np.array(img)
# 	english = pytesseract.image_to_string(img).replace('\r','').replace('\n','').replace('\t','')
# 	text +=english
# 	translator = Translator()
# 	chineseword = translator.translate(english, dest='zh-CN').text
# 	print(chineseword)
# print(text)



import PyPDF2

pdfFile = open(r'D:/工作文件2/光散射/人体参数/Optical properties of human skin subcutaneous and mucous tissues.pdf','rb')

pdfReader = PyPDF2.PdfFileReader(pdfFile)
print(pdfReader.getDocumentInfo())
print(pdfReader.numPages)

page = pdfReader.getPage(0)

print(page.extractText())

pdfFile.close()
# return text
# text = pytesseract.image_to_string(Image.open(r'testjpg3.png'))
# print(text)