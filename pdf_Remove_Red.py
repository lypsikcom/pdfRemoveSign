import sys, fitz, os, datetime
import time
from logger_to_write.Logger import log
from logger_to_write.Logger import logerror
import cv2
from PIL import Image
import numpy as np

'''
fitz库是pymupdf中的一个模块

pip install pymupdf
'''
def pyMuPDF_fitz(pdfPath, imagePath, zoomNum):
    startTime_pdf2img = datetime.datetime.now()#开始时间

    print("imagePath="+imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        # zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_x = zoomNum #(1.33333333-->1056x816)   (2-->1584x1224)
        # zoom_y = 1.33333333
        zoom_y = zoomNum
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建

        if pg < 10:
            pg_str = '00' + str(pg)
        elif 10 <= pg <100:
            pg_str = '0' + str(pg)
        else:
            pg_str = str(pg)
        pix.writePNG(imagePath+'/'+'%s.png' % pg_str)#将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()#结束时间
    log.logger.info('pdf2img时间='+str((endTime_pdf2img - startTime_pdf2img).seconds) + '秒')

def pyMuBinaryzation(binaryzationpath):
    startTime_pdfbinaryzation = datetime.datetime.now()#开始时间
    file_list = os.listdir(binaryzationpath)
    pic_name = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)
    for i in pic_name:
        image = Image.open(binaryzationpath + '/' + i)
        new_file_name = binaryzationpath + '/' + i
        picArray = np.array(image)  # 解析图片成 numpy矩阵
        red_index_or = ((picArray[..., 0] - picArray[..., 1]) > 10) & ((picArray[..., 0] - picArray[..., 2]) > 10)
        picArrayTemp = picArray[red_index_or]
        '''
        先加深100以下的所有
        '''
        black_100_index = (picArrayTemp[...,0] < 110) & (picArrayTemp[...,1] < 100) & (picArrayTemp[...,2] < 100)
        picArrayTemp[black_100_index] = [0, 0, 0]
        '''
        以下是加深150以下的 并且R和GB差值小于60
        '''
        black_150_index = (picArrayTemp[...,0] < 160) & (picArrayTemp[...,1] < 150) & (picArrayTemp[...,2] < 150) & (
                    (picArrayTemp[...,0] - picArrayTemp[...,1]) < 80) & ((picArrayTemp[...,0] - picArrayTemp[...,2]) < 80)
        picArrayTemp[black_150_index] = [0, 0, 0]
        '''
        以下是加深190以下并且差值不大于20的
        '''
        black_190_index = (picArrayTemp[...,0] < 190) & (picArrayTemp[...,1] < 190) & (picArrayTemp[...,2] < 190) & ((picArrayTemp[...,0] - picArrayTemp[...,1])**2 < 400) & ((picArrayTemp[...,0] - picArrayTemp[...,2])**2 < 400) & ((picArrayTemp[...,1] - picArrayTemp[...,2])**2 < 400) # & (picArray[..., 0] != picArray[..., 1])
        picArrayTemp[black_190_index] = [0, 0, 0]
        '''
        以下是红色情况的去除
        '''
        red_index = ((picArrayTemp[...,0] - picArrayTemp[...,1]) > 10) & ((picArrayTemp[...,0] - picArrayTemp[...,2]) > 10)
        picArrayTemp[red_index] = [255, 255, 255]
        '''
        以下是去除200以上的
        '''
        white_200_index = (picArrayTemp[...,0] > 200) & (picArrayTemp[...,1] > 200) & (picArrayTemp[...,2] > 200)
        picArrayTemp[white_200_index] = [255, 255, 255]
        # 赋值picArray
        picArray[red_index_or] = picArrayTemp

        im = Image.fromarray(picArray)
        im.save(new_file_name)
    endTime_pdfbinaryzation = datetime.datetime.now()  # 结束时间
    log.logger.info('pdfpdfbinaryzation时间=' + str((endTime_pdfbinaryzation - startTime_pdfbinaryzation).seconds) + '秒')

def pyMuPicToPdf(picDir,outfilepath):
    startTime_PicToPdf = datetime.datetime.now()  # 开始时间
    file_list = os.listdir(picDir)
    pic_name = []
    im_list = []
    # print(file_list)
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)

    pic_name.sort()

    im1 = Image.open(picDir + '/' + pic_name[0])
    pic_name.pop(0)
    for i in pic_name:
        img = Image.open(picDir + '/' + i)
        # im_list.append(img)
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(outfilepath, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    endTime_PicToPdf = datetime.datetime.now()  # 结束时间
    log.logger.info('用户PicToPdf时间=' + str((endTime_PicToPdf - startTime_PicToPdf).seconds) + '秒')

def compress(outdir, compressNum):
    startTime_PicToPdf = datetime.datetime.now()  # 开始时间
    file_list = os.listdir(outdir)
    pic_name = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)
    for i in pic_name:
        new_file_name = outdir + '/' + i
        img = cv2.imread(outdir + '/' + i)
        y, x, z = img.shape
        res = cv2.resize(img, dsize=(int(x / compressNum), int(y / compressNum)), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(new_file_name, res)

    endTime_PicToPdf = datetime.datetime.now()  # 结束时间
    log.logger.info('用户compress时间=' + str((endTime_PicToPdf - startTime_PicToPdf).seconds) + '秒')

def deleteDir(path):
    try:
        for i in os.listdir(path):
            path_file = os.path.join(path, i)
            if os.path.isfile(path_file):
                os.remove(path_file)
        if os.path.exists(path):  # 如果文件夹
            # 删除文件，可使用以下两种方法。
            os.rmdir(path)
            # os.unlink(path)
        else:
            log.logger.info('no such file:%s' % path)  # 则返回文件不存在
    except Exception as e:
        logerror.logger.error("User Delete Folder Failed! Exception:%s" % e)

def mainProcess(fileName,outfilepath='',zoomNum=2.5,compressNum=1):
    '''
    主函数入口
    :param fileName:需要去章的文件路径,请用绝对路径
    :param outfilepath:需要输出的文件路径，包括文件名，默认在同目录下生成 xxx_out.pdf 文件
    :param zoomNum:转换成图片的比例，影响运行速度，数值越大，去章效果越好，执行时间越长，默认为2
    :param compressNum:压缩图片比例，数值越大压缩成的图片越小，清晰度越低，默认为1，不进行压缩
    :return:
    '''
    startTime = datetime.datetime.now()  # 开始时间
    (filepath, tempfilename) = os.path.split(fileName) # 解析fileName
    (filename, extension) = os.path.splitext(tempfilename) # 解析文件名 文件类型
    if not outfilepath:
        outfilepath = filepath + '/' +filename + '_out' + extension
    outdir = filepath + '/' + filename
    pyMuPDF_fitz(fileName,outdir,zoomNum) # 将pdf文件解析出图片
    pyMuBinaryzation(outdir) # 对图片进行去章
    if compressNum != 1 and compressNum >0:
        compress(outdir,compressNum)
    pyMuPicToPdf(outdir,outfilepath) # 将图片合成pdf
    deleteDir(outdir) # 删除图片文件夹
    endTime = datetime.datetime.now()  # 结束时间
    log.logger.info('用户总耗时=' + str((endTime - startTime).seconds) + '秒')






if __name__ == '__main__':
    fileName = r'D:/Desktop/lyp/文件/100-150PDF/130.pdf'
    mainProcess(fileName, zoomNum=2.5)  # 入口函数 有四个参数
    # binaryzationpath = r"D:\Desktop\lyp\文件\100-150PDF\test"
    # pyMuBinaryzation(binaryzationpath)