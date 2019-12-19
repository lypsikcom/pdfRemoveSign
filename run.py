import sys
import io
from api_pdf2pic2pdf.tornado_api import gooo
from logger_to_write.Logger import log
from logger_to_write.Logger import logerror

sys.path.append(".")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # 改变输出默认编码utf-8 windows 有的时候默认GBK


def main(count=1):
    if count > 3:
        logerror.logger.error("PDF_PIC_PDF:Service Startup Failure!")
    try:
        log.logger.info("PDF_PIC_PDF:Try starting the service for the %s time" % count)
        gooo()
    except Exception as e:
        logerror.logger.error("Initiate error reporting --- %s !" % e)
        main()


if __name__ == '__main__':
    main()
    # gooo()