from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar
from math import isclose

def parse_lt_objs (lt_objs, page_number, text_objs = []):
    for lt_obj in lt_objs:
        # print(lt_obj.bbox)
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            text_objs.append(lt_obj)
            # print(lt_obj.get_text().strip())
        elif isinstance(lt_obj, LTImage):
            pass
        elif isinstance(lt_obj, LTFigure):
            parse_lt_objs(lt_obj, page_number, text_objs)

def parse_document(filename):
    # open the pdf file
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    # extract text objects from pdf file
    text_objs = []
    for i, page in enumerate(PDFPage.create_pages(doc)):
        # print(i)
        interpreter.process_page(page)
        layout = device.get_result()
        parse_lt_objs(layout, i, text_objs)
    # return list of text objects
    return text_objs

def detect_bbox_0(text_objs):
    d = {}
    for i, obj in enumerate(text_objs):
        if obj.bbox[0] not in d:
            d[obj.bbox[0]] = obj.get_text().strip()
    return d

def close_to_list(x, l, abs_tol=1):
    for i in l:
        if isclose(x, i, abs_tol=abs_tol):
            return True
    return False

def string_have_item_in_list(s, l):
    for i in l:
        if i in s:
            return True
    return False

def get_text_objs(pdf_file_name):
    text_objs = parse_document(pdf_file_name)
    return text_objs

def detect_pos(text_objs):
    box2content = {}
    for key, value in detect_bbox_0(text_objs).items():
        box2content[key] = value
    return box2content

def text_objs_to_string_list(text_objs, start_poses:list, intermediate_poses:list, abs_tol:float=0.001, white_list:list=[], black_list:list=[]):
    items = []
    shit = []
    for i, obj in enumerate(text_objs):
        if obj.get_text().strip() in white_list: # white_list: string列表
            items.append(obj.get_text().strip())
        elif close_to_list(obj.bbox[0], start_poses, abs_tol):
            items.append(obj.get_text().strip())
        elif close_to_list(obj.bbox[0], intermediate_poses, abs_tol) == True and len(items) > 0:
            items[-1] += obj.get_text().strip()
        else:
            shit.append((i, obj.bbox[0], obj.get_text().strip()))
    return items, shit

def string_time():
    import time
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

