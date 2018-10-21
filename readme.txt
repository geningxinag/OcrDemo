图片文字识别需要用到 Tesseract-OCR
    下载地址 http://jaist.dl.sourceforge.net/project/tesseract-ocr-alt/tesseract-ocr-setup-3.02.02.exe

识别训练需要用到 jTessBoxEditor
    下载地址 https://nchc.dl.sourceforge.net/project/vietocr/jTessBoxEditor/jTessBoxEditorFX-2.1.0.zip

train 文件夹是训练用的
    请将 num.traineddata 拷贝到 Tesseract-OCR 安装目录下的 /tessdata/
    与eng.traineddata 同级
    使用方法：pytesseract.image_to_string(tempImg, lang='num')

暂时只支持无角度的识别，下一步准备添加角度纠正
