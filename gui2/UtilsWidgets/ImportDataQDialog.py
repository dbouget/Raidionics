from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QDialog, QDialogButtonBox,\
    QComboBox, QPushButton, QScrollArea, QLineEdit, QFileDialog
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
import os

from utils.software_config import SoftwareConfigResources


class ImportDataQDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import data")
        self.line_widgets = []  # Place-holder for the dynamic line-edit custom widgets
        self.__set_interface()
        self.__set_connections()
        self.__set_stylesheets()

    def __set_interface(self):
        self.base_layout = QVBoxLayout(self)

        # Top-panel
        self.import_select_button_layout = QHBoxLayout()
        self.import_select_files_pushbutton = QPushButton("File(s) selection")
        self.import_select_directory_pushbutton = QPushButton("Directory selection")
        self.import_select_button_layout.addWidget(self.import_select_directory_pushbutton)
        self.import_select_button_layout.addWidget(self.import_select_files_pushbutton)
        self.import_select_button_layout.addStretch(1)
        self.base_layout.addLayout(self.import_select_button_layout)

        # Dynamic central scroll area, to accommodate for as many loaded files as necessary
        self.import_scrollarea = QScrollArea()
        self.import_scrollarea_layout = QVBoxLayout()
        self.import_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.import_scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.import_scrollarea.setWidgetResizable(True)
        self.import_scrollarea_dummy_widget = QWidget()
        self.import_scrollarea_layout.setSpacing(0)
        self.import_scrollarea_layout.setContentsMargins(0, 0, 0, 0)
        # self.import_scrollarea.setMaximumSize(QSize(200, 850))
        self.import_scrollarea_layout.addStretch(1)
        self.import_scrollarea_dummy_widget.setLayout(self.import_scrollarea_layout)
        self.import_scrollarea.setWidget(self.import_scrollarea_dummy_widget)
        self.base_layout.addWidget(self.import_scrollarea)

        # Native exit buttons
        self.bottom_exit_layout = QHBoxLayout()
        self.exit_accept_pushbutton = QDialogButtonBox(QDialogButtonBox.Ok)
        self.exit_cancel_pushbutton = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.bottom_exit_layout.addWidget(self.exit_accept_pushbutton)
        self.bottom_exit_layout.addWidget(self.exit_cancel_pushbutton)
        self.bottom_exit_layout.addStretch(1)
        self.base_layout.addLayout(self.bottom_exit_layout)

    def __set_connections(self):
        self.import_select_directory_pushbutton.clicked.connect(self.__on_import_directory_clicked)
        self.import_select_files_pushbutton.clicked.connect(self.__on_import_files_clicked)
        self.exit_accept_pushbutton.clicked.connect(self.__on_exit_accept_clicked)
        self.exit_cancel_pushbutton.clicked.connect(self.__on_exit_cancel_clicked)

    def __set_stylesheets(self):
        pass

    def __on_import_directory_clicked(self):
        input_image_filedialog = QFileDialog(self)
        input_image_filedialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        input_directory = input_image_filedialog.getExistingDirectory(self, caption='Select input directory',
                                                                      directory='~',
                                                                      filter=QFileDialog.ShowDirsOnly and QFileDialog.DontResolveSymlinks)[0]
        found_files = []
        for _, _, files in os.walk(input_directory):
            for f in files:
                extension = '.'.join(os.path.basename(f).split('.')[1:])
                # @TODO. Have to check again against valid extensions from SoftwareResources
            pass

    def __on_import_files_clicked(self):
        input_image_filedialog = QFileDialog(self)
        input_image_filedialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        # @TODO. Should query the allowed file extensions from SoftwareResources
        input_filepaths = input_image_filedialog.getOpenFileNames(self, caption='Select input file(s)',
                                                                       directory='~',
                                                                       filter="Files (*.nii *.nii.gz *.nrrd *.mha *.mhd *.neurorads)")[0]  # , options=QFileDialog.DontUseNativeDialog
        for fp in input_filepaths:
            if fp != '':
                wid = ImportDataLineWidget(self)
                self.import_scrollarea_layout.insertWidget(self.import_scrollarea_layout.count() - 1, wid)
                self.line_widgets.append(wid)
                wid.filepath_lineedit.setText(fp)

                extension = '.'.join(os.path.basename(fp).split('.')[1:])
                if extension == 'neurorads':
                    wid.file_type_selection_combobox.setCurrentIndex(2)
                else:
                    wid.file_type_selection_combobox.setCurrentIndex(0)  # Assuming loading an MRI volume by default

    def __on_exit_accept_clicked(self):
        # Iterating over the list of selected files and internally updating variables
        for wid in self.line_widgets:
            SoftwareConfigResources.getInstance().get_active_patient().import_data(wid.filepath_lineedit.text(),
                                                                                   type=wid.file_type_selection_combobox.currentText())
        self.accept()

    def __on_exit_cancel_clicked(self):
        self.reject()


class ImportDataLineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__set_interface()
        self.__set_connections()
        self.__set_stylesheets()

    def __set_interface(self):
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.filepath_lineedit = QLineEdit()
        self.filepath_browse_edit_pushbutton = QPushButton()
        self.filepath_browse_edit_pushbutton.setIcon(QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                        '../Images/browse_icon.png')))
        self.filepath_browse_edit_pushbutton.setIconSize(QSize(20, 20))
        self.file_type_selection_combobox = QComboBox()
        self.file_type_selection_combobox.addItems(["MRI", "Annotation", "Patient"])

        self.layout.addWidget(self.filepath_lineedit)
        self.layout.addWidget(self.filepath_browse_edit_pushbutton)
        self.layout.addWidget(self.file_type_selection_combobox)

    def __set_connections(self):
        self.filepath_browse_edit_pushbutton.clicked.connect(self.__on_browse_edit_clicked)
        self.file_type_selection_combobox.currentIndexChanged.connect(self.__on_file_type_changed)

    def __set_stylesheets(self):
        pass

    def __on_browse_edit_clicked(self):
        pass

    def __on_file_type_changed(self):
        pass