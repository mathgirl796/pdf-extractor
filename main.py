import utils
import design
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import sys

def select_pdf(ui):
    # select pdf
    directory = QFileDialog.getOpenFileNames(None, 'Select PDF', ".", 'PDF (*.pdf)')
    if not directory:
        return
    ui.data['pdf_path'] = directory[0][0]
    ui.pdf_path.setText(ui.data['pdf_path'])
    print(ui.data['pdf_path'])
    # load text objs
    ui.data['text_objs'] = utils.get_text_objs(ui.data['pdf_path'])
    ui.data['possible_poses'] = utils.detect_pos(ui.data['text_objs'])
    # inflate name list
    ui.name_list.clear()
    for i in ui.data['possible_poses'].values():
        ui.name_list.addItem(i)
    # inflate inter list
    ui.inter_list.clear()
    for i in ui.data['possible_poses'].values():
        ui.inter_list.addItem(i)

def select_outdir(ui):
    # select output dir
    directory = QFileDialog.getExistingDirectory(None, 'Select Output Directory', ".")
    ui.data['output_dir'] = directory
    ui.output_dir.setText(ui.data['output_dir'])
    print(ui.data['output_dir'])

def label_name(ui):
    select_indexes = [x.row() for x in ui.name_list.selectedIndexes()]
    ui.data['name_poses'] = [list(ui.data['possible_poses'].keys())[i] for i in select_indexes]
    print(select_indexes, ui.data['name_poses'])

def label_inter(ui):
    select_indexes = [x.row() for x in ui.inter_list.selectedIndexes()]
    ui.data['inter_poses'] = [list(ui.data['possible_poses'].keys())[i] for i in select_indexes]
    print(select_indexes, ui.data['inter_poses'])

def do_work(ui):
    ui.data['string_list'], ui.data['shit_list'] = utils.text_objs_to_string_list(
        ui.data['text_objs'],
        ui.data['name_poses'],
        ui.data['inter_poses'],
    )
    # inflate string list
    ui.string_list.clear()
    for i in ui.data['string_list']:
        ui.string_list.addItem(i)
    # inflate shit list
    ui.shit_list.clear()
    for i in ui.data['shit_list']:
        ui.shit_list.addItem(i[2])

def do_filter(ui):
    select_indexes = [x.row() for x in ui.shit_list.selectedIndexes()]
    ui.data['white_list'] = [ui.data['shit_list'][i][2] for i in select_indexes]
    print(ui.data['white_list'])
    ui.data['string_list'], _ = utils.text_objs_to_string_list(
        ui.data['text_objs'],
        ui.data['name_poses'],
        ui.data['inter_poses'],
        white_list=ui.data['white_list'],
    )
    # inflate string list
    ui.string_list.clear()
    for i in ui.data['string_list']:
        ui.string_list.addItem(i)

def do_output(ui):
    if 'output_dir' not in ui.data:
        QMessageBox.warning(None, 'Warning', 'Please select output directory first.')
        return
    file_path = f"{ui.data['output_dir']}/output-{utils.string_time()}.txt"
    print(file_path)
    with open(file_path, 'w', encoding="utf-8") as f:
        for string in ui.data['string_list']:
            f.write(f"{string}\n")

def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = design.Ui_mainWindow()
    ui.setupUi(MainWindow)

    # modify ui
    ui.data = {}
    ui.select_pdf.clicked.connect(partial(select_pdf, ui))
    ui.set_outdir.clicked.connect(partial(select_outdir, ui))
    ui.label_name.clicked.connect(partial(label_name, ui))
    ui.label_inter.clicked.connect(partial(label_inter, ui))
    ui.do_work.clicked.connect(partial(do_work, ui))
    ui.do_filter.clicked.connect(partial(do_filter, ui))
    ui.do_output.clicked.connect(partial(do_output, ui))

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()