import sys

from flask import Flask, request, json
from api_pdf2pic2pdf.pdf_Remove_Red import mainProcess
from logger_to_write.Logger import log
from logger_to_write.Logger import logerror

sys.path.append(".")

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to PDF_PIC_PDF</h2>'

@app.route('/removeColor',methods=["POST"])
def get_tasks():
    if request.method=='POST':
        log.logger.info("Users are requesting interfaces!")
        path=request.form['path']
        outpath=request.form['outpath']
        zoomNum=request.form['zoomNum']
        compressNum=request.form['compressNum']
        resultDict = {}
        if not path or not '.pdf' in path:
            resultDict['result'] = 'Parameter Error!'
        if not '.pdf' in outpath:
            resultDict['result'] = 'Parameter Error!'
        if not "Error" in resultDict['result']:
            try:
                zoomNum = float(zoomNum)
            except Exception as e:
                zoomNum = 2
            try:
                compressNum = float(compressNum)
            except Exception as e:
                compressNum = 1
            try:
                mainProcess(path,outpath,zoomNum,compressNum)
                resultDict['result'] = 'Program Running Success!'
            except Exception as e:
                resultDict['result'] = 'Program Running Error!'
                logerror.logger.error("Program Running Error! Exception: %s!" % e)
        log.logger.info("The result of this request is: %s !" % resultDict['result'])
        return json.dumps(resultDict,ensure_ascii=False)


if __name__ == '__main__':
    app.run()